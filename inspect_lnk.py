# -*- coding: utf-8 -*-
import os
import subprocess

desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
lnk = os.path.join(desktop, '천명 신점사주.lnk')

vbs = f'''Set Wsh = CreateObject("WScript.Shell")
Set L = Wsh.CreateShortcut("{lnk}")
WScript.Echo "TargetPath: " & L.TargetPath
WScript.Echo "Arguments: " & L.Arguments
WScript.Echo "WorkingDirectory: " & L.WorkingDirectory
WScript.Echo "IconLocation: " & L.IconLocation
'''

with open('inspect_lnk.vbs', 'w', encoding='cp949') as f:
    f.write(vbs)

res = subprocess.run(['cscript', '//nologo', 'inspect_lnk.vbs'], capture_output=True, text=True)
print(res.stdout)
if os.path.exists('inspect_lnk.vbs'):
    os.remove('inspect_lnk.vbs')
