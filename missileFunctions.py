# Module for the usb missile launcher commands
import usb.core
import usb.util
import time

class Missile_Commands:
    """
    A class to control USB missile launcher commands.
    
    This class provides methods to control a USB-based missile launcher device,
    allowing directional movement (left, right, up, down) and firing capabilities.
    All movement commands accept an optional duration parameter and automatically
    stop the device after movement completes.
    
    Methods:
        send: Send a raw command packet to the launcher device
        stop: Stop all launcher movement
        left: Rotate launcher left for specified duration
        right: Rotate launcher right for specified duration
        up: Tilt launcher up for specified duration
        down: Tilt launcher down for specified duration
        fire: Fire the launcher
    """
    @classmethod
    def send(cls, cmd):
        """
        Send a raw command packet to the launcher device.
        
        Args:
            cmd (int): The command byte to send to the launcher
            
        Returns:
            None
        """
        packet = [0x02, cmd, 0, 0, 0, 0, 0, 0]

        dev.ctrl_transfer(
            0x21, # bmRequestType
            0x09, # bRequest
            0x0200, # wValue
            0,     # wIndex
            packet # data
        )

    @classmethod
    def left(cls, seconds=0.5):
        """
        Rotate launcher left for the specified duration.
        
        Args:
            seconds (float): Duration in seconds to rotate left (default: 0.5)
            
        Returns:
            None
        """
        cls.send(0x04)
        time.sleep(seconds)
        cls.stop()

    @classmethod
    def right(cls, seconds=0.5):
        """
        Rotate launcher right for the specified duration.
        
        Args:
            seconds (float): Duration in seconds to rotate right (default: 0.5)
            
        Returns:
            None
        """
        cls.send(0x08)
        time.sleep(seconds)
        cls.stop()

    @classmethod
    def up(cls, seconds=0.5):
        """
        Tilt launcher up for the specified duration.
        
        Args:
            seconds (float): Duration in seconds to tilt up (default: 0.5)
            
        Returns:
            None
        """
        cls.send(0x02)
        time.sleep(seconds)
        cls.stop()

    @classmethod
    def down(cls, seconds=0.5):
        """
        Tilt launcher down for the specified duration.
        
        Args:
            seconds (float): Duration in seconds to tilt down (default: 0.5)
            
        Returns:
            None
        """
        cls.send(0x01)
        time.sleep(seconds)
        cls.stop()

    @classmethod
    def fire(cls):
        """
        Fire the launcher.
        
        Sends the fire command and waits for 4 seconds before stopping,
        allowing time for the launcher mechanism to complete.
        
        Args:
            None
            
        Returns:
            None
        """
        cls.send(0x10)
        time.sleep(4)
        cls.stop()

    @classmethod
    def stop(cls):
        """
        Stop all launcher movement immediately.
        
        Args:
            None
            
        Returns:
            None
        """
        cls.send(0x20)


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
