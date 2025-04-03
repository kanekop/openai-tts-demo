import streamlit as st

st.set_page_config(
    page_title="TTSツール集",
    page_icon="🎛️",
    layout="centered",
)

st.title("🎛️ TTSツール集")

st.markdown("""
### ようこそ！

このアプリでは以下の2つのText-to-Speech（TTS）ツールが利用できます：

- 🗣️ **スピーチTTS**（単独音声変換）
- 💬 **会話TTS**（2人の会話を交互に読み上げ）

⬅️ 左のサイドバーからページを選んでください。
""")
