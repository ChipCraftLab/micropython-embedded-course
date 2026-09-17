"""Lab 15: MicroPython Wi-Fi Socket Web Server for IoT Telemetry and Control.

Runs on Pico W / Pico 2 W. Serves an interactive HTML dashboard over HTTP
allowing remote web browser clients to toggle the on-board LED and view
uptime telemetry.
"""
import network
import socket
from machine import Pin
from time import sleep_ms, ticks_ms

# Replace with your local 2.4 GHz Wi-Fi credentials
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASS = "YOUR_WIFI_PASSWORD"

led = Pin("LED", Pin.OUT)
led.off()

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi '{}'...".format(WIFI_SSID))
        wlan.connect(WIFI_SSID, WIFI_PASS)
        attempts = 0
        while not wlan.isconnected() and attempts < 20:
            led.toggle()
            sleep_ms(500)
            attempts += 1
            print(".", end="")
        print()

    if wlan.isconnected():
        led.on()
        ip = wlan.ifconfig()[0]
        print("Wi-Fi connected! Assigned IP Address:", ip)
        return ip
    else:
        led.off()
        raise RuntimeError("Failed to connect to Wi-Fi. Check SSID/Password.")

def build_web_page(led_state, uptime_sec):
    state_str = "ON" if led_state else "OFF"
    btn_action = "off" if led_state else "on"
    btn_color = "#e74c3c" if led_state else "#2ecc71"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Pico 2 W IoT Dashboard</title>
    <style>
        body {{ font-family: sans-serif; background: #1a1a2e; color: #e6e6e6; text-align: center; padding: 20px; }}
        .card {{ background: #16213e; border-radius: 12px; padding: 25px; max-width: 400px; margin: 0 auto; box-shadow: 0 8px 16px rgba(0,0,0,0.4); }}
        h1 {{ color: #4ecca3; margin-bottom: 5px; }}
        .badge {{ display: inline-block; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 1.1em; background: {btn_color}; color: #fff; }}
        .btn {{ display: inline-block; margin-top: 20px; padding: 12px 30px; font-size: 1.1em; font-weight: bold; color: white; background: {btn_color}; text-decoration: none; border-radius: 8px; transition: 0.2s; }}
        .btn:hover {{ opacity: 0.85; }}
        .stats {{ margin-top: 20px; font-size: 0.9em; color: #8f9ba8; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Pico 2 W Dashboard</h1>
        <p>Embedded MicroPython Web Server</p>
        <hr style="border: 0; border-top: 1px solid #233554; margin: 20px 0;">
        <p>Current LED State: <span class="badge">{state_str}</span></p>
        <p><a href="/?led={btn_action}" class="btn">TURN LED {btn_action.upper()}</a></p>
        <div class="stats">
            <p>System Uptime: {uptime_sec} seconds</p>
            <p><small>Refresh page to update telemetry</small></p>
        </div>
    </div>
</body>
</html>"""
    return html

def run_server():
    ip = connect_wifi()
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(2)
    print("HTTP server listening at http://{}/".format(ip))

    start_time = ticks_ms()
    while True:
        try:
            cl, client_addr = s.accept()
            req = cl.recv(1024).decode('utf-8', 'ignore')
            
            # Parse query parameters
            if "GET /?led=on" in req:
                led.on()
            elif "GET /?led=off" in req:
                led.off()

            uptime = int((ticks_ms() - start_time) / 1000)
            response = build_web_page(led.value(), uptime)

            cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n')
            cl.send(response)
            cl.close()
        except Exception as e:
            print("Client error:", e)

if __name__ == "__main__":
    run_server()
