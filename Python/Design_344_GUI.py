from IPython import get_ipython;   
get_ipython().magic('reset -sf')

#import Tkinter
import tkinter as tk

# import SerialComms
import SerialComms

# import serial exception handler
from serial import SerialException

comPort = 'COM3'
baudRate = 9600

# create a widow
window = tk.Tk()

# give the window a title
window.title("Design (E.) 344")


# define the dimensions of the window
windowWidth = 330; # width in pixels
windowHeight = 200; # height in pixels

# make the window pop up in the middle of the display, on any size display
widthSystem = window.winfo_screenwidth() # get width of current screen
heightSystem = window.winfo_screenheight() # get height of current screen
windowX = (widthSystem / 2) - (windowWidth / 2) # set the horizontal location of the window
windowY = (heightSystem / 2) - (windowHeight / 2) # set the vertical location of the window
window.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, windowX, windowY)) # set the location of the window
window.resizable(False, False)

# creates an instance of the SerialComms class
sc = SerialComms.SerialComms(comPort, baudRate)

# creates label
connectionLabelText = "Enter your Baud rate and COM Port below, and click connect."
connectionLabel = tk.Label(text=connectionLabelText)
connectionLabel.grid(column = 0, row = 0, columnspan = 2)

# creates label
baudLabelText = "Baud Rate"
baudLabel = tk.Label(text=baudLabelText)
baudLabel.grid(column = 0, row = 1)

# creates label
comLabelText = "COM Port:"
comLabel = tk.Label(text=comLabelText)
comLabel.grid(column = 0, row = 2)

# creates an entry box for the user to enter the baud rate
entryBaudRate = tk.Entry()
entryBaudRate.grid(column = 1, row = 1)
entryBaudRate.insert(0,baudRate)

# creates an entry box for the user to enter the COM port
entryComPort = tk.Entry(text = comPort)
entryComPort.grid(column = 1, row = 2)
entryComPort.insert(0,comPort)

# creates a label indicating the current connection status
connectionStatusLabelText = "The device is currently disconnected."
connectionStatusLabel = tk.Label(text=connectionStatusLabelText)
connectionStatusLabel.grid(column = 0, row = 4, columnspan = 2)
            
# creates a connect/disconnect button
connectionButtonText = "Toggle Connection"
connectionButton = tk.Button(text=connectionButtonText, command = lambda: buttonConnectHandler())
connectionButton.grid(column = 0, row = 3, columnspan = 2)

# creates label showing the latest received data
ledStatusLabel = tk.Label(text="The LED is now OFF.")
ledStatusLabel.grid(column = 0, row = 5, columnspan = 2)

# creates an LED toggle button
ledButtonText = "Toggle LED"
ledButton = tk.Button(text=ledButtonText, command = lambda: buttonLEDHandler())
ledButton.grid(column = 0, row = 6, columnspan = 2)


# updates the display every 100 ms
def updateDisplay():
    # update the variables that you want to stay current here
    if(sc.isOpen==True):
        data = sc.receive()
        if(len(data) == 1):
            if(data[0] == 'LED1\r'):
                print("The LED is now ON.")
                ledStatusLabel.configure(text = "The LED is now ON.")
            elif(data[0] == 'LED0\r'):
                print("The LED is now OFF.")
                ledStatusLabel.configure(text = "The LED is now OFF.")
        data = ""

    window.after(100,lambda: updateDisplay())

def openConnection(sc):
    sc.setCOMPort(comPort)
    sc.setBaudrate(baudRate)
    sc.open()
    
def closeConnection(sc):
    sc.close()
    
def buttonConnectHandler():
    global comPort
    global baudRate

    #If the connection is closed, try open it.
    if(sc.isOpen == False):
        comPort = entryComPort.get()
        baudRate = entryBaudRate.get()
        
        #Tries to open the serial conection. Displays error message in ConnectFeedback if it fails.
        try:
            openConnection(sc);
        except SerialException:
            print("Unable to connect.")
            
        if(sc.isOpen == True):
            print("Connected successfully.")
            connectionStatusLabel.configure(text = "The device is currently connected.")
    
    #If the connection is open, close it.        
    elif(sc.isOpen==1):
        #Tries to close the serial conection. Displays error message in ConnectFeedback if it fails.
        try:
            closeConnection(sc)
        except SerialException:
            print("Unable to close connection.")
        #If the connection is closed, change the label of the button and and update ConnectFeedback to disconnected.
        if(sc.isOpen == False):
            print("Disconnected successfully.")
            connectionStatusLabel.configure(text = "The device is currently disconnected.")
            
def buttonLEDHandler():
    if(sc.isOpen == True):
        sc.send("Toggle LED")         
    
updateDisplay()
    
window.mainloop()