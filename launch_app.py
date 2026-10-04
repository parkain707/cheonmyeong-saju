# -*- coding: utf-8 -*-
import os
import sys
import time
import socket
import subprocess
import webbrowser

PORT = 8088
PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_PY = os.path.join(PROJ_DIR, "server.py")
PYTHON_EXE = r"C:\Users\user\AppData\Local\Programs\Python\Python310\python.exe"
PYTHONW_EXE = r"C:\Users\user\AppData\Local\Programs\Python\Python310\pythonw.exe"
PROFILE_DIR = os.path.join(PROJ_DIR, ".app_profile")

def is_port_in_use(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(('127.0.0.1', port)) == 0
    except Exception:
        return False

def start_server_if_needed():
    if not is_port_in_use(PORT):
        py = PYTHONW_EXE if os.path.exists(PYTHONW_EXE) else PYTHON_EXE
        subprocess.Popen(
            [py, SERVER_PY],
            cwd=PROJ_DIR,
            creationflags=0x08000000 if os.name == 'nt' else 0, # CREATE_NO_WINDOW
            close_fds=True
        )
        for _ in range(15):
            if is_port_in_use(PORT):
                break
            time.sleep(0.2)

def open_app_window():
    # 매번 항상 최신 버전을 로드하도록 타임스탬프 쿼리 부여
    url_with_ts = f"http://localhost:{PORT}/?v={int(time.time())}"

    # 1. Google Chrome 전용 프로필 독립 앱 모드 (캐시 오염 방지 & 독립 창 보장)
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if os.path.exists(chrome_path):
        subprocess.Popen([
            chrome_path,
            f"--app={url_with_ts}",
            f"--user-data-dir={PROFILE_DIR}",
            "--window-size=1000,920",
            "--disable-cache",
            "--disk-cache-size=1"
        ])
        return

    # 2. Microsoft Edge 독립 앱 모드
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    for ep in edge_paths:
        if os.path.exists(ep):
            subprocess.Popen([
                ep,
                f"--app={url_with_ts}",
                f"--user-data-dir={PROFILE_DIR}",
                "--window-size=1000,920"
            ])
            return

    # 3. 기본 브라우저 Fallback
    webbrowser.open_new(url_with_ts)

def main():
    start_server_if_needed()
    open_app_window()

if __name__ == '__main__':
    main()
