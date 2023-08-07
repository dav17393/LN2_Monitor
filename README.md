# LN2_Monitor
This project will use a USB connection to a dymo scale to help graph and weigh the percentage full of an LN2 trap. The percentage full is based on the maximum weight a LN2 trap can hold(about 28.26kg)

**Required Softwares:**
download the softwares below first:

libusb-win32 (https://sourceforge.net/projects/libusb-win32/)

to install the code: python3 -m pip install LN2_Monitor
then go into python and input "from ln2_monitor import d1". 
input "scale = d1.SCL()"

**How to run the Software:** (not needed if pip installed)

After opening up the program, download both softwares and run the libusb-win32 software. In device selection, select the USB input device with product ID 8009(pid:8009). Then pipinstall pyusb, numpy, and matplot. Then run the code by changing the directory whichever folder the d1 file was downloaded to. Then switch powershell to python and import the d1 file. Set scale = d1.SCL() and run scale.main() or scale.plot() to start plotting and transferring the data to a txt file. You can also run scale.getkg() or scale.getdata() to get the kg or the array respectively. The basic minimum and maximum weights(kg) are set to default as the blucifer cryostat. Scale.setweight() can be run to change the minumum and maximum weight of the cryostat.

**To turn off "auto-sleep" mode on the scale, hold the kg/lb button and turn the scale on. **

**The array that is returned when calling the scale.main(), scale.plot(), or scale.getdata() functions can be translated as shown below:**
array('B'[3, 2, 11, 255, 0, 0])

The first element is always 3 and negatable.
The second element is also negatable.
The third element will only return either 2 or 11, with 2 meaning the scale is in kg mode and 11 meaning the scale is in lbs/oz mode.
The fourth element is the scale factor. A value of 255 means the scaling factor is 10^-1(0.1), a value of 254 means a scaling factor of 10^-2(0.01), and so on. 
The fourth and fifth elements together are used to determine the weight.
The sixth element is also negatable. 

Enjoy!
