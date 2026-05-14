"""
AI Service Layer
Abstraction for Claude and OpenAI APIs with fallback mechanisms.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass
import aiohttp

from app.config.settings import get_settings

logger = logging.getLogger(__name__)


@dataclass
class AIResponse:
    """Response from AI service."""
    content: str
    model_used: str
    provider: str
    input_tokens: int
    output_tokens: int
    stop_reason: Optional[str] = None


class AIServiceBase(ABC):
    """Abstract base class for AI services."""

    def __init__(self, api_key: str, timeout: int = 60):
        """Initialize AI service."""
        self.api_key = api_key
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    @abstractmethod
    async def summarize_article(self, article_content: str) -> AIResponse:
        """
        Summarize an article and generate analysis.
        
        Args:
            article_content: Full article text
            
        Returns:
            AIResponse with summary, sentiment, hype score, etc.
        """
        pass

    @abstractmethod
    async def extract_entities(self, text: str) -> dict:
        """Extract entities (games, developers, etc.) from text."""
        pass


class ClaudeAIService(AIServiceBase):
    """Claude API integration via Anthropic."""

    API_URL = "https://api.anthropic.com/v1/messages"
    MODEL = "claude-3-5-sonnet-20241022"

    async def summarize_article(self, article_content: str) -> AIResponse:
        """Summarize article using Claude."""
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context manager.")

        prompt = self._build_summarization_prompt(article_content)
        
        try:
            async with self.session.post(
                self.API_URL,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": self.MODEL,
                    "max_tokens": 1024,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return AIResponse(
                        content=data["content"][0]["text"],
                        model_used=self.MODEL,
                        provider="anthropic",
                        input_tokens=data["usage"]["input_tokens"],
                        output_tokens=data["usage"]["output_tokens"],
                        stop_reason=data.get("stop_reason"),
                    )
                else:
                    error_text = await resp.text()
                    raise Exception(f"Claude API error: {resp.status} - {error_text}")
        except asyncio.TimeoutError:
            raise Exception(f"Claude API timeout after {self.timeout}s")

    async def extract_entities(self, text: str) -> dict:
        """Extract entities using Claude."""
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context manager.")

        prompt = f"""Extract the following from this gaming news text:
        - Game titles mentioned
        - Developer/Publisher names
        - Platform names (PC, PlayStation, Xbox, etc.)
        
        Return as JSON only, no other text:
        {{
            "games": [],
            "developers": [],
            "publishers": [],
            "platforms": []
        }}
        
        Text: {text[:1000]}"""

        try:
            async with self.session.post(
                self.API_URL,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": self.MODEL,
                    "max_tokens": 512,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    import json
                    return json.loads(data["content"][0]["text"])
                else:
                    return {"games": [], "developers": [], "publishers": [], "platforms": []}
        except Exception as e:
            logger.error(f"Entity extraction error: {str(e)}")
            return {"games": [], "developers": [], "publishers": [], "platforms": []}

    @staticmethod
    def _build_summarization_prompt(article_content: str) -> str:
        """Build optimized prompt for article summarization."""
        return f"""Analyze this gaming news article and provide:

1. A concise 2-3 sentence summary
2. Three key bullet points
3. Sentiment classification (bullish/bearish/neutral/mixed)
4. Hype score (0-100) indicating excitement level
5. Category (news/review/feature/interview/rumor/update)
6. Trending probability (0-100) as percentage likelihood this becomes trending
7. Gamer interest (0-100) estimating audience interest level

Return ONLY valid JSON (no markdown, no code blocks):
{{
    "summary": "...",
    "bullet_points": ["...", "...", "..."],
    "sentiment": "bullish|bearish|neutral|mixed",
    "hype_score": 0-100,
    "category": "news|review|feature|interview|rumor|update",
    "trending_probability": 0-100,
    "gamer_interest": 0-100
}}

ARTICLE:
{article_content[:4000]}"""


class OpenAIService(AIServiceBase):
    """OpenAI API integration."""

    API_URL = "https://api.openai.com/v1/chat/completions"
    MODEL = "gpt-4-turbo"

    async def summarize_article(self, article_content: str) -> AIResponse:
        """Summarize article using OpenAI."""
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context manager.")

        prompt = self._build_summarization_prompt(article_content)

        try:
            async with self.session.post(
                self.API_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 1024,
                },
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return AIResponse(
                        content=data["choices"][0]["message"]["content"],
                        model_used=self.MODEL,
                        provider="openai",
                        input_tokens=data["usage"]["prompt_tokens"],
                        output_tokens=data["usage"]["completion_tokens"],
                        stop_reason=data["choices"][0].get("finish_reason"),
                    )
                else:
                    error_text = await resp.text()
                    raise Exception(f"OpenAI API error: {resp.status} - {error_text}")
        except asyncio.TimeoutError:
            raise Exception(f"OpenAI API timeout after {self.timeout}s")

    async def extract_entities(self, text: str) -> dict:
        """Extract entities using OpenAI."""
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context manager.")

        prompt = f"""Extract gaming entities from this text and return ONLY JSON:
        {{"games": [], "developers": [], "publishers": [], "platforms": []}}
        
        Text: {text[:1000]}"""

        try:
            async with self.session.post(
                self.API_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 512,
                },
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    import json
                    return json.loads(data["choices"][0]["message"]["content"])
                else:
                    return {"games": [], "developers": [], "publishers": [], "platforms": []}
        except Exception as e:
            logger.error(f"Entity extraction error: {str(e)}")
            return {"games": [], "developers": [], "publishers": [], "platforms": []}

    @staticmethod
    def _build_summarization_prompt(article_content: str) -> str:
        """Build optimized prompt for article summarization."""
        return f"""Analyze this gaming news article and provide:

1. A concise 2-3 sentence summary
2. Three key bullet points
3. Sentiment classification (bullish/bearish/neutral/mixed)
4. Hype score (0-100) indicating excitement level
5. Category (news/review/feature/interview/rumor/update)
6. Trending probability (0-100) as percentage likelihood this becomes trending
7. Gamer interest (0-100) estimating audience interest level

Return ONLY valid JSON (no markdown, no code blocks):
{{
    "summary": "...",
    "bullet_points": ["...", "...", "..."],
    "sentiment": "bullish|bearish|neutral|mixed",
    "hype_score": 0-100,
    "category": "news|review|feature|interview|rumor|update",
    "trending_probability": 0-100,
    "gamer_interest": 0-100
}}

ARTICLE:
{article_content[:4000]}"""


class AIServiceFactory:
    """Factory for creating AI service instances with fallback support."""

    @staticmethod
    def create_service(provider: Optional[str] = None) -> AIServiceBase:
        """
        Create appropriate AI service based on configuration.
        
        Args:
            provider: Override provider (claude or openai)
            
        Returns:
            Initialized AI service instance
            
        Raises:
            ValueError: If no valid API key is configured
        """
        settings = get_settings()
        
        if provider is None:
            provider = settings.ai_provider

        if provider == "claude":
            api_key = settings.anthropic_api_key or settings.claude_api_key
            if not api_key:
                raise ValueError("Claude API key not configured")
            return ClaudeAIService(api_key, timeout=settings.ai_timeout_seconds)
        
        elif provider == "openai":
            api_key = settings.openai_api_key
            if not api_key:
                raise ValueError("OpenAI API key not configured")
            return OpenAIService(api_key, timeout=settings.ai_timeout_seconds)
        
        else:
            raise ValueError(f"Unknown AI provider: {provider}")
