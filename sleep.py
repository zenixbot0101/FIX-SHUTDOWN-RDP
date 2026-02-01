import os
import time
import subprocess
import textwrap
import ctypes
import urllib.request

def set_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
def get_sys_lang():
    lang = int(input("1.English/2.Vietnamese: "))
    if lang == 1:
        engver()
    elif lang == 2:
        vietver()
    else:
        print("Selection is invalid select 1 for english or select 2 for vietnamese")
    choice = input("Bạn có muốn đổi mật khẩu user RDP không? (y/n): ").strip().lower()
def vietver():    
    if choice == "y":
        user = os.getlogin()
        old_pass = input("Nhập mật khẩu hiện tại: ")
        new_pass = input("Nhập mật khẩu mới: ")
        cmd = f'net user "{user}" "{new_pass}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("[+] Đổi mật khẩu thành công.")
        else:
            print("[-] Đổi mật khẩu thất bại. Có thể sai quyền hoặc sai mật khẩu cũ.")
        time.sleep(2)
    
    print("[*] Đang tải wallpaper...")
    url = "https://github.com/zenixbot0101/FIX-SHUTDOWN-RDP/raw/main/wallpaper/10860875.png"
    wallpaper_path = r"C:\wallpaper.png"
    try:
        urllib.request.urlretrieve(url, wallpaper_path)
        set_wallpaper(wallpaper_path)
        print(f"[+] Wallpaper đã được đổi: {wallpaper_path}")
    except Exception as e:
        print(f"[-] Lỗi tải wallpaper: {e}")
    time.sleep(1)
    
    ps1_code = textwrap.dedent(r'''
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class KeepAlive {
        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern uint SetThreadExecutionState(uint esFlags);
    }
    "@
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "AFK MODE"
    $form.Size = New-Object System.Drawing.Size(300,150)
    $form.StartPosition = "CenterScreen"
    $form.TopMost = $true
    $form.FormBorderStyle = "FixedDialog"
    $form.MaximizeBox = $false
    $form.MinimizeBox = $false
    $form.BackColor = [System.Drawing.Color]::FromArgb(25,25,25)
    $label = New-Object System.Windows.Forms.Label
    $label.Text = "AFK MODE"
    $label.ForeColor = [System.Drawing.Color]::LimeGreen
    $label.Font = New-Object System.Drawing.Font("Segoe UI",24,[System.Drawing.FontStyle]::Bold)
    $label.AutoSize = $true
    $label.Dock = "Fill"
    $label.TextAlign = "MiddleCenter"
    $form.Controls.Add($label)
    $job = Start-Job {
        Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class KeepAlive {
        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern uint SetThreadExecutionState(uint esFlags);
    }
    "@
        while ($true) {
            [KeepAlive]::SetThreadExecutionState([uint32]0x80000002) | Out-Null
            Start-Sleep -Seconds 60
        }
    }
    $form.Add_FormClosing({
        Stop-Job $job -ErrorAction SilentlyContinue
        Remove-Job $job -ErrorAction SilentlyContinue
        [KeepAlive]::SetThreadExecutionState([uint32]0x80000000) | Out-Null
    })
    [System.Windows.Forms.Application]::Run($form)
    ''')
    
    ps1_path = r"C:\keepalive.ps1"
    with open(ps1_path, "w", encoding="utf-8") as f:
        f.write(ps1_code)
    print(f"[+] Đã tạo {ps1_path}")
    
    subprocess.Popen(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps1_path],
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    
    start_time = time.time()
    while True:
        elapsed = int(time.time() - start_time)
        h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
        os.system("cls" if os.name == "nt" else "clear")
        print("==== AFK MODE ĐANG HOẠT ĐỘNG ====")
        print(f"Thời gian hoạt động: {h:02d}:{m:02d}:{s:02d}")
        print("(Đóng cửa sổ này để dừng)")
        time.sleep(1)
def engver():
    choice = input("Do you want to change the RDP user's password? (y/n): ").strip().lower()
if choice == "y":
    user = os.getlogin()
    old_pass = input("Enter current password: ")
    new_pass = input("Enter new password: ")
    cmd = f'net user "{user}" "{new_pass}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("[+] Password changed successfully.")
    else:
        print("[-] Failed to change password. You may lack permission or the old password may be incorrect.")
    time.sleep(2)

print("[*] Downloading wallpaper...")
url = "https://github.com/zenixbot0101/FIX-SHUTDOWN-RDP/raw/main/wallpaper/10860875.png"
wallpaper_path = r"C:\wallpaper.png"
try:
    urllib.request.urlretrieve(url, wallpaper_path)
    set_wallpaper(wallpaper_path)
    print(f"[+] Wallpaper changed: {wallpaper_path}")
except Exception as e:
    print(f"[-] Failed to download wallpaper: {e}")
time.sleep(1)

ps1_code = textwrap.dedent(r'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class KeepAlive {
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@
$form = New-Object System.Windows.Forms.Form
$form.Text = "AFK MODE"
$form.Size = New-Object System.Drawing.Size(300,150)
$form.StartPosition = "CenterScreen"
$form.TopMost = $true
$form.FormBorderStyle = "FixedDialog"
$form.MaximizeBox = $false
$form.MinimizeBox = $false
$form.BackColor = [System.Drawing.Color]::FromArgb(25,25,25)
$label = New-Object System.Windows.Forms.Label
$label.Text = "AFK MODE"
$label.ForeColor = [System.Drawing.Color]::LimeGreen
$label.Font = New-Object System.Drawing.Font("Segoe UI",24,[System.Drawing.FontStyle]::Bold)
$label.AutoSize = $true
$label.Dock = "Fill"
$label.TextAlign = "MiddleCenter"
$form.Controls.Add($label)
$job = Start-Job {
    Add-Type @"
using System;
using System.Runtime.InteropServices;
public class KeepAlive {
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@
    while ($true) {
        [KeepAlive]::SetThreadExecutionState([uint32]0x80000002) | Out-Null
        Start-Sleep -Seconds 60
    }
}
$form.Add_FormClosing({
    Stop-Job $job -ErrorAction SilentlyContinue
    Remove-Job $job -ErrorAction SilentlyContinue
    [KeepAlive]::SetThreadExecutionState([uint32]0x80000000) | Out-Null
})
[System.Windows.Forms.Application]::Run($form)
''')

ps1_path = r"C:\keepalive.ps1"
with open(ps1_path, "w", encoding="utf-8") as f:
    f.write(ps1_code)
print(f"[+] Created {ps1_path}")

subprocess.Popen(
    ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps1_path],
    creationflags=subprocess.CREATE_NO_WINDOW
)

start_time = time.time()
while True:
    elapsed = int(time.time() - start_time)
    h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
    os.system("cls" if os.name == "nt" else "clear")
    print("==== AFK MODE IS ACTIVE ====")
    print(f"Uptime: {h:02d}:{m:02d}:{s:02d}")
    print("(Close this window to stop)")
    time.sleep(1)
get_sys_lang()
