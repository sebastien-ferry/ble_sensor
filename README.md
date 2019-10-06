Related to: <https://sebastien-ferry.github.io/playing-with-ble/>

# ble_sensor : Bluetooth LE sensor

![Raspberry pi zero W](<https://sebastien-ferry.github.io/assets/ble_raspberry_pi_zero_w_1-5_large.png>){: style="float:right; width:30%"}

## Setup: database + raspberry pi zero W

T4 (PostgreSQL)  --- RPI0W

## Bluepy

  * *NOTE that LE scanning must be run as root.* :warning:
  * and loop around...

References:
  * [Github: IanHarvey/bluepy](<https://github.com/IanHarvey/bluepy> "Github: IanHarvey/bluepy")
  * [Documentation bluepy scanner](<http://ianharvey.github.io/bluepy-doc/scanner.html> "Sample code")

```python
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
    print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
    for (adtype, desc, value) in dev.getScanData():
        print "  %s = %s" % (desc, value)
```
