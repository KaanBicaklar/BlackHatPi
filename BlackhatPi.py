import time
import subprocess
import random
import string
import socket
import fcntl
import struct
from PIL import Image, ImageDraw, ImageFont


try:
    import Adafruit_SSD1306
except Exception as e:
    print("Adafruit_SSD1306 Not Found:", e)
    raise SystemExit(1)


OLED_ADDR = 0x3C  
WIDTH = 128
HEIGHT = 64
ANIM_SECONDS = 10
WLAN_IF = "wlan0"

disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
disp.begin()
disp.clear()
disp.display()


font = ImageFont.load_default()

def clear_display():
    disp.clear()
    disp.display()

def display_image(image):
    disp.image(image)
    disp.display()

def draw_lines(lines):
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    y = 0
    line_h = 12
    for line in lines:
        draw.text((0, y), line, font=font, fill=255)
        y += line_h
        if y >= HEIGHT:
            break
    display_image(image)

def get_wlan_ip(ifname=WLAN_IF):

    try:
        out = subprocess.check_output(["ip", "-4", "addr", "show", "dev", ifname], stderr=subprocess.DEVNULL, text=True)
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("inet "):
               
                parts = line.split()
                if len(parts) >= 2:
                    return parts[1]  
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None
    return None

def random_string(length=8):
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))

def random_password(length=12):
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))

def nmcli_start_hotspot(ssid, password, ifname=WLAN_IF):
    try:
        subprocess.run(
            ["nmcli", "device", "wifi", "hotspot", "ifname", ifname, "ssid", ssid, "password", password],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except FileNotFoundError:
        return None  
    except subprocess.CalledProcessError:
        return False  

def startup_animation(seconds=ANIM_SECONDS):

    start = time.time()
    t = 0
    scroll_text = " BlackhatPI booting... "
    scroll_pos = 0

    while time.time() - start < seconds:
        elapsed = time.time() - start
        frac = elapsed / seconds
        bar_len = int(frac * (WIDTH - 20)) 
        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), "Boot", font=font, fill=255)


        draw.rectangle((0, 12, WIDTH-2, 12+10), outline=255, fill=0)

        draw.rectangle((2, 14, 2 + bar_len, 12+10-2), outline=255, fill=255)


        dots = "." * (int(elapsed*4) % 4)
        draw.text((0, 30), "Waiting" + dots, font=font, fill=255)


        full = scroll_text + "   "
        l = len(full)

        visible = ""
        for i in range(16):
            visible += full[(scroll_pos + i) % l]
        draw.text((0, 46), visible, font=font, fill=255)
        scroll_pos = (scroll_pos + 1) % l

        display_image(image)
        time.sleep(0.12)
        t += 1

def main():
    clear_display()
    startup_animation()

    ip = get_wlan_ip()
    if ip:

        display_lines = [
            "wlan0: " + ip,
            "Log in with ssh"
            
        ]
        draw_lines(display_lines)
        return


    ssid = "BlackhatPI" + random_string(5)
    password = random_password(10)

    nmcli_result = nmcli_start_hotspot(ssid, password)
    if nmcli_result is True:
        ip = get_wlan_ip()

        draw_lines(["AP Active ","wlan0"+ ip, "SSID: " + ssid, "PASS: " + password])
        return
    elif nmcli_result is False:

        draw_lines(["AP Error", "SSID: " + ssid, "PASS: " + password])
        return
    else:
 
        draw_lines(["nmcli Not Found", "AP Info:", "SSID: " + ssid, "PASS: " + password])
        return
if __name__ == "__main__":
    main()
