---
title: "Ubuntu + USB Headset"
alias: "ubuntu-usb-headset"
tags:
  - "Uncategorized"
weight: 0
created_at: "2016-06-07T00:00:00Z"
updated_at: "2016-06-07T00:00:00Z"
---

While USB Headsets are already supported by Ubuntu (15.10 in my example), there are some stumbling block. One of them was that the USB Headset is not recognized after (re)booting, only after plugging it out and back in.

To overcome this issue, the USB device needs to be entered in /etc/modprobe.d/snd-usb-audio (you might have to create this file first).

Step 1: Boot without the headset plugged in\
Step 2: Run lsusb tool in commandline, copy the output to a text editor\
Step 3: Plug in your USB headset\
Step 4: Use lsusb tool in commandline to find out what USB devices you have, in my example:

`Bus 002 Device 003: ID 0451:8046 Texas Instruments, Inc.\
Bus 002 Device 002: ID 0451:8046 Texas Instruments, Inc.\
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub\
Bus 001 Device 006: ID 413c:301a Dell Computer Corp.\
Bus 001 Device 005: ID 2034:0102\
Bus 001 Device 004: ID 413c:2113 Dell Computer Corp.\
Bus 001 Device 003: ID 0451:8044 Texas Instruments, Inc.\
Bus 001 Device 002: ID 0451:8044 Texas Instruments, Inc.\
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub`

Step 5: Cross match the lsusb output from step 2 to find out which device your headset is, in my example it was\
`Bus 001 Device 005: ID 2034:0102`

Step 6: Create the following entry in /etc/modprobe.d/snd-usb-audio (you might have to create this file first):\
`options snd-usb-audio index=2 vid=0x2034 pid=0x0102\`

Make sure to replace 0x2034 with the first ID of the lsusb output of your usb device, and 0x0102 with the second one.

Step 7: Reboot, enjoy!