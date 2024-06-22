# programmable_banking_pos

## Description
This is a emulated point of sales device that can be used to perform transactions. It helps to simulate the process of a real POS device. It is programmable and can be used to test different scenarios.

This does not use any real banking system. It is just a simulation and does not perform any real transactions.

## Hardware
The POS device has the following hardware components:
- Microcontroller: Raspberry Pi 4
- Card reader: RC522 RFID reader module
- Cards: 13.56MHZ Mifare 1K RFID cards
- Keypad: 4x4 matrix keypad
- Display: 20x4 LCD display with I2C interface

![POS Device](pos_device.jpg)

## Installation
Setup a virtual environment and install the dependencies.
```bash
python3 -m venv env
source env/bin/activate
```

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 pos.py
```
