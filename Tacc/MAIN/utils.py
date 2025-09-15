import os
import datetime
import inspect

# Kolory dla konsoli
COLORS = {
    'error': '\033[91m',  # Red
    'debug': '\033[93m',  # Yellow
    'success': '\033[92m',  # Green
    'request': '\033[94m',  # Blue
    'response': '\033[36m',  # cyan
    'reset': '\033[0m'   # Reset to default
}

def log(msg, lvl='debug'):
    # Pobierz nazwę modułu, z którego funkcja została wywołana
    caller_frame = inspect.stack()[1]  # [0] to bieżąca funkcja, [1] to wywołująca
    module_name = inspect.getmodule(caller_frame[0]).__name__

    # Aktualny czas
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")  # Data dla nazwy pliku
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")  # Czas dla loga

    # Wiadomość do konsoli z kolorami
    color = COLORS.get(lvl, COLORS['reset'])
    formatted_msg = f"{'        ' if lvl=='request' else '   '}{color}[{lvl.upper()}]\t{time_str}\t[{module_name}]\t{msg}{COLORS['reset']}"
    print(formatted_msg)

    # Ścieżka do pliku logów
    log_dir = "./logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Tworzy katalog, jeśli nie istnieje

    log_file_path = os.path.join(log_dir, f"{date_str}.txt")
    # Zapis do pliku (bez kolorów)
    with open(log_file_path, "a") as log_file:
        log_file.write(f"[{lvl.upper()}]\t{time_str}\t[{module_name}]\t{msg}\n")

# Przykład użycia
if __name__ == "__main__":
    log("To jest komunikat o błędzie!", "err")
    log("To jest komunikat ostrzegawczy.", "war")
    log("Operacja zakończona sukcesem!", "suc")
    log("To jest informacja.", "inf")
    log("To jest komunikat debugowania.", "deb")





# utils/session_messages.py

from django.utils.timezone import now

class Messages:
    @staticmethod
    def _add_message(request, level, text):
        if "session_messages" not in request.session:
            request.session["session_messages"] = []
        request.session["session_messages"].append({
            "id": str(now().timestamp()),
            "level": level,
            "text": text,
        })
        request.session.modified = True

    @staticmethod
    def success(request, text):
        Messages._add_message(request, "success", text)

    @staticmethod
    def warning(request, text):
        Messages._add_message(request, "warning", text)

    @staticmethod
    def error(request, text):
        Messages._add_message(request, "error", text)

    @staticmethod
    def info(request, text):
        Messages._add_message(request, "info", text)


# alias żebyś mógł używać tak samo jak w Django:
messages = Messages

