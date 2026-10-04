# -*- coding: utf-8 -*-
import os
import subprocess

desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
proj_dir = os.path.abspath(os.path.dirname(__file__))
ico_path = os.path.join(proj_dir, 'app_icon.ico')
launch_app_py = os.path.join(proj_dir, 'launch_app.py')
pythonw_exe = r"C:\Users\user\AppData\Local\Programs\Python\Python310\pythonw.exe"
shortcut_path = os.path.join(desktop, '천명 신점사주.lnk')

# WScript.Shell을 통한 깨끗한 무소음 바로가기 생성 (검은창 0% 원천 차단)
vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
Set oLink = WshShell.CreateShortcut("{shortcut_path}")
oLink.TargetPath = "{pythonw_exe}"
oLink.Arguments = """{launch_app_py}"""
oLink.WorkingDirectory = "{proj_dir}"
oLink.WindowStyle = 7
oLink.IconLocation = "{ico_path}, 0"
oLink.Description = "天命明鏡 (천명명경) | 현허도인의 천기 신점사주 (세계 영성 융합 & 정통 명리 혜안)"
oLink.Save
'''

vbs_file = os.path.join(proj_dir, 'temp_create_shortcut.vbs')
with open(vbs_file, 'w', encoding='cp949') as f:
    f.write(vbs_content)

res = subprocess.run(['cscript', '//nologo', vbs_file], capture_output=True, text=True)
if os.path.exists(shortcut_path):
    print(f"SUCCESS: Desktop shortcut updated -> {shortcut_path}")
    if os.path.exists(vbs_file):
        os.remove(vbs_file)
else:
    print(f"FAILED: {res.stderr}")
