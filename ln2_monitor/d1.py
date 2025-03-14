import usb.core
import usb.util
import time
import numpy as np
import math
import os
import sys

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
        self.getdata()
        self.columns,self.lines = os.get_terminal_size()
        self.old_percent_str = None

        try:
            file=open("config.txt", "r")
            lines = file.readlines()
            weightmax_string = lines[0].split(":")[1].split("kg")[0]
            weighmin_string = lines[1].split(":")[1].split("kg")[0]
            self.weighmax = float(weightmax_string)
            self.weighmin = float(weighmin_string)
        except:
            print("no default weight found, weight is now set to a standard LN2 trap(max:29.4588kg, min:12.17694kg)")
            self.weighmax = 29.46
            self.weighmin = 12.18

    def printdata(self):
        time_str = "|"+self.curr_time.strftime("%m/%d/%y, %H:%M:%S ")
        percent_str = " "+str(round(self.per,1))+"%|"
        if len(percent_str)<7:
            percent_str = " "+percent_str
        bar_str_length = self.columns - len(percent_str)-len(time_str)-2
        bar_str = ""
        for i in range(0,int(self.per/100*bar_str_length)):
            bar_str = bar_str + "#"
        for i in range(int(self.per/100*bar_str_length),bar_str_length):
            bar_str = bar_str + " "
        print_str = percent_str+bar_str+time_str
        if self.old_percent_str is None: #first print
            print(print_str,end = "\r",flush = True)
        elif self.old_percent_str == percent_str: #just update time no new line
            print(print_str,end = "\r",flush = True)
        else: #new line
            print(print_str,flush = True)
        self.old_percent_str = percent_str
        
        
    def plotdata(self):
        date_time = datetime.now().strftime("%Y_%m_%d Dymo")
        x_ticks = []
        y_ticks = []
        self.filename = (input("What day's data would you like to plot(YEAR_MONTH_DATE):"))
        file = open(self.filename+' Dymo'+ '.txt', 'r')
        liness = file.readlines()
        x_values = []
        y_values = []
        for i in range(0,len(liness)):
            y_values.append(float(liness[i].split(",")[1].split("%")[0]))
            x_values.append(datetime.strptime((liness[i].split(",")[0]),"%H:%M:%S") )
        line, = pyplot.plot_date(x_values, y_values, '-')
        pyplot.title('LN2 Trap Fullness(based on the txt file)')
        pyplot.ylabel('Percent Full')
        pyplot.xlabel('Time')
        pyplot.xticks(rotation = 30)
        pyplot.show()
    
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
        #print (self.data)
        
     
    def setweight(self):
        self.weighmax = float(input("What is the Maximum Weight(kg) of the LN2 Trap?:"))
        self.weighmin = float(input("What is the Minumum Weight(kg) of the LN2 Trap?:"))
        self.config = input("Would you like to save these values in a txt file and for future uses?(y/n):")
        if str(self.config) == 'y':
            self.tfile = open('config'+ '.txt', 'a')   
            items = "max_weight" + ":" + str(self.weighmax) + "kg" + "\n" + "min_weight" + ":" + str(self.weighmin)+"kg"
            self.tfile.truncate(0)
            self.tfile.write(items)
            self.tfile.close()
        if str(self.config) == 'n':
            print("Ok")
    
    def getpercentfull(self):
        self.per= None
        self.getkg()
        while self.per == None:
            self.getdata()
            try:
                self.per =  ((((self.lbkg)-self.weighmin)/(self.weighmax-self.weighmin))*100)
            except:
                time.sleep(0.1)
                continue
            #print(self.per)
        return self.per
    
    def getkg(self):
        self.kg = None
        while self.kg == None:
            self.getdata()
            try:
                self.kg = ((self.data[4] + (256*self.data[5]))/10)
                if int(self.data[2]) == 12:
                    self.lbkg = (self.kg/2.205)
                else:
                    self.lbkg = (self.kg)

            except:
                time.sleep(0.1)
                continue
        #print(round(self.lbkg,1))       
    
    def plot(self, interval=60):
        self.getpercentfull()
        self.curr_time = datetime.now()
        x_data, y_data = [self.curr_time], [self.per]
        date_time = datetime.now().strftime("%Y_%m_%d_log")
        self.tfile = open(date_time+ '.txt', 'a')
    
        figure = pyplot.figure()
        line, = pyplot.plot_date(x_data, y_data, '-')
        self.interval = interval
        pyplot.title('Percentage Full: ' + str(round(self.per,2)) + '%')
        pyplot.xlabel('Time')
        pyplot.ylabel('Percent Full')

        def update(frame):
            self.getpercentfull()
            ax = pyplot.gca()
            self.curr_time = datetime.now()
            self.printdata()
            x_data.append(self.curr_time)
            y_data.append(self.per)
            items = str(self.curr_time.strftime("%H:%M:%S")) +","+" "+str(round(self.per,2))+"%"+"\n"
            self.tfile.write(items)
            line.set_data(x_data, y_data)
            figure.gca().relim()
            figure.gca().autoscale()
            pyplot.plot(x_data, y_data, '-', color='blue')
            ax.set_title('Percentage Full: ' + str(round(self.per,2)) + '%')
    
            if self.per > 20:
                ax.set_facecolor('white')
            if self.per < 20:
                ax.set_facecolor('red')
            return line,

 
        animation = FuncAnimation(figure, update, interval=self.interval*1000,cache_frame_data = False)
        pyplot.xticks(rotation = 30)
        pyplot.show()

        self.tfile.close()
        
    def monitor(self, interval=60): #just monitor in the terminal
        self.getpercentfull()
        self.curr_time = datetime.now()
        x_data, y_data = [self.curr_time], [self.per]
        date_time = datetime.now().strftime("%Y_%m_%d_log")
        self.tfile = open(date_time+ '.txt', 'a')
        self.interval = interval
        
        try: # to allow killing with ctrl c to exit while loop
            while True:
                self.getpercentfull()
                self.curr_time = datetime.now()
                self.printdata()
                items = str(self.curr_time.strftime("%H:%M:%S")) +","+" "+str(round(self.per,2))+"%"+"\n"
                self.tfile.write(items)
                time.sleep(interval)
            
        except:
            self.tfile.close()
      
   
    def __str__(self):
        return f"{self.data}"
        
    def close(self):
        self.scl.close()
        
   
  
if __name__ == "__main__":
    scale = SCL()
    scale.plot()




