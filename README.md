# プロジェクト環境構築手順

## フォルダ構成

このプロジェクトはPythonで開発されており、Dockerを使用して環境を構築しています。以下はプロジェクトのフォルダ構成です。

```
trading_project
├── Dockerfile
├── README.md
├── app
│   ├── main.py
├── main.py
├── data
├── docker-compose.yml
├── postgres_data
└── requirements.txt

```

- **`Dockerfile`**: Dockerイメージのビルドに使用されるファイルです。Python 3をベースにしています。
- **`README.md`**: プロジェクトの概要や使い方に関するドキュメンテーションが記載されたファイルです。
- **`app`**ディレクトリ: プロジェクトのPythonアプリケーションファイルが含まれています。
- **`data`**ディレクトリ: アプリケーションが使用するデータが保存されるディレクトリです。
- **`docker-compose.yml`**: Dockerコンテナを定義するためのファイルです。PythonアプリケーションとPostgreSQLデータベースのコンテナが含まれます。
- **`postgres_data`**ディレクトリ: PostgreSQLデータベースの永続化データが保存されるディレクトリです。
- **`requirements.txt`**: Pythonアプリケーションの依存関係が記述されたファイルです。

## 環境構築

### 0.gitで環境構築

[**Git環境の構築手順**](https://www.notion.so/Git-db0ace056b354b3c9ca91f375a245b7b?pvs=21) を参考に環境構築

### **1. VS CodeのRemote Development拡張機能のインストール**

1. VS Codeを起動します。
2. 左側のメニューバーで、Extensionsアイコン（四角いパズルピースのアイコン）をクリックします。
3. 拡張機能の検索バーに「Remote Development」と入力します。
4. 「Remote Development」の拡張機能が表示されるので、**Install**ボタンをクリックして拡張機能をインストールします。

### 2**. Dockerのインストール**

1. Dockerをインストールしていない場合は、公式のDockerウェブサイト（**https://www.docker.com/get-docker**）から、各オペレーティングシステムに合わせた手順に従ってダウンロードしてインストールします。

### 3. **プロジェクトの準備**

1. プロジェクトのルートディレクトリに移動します。
2. ルートディレクトリに****`.devcontainer/devcontainer.json`***という名前のファイルが存在するか確認してください。
3. ルートディレクトリに****`Dockerfile`***という名前のファイルが存在するか確認してください。
4. ルートディレクトリに****`docker-compose.yml`***という名前のファイルが存在するか確認してください。

### 4**. Dockerコンテナの作成**

1. ターミナル（コマンドプロンプト）を開きます。
2. **`docker build -t trading_project .`**を実行して、Dockerコンテナを作成します。
3. **`docker-compose up -d`**を実行して、コンテナをバックグラウンドで起動します。

### 5. VS Codeでの開発環境の構築

1. **VS Codeを再起動します。**
    - `cmd + shft + p`（Mac）または `ctrl + shft + p`（Windows/Linux）を押します。
    - コマンドパレットが表示されます。
2. **プロジェクトのルートディレクトリをVS Codeで開きます。**
    - コマンドパレットに`remote-containers.openFolder`と入力し、Enterキーを押します。
    - ファイルエクスプローラーが表示されます。
    - プロジェクトのルートディレクトリを選択してEnterキーを押すか、ダブルクリックして開きます。
3. **左下の緑色の「><」アイコンをクリックします。**
    - サイドバーが表示されます。
4. **ポップアップメニューが表示されるので、「Remote-Containers: Reopen in Container」を選択します。**
    - サイドバーの下部に緑色のアイコンがあります。これをクリックします。

以上で、VS Codeを使用してDockerコンテナ内での開発環境が構築されました。
