# LN2_Monitor
This project will use a USB connection to a dymo scale to help graph and weigh the percentage full of an LN2 trap. The percentage full is based on the maximum weight a LN2 trap can hold(about 28.26kg)

Required Softwares:

PyUSB 1.0 (https://sourceforge.net/projects/pyusb/files/PyUSB%201.0/)

libusb-win32 (https://sourceforge.net/projects/libusb-win32/)

The array that is returned when calling the scale.main(), scale.plot(), or scale.getdata() functions can be translated as shown below:
array('B'[3, 2, 11, 255, 0, 0])

The first element is always 3 and negatable.
The second element is also negatable.
The third element will only return either 2 or 11, with 2 meaning the scale is in kg mode and 11 meaning the scale is in lbs/oz mode.
The fourth element is the scale factor. A value of 255 means the scaling factor is 10^-1(0.1), a value of 254 means a scaling factor of 10^-2(0.01), and so on. 
The fourth and fifth elements together are used to determine the weight.
The sixth element is also negatable. 
