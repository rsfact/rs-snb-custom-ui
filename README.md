# Scanners Base カスタムサブUI テンプレート

Scanners Base（以下 SNB）のメイン画面からリンクされる、**カスタム閲覧・編集UI** を作るためのテンプレートリポジトリです。

非エンジニアの方が、普段お使いの AI（Gemini など）と対話しながら画面を作り、**ローカルで試しながら調整**し、完成したコードをエンジニアに渡します。デプロイ作業自体はエンジニアが行います。

## サブシステムとは

SNB 本体でアップロード・読み取りされたドキュメントを、**admin 権限の人が配布・閲覧用 UI として使える仕組み**です。

- SNB メイン画面（ボード）で Rule を作り、Task にドキュメントをアップロードする
- 各 Task から、このリポジトリで作ったカスタム UI へ遷移する
- user ロールの人は自分の Task だけ一覧できる。URL を知っていれば個別 Task は CRUD 可能
- admin はすべての Task を一覧・操作できる

```
SNB メイン画面（ボード）
  └─ Rule を作成 → Task を作成 → ドキュメントをアップロード
       └─ タスクのクエリをコピー
            └─ カスタムサブUI（このリポジトリで作った HTML）
                 ?board_id=xxx&task_id=yyy
```

## このリポジトリで作るもの

| ファイル | 役割 |
|---|---|
| `frontend/index.html` | メイン画面（タスクの読み取り結果を表示） |
| `frontend/login.html` | ログイン画面 |
| `dify.yml` | Dify ワークフローのテンプレート（output 部分を書き換えて import 用） |
| `AGENT.md` | AI が読む設計書・API仕様・作業手順 |
| `README.md` | 人間向けの説明（このファイル） |

---

## 作業の流れ（非エンジニア向け）

デプロイはエンジニアが行います。あなたが行うのは、**AI と対話して HTML を作り、ローカルで試す**ところまでです。

### 1. AI と対話して HTML を作る

1. この GitHub リポジトリを、普段お使いの AI に渡す
2. AI が URL → **Dify 済みか** → output 構造の順に確認する
3. **Dify 済み** → 構造化出力 JSON をそのまま貼り付ける  
   **Dify 未設定** → AI が `{ labels, content }` で項目案を提案 → **「Dify、お作りしましょうか？」** と提案 → 必要なら `dify.yml` を書き換えて出力 → Dify に import
4. output・Dify・Rule の準備が整ったら、「こんな画面が作りたい」と対話する
5. AI が `index.html` と `login.html` を出力する（デザインの説明付き。**次にやること1つだけ** 案内される）

### 2. ローカルに貼り付ける

1. このリポジトリを PC にダウンロードする（または AI の出力をそのまま使う）
2. `frontend/index.html` をメモ帳などで開く（Windows なら右クリック → プログラムから開く → メモ帳）
3. AI が出してくれたコードを **すべて** 貼り付けて保存する
4. 同様に `frontend/login.html` も保存する

### 3. SNB で Rule・Task を作り、試しにアップロードする

1. SNB にログインする
2. **Dify** … AI が `dify.yml` を書き換えて渡す場合は、それを Dify に **import（DSL のインポート）** する。自分で組む場合も output は `{ labels, content }` 形式
3. **Rule** を作成する。最低限、次を設定する:
   - **name**（Rule 名）
   - **Dify URL**
   - **Dify API キー**
   - **正規表現**（ボード ID にマッチするパターン）
4. **Task** を作成する
5. 試し用のドキュメントをアップロードする
6. 読み取り結果（output）が想定どおり返ることを確認する

### 4. クエリをコピーして、ローカルで確認する

1. SNB のボード画面で、作成した Task のカード左上にマウスを乗せる
2. 表示される **クエリ**（`?board_id=...&task_id=...`）をクリックしてコピーする
3. PC 上の `frontend/index.html` をブラウザで開く
4. アドレスバーの末尾に、コピーしたクエリを貼り付けて Enter

   例:

   ```
   file:///C:/Users/あなた/Downloads/scanners-base-sub-ui/frontend/index.html?board_id=abc&task_id=xyz
   ```

5. ログイン画面が出たら、SNB と同じメールアドレス・パスワードでログインする
6. 読み取り結果が画面に表示される

> **ローカル確認の前提**  
> PC から直接 `index.html` を開く場合、HTML 内の `SNB_ORIGIN` にメインシステムの URL が入っている必要があります。  
> AI は対話の最初に URL を聞くので、教えておけばコードに自動で設定されます。

### 5. 結果を見て、UI を調整する

1. 表示内容・レイアウト・色などを確認する
2. 直したい点を AI に伝える（「氏名を大きく」「金額順に並べたい」など）
3. AI が出した新しいコードを、再びメモ帳で `index.html` に貼り付ける
4. ブラウザを更新（F5）して確認する
5. 満足いくまで **4 → 5** を繰り返す

### 6. 完成したコードをエンジニアに共有する

1. 完成した `index.html` と `login.html` をエンジニアに渡す
2. エンジニアが SNB サーバーに配置し、Rule の遷移先 URL を設定する
3. 以降、SNB の Task からその UI へ直接遷移できるようになる

---

## ローカル確認のコツ

| 項目 | 説明 |
|---|---|
| `SNB_ORIGIN` | HTML 先頭付近にある SNB の URL。ローカル確認時のみ設定する |
| クエリ | `?board_id=xxx&task_id=yyy` の形式。Task カードからコピーする |
| ログイン | SNB と同じアカウント。一度ログインすれば、同じブラウザでは再ログイン不要 |
| 更新 | コードを貼り替えたら、ブラウザで F5（再読み込み）する |

うまく表示されないとき:

- `SNB_ORIGIN` が SNB の URL と一致しているか確認する
- クエリがアドレスバーに付いているか確認する
- SNB と同じアカウントでログインしているか確認する

---

## 配置先 URL（エンジニア向け参考）

完成後、エンジニアが SNB サーバー上の次のパスに配置します。

```
{BASE_URL}/snb/custom/{folder_name}/index.html
{BASE_URL}/snb/custom/{folder_name}/login.html
```

Rule の遷移先 URL（ext_url）の例:

```
{BASE_URL}/snb/custom/{folder_name}/index.html
```

Task クリック時の遷移先:

```
{BASE_URL}/snb/custom/{folder_name}/index.html?board_id={board_id}&task_id={task_id}
```

---

## 認証

- ログインアカウントは **SNB メインシステムと共通**
- ログイン成功後、JWT トークンをブラウザの `localStorage` に保存する
- API 呼び出し時は `Authorization: Bearer {token}` ヘッダーを付与する

## アクセス制御

**一覧の流出だけ防ぐ。admin が配布した URL から開けば、user も GET / PATCH / DELETE / POST できる。**

| | user | admin |
|---|---|---|
| 個別タスクの CRUD（URL で `board_id` + `task_id` 指定） | 可 | 可 |
| タスク一覧・横断検索 | 自分の分のみ | 全件 |

403 が返った場合、UI 側では「このURLからはご覧いただけません。」と表示します。

## デフォルトサンプル UI の動作

`frontend/` に入っているのは、**最小構成のプレーンなサンプル**です（編集・削除 UI なし）。

- URL パラメータ `board_id` / `task_id` からタスクを取得
- 画像一覧をテーブル表示
- 行クリックでモーダルに読み取り結果を表示
- CSV 出力
- 未ログイン時は `login.html` へリダイレクト

AI との対話では、作りたい機能をそのまま伝えればよい（編集・削除・並べ替えなど）。用途のカテゴリ分けは不要。

## output スキーマ

読み取り結果 `output` は **`labels` + `content` 形式のみ** 使用します。この形式は固定で、変更できません。変えられるのは中の項目名・ラベル・値だけです。

```json
{
  "labels": { "name": "氏名", "company": "会社名" },
  "content": { "name": "山田太郎", "company": "株式会社ABC" }
}
```

- `labels` … 各項目の日本語ラベル
- `content` … 読み取り結果の値

Rule 作成時にこの形式で output を決め、AI との対話でも同じ形式を伝えてください。

## 外部 API

外部サービスとの連携（例: 登録番号から会社名を取得）が必要なら、HTML 内に設定値を直接書き込みます。

## API エンドポイント（参考）

API のベース URL は `{BASE_URL}/snb/api` です。

| 操作 | メソッド | パス | 備考 |
|---|---|---|---|
| ログイン | POST | `/snb/api/auth/login` | 共通 |
| タスク取得 | GET | `/snb/api/v1/boards/{board_id}/tasks/{task_id}` | user / admin 共通 |
| タスク一覧 | POST | `/snb/api/v1/boards/{board_id}/tasks/search` | user は自分の分のみ |
| 画像更新 | PATCH | `/snb/api/v1/boards/{board_id}/tasks/{task_id}/imgs/{img_id}` | user / admin 共通 |
| 画像削除 | DELETE | `/snb/api/v1/boards/{board_id}/tasks/{task_id}/imgs/{img_id}` | user / admin 共通 |
| 画像アップロード | POST | `/snb/api/v1/boards/{board_id}/tasks/{task_id}/imgs` | user / admin 共通 |

## 技術スタック

- HTML（単一ファイル、ビルド不要）
- Tailwind CSS（CDN）
- Font Awesome（CDN）
- Alpine.js（CDN、編集 UI など複雑な画面で使用可）
