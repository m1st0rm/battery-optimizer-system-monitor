# Battery Optimizer & System Monitor

## Description

This repo contains a Windows application that can be used to optimize power consumption (relevant for portable devices). Optimization is done by changing the [power policy settings](https://learn.microsoft.com/en-us/windows/win32/power/power-policy-settings) depending on the current battery performance. In addition, the application provides the ability to monitor the utilization of system and hardware resources (information about the load of cores (threads) in the central processor, the number of physical cores, the number of virtual cores, the total load on the processor, the maximum and minimum processor frequencies, the total amount of RAM in the device, the occupied RAM, the read and write load on the data storage, the GPU load, the total GPU RAM, the occupied GPU RAM, battery reserve in terms of percentage and time, and the current battery status of the device).  
If you want to understand the algorithm of the application and the device of its functionality, you can read [this document](battery_optimizer_system_monitor_guide_RUS.pdf) (in Russian only).  
**App Language:** Russian  
**Programming Language:** Python 3.12  
**Framework:** Tkinter  
**Author:** Mikhail Bahamolau  

 ## Requirements

 **OS:** Windows 10 or newer  
 **Programming Language:** Python 3.10 or newer  
 **Packages:** [psutil](https://pypi.org/project/psutil/), [GPUtil](https://pypi.org/project/GPUtil/)

 ## Screenshots
 ![screenshot1](https://i.imgur.com/NjM9dE6.png)  
   
 ![screenshot2](https://i.imgur.com/jy8iD4p.png)  

 ![screenshot3](https://i.imgur.com/gO4tv3d.png)
