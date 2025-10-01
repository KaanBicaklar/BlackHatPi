#!/usr/bin/env bash

set -euo pipefail

SRC="BlackhatPi.py"
TARGET="/usr/local/bin/BlackhatPi.py"
SERVICE_NAME="blackhatpi.service"
SERVICE_PATH="/etc/systemd/system/${SERVICE_NAME}"

if [[ $EUID -ne 0 ]]; then
  echo "Run as root: sudo $0"
  exit 1
fi

echo "=== BlackHatPi installer started ==="

if [[ ! -f "$SRC" ]]; then
  echo "ERROR: $SRC not found in current directory."
  exit 2
fi

echo "Installing apt packages..."
apt update -y
apt install -y python3-pip python3-pil python3-smbus i2c-tools network-manager

echo "Installing Python packages (system-wide)..."
python3 -m pip install --upgrade pip
python3 -m pip install Adafruit-SSD1306 pillow RPi.GPIO || {
  echo "pip install failed, retrying with --break-system-packages..."
  python3 -m pip install Adafruit-SSD1306 pillow RPi.GPIO --break-system-packages || true
}

echo "Copying $SRC to $TARGET"
cp "$SRC" "$TARGET"
chmod +x "$TARGET"
chown root:root "$TARGET"

echo "Creating systemd service at $SERVICE_PATH"
cat > "$SERVICE_PATH" <<EOF
[Unit]
Description=BlackHatPi OLED boot + wlan/AP handler
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 ${TARGET}
User=root
WorkingDirectory=/usr/local/bin
Environment=PYTHONUNBUFFERED=1
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

echo "Reloading systemd and enabling service..."
systemctl daemon-reload
systemctl enable --now "$SERVICE_NAME"

sleep 1
echo
echo "=== Service status ==="
systemctl status "$SERVICE_NAME" --no-pager

echo
echo "=== Last 40 journal lines for $SERVICE_NAME ==="
journalctl -u "$SERVICE_NAME" -n 40 --no-pager || true

echo
echo "=== i2c devices (if available) ==="
if command -v i2cdetect >/dev/null 2>&1; then
  i2cdetect -y 1 || true
else
  echo "i2cdetect not installed"
fi

echo
echo "Installer finished ✅"
echo "Check logs: sudo journalctl -u $SERVICE_NAME -b -f"
