# streamlit_app.py

import streamlit as st
import openai
import os
from pydub import AudioSegment

# ReplitのSecrets機能で登録したAPIキーを使用
openai.api_key = os.getenv("OPENAI_API_KEY")

# 音声モデルの選択肢
voice_options = {
    "女性（US）Nova": "nova",
    "女性（UK）Shimmer": "shimmer",
    "男性（US）Echo": "echo"
}

# 音声スピードを調整する関数（pydub使用）
def change_audio_speed(input_file, output_file, speed=1.0):
    sound = AudioSegment.from_file(input_file)
    sound_with_speed = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    }).set_frame_rate(sound.frame_rate)
    sound_with_speed.export(output_file, format="mp3")

# サイドバー設定
st.sidebar.title("設定")
selected_voice_label = st.sidebar.selectbox("音声を選んでください", list(voice_options.keys()))
selected_voice = voice_options[selected_voice_label]

model = st.sidebar.selectbox("TTSモデルを選んでください", ["tts-1", "tts-1-hd"])

speed = st.sidebar.slider("再生スピード（1.0 = 通常）", 0.5, 2.0, 1.0, 0.1)

st.title("🎤 Text-to-Speech (TTS) ツール")

# サイドバーに追加する場合（おすすめ）
file_name = st.sidebar.text_input("保存するファイル名（拡張子なし）", value="output")
# ファイル名の最終形（.mp3をつける）
final_output_filename = f"{file_name}.mp3"
adjusted_output_filename = f"{file_name}_adjusted.mp3"

# テキスト入力 or ファイルアップロード
uploaded_file = st.file_uploader("📄 テキストファイルをアップロード（.txt）", type="txt")

text_input = ""
if uploaded_file:
    text_input = uploaded_file.read().decode("utf-8")
    st.text_area("🔤 読み上げるテキスト", value=text_input, height=200)
else:
    text_input = st.text_area("🔤 読み上げるテキストを入力", height=200)

if st.button("🎧 音声を生成"):
    if not text_input.strip():
        st.warning("テキストを入力してください。")
    else:
        with st.spinner("音声を生成中..."):
            # OpenAI TTS API 呼び出し
            response = openai.audio.speech.create(
                model=model,  # ✅ ここで動的に選ばれたモデルを使用
                voice=selected_voice,
                input=text_input
            )
            # OpenAIのレスポンスを保存
            with open("output.mp3", "wb") as f:
                f.write(response.content)

            # スピード調整ありなら変更
            if speed != 1.0:
                change_audio_speed(final_output_filename, adjusted_output_filename, speed)
                output_path = adjusted_output_filename
            else:
                output_path = final_output_filename


        st.success("✅ MP3ファイルを作成しました！")

        # 再生
        with open(output_path, "rb") as f:
            audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3")

        # ダウンロードボタン
        with open(output_path, "rb") as f:
            st.download_button("⬇ MP3をダウンロード", f, file_name=output_path)
        