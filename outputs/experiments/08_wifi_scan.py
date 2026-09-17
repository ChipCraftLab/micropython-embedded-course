"""Lab 08: List nearby Wi-Fi access points without joining one."""
import network
from time import sleep_ms

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

while True:
    print("Scanning...")
    networks = wlan.scan()
    for ssid, bssid, channel, rssi, security, hidden in networks:
        name = ssid.decode() if ssid else "<hidden>"
        print("{:<24} RSSI={:4d} dBm  ch={}  security={}".format(name, rssi, channel, security))
    print("{} network(s) found\n".format(len(networks)))
    sleep_ms(10_000)
