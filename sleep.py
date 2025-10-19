import os
import time
import ctypes
import random
import subprocess
import urllib.request
from datetime import datetime

LOG_FILE = "C:\\keepalive.log"
PS1_FILE = "C:\\keepalive.ps1"
WALLPAPER_URL = "https://github.com/zenixbot0101/FIX-SHUTDOWN-RDP/raw/main/wallpaper/10860875.png"
WALLPAPER_PATH = "C:\\Users\\Public\\wallpaper.png"

BANNER = r"""
 █████╗ ███████╗██╗  ██╗    ███╗   ███╗ ██████╗ ██████╗ ███████╗
██╔══██╗██╔════╝██║ ██╔╝    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝
███████║███████╗█████╔╝     ██╔████╔██║██║   ██║██║  ██║███████╗
██╔══██║╚════██║██╔═██╗     ██║╚██╔╝██║██║   ██║██║  ██║╚════██║
██║  ██║███████║██║  ██╗    ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
"""

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] {msg}\n")

def set_wallpaper():
    try:
        if not os.path.exists(WALLPAPER_PATH):
            urllib.request.urlretrieve(WALLPAPER_URL, WALLPAPER_PATH)
            log("Tải wallpaper thành công.")
        ctypes.windll.user32.SystemParametersInfoW(20, 0, WALLPAPER_PATH, 3)
        log(f"Đặt wallpaper: {WALLPAPER_PATH}")
    except Exception as e:
        log(f"Lỗi đặt wallpaper: {e}")

def change_password():
    current = input("Nhập mật khẩu hiện tại: ")
    newpass = input("Nhập mật khẩu mới: ")
    try:
        subprocess.run(["net", "user", os.getlogin(), newpass], shell=True, check=True)
        log(f"Đã đổi mật khẩu RDP cho user {os.getlogin()}")
        print("Đổi mật khẩu thành công.\n")
    except Exception as e:
        log(f"Lỗi đổi mật khẩu: {e}")
        print("Lỗi khi đổi mật khẩu:", e)

def create_ps1():
    ps_script = r'''
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class KeepAlive {
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@

while ($true) {
    [KeepAlive]::SetThreadExecutionState(0x80000002) | Out-Null
    Start-Sleep -Seconds 60
}
'''
    with open(PS1_FILE, "w", encoding="utf-8") as f:
        f.write(ps_script)

def keepalive():
    print(BANNER)
    print("AFK MODE đang hoạt động...\n")
    log("AFK MODE STARTED")
    while True:
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
        x, y = random.randint(0, 500), random.randint(0, 500)
        ctypes.windll.user32.SetCursorPos(x, y)
        log("Ping giữ kết nối")
        time.sleep(60)

if __name__ == "__main__":
    print(BANNER)
    print("Chế độ AFK MODE giúp máy không tự shutdown khi thoát RDP.\n")
    set_wallpaper()
    ans = input("Bạn có muốn đổi mật khẩu user RDP không? (y/n): ").lower()
    if ans == "y":
        change_password()
    create_ps1()
    subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-File", PS1_FILE])
    keepalive()
