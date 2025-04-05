import streamlit as st
import openai
import os
from pydub import AudioSegment
from datetime import datetime
import tempfile

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 音声モデルの選択肢
voice_options = {
    "女性（US）Nova": "nova",
    "女性（UK）Shimmer": "shimmer",
    "男性（US）Echo": "echo"
}

st.title("🗣️ 会話スクリプト TTS ツール")

# 話者AとBの声を選択
voice_a_label = st.selectbox("話者 A の声", list(voice_options.keys()), index=0)
voice_b_label = st.selectbox("話者 B の声", list(voice_options.keys()), index=2)
voice_a = voice_options[voice_a_label]
voice_b = voice_options[voice_b_label]

speed = st.slider("再生スピード (1.0 = 通常)", 0.5, 2.0, 1.0, 0.1)

conversation_text = st.text_area(
    "📄 A: Hello!\\nB: Hi there!\\nA: How are you? のような形式で話を入力", 
    height=300
)

file_name = st.text_input("保存するファイル名 (拡張子は付けない)", value="conversation")

if st.button("⬆️ MP3を作成"):
    if not conversation_text.strip():
        st.warning("スクリプトを入力してください")
    else:
        lines = conversation_text.strip().splitlines()
        audio_segments = []

        with tempfile.TemporaryDirectory() as tmpdir:
            for i, line in enumerate(lines):
                if line.startswith("A:"):
                    voice = voice_a
                    text = line[2:].strip()
                elif line.startswith("B:"):
                    voice = voice_b
                    text = line[2:].strip()
                else:
                    st.warning(f"{i+1} 行目が A: または B: で始まっていません")
                    continue

                response = openai.audio.speech.create(
                    model="tts-1",
                    voice=voice,
                    input=text
                )
                temp_path = os.path.join(tmpdir, f"line_{i}.mp3")
                with open(temp_path, "wb") as f:
                    f.write(response.content)
                audio_segments.append(AudioSegment.from_file(temp_path))

            # 組み合わせ
            if audio_segments:
                final_audio = audio_segments[0]
                for segment in audio_segments[1:]:
                    final_audio += segment

                # スピード調整
                final_audio = final_audio._spawn(final_audio.raw_data, overrides={
                    "frame_rate": int(final_audio.frame_rate * speed)
                }).set_frame_rate(final_audio.frame_rate)

                output_file = f"{file_name}.mp3"
                final_audio.export(output_file, format="mp3")

                st.success("会話MP3を作成しました！")
                if os.path.exists(output_file):
                    with open(output_file, "rb") as f:
                        audio_data = f.read()
                    st.audio(audio_data, format="audio/mp3")
                    if st.download_button("⬇️ MP3ダウンロード", audio_data, file_name=output_file):
                        # Cleanup MP3 file after download
                        if os.path.exists(output_file):
                            os.remove(output_file)
