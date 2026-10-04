# -*- coding: utf-8 -*-
import os
import subprocess

vbs_script = r"""
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "C:\Users\user\Desktop\[천명명경] 신점사주 바로실행.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "C:\Users\user\.gemini\antigravity\scratch\guija_saju\run_onestop.bat"
oLink.WorkingDirectory = "C:\Users\user\.gemini\antigravity\scratch\guija_saju"
oLink.WindowStyle = 1
oLink.Description = "천명명경 현허도인 천기 신점사주 원클릭 실행"
oLink.IconLocation = "shell32.dll,221"
oLink.Save
"""

vbs_path = os.path.join(os.path.dirname(__file__), "make_shortcut.vbs")
with open(vbs_path, "w", encoding="cp949") as f:
    f.write(vbs_script)

subprocess.run(["cscript", "//nologo", vbs_path], check=True)
if os.path.exists(vbs_path):
    os.remove(vbs_path)

print("✅ 바탕화면 바로가기(.lnk) 생성 완료!")
