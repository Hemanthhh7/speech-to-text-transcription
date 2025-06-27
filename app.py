import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Whisper Transcript Viewer", layout="centered")
st.title("📜 Whisper Transcription Viewer & Translator")

# Upload the transcript file
uploaded_txt = st.file_uploader("📂 Upload Whisper transcript (.txt)", type=["txt"])

if uploaded_txt:
    # Read transcript
    content = uploaded_txt.read().decode("utf-8")
    
    st.markdown("### 📝 Original Transcribed Text")
    st.write(content)

    # Translation
    st.markdown("---")
    st.markdown("### 🌍 Translate Transcript")
    target_lang = st.selectbox("Select language to translate to", ["en", "hi", "te", "ta", "bn", "ml", "kn", "mr", "gu", "ur"], index=0)

    if st.button("🔁 Translate"):
        try:
            translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text=content)
            st.success("✅ Translation completed!")
            st.markdown("### 📝 Translated Text")
            st.write(translated_text)
        except Exception as e:
            st.error(f"⚠️ Translation failed: {e}")
