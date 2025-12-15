# 開発方針 (Development Policy)

このドキュメントは `clip.moukaeritai.work` の開発方針と要件を定義する。

## 1. 概要 (Overview)
*   **目的**: ウェブ上のクリップボードとして、認証なしのデータストアを提供する。
*   **ドメイン**: `clip.moukaeritai.work`

## 2. 技術スタック (Technology Stack)
*   **言語**: Python 3.12
*   **フレームワーク**: FastAPI
*   **パッケージ管理**: Poetry
*   **データベース**: SQLite (サーバーレス、単一ファイル)

## 3. アーキテクチャとインフラ (Architecture & Infrastructure)
*   **リバースプロキシ**: Apache が前段に配置される。
    *   TLS終端は Apache が行う。
    *   Apache からアプリケーションへは `8000/tcp` で平文接続される。
    *   通信経路: User -> HTTPS -> Apache -> HTTP -> FastAPI (This App)
*   **セキュリティ設定**:
    *   HTTPS だけでなく HTTP での通信も許容する。

## 4. 認証とセキュリティモデル (Auth & Security Model)
*   **認証**: なし (No Authentication)
*   **セキュリティモデル**:
    *   ユーザーが生成した **UUIDv4** をURLに含めることでアクセス制御を行う。
    *   UUIDv4 の予測不可能性のみに依存するセキュリティモデルである。

## 5. API仕様 (REST API)

### ランディングページ
*   **URL**: `https://clip.moukaeritai.work/index.html`
*   **機能**: 同一ディレクトリにある `index.md` を読み込み、**ブラウザ側（フロントエンド）** でレンダリングして表示する。
*   **ドキュメント**: 使い方は `index.md` に記載する。

### クリップボード操作 API
ベースパス: `https://clip.moukaeritai.work/<UUIDv4>`

| メソッド | パス | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| **PUT** | `/<key>` | 任意の文字列を保存する。 | |
| **GET** | `/<key>` | 文字列を取得する。 | Content-Type は `text/plain` 固定。 |
| **DELETE** | `/<key>` | アイテムを削除する。 | |
| **POST** | `/` | 文字列を新規保存する。 | キーは文字列の SHA1 ハッシュ値が自動生成される。<br>レスポンスは生成されたキーを含むJSONを返却する。 |
| **GET** | `/` | キーの一覧を取得する。 | UUIDv4を知っているユーザー＝所有者とみなす。<br>レスポンスはキーのリストを含むJSONを返却する。 |

### 管理・その他 API
*   **Status**: `https://clip.moukaeritai.work/status`
    *   動作確認用エンドポイント。表示内容は未定。
*   **MCP**: `https://clip.moukaeritai.work/mcp`
    *   Model Context Protocol (MCP) 向けのエンドポイント。
    *   標準仕様に従ってツール等の定義を実装する。

## 6. データ制約とエラーハンドリング (Constraints & Error Handling)
コード内にハードコードせず、設定可能な定数として扱うこと。

*   **文字コード**: UTF-8
*   **値 (Value) の制限**:
    *   任意の文字列。
    *   最大サイズ: **1MB** / key
*   **キー (Key) の制限**:
    *   任意の文字列。
    *   最大長: **100文字**
*   **エラーハンドリング**:
    *   制限超過時: **HTTP 413 (Payload Too Large)** を返す。
    *   エラー詳細: JSON形式でレスポンスする。
    *   *Note*: エラーおよびPOST成功時のJSONスキーマは実装時に決定する。

## 7. データベース運用 (Database Operations)
*   定期的なクリーンアップが行われるが、ロジックはこのアプリケーション**外**のプロセス (cron等) が担当する。
*   本アプリケーションにはクリーンアップ機能を実装しない。

## 8. 開発上の注意 (Development Notes)
*   **FQDN**: `localhost` でのテストを容易にするため、コード内にFQDN (`clip.moukaeritai.work`) をハードコードしない。
