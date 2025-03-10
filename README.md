# LN2_Monitor
This project will use a USB connection to a dymo scale to help graph and weigh the percentage full of an LN2 trap. The percentage full is based on the maximum weight a LN2 trap can hold(about 28.26kg). The scale used in conjunction with this code is the Dymo Digital Shipping Scale (S100) (https://www.dymo.com/scales/dymo-s100-digital-usb-shipping-scale-100-pound-capacity/SAP_1776111.html)

![LN2_dewar](https://github.com/dav17393/LN2_Monitor/blob/main/LN2_dewar.png)

**Required Software:**
download the software below first:

libusb-win32 (https://sourceforge.net/projects/libusb-win32/)


The easiest way to install it is to download the Zadig installer https://zadig.akeo.ie/

Select your device and select the libusb-win32 driver. Then click replace or install driver

![LN2_dewar](https://github.com/dav17393/LN2_Monitor/blob/main/zadig.png)

to install the code: python3 -m pip install LN2_Monitor
then go into python and input
```
from ln2_monitor import d1 
scale = d1.SCL()
scale.monitor()
```
or 
```
scale.plot()
```

Both plot and monitor will generate text file logs in the current directory

**To turn off "auto-sleep" mode on the scale, hold the kg/lb button (sometimes tare button) and turn the scale on. **

The basic minimum and maximum weights(kg) are set to default as the dewar that comes with a bluefors cryostat. Scale.setweight() can be run to change the minumum and maximum weight of the cryostat.


Enjoy!
