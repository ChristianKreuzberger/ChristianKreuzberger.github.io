---
title: "Running ndnSIM 2.0 without root"
alias: "running-ndnsim-20-without-root"
tags:
  - "Uncategorized"
weight: 0
created_at: "2015-02-26T00:00:00Z"
updated_at: "2015-02-26T00:00:00Z"
---

**Update Oct. 7th:** As of version 2.1, ndn-cxx and NFD are now "integrated" in the ndnSIM git repository, therefore this post is now obsolete.

**Update June 25th**: ndn-cxx must be compiled as a shared library now! Changes are already included in this tutorial, but you must also follow the information provided here: [ndn-cxx and ndnSIM - shared library problem](/blog/compile-link-and-run-ndnsim-with-ndn-cxx-as-a-shared-library).

If you ever wondered what you have to do to get ndnSIM + ndn-cxx run without having root access, then this is the right guide.\
However, I do assume that SOMEONE does have root access and can install standard-libraries for you.\
This is what it looks like on Ubuntu 14.04 (64 bit):

Make your administrator install the following packages (if not already installed)\
`\
sudo apt-get install build-essential libsqlite3-dev libcrypto++-dev libboost-all-dev\
sudo apt-get install pkg-config git\`

And then continue with the following commands yourself (assuming you are in your home directory):\
`\
mkdir ndnSIM\
cd ndnSIM\
git clone https://github.com/named-data/ndn-cxx.git ndn-cxx\
git clone https://github.com/named-data/ndn-cxx.git ndn-cxx\
git clone https://github.com/cawka/ns-3-dev-ndnSIM.git ns-3\
git clone https://github.com/cawka/pybindgen.git pybindgen\
git clone https://github.com/named-data/ndnSIM.git ns-3/src/ndnSIM\
cd ndn-cxx\
./waf configure --prefix /home/$USER/ndnSIM/usr/local/ --enable-shared --disable-static\
./waf\
./waf install`

export LIBRARY\_PATH=/home/$USER/ndnSIM/usr/local/lib/\
export LD\_LIBRARY\_PATH=/home/$USER/ndnSIM/usr/local/lib/\
export PKG\_CONFIG\_PATH=$LD\_LIBRARY\_PATH/pkgconfig\
export CPLUS\_INCLUDE\_PATH=/home/$USER/ndnSIM/usr/local/include/\
cd ..\
cd ns-3/

./waf configure --prefix /home/$USER/ndnSIM/usr/local/ -d optimized --disable-python\
./waf\
./waf install

You may copy the exports into your .bashrc file and adapt them like this:

`\
export LIBRARY_PATH=/home/$USER/ndnSIM/usr/local/lib/:$LIBRARY_PATH\
export LD_LIBRARY_PATH=/home/$USER/ndnSIM/usr/local/lib/:$LD_LIBRARY_PATH\
export PKG_CONFIG_PATH=/home/$USER/ndnSIM/usr/local/lib/pkgconfig\
export CPLUS_INCLUDE_PATH=/home/$USER/ndnSIM/usr/local/include/:$CPLUS_INCLUDE_PATH\`