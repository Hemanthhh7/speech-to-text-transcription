import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from deep_translator import GoogleTranslator
import tempfile
import subprocess
import os

st.set_page_config(page_title="🎙️ Speech & Video Transcription", layout="centered")
st.title("🎙️ Speech & Video Transcription + Translation")

st.markdown("Upload **audio** or **video**, or record voice. Transcribe and translate to Indian languages!")

option = st.radio("Choose input type:", ["🎤 Record Audio", "📁 Upload Audio File", "📹 Upload Video File"])

recognizer = sr.Recognizer()

language_options = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Bengali": "bn",
    "Marathi": "mr"
}
target_lang = st.selectbox("🌐 Translate to:", list(language_options.keys()))

def transcribe_audio(path):
    with sr.AudioFile(path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "❌ Could not understand the audio."
        except sr.RequestError:
            return "⚠️ API unavailable or limit exceeded."

def translate_text(text, lang_code):
    try:
        translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
        return translated
    except Exception:
        return "⚠️ Translation failed."

if option == "🎤 Record Audio":
    st.info("You can record audio using your device and upload it below.")
    recorded = st.file_uploader("Upload your recorded audio (WAV preferred)", type=["wav"])
    if recorded:
        st.audio(recorded)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(recorded.read())
            text = transcribe_audio(tmp.name)
            st.subheader("📝 Transcription")
            st.write(text)

            translated = translate_text(text, language_options[target_lang])
            st.subheader(f"🌐 Translation ({target_lang})")
            st.write(translated)

elif option == "📁 Upload Audio File":
    audio = st.file_uploader("Upload Audio", type=["mp3", "wav", "flac"])
    if audio:
        st.audio(audio)
        with tempfile.NamedTemporaryFile(delete=False, suffix=audio.name[-4:]) as tmp:
            tmp.write(audio.read())
            if audio.name.endswith(".mp3") or audio.name.endswith(".flac"):
                sound = AudioSegment.from_file(tmp.name)
                sound.export("converted.wav", format="wav")
                text = transcribe_audio("converted.wav")
            else:
                text = transcribe_audio(tmp.name)

            st.subheader("📝 Transcription")
            st.write(text)

            translated = translate_text(text, language_options[target_lang])
            st.subheader(f"🌐 Translation ({target_lang})")
            st.write(translated)

elif option == "📹 Upload Video File":
    video = st.file_uploader("Upload Video (MP4 recommended)", type=["mp4", "mov", "avi"])
    if video:
        st.video(video)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(video.read())
            audio_path = "video_audio.wav"

            # Extract audio from video using ffmpeg
            cmd = f"ffmpeg -i {tmp.name} -vn -acodec pcm_s16le -ar 44100 -ac 2 {audio_path}"
            subprocess.call(cmd, shell=True)

            text = transcribe_audio(audio_path)
            st.subheader("📝 Transcription")
            st.write(text)

            translated = translate_text(text, language_options[target_lang])
            st.subheader(f"🌐 Translation ({target_lang})")
            st.write(translated)
