import streamlit as st
import tempfile
import whisper
from deep_translator import GoogleTranslator
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import os

st.set_page_config(page_title="🎙️ Whisper Speech Transcriber", layout="centered")
st.title("🗣️ Multilingual Speech Transcription & Translation")

st.markdown("""
Upload audio or video in **any language**, and get transcribed text in your **preferred language**!

---
""")

# Whisper Model (load once)
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# Language selection
output_lang = st.selectbox("🌍 Translate to Language:", ["Telugu", "English", "Hindi", "Kannada", "Tamil", "Bengali", "Urdu"])

# File uploader
uploaded_file = st.file_uploader("Upload Audio or Video", type=["wav", "mp3", "m4a", "mp4", "mov"])

if uploaded_file:
    st.audio(uploaded_file, format="audio/wav")
    
    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name[-4:]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Convert video to audio if needed
    if tmp_path.endswith(('.mp4', '.mov')):
        st.write("Extracting audio from video...")
        videoclip = VideoFileClip(tmp_path)
        audio_path = tmp_path + ".wav"
        videoclip.audio.write_audiofile(audio_path, codec='pcm_s16le')
    else:
        # Convert all to .wav for Whisper
        audio = AudioSegment.from_file(tmp_path)
        audio_path = tmp_path + ".wav"
        audio.export(audio_path, format="wav")

    # Transcribe
    st.info("Transcribing... This may take a few seconds.")
    result = model.transcribe(audio_path, language=None)
    transcript = result["text"]
    
    # Translate
    try:
        translated = GoogleTranslator(source='auto', target=output_lang.lower()).translate(transcript)
        st.success("✅ Transcription & Translation Complete!")
        st.markdown("### 📝 Transcript (Original)")
        st.write(transcript)
        st.markdown(f"### 🌐 Translated to {output_lang}")
        st.write(translated)
    except Exception as e:
        st.error("⚠️ Translation failed: " + str(e))

    # Cleanup
    os.remove(tmp_path)
    if os.path.exists(audio_path):
        os.remove(audio_path)

st.caption("Made with 💬 Whisper, Streamlit & Deep Translator")
