---
title: "How-To: Run your own code/scenario with ndnSIM 2.0 (Ubuntu 14.04)"
alias: "how-to-run-your-own-codescenario-with-ndnsim-20-ubuntu-1404"
tags:
  - "Informatics"
  - "Linux"
  - "Simulations"
weight: 0
created_at: "2015-02-04T00:00:00Z"
updated_at: "2015-02-04T00:00:00Z"
---

Apparently the [tutorial](http://ndnsim.net/2.0/getting-started.html) suggests to download the [ndnSIM scenario template](https://github.com/cawka/ndnSIM-scenario-template), however, this does not look to be compatible with ndnSIM 2.0 (yet).

The mailing list suggests using the ns-3/scratch/ folder (for now), so here is an example of how to use that folder to run your scenario:\
`\
cd ns-3\
cd scratch\
wget https://raw.githubusercontent.com/named-data/ndnSIM/master/examples/ndn-simple.cpp\
mv ndn-simple.cpp my-ndn-code.cc\
cd ..\
./waf --run my-ndn-code --vis\`