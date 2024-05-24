# WiFiQR
This is simple app for connecting to WiFi with QR, or manual input. I use Arch btw, and decided to develop this app to suit my system.
# Requirements
### Python `Textual` module
If you want to use it with GUI, otherwise you can skip it the installation.
```bash
pip install -r requirements.txt
```
### Terminal Commands
- `zbarcam` - for QR from Webcam
- `nmcli` - to connect WiFi

Install on Arch:
```bash
yay -S zbar python-textual networkmanager
```
### Usage
```bash
python3 wifiqr_gui.py
python3 wifiqr_cli.py
```
