# Missile Launcher - User Guide

## Overview

The Missile Launcher is a Python-based control system for the USB desktop missile launcher. This software provides a simple and intuitive interface to control the movement and firing of the launcher using Python function calls.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Transfer Codes](#transfer-codes)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Documentation](#documentation)
- [License](#license)

---

## Requirements

Before using the Missile Launcher, ensure you have the following:

- **Python 3.7+**
- **PyUSB library** - For USB device communication
- **USB desktop missile launcher** connected to your computer
- **Linux/macOS/Windows** operating system

### Device Specifications

| Property | Value |
|----------|-------|
| Vendor ID | 0xVVVV |
| Product ID | 0xPPPP |

**⚠️ Important:** Replace `0xVVVV` and `0xPPPP` with your actual device IDs. See the [Finding Your Device IDs](#finding-your-device-ids) section below.

---

## Installation

### 1. Install PyUSB

```bash
pip install pyusb
```

### 2. Install HID

```bash
pip install hid
```

### 3. Set Up the Missile Launcher

Ensure your USB missile launcher is connected to your computer.

#### Finding Your Device IDs

You need to find your launcher's Vendor ID and Product ID:

```bash
lsusb
```

The output will show devices in the format: `Bus XXX Device YYY: ID VVVV:PPPP`

Example output:
```
Bus 001 Device 002: ID 1234:5678 Generic Device Manufacturer
```

In this example:
- Vendor ID = `0x1234`
- Product ID = `0x5678`

Update the `VENDOR_ID` and `PRODUCT_ID` values in `missileFunctions.py` with your actual device IDs.

### 3. Verify Installation

Run a simple test:

```python
import missileFunctions as mf

# This should print the launcher information if connected
# If an error occurs, see Troubleshooting section
```

---

## Quick Start

Here's the simplest way to get started:

```python
import missileFunctions as mf

# Move the launcher up for 0.5 seconds
mf.up(0.5)

# Move the launcher left for 0.5 seconds
mf.left(0.5)

# Fire the launcher
mf.fire()
```

---

## API Reference

### Basic Functions

#### `up(seconds=0.5)`

Move the launcher upward.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `seconds` | float | 0.5 | Duration of the movement in seconds |

**Example:**
```python
mf.up(1.0)  # Move up for 1 second
```

---

#### `down(seconds=0.5)`

Move the launcher downward.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `seconds` | float | 0.5 | Duration of the movement in seconds |

**Example:**
```python
mf.down(0.3)  # Move down for 0.3 seconds
```

---

#### `left(seconds=0.5)`

Move the launcher to the left.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `seconds` | float | 0.5 | Duration of the movement in seconds |

**Example:**
```python
mf.left(0.75)  # Move left for 0.75 seconds
```

---

#### `right(seconds=0.5)`

Move the launcher to the right.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `seconds` | float | 0.5 | Duration of the movement in seconds |

**Example:**
```python
mf.right(0.5)  # Move right for default 0.5 seconds
```

---

#### `fire()`

Fire the launcher. The firing mechanism includes an automatic 4-second delay to allow for launch sequence completion.

**Example:**
```python
mf.fire()  # Fire the launcher (4-second automatic delay)
```

---

#### `stop()`

Immediately stop all launcher movement.

**Example:**
```python
mf.stop()  # Stop the launcher
```

---

## Transfer Codes

The following table lists all available transfer codes used by the launcher's control protocol. These are sent as control packets to the USB device.

| Function | Hex Code | Decimal | Binary | Direction | Description |
|----------|----------|---------|--------|-----------|-------------|
| Down | 0x01 | 1 | 0b00000001 | ↓ | Move launcher downward |
| Up | 0x02 | 2 | 0b00000010 | ↑ | Move launcher upward |
| Left | 0x04 | 4 | 0b00000100 | ← | Move launcher left |
| Right | 0x08 | 8 | 0b00001000 | → | Move launcher right |
| Fire | 0x10 | 16 | 0b00010000 | ◉ | Fire the launcher |
| Stop | 0x20 | 32 | 0b00100000 | ⊗ | Stop all movement |

### Command Packet Structure

All commands are sent as 8-byte control packets:

```
[0x02, CMD, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
```

Where:
- **0x02** - Packet header (fixed)
- **CMD** - Command code (from the transfer codes table above)
- **0x00** - Reserved bytes (padding)

---

## Usage Examples

### Example 1: Simple Sequence

```python
import missileFunctions as mf

# Move up
mf.up(0.5)

# Move right
mf.right(0.5)

# Fire
mf.fire()

# Stop
mf.stop()
```

### Example 2: Target Practice Loop

```python
import missileFunctions as mf

# Fire 5 times with positioning
for i in range(5):
    if i > 0:
        mf.left(0.2)  # Adjust between shots
    
    mf.up(0.3)
    mf.fire()
    print(f"Shot {i + 1} fired!")

mf.stop()
```

### Example 3: Automated Sweep Pattern

```python
import missileFunctions as mf
import time

def sweep_pattern():
    """Perform a left-to-right sweep"""
    
    # Move to starting position (far left)
    mf.left(1.0)
    time.sleep(0.5)
    
    # Sweep right while firing
    for i in range(3):
        mf.fire()
        time.sleep(0.5)
        mf.right(0.3)
    
    mf.stop()

sweep_pattern()
```

### Example 4: With Error Handling

```python
import missileFunctions as mf

try:
    mf.up(0.5)
    mf.right(0.3)
    mf.fire()
except ValueError as e:
    print(f"Error: {e}")
    print("Ensure the missile launcher is connected and recognized.")
finally:
    mf.stop()
```

---

## Troubleshooting

### Issue: "Launcher not found" Error

**Cause:** The USB device is not detected by the system.

**Solutions:**
1. Ensure the launcher is connected via USB
2. Check the device is recognized:
   ```bash
   lsusb
   ```
3. Look for your device in the output and verify the Vendor ID and Product ID match what you've configured
4. Try reconnecting the USB cable
5. On Linux, you may need to run with `sudo` or configure udev rules

### Issue: Permission Denied

**Cause:** User lacks permissions to access USB devices.

**Solutions (Linux):**
```bash
# Option 1: Run with sudo
sudo python3 missile-launcher.py

# Option 2: Add user to dialout group
sudo usermod -a -G dialout $USER
newgrp dialout
```

### Issue: Launcher Doesn't Respond

**Cause:** Kernel driver may have claimed the device.

**Solution:** The code automatically handles this, but if issues persist:
```bash
# Unload the kernel driver
sudo rmmod -f usbhid
```

### Issue: Commands Seem Delayed

**Cause:** Normal behavior due to USB latency or movement duration.

**Note:** The `fire()` function includes a 4-second automatic delay for the launch sequence. Adjust movement durations with the `seconds` parameter for other functions.

---

## Documentation

### PyUSB Documentation

For advanced usage and custom implementations, refer to the official PyUSB documentation:

- **PyUSB Official Documentation:** https://pyusb.github.io/pyusb/
- **PyUSB GitHub Repository:** https://github.com/pyusb/pyusb
- **PyPI Package Page:** https://pypi.org/project/pyusb/
- **Control Transfer Details:** https://pyusb.github.io/pyusb/tutorial.html#control-transfers

### Key PyUSB Concepts

The missile launcher uses the following PyUSB features:

| Concept | Reference |
|---------|-----------|
| Device Finding | https://pyusb.github.io/pyusb/tutorial.html#device-discovery |
| Control Transfers | https://pyusb.github.io/pyusb/tutorial.html#control-transfers |
| USB Devices | https://pyusb.github.io/pyusb/api/usb.core.html#device |
| Utilities | https://pyusb.github.io/pyusb/api/usb.util.html |

---

## File Structure

```
missile_launcher/
├── missile-launcher.py             # Main control script
├── missileFunctions.py             # Function library
├── MISSILE_LAUNCHER_V2_GUIDE.md   # This guide
└── README.md                       # Project overview
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](../../LICENSE) file for details.

### MIT License

The Missile Launcher software is distributed under the MIT License, which allows for:
- ✓ Commercial use
- ✓ Modification
- ✓ Distribution
- ✓ Private use

With the conditions:
- ⚠ License and copyright notice must be included

---

## Contributing

To report issues or suggest improvements, please refer to the project repository.

---

## Support

For additional support:
1. Review the [Troubleshooting](#troubleshooting) section
2. Check the PyUSB documentation
3. Verify device connection with `lsusb`
4. Test with the provided examples

---

**Last Updated:** May 9, 2026  
**Version:** 2.0  
**Status:** Active
