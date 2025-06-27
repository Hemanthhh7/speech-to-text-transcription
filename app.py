import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from deep_translator import GoogleTranslator
import tempfile
import subprocess

st.set_page_config(page_title="🎙️ Multilingual Speech Transcriber", layout="centered")
st.title("🗣️ Multilingual Speech-to-Text + Translation")

st.markdown("Upload audio/video in any Indian language → transcribe to **source language** → optionally translate to another.")

recognizer = sr.Recognizer()

language_options = {
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Bengali": "bn",
    "Marathi": "mr",
    "English": "en"
}

# Step 1: Input & Output language selections
input_lang = st.selectbox("🎧 Audio Language (Spoken)", list(language_options.keys()), index=0)
target_lang = st.selectbox("🌍 Translate To", list(language_options.keys()), index=1)

file = st.file_uploader("📁 Upload Audio/Video", type=["wav", "mp3", "flac", "mp4", "mov"])

def extract_audio_from_video(video_path, audio_path="extracted.wav"):
    cmd = f"ffmpeg -i {video_path} -vn -acodec pcm_s16le -ar 44100 -ac 2 {audio_path}"
    subprocess.call(cmd, shell=True)
    return audio_path

def transcribe(path, lang_code):
    try:
        with sr.AudioFile(path) as source:
            audio = recognizer.record(source)
            return recognizer.recognize_google(audio, language=lang_code)
    except sr.UnknownValueError:
        return "❌ Could not understand audio."
    except sr.RequestError:
        return "⚠️ API unavailable or quota exceeded."

if file:
    st.audio(file)
    file_ext = file.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
        tmp.write(file.read())
        audio_path = tmp.name

    # If video, extract audio
    if file_ext in ["mp4", "mov"]:
        audio_path = extract_audio_from_video(audio_path)

    # Convert to wav if needed
    if file_ext in ["mp3", "flac"]:
        sound = AudioSegment.from_file(audio_path)
        audio_path = "converted.wav"
        sound.export(audio_path, format="wav")

    st.write("🕒 Transcribing...")
    lang_code = language_options[input_lang]
    transcript = transcribe(audio_path, lang_code)
    st.success("✅ Transcription Complete")
    st.subheader("📝 Transcript")
    st.write(transcript)

    if input_lang != target_lang:
        st.write("🌐 Translating...")
        translated = GoogleTranslator(source='auto', target=language_options[target_lang]).translate(transcript)
        st.subheader(f"🔁 Translated to {target_lang}")
        st.write(translated)
