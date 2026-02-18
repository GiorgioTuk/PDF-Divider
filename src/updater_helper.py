import sys
import os
import time
import zipfile
import subprocess
import psutil

def wait_for_process_to_close(exe_name):
    """Aspetta che PDF_Divider.exe si chiuda completamente."""
    for _ in range(30):  # aspetta max 30 secondi
        found = any(p.name() == exe_name for p in psutil.process_iter())
        if not found:
            return True
        time.sleep(1)
    return False

def apply_update(zip_path, app_dir, app_exe):
    # Aspetta che l'app principale si chiuda
    wait_for_process_to_close("PDF_Divider.exe")

    # Estrai lo zip sovrascrivendo i file esistenti
    with zipfile.ZipFile(zip_path, 'r') as z:
        for member in z.namelist():
            # Rimuove il primo livello di cartella dallo zip (PDF_Divider/)
            parts = member.split('/', 1)
            if len(parts) == 2 and parts[1]:
                target = os.path.join(app_dir, parts[1])
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with z.open(member) as src, open(target, 'wb') as dst:
                    dst.write(src.read())

    # Riavvia l'applicazione principale
    subprocess.Popen([app_exe])
    sys.exit(0)

if __name__ == "__main__":
    # Argomenti: zip_path, app_dir, app_exe
    if len(sys.argv) != 4:
        sys.exit(1)
    apply_update(sys.argv[1], sys.argv[2], sys.argv[3])
