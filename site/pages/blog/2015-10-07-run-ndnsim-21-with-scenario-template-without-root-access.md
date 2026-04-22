---
title: "Run ndnSIM 2.1 with scenario template without root access"
alias: "run-ndnsim-21-with-scenario-template-without-root-access"
tags:
  - "Informatics"
  - "Linux"
  - "Simulations"
weight: 0
created_at: "2015-10-07T00:00:00Z"
updated_at: "2015-10-07T00:00:00Z"
---

Due to the new release of ndnSIM ([version 2.1](http://ndnsim.net/2.1/)) my last post about [running ndnSIM without root](http://chkr.at/wordpress/?p=77) has become obsolete. It is also no longer necessary to compile ndn-cxx as a separate library now. However, if you still want to use the (recommended) [ndnSIM scenario template](https://github.com/cawka/ndnSIM-scenario-template) without having root access, here are the steps to follow (for version 2.1):

Step 1: follow the [installation (requirements, etc...) instructions](http://ndnsim.net/2.1/getting-started.html) on the ndnSIM website until you have to type ./waf the first time.

For instance (after having installed all pre-requesits):\
`mkdir ndnSIM\
cd ndnSIM\
git clone https://github.com/named-data-ndnSIM/ns-3-dev.git ns-3\
git clone https://github.com/named-data-ndnSIM/pybindgen.git pybindgen\
git clone --recursive https://github.com/named-data-ndnSIM/ndnSIM.git ns-3/src/ndnSIM\`

Step 1.a: If you require [BRITE](http://www.cs.bu.edu/brite/), do this in addition:\
`\
hg clone http://code.nsnam.org/BRITE\
cd BRITE\
make\
export BRITE_HOME=$(pwd)\
cd ..\`

Step 2: Create a directory where ns-3 and ndnSIM will be "installed" into, e.g.:\
`mkdir ndnSIM-build\`

Step 3: Go to the ns-3 subfolder and compile ns-3 and ndnSIM:\
`cd ns-3\
./waf configure --prefix ../ndnSIM-build -d optimized\
./waf\`\
Note: --prefix ../ndnSIM-build tells the build-script to not install the libraries to the default location, but to ../ndnSIM-build.

Step 3.a: If you followed Step 1.a for BRITE, you will have to add --with-brite=$BRITE\_HOME to the ./waf command:\
`./waf configure --prefix ../ndnSIM-build -d optimized --with-brite=$BRITE_HOME\`

Step 4: Grab a coffee, tea, beer, etc.! This step takes some time...

Step 5: Once this has finished, type\
`./waf install\`\
Note: You did not have to use sudo! ns3 and ndnSIM are now being "installed" to ../ndnSIM-build

Step 6: Set up LD\_LIBRARY\_PATH and PKG\_CONFIG\_PATH for being able to use the scenario template\
`cd ..\
export LD_LIBRARY_PATH=$(pwd)/ndnSIM-build/lib/\
export PKG_CONFIG_PATH=$LD_LIBRARY_PATH/pkgconfig\`

Step 6.a: You might need to add those exports to your ~/.bashrc file.

Step 7: Download and configure scenario template\
`git clone https://github.com/named-data-ndnSIM/scenario-template.git scenario\
cd scenario\
./waf configure\`

Step 8: Create your examples in the scenario template and run them!