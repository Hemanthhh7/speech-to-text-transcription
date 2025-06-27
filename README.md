# 🎙️ Speech & Video Transcription + Translator App

This Streamlit app allows users to:

✅ Transcribe speech from audio or video files  
✅ Translate transcribed text into Indian languages like **Hindi, Telugu, Tamil, Bengali**, and more  
✅ Works with **WAV, MP3, FLAC, MP4**, and other common formats  

---

## 🚀 Features

- 🔊 **Audio File Support:** Upload `.wav`, `.mp3`, or `.flac`
- 🎥 **Video File Support:** Upload `.mp4`, `.mov`, or `.avi` and extract audio
- 📝 **Speech-to-Text:** Uses Google Web Speech API
- 🌐 **Translation:** Converts output text into 7 Indian languages
- 🎛️ Built with Python and Streamlit
- ☁️ Deployable on Streamlit Cloud
---

## 🧪 Demo

🎥 **Demo Video:**  
[📂 demo.mp4](demo.mp4) *(Attach your screen recording demo here)*

---

## 🛠️ Technologies Used

| Technology         | Purpose                         |
|--------------------|----------------------------------|
| `Streamlit`        | Web app frontend                |
| `SpeechRecognition`| Speech-to-text (Google API)     |
| `pydub`            | Audio format conversion          |
| `moviepy`          | Extract audio from video files   |
| `googletrans`      | Translate text to Indian languages |
| `Python 3.9+`      | Programming language              |

---

## 📂 Project Structure



## 🌐 Live App  
👉 [Try the app here](https://speech-to-text-transcription.streamlit.app/)  

## 🗂 Files
- `app.py` — Streamlit app
- `requirements.txt` — Dependencies
- `demo.mp4` — App demo (to be recorded)

## 🛠 How to Run
### Local
```bash
streamlit run app.py
