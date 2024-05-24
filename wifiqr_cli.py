import subprocess

def scan_qr_code():
    try:
        print("Scanning QR code...")
        result = subprocess.run(['zbarcam', '-1', '--raw'], capture_output=True, text=True, check=True)
        qr_data = result.stdout.strip()
        print(f"QR Code Data: {qr_data}")
        return qr_data
    except subprocess.CalledProcessError as e:
        print(f"Failed to scan QR code: {e}")
        return None

def parse_wifi_credentials(wifi_string):
    if "WIFI:" in wifi_string:
        wifi_string = wifi_string[len("WIFI:"):]
        components = wifi_string.split(';')
        wifi_config = {}
        for component in components:
            if component:
                key, value = component.split(':', 1)
                wifi_config[key] = value
        print(wifi_config)
        return wifi_config
    else:
        raise ValueError("The provided string does not contain WiFi credentials.")

def connect_to_wifi(ssid, password):
    try:
        print(f"Connecting to WiFi network: {ssid}")
        result = subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password], capture_output=True, text=True, check=True)
        print(result.stdout)
        print("Successfully connected to the WiFi network.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to WiFi network: {e}")
        print(e.stdout)
        print(e.stderr)

def main():
    while True:
        print("Options:")
        print("1. Scan QR code")
        print("2. Input Manually")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            qr_data = scan_qr_code()
            if qr_data:
                credentials = parse_wifi_credentials(qr_data)
                if credentials:
                    connect_to_wifi(credentials['S'], credentials['P'])
        elif choice == "2":
            SSID = input("SSID: ")
            password = input("Password: ")
            connect_to_wifi(SSID, password)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()

