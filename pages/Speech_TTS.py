# streamlit_app.py

import streamlit as st
import openai
import os
from pydub import AudioSegment

from datetime import datetime
import pandas as pd


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

# モード選択
mode = st.radio("生成モード", ["単一MP3", "複数MP3（1行ごと）"])

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
        if mode == "単一MP3":
            with st.spinner("音声を生成中..."):
                response = openai.audio.speech.create(
                    model=model,
                    voice=selected_voice,
                    input=text_input
                )
                with open(final_output_filename, "wb") as f:
                    f.write(response.content)

                if speed != 1.0:
                    change_audio_speed(final_output_filename, adjusted_output_filename, speed)
                    output_path = adjusted_output_filename
                else:
                    output_path = final_output_filename
                
                output_files = [output_path]
        else:  # 複数MP3モード
            lines = [line.strip() for line in text_input.split('\n') if line.strip()]
            output_files = []
            
            progress_bar = st.progress(0)
            for i, line in enumerate(lines):
                progress_text = st.empty()
                progress_text.text(f"生成中... ({i+1}/{len(lines)})")
                
                serial = str(i + 1).zfill(3)
                current_filename = f"{file_name}_{serial}.mp3"
                current_adjusted_filename = f"{file_name}_{serial}_adjusted.mp3"
                
                response = openai.audio.speech.create(
                    model=model,
                    voice=selected_voice,
                    input=line
                )
                with open(current_filename, "wb") as f:
                    f.write(response.content)
                
                if speed != 1.0:
                    change_audio_speed(current_filename, current_adjusted_filename, speed)
                    output_files.append(current_adjusted_filename)
                else:
                    output_files.append(current_filename)
                    
                progress_bar.progress((i + 1) / len(lines))
            
            progress_bar.empty()
            progress_text.empty()


        st.success("✅ MP3ファイルを作成しました！")

        # Play each audio file
        for output_path in output_files:
            with open(output_path, "rb") as f:
                st.audio(f.read(), format="audio/mp3")

        # For multiple MP3 mode, create a zip file
        if mode == "複数MP3（1行ごと）" and len(output_files) > 1:
            import zipfile
            import io

            # Create text files and prepare zip file in memory
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                # Add MP3 files
                for output_path in output_files:
                    zip_file.write(output_path, os.path.basename(output_path))
                
                # Create and add text files
                lines = [line.strip() for line in text_input.split('\n') if line.strip()]
                for i, line in enumerate(lines, 1):
                    text_filename = f"script_{str(i).zfill(3)}.txt"
                    # Create text file
                    with open(text_filename, "w", encoding="utf-8") as f:
                        f.write(line)
                    # Add to zip
                    zip_file.write(text_filename, text_filename)
                    # Clean up text file
                    os.remove(text_filename)
            
            # Download button for zip file
            if st.download_button(
                "⬇ すべてのMP3とスクリプトをZIPでダウンロード",
                zip_buffer.getvalue(),
                file_name=f"{file_name}_all_files.zip",
                mime="application/zip"
            ):
                # Cleanup MP3 files after download
                for output_path in output_files:
                    if os.path.exists(output_path):
                        os.remove(output_path)
        else:
            # Single file download for single MP3 mode
            with open(output_files[0], "rb") as f:
                if st.download_button(
                    "⬇ MP3をダウンロード",
                    f,
                    file_name=os.path.basename(output_files[0])
                ):
                    # Cleanup single MP3 file after download
                    if os.path.exists(output_files[0]):
                        os.remove(output_files[0])


        # 使用量ログに記録
        char_count = len(text_input)
        price_per_1000 = 0.015 if model == "tts-1" else 0.030
        cost = round((char_count / 1000) * price_per_1000, 4)
        
        log_data = {
            "datetime": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "filename": [os.path.basename(output_path)],
            "model": [model],
            "chars": [char_count],
            "estimated_cost($)": [cost]
        }
        
        log_df = pd.DataFrame(log_data)
        
        # 既存のログがあれば読み込んで追記
        if os.path.exists("usage_log.csv"):
            old_log = pd.read_csv("usage_log.csv")
            log_df = pd.concat([old_log, log_df], ignore_index=True)
        
        log_df.to_csv("usage_log.csv", index=False)
        
        # ログ表示
        st.subheader("📈 使用量ログ（直近の一覧）")
        st.dataframe(log_df.tail(10))
        