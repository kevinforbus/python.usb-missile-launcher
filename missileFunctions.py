# Module for the usb missile launcher commands
import usb.core
import usb.util
import time

def send(cmd):
    packet = [0x02, cmd, 0, 0, 0, 0, 0, 0]

    dev.ctrl_transfer(
        0x21, # bmRequestType
        0x09, # bRequest
        0x0200, # wValue
        0,     # wIndex
        packet # data
    )

def stop():
    send(0x20)

def left(seconds=0.5):
    send(0x04)
    time.sleep(seconds)
    stop()

def right(seconds=0.5):
    send(0x08)
    time.sleep(seconds)
    stop()

def up(seconds=0.5):
    send(0x02)
    time.sleep(seconds)
    stop()

def down(seconds=0.5):
    send(0x01)
    time.sleep(seconds)
    stop()

def fire():
    send(0x10)
    time.sleep(4)
    stop()

def stop():
    send(0x20)


# Begin Program

# Replace with YOUR values from lsusb
VENDOR_ID = 0x2123
PRODUCT_ID = 0x1010

dev = usb.core.find(idVendor=VENDOR_ID,
                    idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError("Launcher not found")

# Linux may auto-claim HID devices
if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

dev.set_configuration()


