import usb.core
import usb.util
import time
import numpy as np
import math

from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from random import randrange


class SCL():

    def __init__(self):
        self.VENDOR_ID = 0x0922
        self.PRODUCT_ID = 0x8009
        self.device = usb.core.find(idVendor=self.VENDOR_ID,idProduct=self.PRODUCT_ID)
        self.device.set_configuration()
        self.endpoint = self.device[0][(0,0)][0]
        self.data = None
       
    
    def main(self):
        self.plot()
    
    if __name__ == "__main":
        main()
    
   
        
        
        # outfile = open('data.txt', 'w')
        
        # percent = input("self.getpercentfull")
        
        # outfile.write(percent+ "\n")
        
        # outfile.close()
        
        # lines = ['0']
        # with open('percentfull.txt', 'w') as f:
            # for line in lines:
                # f.write(line)
                # f.write('\n')
        # more_lines = ['', self.getpercentfull()]
        
        # with open('percentfull.txt', 'a') as f:
            # f.write('\n'.join(more_lines))
       

    def getdata(self):
        try:
           self.data = self.device.read(self.endpoint.bEndpointAddress,self.endpoint.wMaxPacketSize)
        except:
            usb.util.dispose_resources(self.device)
            time.sleep(0.1)
            self.device = usb.core.find(idVendor=self.VENDOR_ID,idProduct=self.PRODUCT_ID)
            self.device.set_configuration()
            self.endpoint = self.device[0][(0,0)][0]
            self.data = self.device.read(self.endpoint.bEndpointAddress,self.endpoint.wMaxPacketSize)
        print (self.data)
        

        
    def getpercentfull(self):
        self.per= None
        
        while self.per == None:
            self.getdata()
            try:
                self.per = (((self.data[4] + (256*self.data[5]))/10)/28.2588)*100
            except:
                time.sleep(0.1)
                continue
            print(self.per)
        return self.per
        # try:
            # self.data = self.device.read(self.endpoint.bEndpointAddress,self.endpoint.wMaxPacketSize)
        # except:
            # usb.util.dispose_resources(self.device)
            # time.sleep(0.1)
            # self.device = usb.core.find(idVendor=self.VENDOR_ID,idProduct=self.PRODUCT_ID)
            # self.device.set_configuration()
            # self.endpoint = self.device[0][(0,0)][0]
            # self.data = self.device.read(self.endpoint.bEndpointAddress,self.endpoint.wMaxPacketSize)
        # self.full = (((self.data[4] + (256*self.data[5]))/10)/28.2588)*100
        # print(self.full)
        
    def getkg(self):
        self.kg = None
        
        while self.kg == None:
            self.getdata()
            try:
                self.kg = ((self.data[4] + (256*self.data[5]))/10)

            except:
                time.sleep(0.1)
                continue
        print(self.kg)       
    
    def plot(self, interval=1000):
        x_data, y_data = [], []
        now = datetime.now()
        date_time = now.strftime("%Y_%m_%d, Dymo")
        date_timesec = now.strftime("%Y/%m/%d, %H:%M:%S")
        self.tfile = open(date_time+'.txt', 'a')
    
        figure = pyplot.figure()
        line, = pyplot.plot_date(x_data, y_data, '-')
        self.interval = interval
        pyplot.title('Dymo Scale fullness')
        pyplot.ylabel('Percent full')
       
        
        def update(frame):
            self.getpercentfull()
            x_data.append(datetime.now())
            y_data.append(self.per)
            items = str(date_timesec)+","+" "+str(round(self.per,2))+"%"+"\n"
            self.tfile.write(items)
            line.set_data(x_data, y_data)
            figure.gca().relim()
            figure.gca().autoscale_view()
            return line,
        
        
        #append to array, clear, then replot?
        animation = FuncAnimation(figure, update, interval=self.interval)
      
        pyplot.show()
        self.tfile.close()
        #self.tfile.close()
    # def imp(self):
        # x_data, y_data = [], []
        # items = [str(datetime.now()), str(self.per)]
        
        # with open('items.txt', 'w') as tfile:
            # tfile.write('\n'.join(items))
  
    def __str__(self):
        return f"{self.data}"
        
    def close(self):
        self.scl.close()
        
   
  

  




