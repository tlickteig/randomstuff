import serial
import math
import sys
import tkinter
from tkinter import messagebox as mb
from time import sleep
import datetime
import math
import statistics
import psutil
import random
from flask import Flask, request
import threading

#Declare data variables
displaymode = 'DEFAULT'
ledMode = 'SYNC'
ledColorArray = [  [255, 255, 100]
                 , [0, 0, 255]
                 , [255, 255, 100]
                 , [0, 0, 255]
                 , [255, 255, 100]
                 , [0, 0, 255] ]
color = [0, 0, 0]
displayitems = [[' ', ' '], [' ', ' ']]
delaytime = 50
app = Flask(__name__)

@app.before_first_request
def start_main_background_thread():
    thread = threading.Thread(target=main_background_thread)
    thread.start()

@app.route("/", methods=['GET', 'POST'])
def index():
    
    global displaymode
    global ledMode
    global color
    global displayitems
    global delaytime
    
    if request.method == "POST":
        rawColor = request.form.get('color', "")
        displaylineone = request.form.get('displaylineone', "")
        displaylinetwo = request.form.get('displaylinetwo', "")
        driveletter = request.form.get('driveLetter', "")
        delaytime = request.form.get('delaytime', 0)
        
        if request.form.get('displayMode') != "":
            displaymode = request.form.get('displayMode', displaymode)
        
        if request.form.get('ledMode') != "":
            ledMode = request.form.get('ledMode', ledMode)
       
        if rawColor != "":
            colorString = rawColor.split(" ")
            color = [int(colorString[0]), int(colorString[1]), int(colorString[2])]
            
        if displaylineone != "" and displaylinetwo != "":
            displaymode = "DEFAULT"
            displaylineoneitems = displaylineone.split("|")
            displaylinetwoitems = displaylinetwo.split("|")
            
            for i in range(len(displaylineoneitems)):
                displayitems.append([displaylineoneitems[i], displaylinetwoitems[i]])

        if driveletter != "":
            displaymode = "DISK_USAGE " + driveletter

    rawColorTemp = f"{str(color[0])} {str(color[1])} {str(color[2])}"

    return f"""<form action='/' method='post'>
            <select name='displayMode'>
                <option value='' selected>No Change</option>
                <option value='DATETIME'>Date and time</option>
                <option value='CPU_LOAD'>CPU Load</option>
                <option value='MEMORY_USAGE'>Memory usage</option>
            </select>
            <input type='text' value='' name='driveLetter' placeholder='Enter drive letter' />
            <p></p>
            <select name='ledMode'>
                <option value='' selected>No Change</option>
                <option value='SYNC'>Sync</option>
                <option value='OFF'>Off</option>
                <option value='RANDOM'>Random</option>
                <option value='TWINKLE'>Twinkle</option>
                <option value='AMERICA'>America</option>
            </select>
            <p></p>
            <input type='text' name='color' value='{rawColorTemp}' placeholder='Enter color values, use space as separator' />
            <p></p>
            <p>Enter custom display items below. Separate using |</p>
            <input type='text' name='displaylineone' value='' placeholder='Line one items' />
            <br />
            <input type='text' name='displaylinetwo' value='' placeholder='Line two items' />
            <p></p>
            <input type='submit' value='Submit' />
        </form>"""

def main_background_thread():

    #Start
    log_message("Hello world!")

    #Declare index variables
    delayindex = 0
    displayindex = 0
    screenindex = 0
    serialindex = 0
    
    #Declare other variables
    oldcolor = [0, 0, 0]
    
    try:
        ser, serialindex = connect_to_device()
        print("Serial device found on COM" + str(serialindex))
    except IOError:
        print("Unable to detect a device")
        sys.exit(1)

    while True:
        #Print to the screen
        delayindex, screenindex = write_screen_data(ser, displaymode, displayitems, delayindex, delaytime, screenindex)

        #Update the led's
        update_led(ser, ledMode, ledColorArray, color)

        #Change color if applicable
        if color != oldcolor:
            change_color(ser, color)
            oldcolor = color
            
def connect_to_device():

    x = 2
    loop = True

    while loop:

        try:
            device = serial.Serial('COM' + str(x), timeout = 2)
            loop = False
        except serial.serialutil.SerialException:

            if(x < 100):
                x += 1
            else:
                raise IOError

    return device, x

def log_message(message):
    with open('service.log', 'a') as file:
        file.write(message)

def write_screen_data(ser, displaymode, displayitems, delayindex, delaytime, screenindex):

    line1 = ' '
    line2 = ' '

    #Print the current date and time
    if displaymode == 'DATETIME':
        [line1, line2] = current_date()

    #Print the current cpu load
    elif displaymode == 'CPU_LOAD':
        percent = cpu_usage()
        line1 = 'CPU load: ' + str(percent) + '%'
        line2 = bar_graph(100, int(percent))

    #Print the current memory usage
    elif displaymode == 'MEMORY_USAGE':
        line1 = 'RAM usage: ' + str(int(memory_usage())) + '%'
        line2 = bar_graph(100, int(memory_usage()))

    #Print the current disk usage
    elif displaymode.find('DISK_USAGE') == 0:
        letter = displaymode[11 : 13]
        try:
            usage = int(psutil.disk_usage(letter)[3])
            line1 = letter + ' usage: ' + str(usage) + '%'
            line2 = bar_graph(100, usage)
        except FileNotFoundError:
            line1 = 'ERROR'
            line2 = letter  + 'is unavailable'

    #If the mode is default, choose an item from the file
    elif displaymode == 'DEFAULT':

        try:
            line1 = displayitems[screenindex][0]
            line2 = displayitems[screenindex][1]
        except IndexError:
            pass

    #Print to the display
    if (int(delaytime) <= delayindex) or (displaymode != 'DEFAULT'):   

        #Encode into bytes
        x = str.encode(line1 + '\\0')
        y = str.encode(line2 + '\\1')

        #Print to the display
        sleep(.05)
        ser.write(x)
        sleep(.05)
        ser.write(y)
        
        delayindex = 0

        #Increment the display index
        if displaymode == 'DEFAULT':
            if (screenindex + 1) >= len(displayitems):            
                screenindex = 0
            else:
                screenindex += 1
        
    else:
        delayindex += 1

    if(displaymode == 'DEFAULT'):
        print(screenindex)
        sleep(.01)
            
    return delayindex, screenindex

def change_color(ser, color):

    #Pull colors from the array
    red = str(color[0])
    green = str(color[1])
    blue = str(color[2])

    #Increase length of strings to the appropriate amount
    while len(red) < 3:
        red = '0' + red
    while len(green) < 3:
        green = '0' + green
    while len(blue) < 3:
        blue = '0' + blue

    #Encode into bytes and send to serial device
    value = red + green + blue + '\\2'
    value2 = str.encode(value)
    sleep(.2)
    ser.write(value2)

def update_led(ser, ledMode, ledColorArray, color):

    if ledMode == 'SYNC':
        for i in range(6):
            ledColorArray[i] = color

    elif ledMode == 'OFF':
        for i in range(6):
            ledColorArray[i] = [0, 0, 0]

    elif ledMode == 'RANDOM':
        index = random.randint(0, 5)
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        ledColorArray[index] = [red, green, blue]

    elif ledMode == 'TWINKLE':
        ledColorArray[0] = color
        ledColorArray[1] = color
        ledColorArray[2] = color
        ledColorArray[3] = color
        ledColorArray[4] = color
        ledColorArray[5] = color

        index = random.randint(0, 5);
        ledColorArray[index] = [0, 0, 0]

    elif ledMode == 'AMERICA':
        ledColorArray[0] = [255, 0, 0]
        ledColorArray[3] = [255, 0, 0]
        ledColorArray[1] = [255, 255, 100]
        ledColorArray[4] = [255, 255, 100]
        ledColorArray[2] = [0, 0, 255]
        ledColorArray[5] = [0, 0, 255]

    #Send the data to the serial device
    index = 0
    for i in ledColorArray:

        #Pull red, green, and blue values from the array
        red = str(i[0])
        green = str(i[1])
        blue = str(i[2])

        #Increase length of strings to the appropriate amount
        while len(red) < 3:
            red = '0' + red
        while len(green) < 3:
            green = '0' + green
        while len(blue) < 3:
            blue = '0' + blue

        #Encode into bytes and send to serial device
        value = red + green + blue + str(index) + '\\3'
        value2 = str.encode(value)
        sleep(.05)
        ser.write(value2)
        index += 1
    

def bar_graph(maximum, value):

    step = float(maximum) / 16.0    
    numberofbars = float(value) / step
    return '=' * int(numberofbars)

###DATA COLLECTION FUNCTIONS###
def current_date():

    #Get current date and time
    date = datetime.date.today()
    time = datetime.datetime.now()
    hour = datetime.datetime.now()

    #Format date value
    date = str(date)
    date = date.replace('-', '/')

    #Format seconds and minutes
    time = str(time)
    time = time[13 : 19]

    #Get hour
    hour = str(hour)
    hour = hour[11 : 13]
    inthour = int(hour)

    #Make colons flash
    second = int(time[4 : 6])
    if (second % 2) == 0:
        time = time.replace(':',' ')

    #Convert to 12 hour time and format
    if inthour >= 12:
        inthour = inthour - 12
        after = 'PM'
    else:
        after = 'AM'

    hour = str(inthour)
    
    if inthour < 10:
        hour = '0' + hour

    if inthour == 0:
        hour = '12'

    #Construct formatted time
    time = hour + time + ' ' + after
    
    return [time, date]

def memory_usage():

   usage = psutil.virtual_memory()[2]
   return usage

def cpu_usage():

    numberofsamples = 5
    total = 0

    for x in range(numberofsamples):
        total += psutil.cpu_percent(interval=.1)

    return int(total / numberofsamples)

#main()
