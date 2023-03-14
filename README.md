# Whisperを活用して動画の内容を簡単に文字起こしに変換する方法

OpenAIのWhisperは、自動音声認識（ASR）技術に基づくシステムです。Whisperは、大量の音声データと対応するテキストデータを用いて訓練されており、音声をテキストに変換する機能を提供しています。この技術は、様々な言語やアクセントに対応し、動画やオーディオの字幕生成、通話の文字起こし、音声アシスタントなど、多くの用途に活用されています。今回はOpenAIのWhisper APIを使用して動画から文字起こしをする方法を説明します。以下はより詳細な手順の説明です。

# 事前準備

まず、MacOSにffmpegをインストールします。Terminal.appを開き、以下のコマンドを実行します。

```shell
brew install ffmpeg
```

次に、Pythonパッケージであるopenaiとffmpeg-pythonをインストールします。同じターミナルウィンドウで、以下のコマンドを実行します。

```shell
pip install openai
pip install ffmpeg-python
```

これで、必要なパッケージがすべてインストールされました。

# プログラミング

次に、Pythonスクリプトで音声から文字起こしを行います。上記のブログ記事のサンプルスクリプトを参考に、以下の手順を実行します。
※一度に文字起こしできるサイズに制限があるので音声を5分毎に分割して変換します。

### 1.必要なモジュールをインポートします。

```python
import os
import openai
import ffmpeg
```

### 2.OpenAIのAPIキーを環境変数から取得します。APIキーは、OpenAIのウェブサイトで取得できます。

```python
# OpenAIのAPIキーを環境変数より取得
openai.api_key = os.environ.get('OPEN_AI_KEY')
```

### 3.入力動画ファイルのパスを設定します。

```python
input_file = './audio/sample_all.mp4'
```

### 4.分割された音声ファイルを保存するフォルダを設定します。

```python
output_dir = './audio/'
```

### 5.音声ファイルを5分間隔で分割します。

```python
split_time = 5 * 60
```

### 6.分割された音声ファイルから文字起こしを行います。

```python
# 入力ファイルの情報を取得
probe = ffmpeg.probe(input_file)
video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
duration = float(video_info['duration'])

# 分割された音声ファイルの抽出
for t in range(0, int(duration), split_time):
    # 分割された音声ファイルのファイル名
    output_file = f'{output_dir}/audio_{t}.mp3'

    # 分割された部分の動画ファイルを作成
    stream = ffmpeg.input(input_file, ss=t, t=split_time)

    # 音声ストリームの抽出とエンコード
    audio = stream.audio
    audio = ffmpeg.output(audio, output_file, acodec='libmp3lame')

    # FFmpegを実行する
    ffmpeg.run(audio)

    # OpenAIのWhisperを使って音声から文字起こしする
    audio_file = open(output_file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    # 文字起こし結果をためる
    text += transcript.text
```

### 7.最後に、変換されたテキストを出力します。

```python
print(text)
```

出力されたテキストを見ると、以下の様に日本語でそれなりの精度では出力されましたが、ご認識もあるため人手でチェックや修正する必要はありそうでした。
また、音声の間は空白となり点（てん）や丸（まる）までは自動で付かないので、校正する必要もありました。

【修正前】
```text
皆さんこんばんはそれでは指示帝国になりましたので始めたいと思います はい本日は第28回ピンテック養成勉強会 金融に生かすデータの開拓と利活用の技術編ということで勉強会を始めたいと思います 本日は優れたテクノロジーを駆使して金融業界に新たな可能性を創出する 素晴らしい講演者の方々をにお招きしております 皆様の専門分野において....
```

【手作業での修正】
```text
皆さんこんばんはそれでは定刻になりましたので始めたいと思います。
はい本日は第28回フィンテック養成勉強会 金融に生かすデータの開拓と利活用の技術編ということで勉強会を始めたいと思います。
本日は優れたテクノロジーを駆使して金融業界に新たな可能性を創出する 素晴らしい講演者の方々をにお招きしております。
皆様の専門分野において....
