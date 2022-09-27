#!/bin/bash
RULE_FILE="/etc/udev/rules.d/pickit2.rules"
echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="04d8", ATTRS{idProduct}=="0033", GROUP="users", MODE="0666"' > $RULE_FILE
udevadm control --reload