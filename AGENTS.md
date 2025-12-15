# このリポジトリで開発しているもの

このリポジトリでは、ウェブ上のクリップボードとして、認証なしのデータストアを提供するためのウェブアプリケーション開発を行う。

このウェブアプリケーションのドメインは clip.moukaeritai.work である。

# 使用言語

Python 3.12 を想定している。
FastAPIを使用することを想定している。

# パッケージ管理

Poetry を使ってパッケージ管理する。

# Apache との関係

clip.moukaeritai.work ではすでにApacheが動いており、
TLSの終端もApacheが行う。
このウェブアプリケーションはApacheからリバースプロキシで接続されることを想定している。
Apacheからは 8000/tcp で平文で接続される。

# 認証

認証は行わない。
ユーザーが生成したUUIDv4を含む十分に予測不可能なURLであることを想定しているからである。

# REST API
https://clip.moukaeritai.work/index.html がランディングページである。
使い方は https://clip.moukaeritai.work/index.md に記載する。
https://clip.moukaeritai.work/index.html は同じディレクトリにある index.md を読み込み、ブラウザ側（フロントエンド）でレンダリングする。


クリップボードの各アイテムは https://clip.moukaeritai.work/<UUIDv4>/<key> という形式で提供する。
https://clip.moukaeritai.work/<UUIDv4>/<key> に任意の文字列をPUTできる。
https://clip.moukaeritai.work/<UUIDv4>/<key> から文字列をGETできる。この際の Content-Type は text/plain 固定とする。
https://clip.moukaeritai.work/<UUIDv4>/<key> をDELETEできる。
https://clip.moukaeritai.work/<UUIDv4> に文字列をPOSTしたときには、その文字列のSHA1ハッシュ値が自動的にkeyとして採用される。POSTのレスポンスはJSON形式でキーを返却する。
つまりREST APIも提供する。

# データ制約

- 投入できる値は任意の文字列とし、文字コードは UTF-8 を想定する。
- 1つのキーに対する値の最大サイズは 1MB とする。
- キーは任意の文字列とするが、最大長は 100文字 とする。
- これらの制限値（1MB, 100文字）は将来変更する可能性があるため、コード内にハードコードせず、設定可能な定数として扱う。
- キー長や値のサイズ制限を超過した場合は、HTTP 413 (Payload Too Large) を返す。
- エラーの詳細はJSON形式でレスポンスする。
- なお、エラーレスポンスのJSONスキーマや、POST成功時にキーを返却する際のJSONスキーマは現時点では未定とし、実装時に決定する。


# MCP
https://clip.moukaeritai.work/mcp 
でMCP （Model Context Protocol）向けのエンドポイントを提供する。
MCPとして機能するために必要なツールの説明なども
MCPの標準仕様に従って実装する。

# データベース

バックエンドデータベースにはサーバを使わず、SQLite ファイルを使う。

# セキュリティ

通信には HTTPS だけでなく HTTP も許容する。
なお、定期的にデータベースはクリーンアップされるが、
クリーンアップのロジックはこのウェブアプリケーション以外のcronで起動されるプロセスから行うため、
このウェブアプリケーションではデータベースのクリーンアップを実装しない。

# コードに関するその他の注意点

localhost でテストできるように、コードにはFQDNをハードコードしない。
