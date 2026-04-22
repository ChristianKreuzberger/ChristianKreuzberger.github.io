---
title: "Android SDK and AVD Manager in your (Linux) Start Menu"
alias: "android-sdk-and-avd-manager-in-your-linux-start-menu"
tags:
  - "Linux"
weight: 0
created_at: "2016-08-23T00:00:00Z"
updated_at: "2016-08-23T00:00:00Z"
---

The Android SDK and also AVD Manager can be started from the commandline, if you have the Android SDK Tools installed.

For instance, on my system I have android-sdk-tools in ~/android-sdk-tools, therefore I only need to go into that directory (cd ~/android-sdk-tools) and use the following command:\
`\
./Tools/android avd # start android avd manager\
# or\
./Tools/android sdk # start android sdk manager\`

This can be used for creating start menu entries, e.g., for XFCE. Mine look as follows:\
~/.local/share/applications/menulibre-android-avd-manager.desktop\
`[Desktop Entry]\
Version=1.0\
Type=Application\
Name=Android AVD Manager\
Icon=phone-apple-iphone-symbolic\
Exec=./android avd\
Path=/home/ckreuzberger/android-sdk-linux/tools/\
NoDisplay=false\
Categories=Development;Utility;X-XFCE;X-Xfce-Toplevel;\
StartupNotify=false\
Terminal=false`

~/.local/share/applications/menulibre-android-sdk-manager.desktop\
`[Desktop Entry]\
Version=1.0\
Type=Application\
Name=Android SDK Manager\
Icon=phone-apple-iphone-symbolic\
Exec=./android sdk\
Path=/home/ckreuzberger/android-sdk-linux/tools/\
NoDisplay=false\
Categories=Development;Utility;X-XFCE;X-Xfce-Toplevel;\
StartupNotify=false\
Terminal=false`