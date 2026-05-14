# AI対応ゲームニュースインテリジェンスプラットフォーム

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

> **大規模ゲームニュースサイトから継続的にコンテンツをスクレイピングし、インテリジェントに記事を抽出し、LLM APIを使用して要約を生成し、ゲームに対するセンチメント分析を実施し、構造化されたインテリジェンスデータをアナリティクスとダッシュボード向けに保存するエンタープライズグレードの自律システム。**

## 概要

**ゲームニュースAIプラットフォーム**は、大規模でゲームニュースを処理する本番環境対応の自律型メディアインテリジェンスエンジンです。IGN、GameSpot、および最新のメディア監視プラットフォームなどの企業が使用するシステムのように設計されています。

### 主な機能

- **🤖 自律スクレイピング**: インテリジェントなレート制限を備えたマルチサイト同時スクレイピング
- **🧠 AI要約**: Claude/GPT ベースの記事分析とセンチメント・ハイプスコアリング
- **📊 高度なアナリティクス**: トレンド検出、センチメント分布、ゲーマー関心度メトリクス
- **🔄 非同期アーキテクチャ**: タスクオーケストレーション機能を備えた本番グレードの非同期パイプライン
- **💾 PostgreSQL統合**: 効率的なクエリのための正規化スキーマ
- **📤 データエクスポート**: 分析とダッシュボード用のJSONおよびCSVエクスポート
- **📝 エンタープライズロギング**: 完全なコンテキスト情報を含む構造化ロギング
- **🐳 Dockerサポート**: 完全なコンテナ化デプロイメントスタック

---

## アーキテクチャ

### 高レベルパイプライン

```
スクレイピング層
    ↓
[IGN] [GameSpot] [PC Gamer] [Polygon] [Eurogamer]
    ↓ (非同期プール)
コンテンツ処理
    ↓
[重複検出] → [HTML無害化] → [正規化]
    ↓
データベース層
    ↓
PostgreSQL (記事)
    ↓
AI分析層
    ↓
[Claude/OpenAI API] → [要約] → [センチメント分析] → [ハイプスコアリング]
    ↓
データベース層 (要約)
    ↓
エクスポート/アナリティクス
    ↓
[JSONエクスポート] [CSVエクスポート] [トレンド分析] [ダッシュボード]
```

### コンポーネントアーキテクチャ

```
app/
├── core/                    # コア機能とコンスタンス
├── config/                  # 設定管理 (pydantic-settings)
├── database/                # データベース接続とライフサイクル
├── models/                  # SQLAlchemy ORM モデル
├── scrapers/                # Webスクレイピングモジュール
│   ├── base.py             # 抽象スクレイパーベースクラス
│   └── sites.py            # 具体的な実装 (IGN, GameSpot など)
├── ai/                      # AI サービス層
│   └── service.py          # Claude/OpenAI 抽象化
├── services/                # ビジネスロジックサービス
│   └── article.py          # 記事処理サービス
├── pipelines/               # 非同期オーケストレーション
│   └── processing.py       # メインパイプライン & スケジューラー
├── exporters/               # データエクスポートサービス
│   └── service.py          # JSON/CSVエクスポート
├── utils/                   # ユーティリティ
│   └── logging_config.py   # 構造化ロギング
└── main.py                  # アプリケーションエントリーポイント
```

---

## 機能

### 1. マルチサイト自律スクレイピング

スクレイピング対象:
- **IGN.com** - 主要ゲーム出版物
- **GameSpot.com** - 包括的なゲームカバレッジ
- **PC Gamer** - PC ゲーム中心
- **Polygon.com** - ゲーム文化 & 分析
- **Eurogamer.net** - ヨーロッパのゲームニュース

**機能:**
- 非同期同時スクレイピング (設定可能なワーカー)
- User-Agent ローテーション
- サイト単位のレート制限
- 指数バックオフによるインテリジェント再試行
- タイムアウト処理
- 重複URL検出

### 2. インテリジェント記事抽出

**抽出内容:**
- タイトル、URL、著者、公開日
- 記事本文全文
- サムネイル画像
- タグ/カテゴリ
- 関連ゲームタイトル

**処理:**
- HTML無害化
- コンテンツ正規化
- コンテンツハッシュによる重複検出
- 品質フィルタリング

### 3. AI要約パイプライン

**Claude 3.5 Sonnet または GPT-4 Turbo を使用:**

生成内容:
- **簡潔な要約**: 2-3文の要約
- **ポイント箇条書き**: 3つの主要なテイクアウェイ
- **センチメント**: 強気/弱気/中立/混合
- **ハイプスコア**: 興奮度を示す 0-100
- **カテゴリ**: ニュース/レビュー/フィーチャー/インタビュー/うわさ/更新
- **トレンド確率**: トレンド化の可能性 0-100
- **ゲーマー関心度**: 視聴者関心 0-100

**アーキテクチャ:**
- フォールバック付きAIサービス抽象化
- トークン使用量追跡
- コスト推定
- 非同期リクエスト処理
- 指数バックオフ付き再試行

### 4. 高度な非同期アーキテクチャ

**構築基盤:**
- `asyncio` - 非同期ランタイム
- `aiohttp` - 非同期HTTPクライアント
- `SQLAlchemy 2.0` - 非同期 ORM
- `asyncpg` - ネイティブ非同期PostgreSQLドライバ

**パイプライン機能:**
- セマフォプールによるタスクオーケストレーション
- キューベースアーキテクチャ
- グレースフルシャットダウン処理
- ワーカー同時実行制御
- タイムアウト管理

### 5. PostgreSQL データベース

**スキーマ内容:**
- `articles` - コア記事レコード
- `ai_summaries` - LLM生成分析
- `source_sites` - スクレイピングソースメタデータ
- `scraping_logs` - アクティビティログ
- `trending_scores` - 時系列メトリクス

**最適化:**
- 一般的なクエリ上の複合インデックス
- コネクションプーリング (非同期)
- 効率的なJSON保存
- 正規化された関係

### 6. データエクスポートシステム

**エクスポート形式:**
- 完全なメタデータ付きJSON
- スプレッドシート分析用CSV

**エクスポートタイプ:**
- 要約付きすべての記事
- センチメント別フィルター
- トレンド記事 (24時間/7日)
- カスタムクエリ

### 7. エンタープライズログ

**機能:**
- コンテキスト付き構造化ログ
- ローテーティングファイルハンドラ (10MB、5バックアップ)
- カラーコンソール出力
- 複数のログレベル
- スタックトレースコンテキスト
- アクティビティ監査証跡

### 8. 設定 & シークレット

**環境管理:**
- `.env` ファイルのシークレット
- Pydantic Settings 検証
- ハードコードされた認証情報なし
- 環境ごとのオーバーライド

**設定可能な設定:**
- APIキー (OpenAI, Claude)
- データベース接続文字列
- スクレイパー同時実行とタイムアウト
- 再試行ポリシー
- キャッシュ TTL
- フィーチャーフラグ

---

## インストール & セットアップ

### 前提条件

- Python 3.10+
- Docker & Docker Compose (オプション、推奨)
- PostgreSQL 13+ (Docker を使用しない場合)
- Redis (オプション、キャッシング用)
- Claude または OpenAI のAPIキー

### Docker クイックスタート

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/game-news-ai.git
cd game-news-ai

# 環境テンプレートをコピー
cp .env.example .env

# APIキーで .env を編集
# ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...

# すべてのサービスを開始
docker-compose up -d

# ログを確認
docker-compose logs -f app

# データベースを表示
# postgres://user:password@localhost:5432/game_news_ai
```

### ローカル開発セットアップ

```bash
# 仮想環境を作成
python3.11 -m venv venv
source venv/bin/activate  # Windows では: venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt

# 環境をセットアップ
cp .env.example .env
# .env を編集して設定とAPIキーを入力

# データベースを初期化
python -c "
import asyncio
from app.database.connection import init_db, Database
asyncio.run(Database.create_all_tables())
"

# アプリケーションを実行
python -m app.main
```

---

## 設定

### 環境変数

**データベース:**
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/game_news_ai
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
```

**AI サービス:**
```
AI_PROVIDER=claude                                    # claude または openai
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
AI_TIMEOUT_SECONDS=60
AI_RETRIES=3
```

**スクレイピング:**
```
SCRAPER_CONCURRENT_WORKERS=4
SCRAPER_TIMEOUT_SECONDS=30
SCRAPER_RETRY_ATTEMPTS=3
SCRAPING_INTERVAL_MINUTES=30
RATE_LIMIT_PER_SECOND=2
```

**ログ:**
```
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=logs/app.log
LOG_MAX_BYTES=10485760           # 10MB
LOG_BACKUP_COUNT=5
```

**デプロイ:**
```
ENVIRONMENT=production            # development, staging, production
DEBUG=False
ENABLE_HEALTH_CHECK=True
ENABLE_SENTRY=False
SENTRY_DSN=https://...
```

---

## 使用方法

### パイプラインの実行 (自律)

```bash
# デーモンを開始 (スケジュール間隔で継続実行)
python -m app.main

# パイプラインは 30 分ごとに実行 (設定可能)
# スクレイプ → 処理 → 保存 → 要約 → エクスポート
```

### 1回のパイプラインサイクルを実行

```python
import asyncio
from app.pipelines.processing import run_pipeline_once
from app.database.connection import init_db, close_db

async def main():
    await init_db()
    stats = await run_pipeline_once()
    await close_db()
    print(stats)

asyncio.run(main())
```

### 結果をクエリ

```python
from sqlalchemy import select
from app.models.models import Article, AISummary, SentimentType
from app.database.connection import get_session_factory

async def get_trending_games():
    factory = get_session_factory()
    async with factory() as db:
        # 要約付き記事を取得
        query = (
            select(Article, AISummary)
            .outerjoin(AISummary)
            .where(AISummary.hype_score > 80)
            .order_by(AISummary.hype_score.desc())
            .limit(10)
        )
        result = await db.execute(query)
        return result.all()
```

### データをエクスポート

```python
from app.exporters.service import ExportService
from app.database.connection import get_session_factory

async def export_results():
    factory = get_session_factory()
    async with factory() as db:
        export_service = ExportService(db)
        
        # すべての記事をエクスポート
        json_path = await export_service.export_all_articles(format_type="json")
        csv_path = await export_service.export_all_articles(format_type="csv")
        
        # トレンド記事をエクスポート
        trending_path = await export_service.export_trending(hours=24)
        
        # センチメント別にエクスポート
        bullish_path = await export_service.export_by_sentiment("bullish")
```

---

## データベーススキーマ

### 記事テーブル

```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(512) NOT NULL,
    url VARCHAR(2048) NOT NULL UNIQUE,
    author VARCHAR(255),
    body TEXT NOT NULL,
    published_at TIMESTAMP NOT NULL,
    scraped_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    thumbnail_url VARCHAR(2048),
    tags JSON DEFAULT '[]',
    related_games JSON DEFAULT '[]',
    category VARCHAR(50),
    source_site VARCHAR(100) NOT NULL,
    is_duplicate BOOLEAN DEFAULT FALSE,
    is_processed BOOLEAN DEFAULT FALSE,
    content_hash VARCHAR(64) UNIQUE
);

-- インデックス
CREATE INDEX idx_article_source_published ON articles(source_site, published_at);
CREATE INDEX idx_article_processed ON articles(is_processed, published_at);
CREATE INDEX idx_article_duplicate ON articles(is_duplicate);
```

### AI 要約テーブル

```sql
CREATE TABLE ai_summaries (
    id SERIAL PRIMARY KEY,
    article_id INTEGER NOT NULL UNIQUE REFERENCES articles(id),
    summary TEXT NOT NULL,
    bullet_points JSON DEFAULT '[]',
    sentiment VARCHAR(20) NOT NULL,  -- bullish, bearish, neutral, mixed
    hype_score INTEGER NOT NULL,     -- 0-100
    trend_probability FLOAT,         -- 0.0-1.0
    gamer_interest INTEGER,          -- 0-100
    main_category VARCHAR(100),
    mentioned_games JSON DEFAULT '[]',
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    estimated_cost FLOAT NOT NULL,
    ai_model_used VARCHAR(100),
    ai_provider VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- インデックス
CREATE INDEX idx_summary_sentiment ON ai_summaries(sentiment);
CREATE INDEX idx_summary_hype_score ON ai_summaries(hype_score);
CREATE INDEX idx_summary_trend_probability ON ai_summaries(trend_probability);
```

---

## API コスト & 推定

### 現在の価格 (2024)

**Claude 3.5 Sonnet:**
- 入力: 100万トークンあたり $3
- 出力: 100万トークンあたり $15

**GPT-4 Turbo:**
- 入力: 100万トークンあたり $10
- 出力: 100万トークンあたり $30

### コスト推定

```python
# 例: 1日あたり 100 記事
# 平均記事: 500 入力トークン、200 出力トークン

# Claude:
# 入力コスト: (100 * 500 / 1,000,000) * $3 = $0.15/日
# 出力コスト: (100 * 200 / 1,000,000) * $15 = $0.30/日
# 合計: 約 $0.45/日 = 約 $13.50/月

# GPT-4:
# 入力コスト: (100 * 500 / 1,000,000) * $10 = $0.50/日
# 出力コスト: (100 * 200 / 1,000,000) * $30 = $0.60/日
# 合計: 約 $1.10/日 = 約 $33/月
```

---

## テスト

### すべてのテストを実行

```bash
pytest tests/ -v

# カバレッジ付き
pytest tests/ --cov=app --cov-report=html

# 特定のテストファイルを実行
pytest tests/test_scrapers.py -v

# 特定のテストを実行
pytest tests/test_scrapers.py::test_article_data_hash -v

# 非同期テストを実行
pytest tests/ -v -m asyncio
```

### テスト例

```python
# スクレイパーテスト
test_article_data_hash()
test_rate_limiter()
test_scraper_url_normalization()
test_scraper_html_cleaning()

# サービステスト
test_article_creation()
test_duplicate_detection()
test_summarization()

# データベーステスト
test_database_connection()
test_article_queries()
test_transaction_handling()
```

---

## パフォーマンスメトリクス

### ベンチマーク結果

- **スクレイピング**: 50-100 記事/分 (4並行ワーカー)
- **AI要約**: 10-20 記事/分 (Claude API制限)
- **データベース書き込み**: 1000+ 記事/分
- **クエリパフォーマンス**: トレンドクエリで <100ms
- **メモリ使用量**: ベース ~200-300MB、プールサイズに応じてスケーリング

### 最適化戦略

1. **接続プーリング**: プリウォーミング非同期接続プール
2. **バッチ処理**: 設定可能なバッチで記事を処理
3. **キャッシング**: 頻繁にアクセスされるデータ用 Redis レイヤー
4. **インデックス**: クエリヘビーな列への戦略的インデックス
5. **並行ワーカー**: 設定可能な非同期セマフォ

---

## デプロイ

### Docker Compose (推奨)

```bash
# すべてのサービスを開始
docker-compose up -d

# ログを表示
docker-compose logs -f app

# ワーカーをスケーリング (必要に応じて)
docker-compose up -d --scale app=3

# シャットダウン
docker-compose down
```

### Kubernetes デプロイ

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: game-news-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: game-news-app
  template:
    metadata:
      labels:
        app: game-news-app
    spec:
      containers:
      - name: app
        image: game-news-ai:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: anthropic
```

### 環境別設定

**開発:**
```
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG
SCRAPER_CONCURRENT_WORKERS=2
```

**ステージング:**
```
ENVIRONMENT=staging
DEBUG=False
LOG_LEVEL=INFO
SCRAPER_CONCURRENT_WORKERS=4
```

**本番:**
```
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
SCRAPER_CONCURRENT_WORKERS=8
DATABASE_POOL_SIZE=50
ENABLE_SENTRY=True
```

---

## 監視 & 観測可能性

### ヘルスチェック

```bash
# アプリケーションヘルス
curl http://localhost:8000/health

# データベース接続性
curl http://localhost:8000/health/db

# Redis 接続性
curl http://localhost:8000/health/cache
```

### ログの例

```
[INFO] 2024-01-15 10:30:45 - パイプラインがスクレイピング段階を開始しました
[INFO] 2024-01-15 10:31:05 - IGN: 25 記事をスクレイピング
[INFO] 2024-01-15 10:31:15 - GameSpot: 18 記事をスクレイピング
[INFO] 2024-01-15 10:31:25 - フェーズ 2: 記事の処理と保存
[INFO] 2024-01-15 10:31:35 - 40 記事を保存
[INFO] 2024-01-15 10:31:36 - フェーズ 3: AI で記事を要約中
[INFO] 2024-01-15 10:32:15 - 15 記事を要約
[INFO] 2024-01-15 10:32:16 - パイプライン完了: {'scraped': 67, 'stored': 40, 'summarized': 15}
```

### メトリクス収集

- サイト別にスクレイピングされた記事数
- 重複率の割合
- AI 要約成功率
- 平均処理時間
- 1日/月ごとの API コスト
- データベースクエリパフォーマンス

---

## プラットフォームの拡張

### 新しいスクレイパーを追加

```python
from app.scrapers.base import ScraperBase, ArticleData

class CustomSiteScraper(ScraperBase):
    def __init__(self):
        super().__init__(
            site_name="CustomSite",
            base_url="https://customsite.com",
            timeout=30
        )
    
    async def scrape(self):
        articles = []
        html = await self.fetch_page("https://customsite.com/news")
        
        # HTML を解析して記事を抽出
        soup = BeautifulSoup(html, 'html.parser')
        for element in soup.find_all('article', limit=20):
            article = ArticleData(...)
            articles.append(article)
        
        return articles

# get_all_scrapers() に登録
```

### カスタム AI プロバイダー

```python
class CustomAIService(AIServiceBase):
    async def summarize_article(self, article_content):
        # カスタム実装
        pass
    
    async def extract_entities(self, text):
        # カスタム実装
        pass
```

### カスタムエクスポート形式

```python
async def export_xml(articles, path):
    # XML エクスポート実装
    pass
```

---

## トラブルシューティング

### よくある問題

**問題**: API レート制限
```
解決策: SCRAPER_TIMEOUT_SECONDS を増やし、SCRAPER_CONCURRENT_WORKERS を減らします
```

**問題**: データベース接続プール枯渇
```
解決策: アクティブな接続を確認し、DATABASE_POOL_SIZE を増やし、クエリタイムアウトを確認します
```

**問題**: AI API タイムアウト
```
解決策: AI_TIMEOUT_SECONDS を増やし、バッチサイズを減らし、ネットワーク接続を確認します
```

**問題**: メモリ使用量が増加
```
解決策: 接続プール プリピングを有効にし、バッチサイズを減やし、ガベージコレクションを有効にします
```

---

## 本番環境チェックリスト

- [ ] `ENVIRONMENT=production` を設定
- [ ] `DEBUG=False` を設定
- [ ] 強力なデータベースパスワードを設定
- [ ] 有効な API キー (Claude/OpenAI) を設定
- [ ] Sentry エラー追跡を有効化
- [ ] キャッシング用に Redis を設定
- [ ] ログローテーション & リテンション を設定
- [ ] ヘルスチェック監視を設定
- [ ] データベースバックアップを設定
- [ ] リソース制限 (CPU、メモリ) を設定
- [ ] レート制限を有効化
- [ ] スクレイピング画像用に CDN を設定
- [ ] 障害時のアラートを設定

---

## 今後の改善

### フェーズ 2 機能
- [ ] リアルタイム WebSocket ストリーミング
- [ ] ML ベースのゲームタイトル認識
- [ ] 高度な NLP エンティティ抽出
- [ ] 多言語サポート
- [ ] 画像処理と分析
- [ ] ビデオゲームトレーラースクレイピング
- [ ] コミュニティセンチメント統合 (Twitter、Reddit)

### フェーズ 3 機能
- [ ] ダッシュボード UI (React/Vue)
- [ ] 認証付き REST API
- [ ] GraphQL エンドポイント
- [ ] 高度なフィルタリングと検索
- [ ] カスタマイズ可能なアラート
- [ ] サードパーティ統合
- [ ] モバイルアプリ
- [ ] 機械学習推奨

### スケーラビリティロードマップ
- [ ] Kubernetes でのスケーリング
- [ ] マルチリージョンデプロイ
- [ ] シャード化データベース戦略
- [ ] 高度なキャッシング階層
- [ ] メッセージキュー統合 (RabbitMQ/Kafka)
- [ ] 検索エンジン統合 (Elasticsearch)

---

## ライセンス

MIT ライセンス - [LICENSE](LICENSE) ファイルを参照

---

## サポート & 貢献

### 貢献

貢献を歓迎します。次の手順に従ってください:

1. リポジトリをフォーク
2. フィーチャーブランチを作成
3. 新機能についてテストを追加
4. プルリクエストを送信

### ヘルプを取得

- 📧 メール: support@gamenewsai.com
- 💬 Discord: [コミュニティに参加](https://discord.gg/gamenewsai)
- 📖 ドキュメント: [完全ドキュメント](https://docs.gamenewsai.com)
- 🐛 イシュー: [GitHub Issues](https://github.com/yourusername/game-news-ai/issues)

---

## 謝辞

構築者:
- SQLAlchemy 2.0
- Anthropic Claude API
- OpenAI API
- PostgreSQL
- FastAPI (非同期基盤)
- Beautiful Soup 4
- Playwright

---

**AI エンジニアリングチームによって ❤️ で作成されました**
