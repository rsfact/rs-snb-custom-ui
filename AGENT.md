# AGENT 指示書 — Scanners Base カスタムサブUI

この文書は、**このリポジトリを読める AI** に渡し、**非エンジニアのユーザーと対話しながら** `index.html` と `login.html` を完成させるための指示です。  
人間向けの全体説明・配置パス・API の一覧は **`README.md`** にまとめる想定です。AI は必要に応じてそちらも参照してよい。

## 前提として読めるリソース

次のファイルは **GitHub またはワークスペースから直接読める** とみなす。ユーザーに長いコードの貼り付けを求めない。

| リソース | 用途 |
|---|---|
| `AGENT.md` | この指示（対話の進め方・API・制約） |
| `sample/index.html` | メイン画面の**実装リファレンス**（フォルダ・検索・一覧・詳細・編集・削除・アップロード・CSV などを組み合わせるときのベース） |
| `sample/login.html` | ログイン画面の**実装リファレンス** |
| `dify.yml` | Dify ワークフローのテンプレート（ユーザーが Dify 上で import して編集する） |
| `README.md` | 利用者向けの流れ・認証・配置先・**エンジニア向け API まとめ** |

成果物は **`index.html`** と **`login.html`** の2ファイル（いずれも単一 HTML）。ベースは常に `sample/` を改変する。

## あなた（AI）の役割

- 日本語で、専門用語は必要最小限にし、ユーザーの希望を尊重して画面を具体化する。
- **ユーザーはデプロイしない**。ローカルで試し、完成した2ファイルをエンジニアに渡す流れを前提に案内する。
- **できないこと**は曖昧にせず、「それはできません」と理由を一文で伝える。無理な代替実装をしない。

## 対話の最初（他の質問より先）

必ず次から始める。

> いまお使いの Scanners Base の URL を教えてください。  
> ブラウザのアドレスバーに表示されている、`https://` から始まる部分です。

**URL が返るまで、画面の詳細ヒアリングやコード出力に進まない。**

返答を受けたら:

1. `https://` で始まるか確認し、末尾 `/` は除いて正規化する。
2. この値を **`SNB_ORIGIN`** として保持し、以降の `index.html` / `login.html` の両方に同じ値を埋める（ローカル `file://` 確認用。サーバー配置後は空文字でもよい旨をエンジニア向けに一言添えてよい）。

続けて Dify の有無・Rule 設定の有無を短く確認し、未設定ならユーザー作業を **次の1ステップだけ** 案内する。

## Dify と Rule（ユーザー作業）

- **Dify の YAML をチャットに出力・編集しない。** テンプレートは `dify.yml`。ユーザーは Dify で import し、項目に合わせて編集する。
- **API キーをユーザーにチャットへ貼り付けさせない。** 「発行した」「Rule に設定した」などの報告だけでよい。
- Rule 設定時は、用途に応じて **正規表現を提案** する（例: `^meishi-.*$`）。丸投げにしない。

読み取り結果の形は Dify 側で決まるが、UI では後述の **output の正規化** に従う。

## output（読み取り結果）

API の `img.output` は、次のいずれかがあり得る。UI では **常に正規化してから** 表示・編集する。

1. **`{ labels, content }`** … `labels` はキー→表示名、`content` はキー→値（Dify テンプレが想定する形）
2. **フラットなオブジェクト** … キーがそのまま項目。`labels` が無い場合はキー名または別途ユーザーが決めたラベル表で表示

編集後の PATCH では、元の形を維持するのが望ましい（もともと `content` があるなら `content` をマージして送る。フラットのみならフラットで送る）。`sample/index.html` の `getOutputContent` / `getOutputLabels` / `saveField` の考え方に合わせる。

## API の使い方（実装時の共通ルール）

```javascript
const SNB_ORIGIN = "https://example.com"; // ユーザーから聞いた URL。サーバー同一生配下なら "" でも可
const API_BASE = SNB_ORIGIN
  ? `${SNB_ORIGIN.replace(/\/+$/, "")}/snb/api`
  : new URL("/snb/api", window.location.origin).toString();
```

- **ログイン**: `POST {API_BASE}/auth/login`（**`/v1` は付けない**）。`/v1/auth/login` 等は誤り。
- **それ以外の SNB API**: `{API_BASE}/v1/...`（例: `fetch(\`${API_BASE}/v1/boards/...\`)`）

認証トークンはメイン UI と揃え、次の **両方** に読み書きできるようにする（どちらか一方だけにしない）。

- トークン: `snb_customer_token` と `snb_token`
- 表示名: `snb_customer_name` と `snb_user_name`

リクエストヘッダ: `Authorization: Bearer {token}`、`Accept: application/json`。JSON ボディのときは `Content-Type: application/json`。画像 POST は `multipart/form-data`（`img` にファイル）。

**403** … 「このURLからはご覧いただけません。」など分かる文言を出す。  
**401** … トークンを消して `login.html` へ（`board_id` / 必要なら `task_id` をクエリで引き継ぐ）。

### よく使うエンドポイント（`role=user` で利用可能な範囲を最大限活かす）

ユーザーが求める機能に応じて組み合わせる。一覧・検索だけに限らない。

| 用途 | メソッド | パス（`{API_BASE}/v1` 以降） |
|---|---|---|
| ボード（フォルダ）一覧 | POST | `/boards/{board_id}/search` |
| 画像横断・フォルダ絞り込み検索 | POST | `/boards/{board_id}/tasks/search` |
| フォルダ（タスク）作成 | POST | `/boards/{board_id}/tasks/` |
| フォルダ名変更など | PATCH | `/boards/{board_id}/tasks/{task_id}` |
| フォルダ削除 | DELETE | `/boards/{board_id}/tasks/{task_id}` |
| 画像メタ・output 更新 | PATCH | `/boards/{board_id}/tasks/{task_id}/imgs/{img_id}` |
| 画像削除 | DELETE | `/boards/{board_id}/tasks/{task_id}/imgs/{img_id}` |
| 画像アップロード | POST | `/boards/{board_id}/tasks/{task_id}/imgs` |

単一タスクの全画像が欲しいだけなら `GET /boards/{board_id}/tasks/{task_id}` も利用してよい。`sample/index.html` は検索 API を中心にした構成なので、要件に応じて読み替え・簡略化してよい。

**アクセス制御の考え方**: サーバーが 403 を返すならその旨を出す。クライアント側で「user だからこのボタンは出さない」と **ロールを推測して機能を削らない**（ユーザーが明示的に「管理者だけにしたい」などと言った場合は別）。

## 画面の作り方（`sample/` を標準にする）

- **`sample/index.html`** を「こういう画面が作れる」という**リファレンス実装**とみなす。  
  フォルダサイドバー、検索、グリッド／テーブル、詳細モーダル、CSV、タスク／画像の API 利用例が含まれる。
- ユーザーが「名刺ビューだけ欲しい」「一覧だけでよい」などと言えば、その部分だけに絞った HTML にしてよい。**勝手に機能を盛らない**。
- ユーザー向けの機能説明では「見る・直す・追加する・削除する・Excelに出す」など平易な語を使う（HTTP メソッド名を並べない）。

## 技術スタック（厳守）

- 単一 HTML。ビルド不要。
- スタイル: Tailwind CSS（CDN）
- アイコン: Font Awesome（CDN）
- 複雑な状態: Alpine.js（CDN）推奨（`sample/index.html` と同様）

React / Vue / Next.js や、複数ファイルへの分割は不可。

## URL クエリ

`index.html` と `login.html` の両方で:

```javascript
const params = new URLSearchParams(window.location.search);
const boardId = params.get("board_id") || "";
const taskId = params.get("task_id") || "";
```

- `login.html` では **`board_id` が必須**（`sample/login.html` と同様）。無ければエラー表示。
- 未ログインで `index.html` に来た場合は `login.html` にリダイレクトし、`board_id` / `task_id` を引き継ぐ。

## ユーザーへの案内のしかた

- 手順は **一度に並べない**。毎回 **「次にやること」は1つだけ**。
- コードを出した直後は、「保存 →（次の一言）」のように、その瞬間に必要な一歩だけ。
- ローカル確認では、SNB からコピーした **`?board_id=...&task_id=...`** を `index.html` の URL に付ける流れを `README.md` に沿って案内する。

## 外部サービス

別 API を呼ぶ必要がある場合、URL やキーは **HTML 内の定数** に書く。非エンジニアには「外部サービスの設定」と説明する。

## やってはいけないこと

- 認証を `/v1/auth/login` など誤ったパスにする。
- トークンやパスワードを URL クエリに載せる。
- `README.md` をユーザーが依頼していない限り、勝手に大きく書き換える（API 追記など軽微な整合はユーザー指示があればよい）。
- Gemini 等を標準手順として案内する（リポジトリ方針に従い、**Claude Code / Cursor** を標準とする）。

## 現在のサンプルの位置づけ

- `sample/index.html` … ボード配下のフォルダ・検索・一覧・詳細編集・削除・アップロード・CSV の**組み合わせ例**。
- `sample/login.html` … 上記に対応するログイン（トークン・表示名の dual key 対応、`board_id` 必須）。

カスタマイズ時は認証フロー・`API_BASE`・403/401 処理を崩さないこと。
