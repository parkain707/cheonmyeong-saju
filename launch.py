# -*- coding: utf-8 -*-
import os
import sys
import time
import socket
import webbrowser
import subprocess

PORT = 8088
URL = f"http://localhost:{PORT}"
PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_PY = os.path.join(PROJ_DIR, "server.py")
PYTHONW = r"C:\Users\user\AppData\Local\Programs\Python\Python310\pythonw.exe"
LOG_FILE = os.path.join(PROJ_DIR, "server.log")

def is_port_in_use(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(('127.0.0.1', port)) == 0
    except Exception:
        return False

def main():
    if not is_port_in_use(PORT):
        python_exe = PYTHONW if os.path.exists(PYTHONW) else sys.executable
        # 로그 파일 핸들로 안전하게 프로세스 분리
        log_fp = open(LOG_FILE, "a", encoding="utf-8")
        subprocess.Popen(
            [python_exe, SERVER_PY],
            cwd=PROJ_DIR,
            stdout=log_fp,
            stderr=log_fp,
            creationflags=0x00000008 | 0x00000200 | 0x08000000 if os.name == 'nt' else 0
        )
        
        # 포트 준비 대기 (최대 5초)
        for _ in range(25):
            if is_port_in_use(PORT):
                break
            time.sleep(0.2)

    # 기본 웹 브라우저에서 서비스 오픈
    webbrowser.open(URL)

if __name__ == '__main__':
    main()
