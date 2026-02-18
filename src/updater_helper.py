import sys, os, time, zipfile, subprocess, psutil

def wait_for_process_to_close(exe_name):
    for _ in range(30):
        found = any(p.name() == exe_name for p in psutil.process_iter())
        if not found:
            return True
        time.sleep(1)
    return False

def apply_update(zip_path, app_dir, app_exe):
    wait_for_process_to_close("PDF_Divider.exe")
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            for member in z.namelist():
                if member.endswith('/'):
                    continue
                parts = member.split('/', 1)
                if len(parts) == 2 and parts[1]:
                    if parts[1].lower() == 'updater_helper.exe':
                        continue
                    target = os.path.join(app_dir, parts[1])
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    try:
                        with z.open(member) as src, open(target, 'wb') as dst:
                            dst.write(src.read())
                    except PermissionError:
                        pass  # ← DLL in uso, si saltano
    except Exception as e:
        sys.exit(1)
    subprocess.Popen([app_exe])
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(1)
    apply_update(sys.argv[1], sys.argv[2], sys.argv[3])
