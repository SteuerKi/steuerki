import ollama

print("=== SteuerKi ===")
print("Lokaler Steuerassistent")
print("Zum Beenden: exit")

while True:

    frage = input("\nDu: ")

    if frage.lower() == "exit":
        print("SteuerKi beendet.")
        break

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "system",
                "content": """
                Du bist SteuerKi.

                Du beantwortest allgemeine Steuerfragen.

                Du bist kein Steuerberater.

                Weise darauf hin, dass deine Antworten
                keine Steuerberatung darstellen.
                """
            },
            {
                "role": "user",
                "content": frage
            }
        ]
    )

    print("\nSteuerKi:")
    print(response["message"]["content"])