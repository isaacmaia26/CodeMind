"""Optional text-to-speech helper for CodeMind."""

from __future__ import annotations


def speak(text: str) -> tuple[bool, str]:
    """Speak text aloud if pyttsx3 is installed.

    Returns:
        (success, message)
    """
    try:
        import pyttsx3
    except ImportError:
        return False, "Instala o requirements para ativar voz ou cola isto no teu cmd: pip install pyttsx3"

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.say(text[:1200])
        engine.runAndWait()
        return True, "Voz reproduzida com sucesso."
    except Exception as exc:
        return False, f"Não foi possível reproduzir voz: {exc}"
