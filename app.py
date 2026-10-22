import streamlit as st
from deep_translator import MyMemoryTranslator
from gtts import gTTS
import io

# Page configuration
st.set_page_config(
    page_title="LinguaBridge AI | CodeAlpha",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern design and typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .hero-container {
        text-align: center;
        padding: 1.5rem 1rem 2rem 1rem;
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.08) 0%, rgba(147, 51, 234, 0.08) 100%);
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(124, 58, 237, 0.15);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4F46E5, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    .hero-subtitle {
        color: #64748B;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    .badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 6px;
        background: #EEF2FF;
        color: #4338CA;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🌐 LinguaBridge AI</div>
    <div class="hero-subtitle">Real-time Cross-Lingual Translation with Neural TTS | CodeAlpha Internship</div>
</div>
""", unsafe_allow_html=True)

# Supported language catalog
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
lang_names = list(LANGUAGES.keys())


@st.cache_data(show_spinner=False, ttl=3600)
def cached_translate(text: str, src: str, tgt: str) -> str:
    """Translates text with an in-memory cache to prevent redundant API calls."""
    translator = MyMemoryTranslator(source=src, target=tgt)
    result = translator.translate(text)
    return str(result) if result else ""


# Session State initialization for language swap
if "source_idx" not in st.session_state:
    st.session_state.source_idx = 0  # English
if "target_idx" not in st.session_state:
    st.session_state.target_idx = 4  # Hindi

# Top bar: Language Selectors and Swap button
sel_col1, sel_mid, sel_col2 = st.columns([5, 1, 5], vertical_alignment="bottom")

with sel_col1:
    source_name = st.selectbox("Source Language", lang_names, index=st.session_state.source_idx, key="src_lang")
with sel_mid:
    if st.button("⇄ Swap", use_container_width=True, help="Swap source and target languages"):
        s_curr = lang_names.index(st.session_state.src_lang)
        t_curr = lang_names.index(st.session_state.tgt_lang)
        st.session_state.source_idx = t_curr
        st.session_state.target_idx = s_curr
        st.rerun()
with sel_col2:
    target_name = st.selectbox("Target Language", lang_names, index=st.session_state.target_idx, key="tgt_lang")

source_code = LANGUAGES[source_name]
target_code = LANGUAGES[target_name]

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# Main Translation Workspace
left_col, right_col = st.columns(2, gap="medium")

with left_col:
    st.markdown(f"**Input Text** <span class='badge'>{source_name}</span>", unsafe_allow_html=True)
    input_text = st.text_area(
        "Enter text",
        label_visibility="collapsed",
        height=220,
        placeholder="Type or paste sentences here to translate..."
    )
    
    char_count = len(input_text)
    word_count = len(input_text.split()) if input_text.strip() else 0
    st.caption(f"📊 Words: {word_count} | Characters: {char_count}")

# Translate execution logic
if "last_translation" not in st.session_state:
    st.session_state.last_translation = ""

action_col1, action_col2 = st.columns([3, 1])
with action_col1:
  translate_clicked = st.button(
      "🚀 Translate Now", type="primary", use_container_width=True
  )
with action_col2:
  clear_clicked = st.button("🧹 Clear", use_container_width=True)

if clear_clicked:
  st.session_state.last_translation = ""
  st.rerun()

if translate_clicked:
    if not input_text.strip():
        st.warning("Please enter text before requesting a translation.")
    elif source_code == target_code:
        st.warning("Please choose two different languages.")
    else:
        try:
            with st.spinner("Translating text..."):
                translated_text = cached_translate(input_text.strip(), source_code, target_code)
                st.session_state.last_translation = translated_text
        except Exception as e:
            st.error(f"Translation service error: {e}")

with right_col:
    st.markdown(f"**Translated Output** <span class='badge'>{target_name}</span>", unsafe_allow_html=True)
    display_val = st.session_state.last_translation
    
    st.text_area(
        "Output text",
        label_visibility="collapsed",
        value=display_val,
        height=220,
        disabled=True,
        placeholder="Your translated output will appear here..."
    )

    if display_val:
        sub_col1, sub_col2 = st.columns(2)
        
        with sub_col1:
            st.markdown("**🔊 Audio Pronunciation:**")
            try:
                base_code = target_code.split("-")[0]
                tts = gTTS(text=display_val, lang=base_code)
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                st.audio(audio_fp, format="audio/mp3")
            except Exception:
                st.caption("Audio unavailable for this dialect.")
        
        with sub_col2:
            st.markdown("**📋 Quick Copy:**")
            st.code(display_val, language="")