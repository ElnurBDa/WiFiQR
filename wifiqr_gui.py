import subprocess

from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Label, Footer
from textual.screen import Screen

def scan_qr_code():
    try:
        result = subprocess.run(['zbarcam', '-1', '--raw'], capture_output=True, text=True, check=True)
        qr_data = result.stdout.strip()
        return qr_data
    except subprocess.CalledProcessError as e:
        return "Failed to scan QR :("

def parse_wifi_credentials(wifi_string):
    if "WIFI:" in wifi_string:
        wifi_string = wifi_string[len("WIFI:"):]
        components = wifi_string.split(';')
        wifi_config = {}
        for component in components:
            if component:
                key, value = component.split(':', 1)
                wifi_config[key] = value
        return wifi_config
    else:
        raise "No WiFi credentials in QR"

def connect_to_wifi(ssid, password):
    try:
        result = subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return False #[f"Failed to connect to WiFi network: {e}", e.stdout, e.stderr]

class OptionScreen(Screen):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "input":
            self.app.switch_mode('InputScreen')
        elif event.button.id == "qr":
            self.app.switch_mode('QRScreen')
        elif event.button.id == "quit":
            self.app.quit()

    def compose(self) -> ComposeResult:
        yield Button("Input manually", id="input")
        yield Button("QR", id="qr")
        yield Button("Quit",id="quit")
        yield Footer()


class InputScreen(Screen):
    ssid = ""
    password = ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back_i":
            self.app.switch_mode('OptionScreen')
        if event.button.id == "submit":
            res = connect_to_wifi(self.ssid, self.password)
            if res: SuccessScreen
            else: FailureScreen

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "ssid":
            self.ssid = event.input.value
        elif event.input.id == "password":
            self.password = event.input.value


    def compose(self) -> ComposeResult:
        yield Input(placeholder="SSID", id="ssid")
        yield Input(placeholder="Password", id="password")
        yield Button("Submit", id="submit")
        yield Button("Back", id="back_i", classes="back")
        yield Footer()

class QRScreen(Screen):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "qrscan":
            qr_data = scan_qr_code()
            if qr_data:
                credentials = parse_wifi_credentials(qr_data)
                if credentials:
                    connect_to_wifi(credentials['S'], credentials['P'])
                    self.app.switch_mode('SuccessScreen')
            else: self.app.switch_mode('FailureScreen')
        elif event.button.id == "back_qr":
            self.app.switch_mode('OptionScreen')

    def compose(self) -> ComposeResult:
        yield Button("Start QR Scan", id="qrscan")
        yield Button("Back", id="back_qr", classes="back")
        yield Footer()

class SuccessScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Success!!!", id="success")
        yield Footer()

class FailureScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Failure!!!", id="fail")
        yield Footer()

class WiFiQRApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
        ("3", "switch_mode('InputScreen')", "Input manually"),
        ("2", "switch_mode('QRScreen')", "Scan QR Code"),
        ("1", "switch_mode('OptionScreen')", "Main Page")
    ]

    MODES = {
        "OptionScreen": OptionScreen,  
        "InputScreen": InputScreen,
        "QRScreen": QRScreen,
        "SuccessScreen": SuccessScreen,
        "FailureScreen": FailureScreen
    }

    def on_mount(self) -> None:
        self.switch_mode("OptionScreen")

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def quit(self):
        exit()


if __name__ == "__main__":
    app = WiFiQRApp()
    app.run()