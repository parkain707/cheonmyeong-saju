# -*- coding: utf-8 -*-
import os
import subprocess

desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
target_lnk = os.path.join(desktop, '천명 신점사주.lnk')

ps_script = f'''
$sh = New-Object -ComObject WScript.Shell
$lnk = $sh.CreateShortcut('{target_lnk}')
Write-Output "TargetPath: $($lnk.TargetPath)"
Write-Output "Arguments: $($lnk.Arguments)"
Write-Output "WorkingDirectory: $($lnk.WorkingDirectory)"
Write-Output "IconLocation: $($lnk.IconLocation)"
'''

with open('read_lnk.ps1', 'w', encoding='utf-8-sig') as f:
    f.write(ps_script)

res = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', 'read_lnk.ps1'], capture_output=True, text=True)
print(res.stdout)
if os.path.exists('read_lnk.ps1'):
    os.remove('read_lnk.ps1')
