---
title: "How-To: Install ndnSIM 2.0 with BRITE on Ubuntu 14.04 (Part 1)"
alias: "how-to-install-ndnsim-20-with-brite-on-ubuntu-1404-part-1"
tags:
  - "Informatics"
  - "Linux"
  - "Simulations"
weight: 0
created_at: "2015-02-04T00:00:00Z"
updated_at: "2015-02-04T00:00:00Z"
---

**UPDATE June 25th:** ndn-cxx MUST be compiled as a shared library now, the tutorial is now reflecting this change by executing `./waf configure --enable-shared --disable-static` for ndn-cxx

**First of all:** follow the tutorial provided here:\
**Second:** If you feel comfortable enough, you can copy and paste the commands from this how-to, which will generate the following directory structure:

`~/ndnSIM\
~/ndnSIM/BRITE\
~/ndnSIM/ndn-cxx\
~/ndnSIM/ns-3`

**Third:** This tutorial comes without warranty. Double check every command before you copy/paste it to your commandline.

Commands for Ubuntu 14.04:\
`\
# install pre-requesits for ndn-cxx, ns-3, etc...\
sudo apt-get install git\
sudo apt-get install python-dev python-pygraphviz python-kiwi\
sudo apt-get install python-pygoocanvas python-gnome2\
sudo apt-get install python-rsvg ipython\
sudo apt-get install build-essential\
sudo apt-get install libsqlite3-dev libcrypto++-dev\
sudo apt-get install libboost-all-dev`

# install mercurial for BRITE\
sudo apt-get install mercurial

mkdir ndnSIM\
cd ndnSIM

# clone git repositories for ndn/ndnSIM\
git clone https://github.com/named-data/ndn-cxx.git ndn-cxx\
git clone https://github.com/cawka/ns-3-dev-ndnSIM.git ns-3\
git clone https://github.com/cawka/pybindgen.git pybindgen\
git clone https://github.com/named-data/ndnSIM.git ns-3/src/ndnSIM

# download and built BRITE\
hg clone http://code.nsnam.org/BRITE\
ls -la\
cd BRITE\
make\
cd ..

# build ndn-cxx\
cd ndn-cxx\
./waf configure --enable-shared --disable-static\
./waf\
# install ndn-cxx\
sudo ./waf install\
cd ..

# build ns-3/ndnSIM with brite\
cd ns-3\
./waf configure -d optimized --with-brite=/home/$USER/ndnSIM/BRITE\
./waf\
sudo ./waf install\

Ideally, this outputs:\
`\
Modules built:\
antenna aodv applications\
bridge brite (no Python) buildings\
config-store core csma\
csma-layout dsdv dsr\
emu energy fd-net-device\
flow-monitor internet lr-wpan\
lte mesh mobility\
mpi ndnSIM netanim (no Python)\
network nix-vector-routing olsr\
point-to-point point-to-point-layout propagation\
sixlowpan spectrum stats\
tap-bridge test (no Python) topology-read\
uan virtual-net-device visualizer\
wave wifi wimax`

Modules not built (see ns-3 tutorial for explanation):\
click openflow\

Done!