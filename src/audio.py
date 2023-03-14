import os
import openai
import ffmpeg

text = ""
openai.api_key = os.environ.get('OPEN_AI_KEY')

# 入力ファイルパス
input_file = './audio/sample_all.mp4'

# 分割された音声ファイルの出力先フォルダ
output_dir = './audio/'

# 5分ごとに分割
split_time = 5 * 60

text = ""

# 入力ファイルの情報を取得
probe = ffmpeg.probe(input_file)
video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
duration = float(video_info['duration'])

# 分割された音声ファイルの抽出（５分おき）
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

    # Whisperで音声から文字起こし
    audio_file = open(output_file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    # 文字起こし結果を追加
    text += transcript.text

# 結果を出力
print(text)
