# BlackHatPi

BlackHatPi is a portable **Kali Linux hacking workstation** built with a Raspberry Pi Zero, an integrated OLED screen, and a powerbank module.  
It is designed as a **compact, mobile penetration testing device** that can be carried anywhere and instantly deployed for offensive security research.  

---

## Features
- Lightweight portable design with custom 3D-printed case  
- Runs Kali Linux on Raspberry Pi Zero 2 W  
- OLED display for status, IP address, and boot messages  
- Automatic fallback to AP mode if no Wi-Fi is available  
- Battery-powered with charging module for full portability  
- Expandable with custom tools, modules, and payloads  

---

## Hardware Components

Below is the full hardware list used in this project with reference links:

- [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) — Recommended for higher performance  
- [0.96" SSD1306 OLED Display (I²C, 128x64)](https://www.aliexpress.us/item/3256804169233174.html) — For system status and smiley boot screen  
- Any 18650 battery


---

## 3D Printed Models

The project includes custom **3D printable case designs** for Raspberry Pi Zero + OLED + Powerbank integration.

- `case_bottom.stl` — Bottom shell with slots for power module  
- `case_top.stl` — Top shell with OLED window cutout  
- `bridge.stl` — Holder piece for OLED display  

All models are included in the `/3d-models` directory.

---

## Software Setup

1. Flash Kali Linux ARM image onto the microSD card.  
2. Install required Python libraries:  
   ```bash
chmod +x installer.sh
./installer.sh

