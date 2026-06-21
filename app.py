import streamlit as st
import ollama
from pypdf import PdfReader
import json
import os

# -------------------------
# MEMORY SYSTEM
# -------------------------
MEMORY_FILE = "memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_memory(chat):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(chat, f, ensure_ascii=False, indent=2)


# -------------------------
# STREAMLIT SETUP
# -------------------------
st.set_page_config(page_title="SteuerKi", layout="centered")

st.title("🧾 SteuerKi Web App")


# -------------------------
# PDF FUNCTION
# -------------------------
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# -------------------------
# CHAT INITIALISIERUNG
# -------------------------
if "chat_history" not in st.session_state:
    loaded = load_memory()

    if loaded:
        st.session_state.chat_history = loaded
    else:
        st.session_state.chat_history = [
            {
                "role": "system",
                "content": "Du bist SteuerKi. Du gibst allgemeine Steuerinfos, keine Beratung."
            }
        ]


# -------------------------
# PDF UPLOAD
# -------------------------
uploaded_file = st.file_uploader("PDF hochladen", type="pdf")

if uploaded_file:
    pdf_text = read_pdf(uploaded_file)

    st.write("📄 Vorschau:")
    st.write(pdf_text[:2000])

    st.session_state.chat_history.append({
        "role": "user",
        "content": f"Analysiere diese PDF steuerlich:\n{pdf_text[:3000]}"
    })

    response = ollama.chat(
        model="qwen3:8b",
        messages=st.session_state.chat_history
    )

    answer = response["message"]["content"]

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })

    save_memory(st.session_state.chat_history)

    st.subheader("🧠 Analyse")
    st.write(answer)


# -------------------------
# CHAT UI
# -------------------------
st.divider()

user_input = st.text_input("Frage stellen")

if st.button("Senden") and user_input:

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    response = ollama.chat(
        model="qwen3:8b",
        messages=st.session_state.chat_history
    )

    answer = response["message"]["content"]

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })

    save_memory(st.session_state.chat_history)

    st.write(answer)