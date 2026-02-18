import requests
import os
import sys
import threading
import tkinter.messagebox as mb

CURRENT_VERSION = "1.0.0"
VERSION_URL = "https://raw.githubusercontent.com/GiorgioTuk/PDF-Divider/main/version.json"

def get_remote_version_info():
    try:
        r = requests.get(VERSION_URL, timeout=5)
        return r.json()
    except Exception:
        return None

def check_and_update(master):
    info = get_remote_version_info()
    if not info:
        return
    if info["version"] <= CURRENT_VERSION:
        return
    master.after(0, lambda: _prompt_update(master, info))

def _prompt_update(master, info):
    try:
        risposta = mb.askyesno(
            "Aggiornamento disponibile",
            f"È disponibile la versione {info['version']}.\n"
            f"Vuoi aggiornare ora? L'app si riavvierà automaticamente."
        )
        if risposta:
            master.destroy()
            thread = threading.Thread(target=_download_and_apply, args=(info["url"],), daemon=False)
            thread.start()
    except Exception:
        pass


def _download_and_apply(url):
    import tempfile, subprocess
    try:
        tmp = tempfile.mkdtemp()
        zip_path = os.path.join(tmp, "update.zip")
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        app_dir = os.path.dirname(sys.executable)
        updater_exe = os.path.join(app_dir, "updater_helper.exe")
        if not os.path.exists(updater_exe):
            return
        subprocess.Popen([updater_exe, zip_path, app_dir, sys.executable])
    except Exception as e:
        mb.showerror("Errore aggiornamento", str(e))
    finally:
        os._exit(0)  # ← forza la chiusura del processo dopo aver lanciato updater_helper

