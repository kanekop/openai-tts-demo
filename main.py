# main.py

import os
from dotenv import load_dotenv
import openai

# 環境変数を読み込む
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 読み上げるテキスト
text = "Hello, welcome to your first text-to-speech project on Replit!"

# 音声を生成
response = openai.audio.speech.create(
    model="tts-1",       # または "tts-1-hd"
    voice="nova",        # shimmer, echo もOK
    input=text
)

# MP3として保存
with open("output.mp3", "wb") as f:
    f.write(response.content)

print("✅ MP3ファイルが作成されました。")
