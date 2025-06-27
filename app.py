import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from deep_translator import GoogleTranslator
import tempfile
import subprocess

st.set_page_config(page_title="🗣 Multilingual Speech-to-Text", layout="centered")
st.title("🎙 Multilingual Speech Transcriber & Translator")

st.markdown("""
Upload audio or video in any Indian language. The app will:
- 🔊 Transcribe the speech to text in the spoken language
- 🌐 Optionally translate it to your selected target language
""")

recognizer = sr.Recognizer()

# ✅ Updated language codes (for Google API)
language_options = {
    "Telugu": "te-IN",
    "Hindi": "hi-IN",
    "Tamil": "ta-IN",
    "Kannada": "kn-IN",
    "Bengali": "bn-IN",
    "Marathi": "mr-IN",
    "English": "en-US"
}

# 🎧 Audio Input Language
input_lang = st.selectbox("🗣 Spoken Language", list(language_options.keys()), index=0)
# 🌐 Translate To
target_lang = st.selectbox("🌍 Translate Transcript To", list(language_options.keys()), index=6)

file = st.file_uploader("📁 Upload Audio/Video File", type=["wav", "mp3", "flac", "mp4", "mov"])

# 🛠 Function to extract audio from video using ffmpeg
def extract_audio_from_video(video_path, audio_path="extracted.wav"):
    cmd = f"ffmpeg -i {video_path} -vn -acodec pcm_s16le -ar 44100 -ac 2 {audio_path}"
    subprocess.call(cmd, shell=True)
    return audio_path

# 🧠 Transcription logic
def transcribe(path, lang_code):
    try:
        with sr.AudioFile(path) as source:
            audio = recognizer.record(source)
            return recognizer.recognize_google(audio, language=lang_code)
    except sr.UnknownValueError:
        return "❌ Could not understand the audio."
    except sr.RequestError:
        return "⚠ API unavailable or quota exceeded."

if file:
    st.audio(file)
    file_ext = file.name.split(".")[-1]

    # Save to temporary file
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

    st.info("⏳ Transcribing...")
    lang_code = language_options[input_lang]
    transcript = transcribe(audio_path, lang_code)

    st.success("✅ Transcription Complete!")
    st.subheader("📝 Transcript")
    st.write(transcript)

    if input_lang != target_lang and "❌" not in transcript and "⚠" not in transcript:
        st.info("🌐 Translating...")
        try:
            translated = GoogleTranslator(source='auto', target=language_options[target_lang][:2]).translate(transcript)
            st.subheader(f"🔁 Translated to {target_lang}")
            st.write(translated)
        except:
            st.error("⚠ Translation failed or API error.")
