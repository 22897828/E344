from IPython import get_ipython;   
get_ipython().magic('reset -sf')

import time

#import Tkinter
import tkinter as tk
from tkinter import ttk

# import SerialComms
import SerialComms

# import serial exception handler
from serial import SerialException


#declare global variables
width = 330; # display width in pixels
height = 400; # displayheight in pixels
comPort = 'COM6'
baudRate = 9600
chargeComms = 'OV1';#variable to control charging
chargeHold = 0;

#create charging button
#chargeText = "Toggle Charging"
#chargeButt = tk.Button(text=chargeText, command = lambda: buttonConnectHandler())
#chargeButt.grid(column = 0, row = 0, columnspan = 2)


#Create a display
display = tk.Tk()

# give the Display a title
display.title("Design (E.) 344")

#Display GUI in top left of screen
systemWidth = display.winfo_screenwidth() # get width of current screen
systemHeight = display.winfo_screenheight() # get height of current screen
displayX = (systemWidth / 4) - (width / 2) # set the horizontal location of the display
displayY = (systemHeight / 1.5) - (height / 2) # set the vertical location of the display
display.geometry('%dx%d+%d+%d' % (width, height, displayX, displayY)) # set the location of the display
#display.resizable(False, False)

#enable and disable charging
chargeButtonText = "Toggle Charging"
chargeButton = tk.Button(text = chargeButtonText, command = lambda: chargeButtonHandler())
chargeButton.grid(column = 0,row = 3, columnspan = 2)

#label the current Charging statuss
chargeLabelText = "Charging is inactive"
chargeLabel = tk.Label(text = chargeLabelText)
chargeLabel.grid(column = 0,row = 4, columnspan = 2)

#create analogue labels and data display
ldrLabel = tk.Label(text = "Ambient Brightness:")
batteryLabel = tk.Label(text = "Battery Voltage:")
supplyLabel = tk.Label(text = "Supply Voltage:")
currentLabel = tk.Label(text = "current:")
batteryLabel.grid(column = 0, row = 6, sticky = tk.E)
supplyLabel.grid(column = 0, row = 7, sticky = tk.E)
currentLabel.grid(column = 0, row = 8, sticky = tk.E)
ldrLabel.grid(column = 0, row = 9, sticky = tk.E) 


ldrDataLabel = tk.Label(text = "0")
batteryDataLabel = tk.Label(text = "0")
supplyDataLabel = tk.Label(text = "0")
currentDataLabel = tk.Label(text = "0")
batteryDataLabel.grid(column = 1, row = 6)
supplyDataLabel.grid(column = 1, row = 7)
currentDataLabel.grid(column = 1, row = 8)
ldrDataLabel.grid(column = 1, row = 9) 


# creates an instance of the SerialComms class
serialComs = SerialComms.SerialComms(comPort, baudRate)

# creates label
comLabelText = "COM Port:"
comLabel = tk.Label(text = "COM Port:")
comLabel.grid(column = 0, row = 0)

# creates an entry box for the user to enter the COM port
comPortEntry = tk.Entry(text = comPort)
comPortEntry.grid(column = 1, row = 0)
comPortEntry.insert(0,comPort)

# creates label
pwmLabel = tk.Label(text = "Enter PWM%")
pwmLabel.grid(column = 0, row = 5)

# creates an entry box for the user to enter the COM port
pwmEntry = tk.Entry(text = 100)
pwmEntry.grid(column = 1, row = 5)
pwmEntry.insert(0,100)

#button to start serial connection
connectButtonText = "Toggle Serial Connection"
connectButton = tk.Button(text=connectButtonText, command = lambda: connectButtonHandler())
connectButton.grid(column = 0, row = 1, columnspan = 2)

connectStatusLabelText = "The device is currently disconnected."
connectStatusLabel = tk.Label(text=connectStatusLabelText)
connectStatusLabel.grid(column = 0, row = 2, columnspan = 2)

def openConnection(sc):
    serialComs.setCOMPort(comPort)
    serialComs.setBaudrate(baudRate)
    serialComs.open()
    
def closeConnection(sc):
    serialComs.close()
    
def connectButtonHandler():
    global comPort
    global baudRate
    global chargeHold

    #If the connection is closed, try open it.
    if(serialComs.isOpen == False):
        comPort = comPortEntry.get()
        #Tries to open the serial conection. Displays error message in ConnectFeedback if it fails.
        try:
            openConnection(serialComs);
        except SerialException:
            print("Unable to connect.")
            
        if(serialComs.isOpen == True):
            print("Connected successfully.")
            connectStatusLabel.configure(text = "The device is currently connected.")
            
            #get the current charging statuss
            
            i = 1;       
            while(i == 1):
                data = serialComs.receive()
                csvData = ""
                if(len(data)>0):
                    print(data[0])
                    csvData = data[0].split(",")
                if(len(csvData) == 5):            
                    if(csvData[0] == '1'):
                        chargeHold = 1
                        chargeLabel.configure(text = "Charging is Active")
                    if(csvData[0] == '0'): 
                        chargeHold = 0
                        chargeLabel.configure(text = "Charging is inActive")
                    i = 0
                time.sleep(0.1)
            
    
    #If the connection is open, close it.        
    elif(serialComs.isOpen==1):
        #Tries to close the serial conection. Displays error message in ConnectFeedback if it fails.
        try:
            closeConnection(serialComs)
        except SerialException:
            print("Unable to close connection.")
        #If the connection is closed, change the label of the button and and update ConnectFeedback to disconnected.
        if(serialComs.isOpen == False):
            print("Disconnected successfully.")
            connectStatusLabel.configure(text = "The device is currently disconnected.")
    
def updateDisplay():   
    global chargeHold
    if(serialComs.isOpen==True):
        data = serialComs.receive()
        csvData = ""
        if(len(data)>0):
            print(data[0])
            csvData = data[0].split(",")
        if(len(csvData) == 5):
            batteryDataLabel.configure(text = csvData[1] + " V")
            supplyDataLabel.configure(text = csvData[2] + " V")
            currentDataLabel.configure(text = csvData[3] + " mA")
            ldrDataLabel.configure(text = csvData[4])
            
            if(csvData[0] == '1'):
                chargeHold = 1
            if(csvData[0] == '0'): 
                chargeHold = 0
                
        data = ""
        pwm = int(pwmEntry.get()) + 100
        pwmSend = str(pwm)
        serialComs.send(pwmSend)
        print(pwmSend)
         
    display.after(1000,lambda: updateDisplay())

def chargeButtonHandler():
    global chargeHold
    if(serialComs.isOpen == True):
        if(chargeHold==1):
            serialComs.send("OV0")
            chargeLabel.configure(text = "Charging is inActive")            
        if(chargeHold == 0):
            serialComs.send("OV1")
            chargeLabel.configure(text = "Charging is Active")            




updateDisplay()
display.mainloop()


