#-*- coding:utf-8 -*-

"""
    desc: |    
"""

from libopensesame.oslogging import oslogger
import hid
import sys
from types import *
import os
import ctypes
import time


class EvtExchanger:
    """
    desc: |
    """
    SelectedDevice = hid.device()
    ListOfDevices = []
    
    def __init__(self):
        try:
            EvtExchanger.Attached()
            oslogger.info("EventExchanger Initialized")
        except Exception as e:
            raise Exception('EventExchanger (LibUSB) Initialisation Error')

    @staticmethod
    def Device():
        return EvtExchanger

    @staticmethod
    def Attached(matchingkey = "EventExchanger"):   
        EvtExchanger.ListOfDevices = []
        EvtExchanger.SelectedDevice.close()
        for d in hid.enumerate():
            longname = d["product_string"] + " SN## " + d["serial_number"]
            if matchingkey in longname:
                if EvtExchanger.ListOfDevices == []:
                    EvtExchanger.SelectedDevice.open_path(d['path'])
                    EvtExchanger.SelectedDevice.set_nonblocking(True)
                EvtExchanger.ListOfDevices.append(longname)
        return EvtExchanger.ListOfDevices


    @staticmethod
    def Select(deviceName):
        EvtExchanger.Attached(deviceName)
        return [EvtExchanger.Device()]
    
    @staticmethod
    def WaitForDigEvents(AllowedEventLines, TimeoutMSecs):
        # flush the buffer!
        while (EvtExchanger.SelectedDevice.read(1) != []):
            continue
        TimeoutSecs = TimeoutMSecs / 1000
        startTime = time.time()        
        while 1:
            ElapsedSecs = (time.time()-startTime)
            lastbtn = EvtExchanger.SelectedDevice.read(1)           
            if (lastbtn != []):
                if (lastbtn[0] & AllowedEventLines > 0):
                    break
            # break for timeout:
            if (TimeoutMSecs != -1):
                if (ElapsedSecs >= (TimeoutSecs)):
                    lastbtn = [-1]
                    ElapsedSecs = TimeoutSecs
                    break
        return lastbtn[0],round(ElapsedSecs/1000)
        
    def GetAxis():
        while (EvtExchanger.SelectedDevice.read(1) != []):
            pass
        time.sleep(.01)
        valueList = EvtExchanger.SelectedDevice.read(3)   
        if (valueList == []):
            return EvtExchanger.__AxisValue
        EvtExchanger.__AxisValue = valueList[1] + (256*valueList[2])
        
        return EvtExchanger.__AxisValue  
    '''
        Functions that only require a single USB command to be sent to the device.
    '''

    @staticmethod
    def SetLines(OutValue):
        EvtExchanger.SelectedDevice.write([ 0, EvtExchanger.__SETOUTPUTLINES, OutValue, 0, 0, 0, 0, 0, 0, 0, 0 ])
        
    @staticmethod
    def PulseLines(OutValue, DurationInMillisecs):
        EvtExchanger.SelectedDevice.write([ 0, EvtExchanger.__PULSEOUTPUTLINES, OutValue, DurationInMillisecs & 255, DurationInMillisecs >> 8, 0, 0, 0, 0, 0, 0])
              
    @staticmethod
    def SetAnalogEventStepSize(NumberOfSamplesPerStep):
        EvtExchanger.SelectedDevice.write([ 0, EvtExchanger.__SETANALOGEVENTSTEPSIZE, NumberOfSamplesPerStep, 0, 0, 0, 0, 0, 0, 0, 0 ])

    @staticmethod
    def RENC_SetUp(Range, MinimumValue, Position, InputChange, PulseInputDivider):
        EvtExchanger.__AxisValue = Position
        EvtExchanger.SelectedDevice.write([ 0, EvtExchanger.__SETUPROTARYCONTROLLER, Range & 255, Range >> 8, MinimumValue & 255 , MinimumValue >> 8, Position & 255, Position >> 8, InputChange, PulseInputDivider, 0])
    
    @staticmethod
    def RENC_SetPosition(Position):
        EvtExchanger.__AxisValue = Position
        EvtExchanger.SelectedDevice.write([ 0, EvtExchanger.__SETROTARYCONTROLLERPOSITION, Position & 255, Position >> 8, 0, 0, 0, 0, 0, 0, 0])
        
    @staticmethod
    def SetLedColor(RedValue, GreenValue, BlueValue, LedNumber, Mode):
        EvtExchanger.SelectedDevice.write([ 0, EvtExchanger.__SETWS2811RGBLEDCOLOR, RedValue, GreenValue, BlueValue, LedNumber, Mode, 0, 0, 0, 0 ])
        
    @staticmethod
    def SendColors(NumberOfLeds,Mode):
        EvtExchanger.SelectedDevice.write([ 0, EvtExchanger.__SENDLEDCOLORS, NumberOfLeds, Mode, 0, 0, 0, 0, 0, 0, 0 ])
   
    __AxisValue = 0
    
    # CONSTANTS:
    __CLEAROUTPUTPORT = 0# 0x00
    __SETOUTPUTPORT = 1   # 0x01
    __SETOUTPUTLINES = 2   # 0x02
    __SETOUTPUTLINE = 3   # 0x03
    __PULSEOUTPUTLINES = 4   # 0x04
    __PULSEOUTPUTLINE = 5   # 0x05

    __SENDLASTOUTPUTBYTE = 10   # 0x0A

    __CONVEYEVENT2OUTPUT = 20   # 0x14
    __CONVEYEVENT2OUTPUTEX = 21   # 0x15
    __CANCELCONVEYEVENT2OUTPUT = 22   # 0x16

    __CANCELEVENTREROUTES = 30   # 0x1E
    __REROUTEEVENTINPUT = 31   # 0x1F

    __SETUPROTARYCONTROLLER = 40# 0x28
    __SETROTARYCONTROLLERPOSITION = 41  # 0x29

    __CONFIGUREDEBOUNCE = 50   # 0x32

    __SETWS2811RGBLEDCOLOR = 60  # 0x3C
    __SENDLEDCOLORS = 61  # 0x3D

    __SWITCHALLLINESEVENTDETECTION = 100   # 0x64
    __SWITCHLINEEVENTDETECTION = 101   # 0x65

    __SETANALOGINPUTDETECTION = 102   # 0x66
    __REROUTEANALOGINPUT = 103# 0X67
    __SETANALOGEVENTSTEPSIZE = 104 # 0X68

    __SWITCHDIAGNOSTICMODE = 200   # 0xC8
    __SWITCHEVENTTEST = 201   # 0xC9

#-*- coding:utf-8 -*-

