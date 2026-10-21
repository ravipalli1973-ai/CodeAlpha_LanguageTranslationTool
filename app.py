import streamlit as st
from deep_translator import MyMemoryTranslator
from gtts import gTTS
import io

# Page setup
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 AI Language Translation Tool")
st.caption("CodeAlpha AI Internship - Task 1")

# Supported language codes for MyMemory
LANGUAGES = {
    "English": "en-US",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Hindi": "hi-IN",
    "Telugu": "te-IN",
    "Tamil": "ta-IN",
    "Kannada": "kn-IN",
    "Bengali": "bn-IN",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja-JP",
    "Arabic": "ar-SA",
    "Russian": "ru-RU",
    "Portuguese": "pt-PT",
    "Italian": "it-IT"
}

# UI Dropdowns for source and target language
col1, col2 = st.columns(2)
with col1:
    source_name = st.selectbox("Source Language", list(LANGUAGES.keys()), index=0)
with col2:
    target_name = st.selectbox("Target Language", list(LANGUAGES.keys()), index=1)

source_code = LANGUAGES[source_name]
target_code = LANGUAGES[target_name]

# Input area
input_text = st.text_area("Enter text to translate:", height=140, placeholder="Type your text here...")

# Translation execution
if st.button("🚀 Translate", type="primary", use_container_width=True):
    if not input_text.strip():
        st.warning("Please enter text first.")
    elif source_code == target_code:
        st.warning("Source and Target languages must be different.")
    else:
        try:
            with st.spinner("Translating..."):
                translator = MyMemoryTranslator(source=source_code, target=target_code)
                translated_text = translator.translate(input_text)

            st.success("Translated Successfully!")

            # Display translated text
            st.subheader("Translated Output:")
            st.text_area(label="Result", value=translated_text, height=140, disabled=True)

            # Features: Audio & Copy
            col_audio, col_copy = st.columns([1, 1])

            with col_audio:
                st.markdown("**🔊 Pronunciation (Audio):**")
                try:
                    # gTTS expects base code like 'en', 'fr', 'hi'
                    base_lang = target_code.split("-")[0]
                    tts = gTTS(text=translated_text, lang=base_lang)
                    audio_buffer = io.BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    st.audio(audio_buffer, format="audio/mp3")
                except Exception:
                    st.info("Audio playback not supported for this language.")

            with col_copy:
                st.markdown("**📋 Copy Text:**")
                st.code(translated_text, language="")

        except Exception as e:
            st.error(f"Error during translation: {e}")