Project Apiary - A Machine Data analysis tool  
=============================================

To install Apiary on Ubuntu 12.04:
  
  sudo add-apt-repository -y ppa:chris-lea/node.js
  
  sudo ./installEverything.sh
  
This script will install all of the Apiary components and their dependencies using default configuration options. It will take some time, so grab yourself a nice cup of tea while you wait.

If you see a JVM error make sure your Hive/installrc file is configured to look for the java version of your machine (i386, amd64, etc).

See the documentation for individual components for custom installation and initialisation instructions.

* * *

**Components 

* Bee Agents - Software Agents running on the nodes, harvesting data and returning it to the Hive

* Hive - The middleware for the Apiary stack.

* Queen - The Graphic visual dashboard for the Apiary Project
  
* * *

**Links

* Wiki Page - [https://github.com/bradleyjones/apiary/wiki]

* * *

Copyright 2014 "The Minions" 

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
