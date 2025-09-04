import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os

def main():
    st.title("🎙 Voice Prescription System")
    st.write("Convert voice prescriptions to text and text prescriptions to audio.")

    # -----------------------------
    # Voice to Text
    # -----------------------------
    st.subheader("🎧 Voice to Text")
    audio_file = st.file_uploader("Upload your prescription audio (wav or mp3)", type=["wav", "mp3"])
    if audio_file is not None:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                st.success("✅ Converted Text:")
                st.write(text)
            except sr.UnknownValueError:
                st.error("Could not understand audio")
            except sr.RequestError:
                st.error("Could not request results; check your internet connection")

    # -----------------------------
    # Text to Voice
    # -----------------------------
    st.subheader("🔊 Text to Voice")
    prescription_text = st.text_area("Enter prescription text to convert to audio")
    if st.button("Convert Text to Speech"):
        if prescription_text.strip() != "":
            tts = gTTS(text=prescription_text, lang="en")
            tts_file = "prescription_audio.mp3"
            tts.save(tts_file)
            st.success("✅ Audio generated!")
            st.audio(tts_file, format="audio/mp3")
            # Optional: delete file after playback
            # os.remove(tts_file)
        else:
            st.warning("Please enter some text to convert")

if __name__ == "__main__":
    main()