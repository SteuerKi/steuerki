import ollama
from pypdf import PdfReader


def read_pdf(path):
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


chat_history = [
    {
        "role": "system",
        "content": """
        Du bist SteuerKi.

        Du beantwortest allgemeine Steuerfragen.

        Du bist kein Steuerberater.

        Du gibst nur allgemeine Informationen.
        """
    }
]

print("=== SteuerKi ===")
print("Lokaler Steuerassistent")
print("Zum Beenden: exit")

while True:

    frage = input("\nDu: ")

    if frage.lower() == "exit":
        print("SteuerKi beendet.")
        break

    if frage.startswith("pdf "):
        path = frage.replace("pdf ", "").strip()

        try:
            text = read_pdf(path)
            print("\n📄 PDF Inhalt:\n")
            print(text[:2000])
        except Exception as e:
            print("Fehler beim Lesen:", e)

        continue

    chat_history.append({
        "role": "user",
        "content": frage
    })

    response = ollama.chat(
        model="qwen3:8b",
        messages=chat_history
    )

    antwort = response["message"]["content"]

    print("\nSteuerKi:")
    print(antwort)

    chat_history.append({
        "role": "assistant",
        "content": antwort
    })
