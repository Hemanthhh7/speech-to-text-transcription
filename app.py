import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment

st.title("🎙️ Speech-to-Text Transcription App")

st.write("Upload an audio file (WAV, MP3, or FLAC) and get the text transcript!")

# File uploader
audio_file = st.file_uploader("Upload your audio file", type=["wav", "mp3", "flac"])

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")

    # Save the file temporarily
    with open("temp_audio", "wb") as f:
        f.write(audio_file.read())

    # Convert MP3 to WAV if needed
    if audio_file.name.endswith(".mp3"):
        sound = AudioSegment.from_mp3("temp_audio")
        sound.export("converted.wav", format="wav")
        file_path = "converted.wav"
    elif audio_file.name.endswith(".flac"):
        sound = AudioSegment.from_file("temp_audio", format="flac")
        sound.export("converted.wav", format="wav")
        file_path = "converted.wav"
    else:
        file_path = "temp_audio"

    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        st.write("Transcribing...")
        try:
            text = recognizer.recognize_google(audio_data)
            st.success("Transcription Complete!")
            st.write("**Transcript:**")
            st.write(text)
        except sr.UnknownValueError:
            st.error("Sorry, could not understand the audio.")
        except sr.RequestError:
            st.error("API unavailable or quota exceeded.")
