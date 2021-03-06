'''
Created on May 31, 2017

@author: Nandal
'''
import subprocess
from datetime import datetime
import time
import os
import xml.etree.ElementTree as ET
from time import sleep
from pathlib import Path



class Cache(object):
    """
    A class used internally by pydroid as cache

    ...

    Attributes
    ----------
    previousUIDumpText : str
        xml dump of screen in conditions before passing any event or action
        
    currentUIDumpText : str
        xml dump of screen after the applying any event or action.
        
    """
    previousUIDumpText = ""
    currentUIDumpText = ""
    


class Adb(object):
    """
    A class used to represent Python ADB Client for Android Devices

    ...

    Attributes
    ----------
    adbExe : str
        a string containing full path for adb executable utility.
    deviceId : str
        android device id, which we get using adb devices command. it represents android device uniquely
    tempDataDir : str
        a string representing the full path for the folder which can be used by pydroid to store temp files
    resultDir : str
        a string representing the full path for the folder which can be used by pydroid to store result files
    resultFilePath : str
        a string representing the full path for the file which contains the result logs

    Methods
    -------
    cmdShell(cmd=[])
        Executes any command in terminal and returns the output,error as tupple
        
    devices()
        Returns a dictionary of connected android devices. key:deviceId and value:status
        
    kill_server()
        Function to kill ADB Server
        
    start_server()
        Function to start ADB Server
        
    restart_server()
        Function to restart ADB Server
        
    getprop()
        Function returns a dictionary containing all details about the device connected. It returns a dictionary key:propertyKey and value:propertyValue
        
    shell(cmd=[])
        Function which run a command in shell of connected Android Device and returns a tupple of output,error
        
    uninstall_all_user_apps()
        Function to uninstall all installed apps in user space
        
    reboot()
        Function to reboot connected android device
        
    pull(remote, local)
        Function to fetch a file from device to local machine. remote is the path of file in android device and local is the path in local machine 
        
    push(remote, local)
        Function to send a file to device from local machine. remote is the path of file in android device and local is the path in local machine 
        
    version()
        Function to return version of ADB Tool as string
        
    
    screencap(filename)
        Function to capture the screenshot of android device and save it as a PNG file locally
            
    install(apkFilepath)
        Function to install an APK on android device
            
    uidump(filename=None)
        Function to take uidump on device for all the vies on screen
        
    
            
    get_screencap(filepath)
        Function to take screenshot and save it locally on machine
    
            
    get_logs(filepath)
        Function to get logs from android device and save in a file locally.
        
                
    get_uidump(filepath)
        Function to get view elements xml dump of android foreground activity and save it in a local file
        
    
    
    click(x,y,refreshDump=False)
        Function to click on X and Y coordinates of android screen.
            
        
    long_press(x,y,time_in_seconds=2, refreshDump=False)
        Function to long press on android device on given X and Y coordinates and a default delay of 2 seconds
        
        
    swipe(x1, y1, x2, y2, refreshDump=False)
        Function to swipe on android device from x1, y1 point towards x2,y2 point
        
    
    inputText(text)
        Function to write down text on selected view of android device
        
    
    back(refreshDump=False)
        Function to press Back Key of android device
        

    home(refreshDump=False)
        Function to press Home Key of android device
            
        
    screensize()
        Function to return {'width':int, 'height':int} screensize of device
            
    
    startApp(packageAndActivity,refreshDump=False)
        Function to start an App on Android Device using packageName and Start Activity
        

    """
    
    def __init__(self, adbExe="adb", deviceId=None, tempDataDir=None, resultDir=None, resultFilePath=None):
        self.adbExe = adbExe
        self.deviceId = deviceId
        self.homeDir = str(Path.home())
        
        if not tempDataDir:
            self.tempDataDir = self.homeDir+"/temp"
        else:
            self.tempDataDir = tempDataDir
        if not resultDir:
            self.resultDir = self.homeDir+"/result"
        else:
            self.resultDir = resultDir
            
        if not resultFilePath:
            self.resultFilePath = self.resultDir+"/result.txt"
        else:
            self.resultFilePath = resultFilePath
        
        if not os.path.exists(self.tempDataDir):
            os.mkdir(self.tempDataDir)
        if not os.path.exists(self.resultDir):
            os.mkdir(self.resultDir)


    def cmdShell(self, cmd):
        print("CMD\t"+ ' '.join(cmd))
        if os.name == 'nt':
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)            
        else:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        out, err = p.communicate()
        print("OUT\t{}".format(out))
        print("ERR\t{}".format(err))
        return out.decode("utf-8"), err.decode("utf-8")
    
    
    def devices(self):
        print("1")
        result = {}
        cmd = ["adb", "devices"]
        print("CMD\t"+ " ".join(cmd))
        if os.name == 'nt':
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)            
        else:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        out, err = p.communicate()
        print("OUT\t{}".format(out))
        print("ERR\t{}".format(err))
        if not err and out:
            output = out.decode("utf-8")
            devices_lines = output.split("\n")
            for device_line in devices_lines[1:]:
                values = device_line.split()
                if len(values) == 2:
                    result[values[0].strip()] = values[1].strip()
                
        print("OUT\t{}".format(out))
        print("ERR\t{}".format(err))
        return result
    
    def kill_server(self):
        output, err = self.cmdShell([self.adbExe, "kill-server"])
        print("OUT\t{}".format(output))
        print("ERR\t{}".format(err))
        
    
    def start_server(self):
        output, err = self.cmdShell([self.adbExe, "start-server"])
        print("OUT\t{}".format(output))
        print("ERR\t{}".format(err))
        
    
    def restart_server(self):
        self.kill_server()
        self.start_server()
        
    
    def getprop(self):
        print("1")
        result = {}
        
        if self.deviceId:
            output, err = self.cmdShell([self.adbExe, "-s",self.deviceId, "shell", "getprop"])
        else:
            output, err = self.cmdShell([self.adbExe, "shell", "getprop"])
            
        if not err and output:
            output_lines = output.split("\n")
            for line in output_lines:
                values = line.split(":")
                if len(values) == 2:
                    key = values[0].strip().replace("[","").replace("]", "")
                    value = values[1].strip().replace("[","").replace("]", "")
                    result[key.strip()] = value.strip()
                
        print("OUT\t{}".format(output))
        print("ERR\t{}".format(err))
        return result
    
    
    
    
    
    
    def shell(self, cmd):
        if self.deviceId:
            self.cmdShell([self.adbExe, "-s",self.deviceId,"shell", ' '.join(cmd)])
        else:
            self.cmdShell([self.adbExe,"shell", ' '.join(cmd)])
            
    
    def uninstall_all_user_apps(self):
        #pm list packages -3 | cut -d':' -f2 | tr '\r' ' ' | xargs -r -n1 -t adb uninstall
        if self.deviceId:
            self.cmdShell([self.adbExe, "-s",self.deviceId, "shell", "pm", "list", "packages", "-3", "|", "cut", "-d':'", "-f2", "|", "tr", "'\r'","' '", "|", "xargs", "-r", "-n1", "-t", self.adbExe, "uninstall"])
        else:
            self.cmdShell([self.adbExe, "shell", "pm", "list", "packages", "-3", "|", "cut", "-d':'", "-f2", "|", "tr", "'\r'","' '", "|", "xargs", "-r", "-n1", "-t", self.adbExe, "uninstall"])
            
        
    
    def reboot(self):
        if self.deviceId:
            self.cmdShell([self.adbExe, "-s",self.deviceId, "reboot"])
        else:
            self.cmdShell([self.adbExe, "reboot"])
            
        
    
    def pull(self, remote, local):
        if self.deviceId:
            self.cmdShell([self.adbExe, "-s",self.deviceId, "pull", remote, local])
        else:
            self.cmdShell([self.adbExe, "pull", remote, local])
            
        
    def push(self, local, remote):
        if self.deviceId:
            self.cmdShell([self.adbExe, "-s",self.deviceId, "push", local, remote])
        else:
            self.cmdShell([self.adbExe, "push", local, remote])
    
    
    def version(self):
        return self.cmdShell([self.adbExe,"version"])
    
    def screencap(self, filename):
        if self.deviceId:
            self.cmdShell([self.adbExe,"-s",self.deviceId,"shell", "screencap", filename])
        else:
            self.cmdShell([self.adbExe,"shell","screencap", filename])
            
    def install(self, apkFilepath):
        if self.deviceId:
            self.cmdShell([self.adbExe,"-s",self.deviceId, "install","-r","-d", apkFilepath])
        else:
            self.cmdShell([self.adbExe,"install","-r","-d", apkFilepath])
            
    def uidump(self, filename=None):
        if self.deviceId:
            if filename:
                self.cmdShell([self.adbExe,"-s",self.deviceId,"shell", "uiautomator", "dump", filename])
            else:
                self.cmdShell([self.adbExe,"-s",self.deviceId,"shell", "uiautomator", "dump"])
        else:
            if filename:
                self.cmdShell([self.adbExe,"shell", "uiautomator", "dump", filename])
            else:
                self.cmdShell([self.adbExe,"shell", "uiautomator", "dump"])
            
            
    def get_screencap(self, filepath):
        i = datetime.now()
        temp_filename = '/sdcard/'+ i.strftime('%Y_%m_%d_%H_%M_%S'+'_screenshot.png')
        self.screencap(temp_filename)
        #time.sleep(3)
        self.pull(temp_filename, filepath)
        
                
            
    def get_logs(self, filepath):
        raise NotImplemented
        i = datetime.now()
        temp_filename = '/sdcard/'+ i.strftime('%Y_%m_%d_%H_%M_%S'+'_logs.png')
        self.screencap(temp_filename)
        #time.sleep(3)
        self.pull(temp_filename, filepath)
        
                
            
    def get_uidump(self, filepath):
        i = datetime.now()
        temp_filename = '/sdcard/'+ i.strftime('%Y_%m_%d_%H_%M_%S'+'_view.xml')
        self.uidump(temp_filename)
        #time.sleep(3)
        self.pull(temp_filename, filepath)
        
    def _refresh_dump(self):
        device_adb_id = "device_adb_id"
        if self.deviceId:
            device_adb_id = self.deviceId
            
        localDumpFilePath = self.tempDataDir+"/localDumpFile_"+device_adb_id+"_"+str(os.getpid())+".xml"
        deviceDumpFilePath = "/sdcard/uidump_"+device_adb_id+"_"+str(os.getpid())+".xml"
        self.uidump(deviceDumpFilePath)
        self.pull(deviceDumpFilePath, localDumpFilePath)
        uiDumpString = open(localDumpFilePath, "r").read()
        Cache.previousUIDumpText = Cache.currentUIDumpText
        Cache.currentUIDumpText = uiDumpString
        
        
    def click(self, x,y,refreshDump=False):
        if self.deviceId:
            self.cmdShell([self.adbExe, "-s", self.deviceId, "shell", "input", "tap", str(x),str(y)])
        else:
            self.cmdShell([self.adbExe, "shell", "input", "tap", str(x),str(y)])
        
        if refreshDump:
            self._refresh_dump()
            
        
    def long_press(self, x,y,time_in_seconds=2, refreshDump=False):
        #adb shell input touchscreen swipe 170 187 170 187 2000
        if self.deviceId:
            self.cmdShell([self.adbExe, "-s", self.deviceId, "shell", "input", "touchscreen", "swipe", str(x),str(y), str(x),str(y), str(time_in_seconds*1000)])
        else:
            self.cmdShell([self.adbExe, "shell", "input", "touchscreen", "swipe", str(x),str(y), str(x),str(y), str(time_in_seconds*1000)])
        
        if refreshDump:
            self._refresh_dump()
            
        
    def swipe(self, x1, y1, x2, y2, refreshDump=False):
        #print 'swipe',x1, y1, x2, y2
        if self.deviceId:
            self.cmdShell([self.adbExe, "-s", self.deviceId, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2)])
        else:
            self.cmdShell([self.adbExe, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2)])
            
        
        if refreshDump:
            self._refresh_dump()
        
    
    
    def inputText(self, text):
        text = self.escapeTextInput(text)
        print('excaped text is ',text)
        if self.deviceId:
            self.cmdShell([self.adbExe, "-s", self.deviceId, "shell", "input", "text", text])
        else:
            self.cmdShell([self.adbExe, "shell", "input", "text", text])
    
    def back(self, refreshDump=False):
        if self.deviceId:
            self.cmdShell([self.adbExe, "-s", self.deviceId, "shell", "input", "keyevent", "4"])
        else:
            self.cmdShell([self.adbExe, "shell", "input", "keyevent", "4"])
            
        
        if refreshDump:
            self._refresh_dump()
        

    def home(self, refreshDump=False):
        if self.deviceId:
            self.cmdShell([self.adbExe, "-s", self.deviceId, "shell", "input", "keyevent", "3"])
        else:
            self.cmdShell([self.adbExe, "shell", "input", "keyevent", "3"])
            
        
        if refreshDump:
            self._refresh_dump()
            
        
    def screensize(self):
        out = False
        if self.deviceId:
            out, err = self.cmdShell([self.adbExe, "-s", self.deviceId, "shell", "wm", "size"])
        else:
            out, err = self.cmdShell([self.adbExe, "shell", "wm", "size"])
        if out:
            #Physical size: 1080x1920
            valueString = out.strip().split(":")[1].strip().split('x')
            if len(valueString) == 2:
                return {'width':int(valueString[0]), 'height':int(valueString[1])}
        return False
            
    
    def startApp(self, packageAndActivity,refreshDump=False):
        if self.deviceId:
            self.cmdShell([self.adbExe, "-s", self.deviceId, "shell","am", "start", "-n", packageAndActivity])
        else:
            self.cmdShell([self.adbExe, "shell", "am", "start", "-n", packageAndActivity])
        
        
        if refreshDump:
            self._refresh_dump()
            
            
    def escapeTextInput(self, inputText):
        inputText = inputText.replace('%','\%')
        inputText = inputText.replace(' ','%s')
        inputText = inputText.replace('"','\"')
        inputText = inputText.replace('(','\(')
        inputText = inputText.replace(')','\)')
        inputText = inputText.replace('&','\&')
        inputText = inputText.replace('<','\<')
        inputText = inputText.replace('>','\>')
        inputText = inputText.replace("'","\'")
        inputText = inputText.replace(';','\;')
        inputText = inputText.replace('*','\*')
        inputText = inputText.replace('|','\|')
        inputText = inputText.replace('~','\~')
        inputText = inputText.replace('`','\`')
        return inputText
    
    

class Element(object):
    
    """
    A class used to represent Android Devices and Any Specific View on the Screen

    ...

    Attributes
    ----------
    xmlString : str
        a string containing xml dump of the screen view elements.
    parent: Element
        an Element object represents parent of the current view element. 
    adbExe : str
        a string containing full path for adb executable utility.
    deviceId : str
        android device id, which we get using adb devices command. it represents android device uniquely
    tempDataDir : str
        a string representing the full path for the folder which can be used by pydroid to store temp files
    resultDir : str
        a string representing the full path for the folder which can be used by pydroid to store result files
    resultFilePath : str
        a string representing the full path for the file which contains the result logs

    Methods
    -------
        
    configureEnglishQwertyLowerKeys(refreshDump=True)
        Function to configure the keyboard elements of the current screen and put their values in keyboard dictionary
        
        
    explicitWait(seconds)
        Function to halt execution of test script by the number of seconds
        
        
    readEnglishQwertyLowerKeys(refreshDump=True)
        Function to configure keyboard elements of current screen used internally by configureEnglishLowerKeys() Function
        
        
    click(refreshDump=False)
        Function to click on current element
    
    long_press(refreshDump=False)
        Function to long press on current element
    
    refresh()
        Function to refresh current screen elements of android device in current object.
    
    typeTextByKeyboard(text)
        Function to type a text on selected element using onscreen keyboard
        
        
    swipe(direction="RIGHT")
        Function to swipe on screen of android device. LEFT,RIGHT,UP,DOWN
        
    getParent()
        Function to return parent element of current object
    
    inputText(text)
        Function to input text string in selected view element on android device
        
    getText()
        Function to return the text of current selected element of android device
    
    home()
        Function to press home key on android device.
        
    back()
        Function to press back key on android device.
    
    
    getChild(value=0, attr=None)
        Function to return view element which is child of current object.
    
    
    getChildren(value=0, attr=None)
        Function to return view elements as list which are child of current object as per criteria
        
    
    getNode(value=0, attr=None)
        Function to return view element from whole current screen of android device
        
    
    getNodes(value=0, attr=None)
        Function to return view elements as list from whole current screen which matches given attr as argument.
        
    
    """
    
    def __init__(self, xmlString=None, parent=None, deviceId=None, adbExe="adb", tempDataDir=None, resultDir=None, resultFilePath=None):

        '''
        Constructor
        '''
        self.homeDir = str(Path.home())
        if not tempDataDir:
            self.tempDataDir = self.homeDir+"/temp"
        else:
            self.tempDataDir = tempDataDir
        if not resultDir:
            self.resultDir = self.homeDir+"/result"
        else:
            self.resultDir = resultDir
            
        if not resultFilePath:
            self.resultFilePath = self.resultDir+"/result.txt"
        else:
            self.resultFilePath = resultFilePath
        
        if not os.path.exists(self.tempDataDir):
            os.mkdir(self.tempDataDir)
        if not os.path.exists(self.resultDir):
            os.mkdir(self.resultDir)
            
        self.keyboards = {}
        self.keyboards['en_qwerty_lower'] = {}
        self.keyboards['en_qwerty_upper'] = {}
        self.keyboards['en_qwerty_number'] = {}
        self.keyboards['en_qwerty_symbols'] = {}
        self.keyboards['en_date'] = {}
        self.keyboards['en_datetime'] = {}
        self.keyboards['en_time'] = {}
        self.keyboards['en_number'] = {}
        self.keyboards['en_number_password'] = {}
        
        self.keyboards['en_email_lower'] = {}
        self.keyboards['en_email_upper'] = {}
        self.keyboards['en_email_number'] = {}
        self.keyboards['en_email_symbols'] = {}
        
        self.keyboards['en_phone_number'] = {}
        self.keyboards['en_phone_symbols'] = {}
        
        
        self.deviceId = deviceId
        self.adb = Adb(adbExe=adbExe, deviceId=deviceId)
        
        if not xmlString:
            self._refresh_dump()
            
            
        root = ET.fromstring(Cache.currentUIDumpText)
        if root.tag == "hierarchy":
            root = root.find("node")
        
        if root.tag == "node":
            self.scrollable = root.get("scrollable")
            self.text = root.get("text")
            self.long_clickable = root.get("long-clickable")
            self.focused = root.get("focused")
            self.checkable = root.get("checkable")
            self.clickable = root.get("clickable")
            self.password = root.get("password")
            self.tag = root.get("class")
            self.index = root.get("index")
            self.checked = root.get("checked")
            self.package = root.get("package")
            self.selected = root.get("selected")
            self.enabled = root.get("enabled")
            self.bounds = root.get("bounds")
            self.content_desc = root.get("content-desc")
            self.resource_id = root.get("resource-id")
            self.focusable = root.get("focusable")
            self.bounds = self.bounds[1:-1].replace("][",",").split(",")
            self.bounds = list(map(int, self.bounds))
            
            self.totalChildren = len(root)
            self.xmlString = xmlString
            self.xmlNode = root
            self.parentElement = parent
            
    
    def _refresh_dump(self):
        device_adb_id = "device_adb_id"
        if self.deviceId:
            device_adb_id = self.deviceId
            
        localDumpFilePath = self.tempDataDir+"/localDumpFile_"+device_adb_id+"_"+str(os.getpid())+".xml"
        deviceDumpFilePath = "/sdcard/uidump_"+device_adb_id+"_"+str(os.getpid())+".xml"
        self.adb.uidump(deviceDumpFilePath)
        self.adb.pull(deviceDumpFilePath, localDumpFilePath)
        xmlString = open(localDumpFilePath, "r").read()
        Cache.currentUIDumpText = xmlString
        
        
    def __reInit(self, xmlString=None, parent=None, deviceId=None, adbExe="adb"):
        '''
        Constructor
        '''
        self.deviceId = deviceId
        self.adb = Adb(adbExe, deviceId)
        if not xmlString:
            self._refresh_dump()
            
            
        root = ET.fromstring(Cache.currentUIDumpText)
        if root.tag == "hierarchy":
            root = root.find("node")
        
        if root.tag == "node":
            self.scrollable = root.get("scrollable")
            self.text = root.get("text")
            self.long_clickable = root.get("long-clickable")
            self.focused = root.get("focused")
            self.checkable = root.get("checkable")
            self.clickable = root.get("clickable")
            self.password = root.get("password")
            self.tag = root.get("class")
            self.index = root.get("index")
            self.checked = root.get("checked")
            self.package = root.get("package")
            self.selected = root.get("selected")
            self.enabled = root.get("enabled")
            self.bounds = root.get("bounds")
            self.content_desc = root.get("content-desc")
            self.resource_id = root.get("resource-id")
            self.focusable = root.get("focusable")
            self.bounds = self.bounds[1:-1].replace("][",",").split(",")
            self.bounds = list(map(int, self.bounds))
            
            self.totalChildren = len(root)
            self.xmlString = xmlString
            self.xmlNode = root
            self.parentElement = parent
            
        
    def configureEnglishQwertyLowerKeys(self, refreshDump=True):
        self.adb.startApp('indus.com.kbTest/.MainActivity', refreshDump=refreshDump)
        if Cache.currentUIDumpText != Cache.previousUIDumpText:
            self.__reInit(Cache.currentUIDumpText, deviceId=self.deviceId, adbExe=self.adb.adbExe)
        
        sleep(1.5)
        indusKeyBoardOptionElement = self.getNode('Indus', 'text').click(refreshDump=True)
    
        sleep(4.5)
        contentViewElement = indusKeyBoardOptionElement.getNode('android:id/content')
        print(contentViewElement.bounds)
        print(contentViewElement.xmlString)

        self.effectiveScreensize = {'width':indusKeyBoardOptionElement.bounds[2],'height':indusKeyBoardOptionElement.bounds[3]}
        
        keyboardX = 0
        keyboardY = contentViewElement.bounds[3]
        keyboardWidth = self.effectiveScreensize['width']
        keyboardHeight = self.effectiveScreensize['height']-keyboardY
        keyboard = {}
        keyboard['cordinates'] = (keyboardX, keyboardY, keyboardX+keyboardWidth, keyboardY+keyboardHeight)
        keyboard['location'] = {'x':keyboardX, 'y':keyboardY}
        keyboard['size'] = {'height':keyboardHeight, 'width':keyboardWidth}
        print(keyboard)
        
        keys = {}
        qweRow = 'qwertyuiop'
        asdRow = 'asdfghjkl'
        zxcRow = 'zxcvbnm'
        # case : textCaseChangeKey, backspace : Backspace Key, symbols: Symbols Key, regional: regional key, space: spacebar
        keyHeight = keyboard['size']['height']/5
        keyWidth = keyboard['size']['width']/len(qweRow)
        for i in range(len(qweRow)):
            ch = qweRow[i]
            x = keyboard['location']['x']+(i*keyWidth)
            y = keyboard['location']['y']+keyHeight
            width = keyWidth
            height = keyHeight
            keys[ch] = {'x':x, 'y':y, 'height':height, 'width':width}
             
             
        for i in range(len(asdRow[1:-1])):
            ch = asdRow[i+1]
            x = keyboard['location']['x']+(keyWidth*1.5)+(i*keyWidth)
            y = keyboard['location']['y']+(keyHeight*2)
            width = keyWidth
            height = keyHeight
            keys[ch] = {'x':x, 'y':y, 'height':height, 'width':width}
             
        keys[asdRow[0]] = {'x':keyboard['location']['x'], 'y':keyboard['location']['y']+(keyHeight*2), 'height':keyHeight, 'width':(keyWidth*1.5)}
        keys[asdRow[-1]] = {'x':keys[asdRow[-2]]['x']+keys[asdRow[-2]]['width'], 'y':keyboard['location']['y']+(keyHeight*2), 'height':keyHeight, 'width':(keyWidth*1.5)}
        
             
        for i in range(len(asdRow[1:-1])):
            ch = asdRow[i+1]
            zxcCh = zxcRow[i]
            keys[zxcCh] = {'x':keys[ch]['x'], 'y':keys[ch]['y']+keyHeight, 'height':keyHeight, 'width':keyWidth}
            
        keys['case'] = {'x':keys[asdRow[0]]['x'], 'y':keys[asdRow[0]]['y']+keyHeight, 'height':keyHeight, 'width':(keyWidth*1.5)}
        keys['backspace'] = {'x':keys[asdRow[-1]]['x'], 'y':keys[asdRow[-1]]['y']+keyHeight, 'height':keyHeight, 'width':(keyWidth*1.5)}
        
        # bottom row
        
        keys['symbol'] = {'x':keys[asdRow[0]]['x'], 'y':keys[asdRow[0]]['y']+(keyHeight*2), 'height':keyHeight, 'width':(keyWidth*1.5)}
        keys['regional'] = {'x':keys[asdRow[1]]['x'], 'y':keys[asdRow[1]]['y']+(keyHeight*2), 'height':keyHeight, 'width':keyWidth}
        keys['.'] = {'x':keys[asdRow[-3]]['x'], 'y':keys[asdRow[-3]]['y']+(keyHeight*2), 'height':keyHeight, 'width':keyWidth}
        keys[','] = {'x':keys[asdRow[-2]]['x'], 'y':keys[asdRow[-2]]['y']+(keyHeight*2), 'height':keyHeight, 'width':keyWidth}
        keys['enter'] = {'x':keys[asdRow[-1]]['x'], 'y':keys[asdRow[-1]]['y']+(keyHeight*2), 'height':keyHeight, 'width':(keyWidth*1.5)}
        
        keys['spacebar'] = {'x':(keyWidth*2.5), 'y':keys['enter']['y'], 'height':keyHeight, 'width':(keyWidth*6)}
        self.keyboards['en_qwerty_lower'] = keys
        
        print(keys)
        
        
    def explicitWait(self, seconds):
        import time
        print('Explicit Wait ['+str(seconds)+' seconds].',end="")
        for i in range(seconds):
            sleep(1)
            print ('.',end="")
        print('.')
        
        
    def readEnglishQwertyLowerKeys(self, refreshDump=True):
        contentViewElement = self.getNode('android:id/content')
        print(contentViewElement.bounds)
        print(contentViewElement.xmlString)

        self.effectiveScreensize = {'width':self.bounds[2],'height':self.bounds[3]}
        
        keyboardX = 0
        keyboardY = contentViewElement.bounds[3]
        keyboardWidth = self.effectiveScreensize['width']
        keyboardHeight = self.effectiveScreensize['height']-keyboardY
        keyboard = {}
        keyboard['cordinates'] = (keyboardX, keyboardY, keyboardX+keyboardWidth, keyboardY+keyboardHeight)
        keyboard['location'] = {'x':keyboardX, 'y':keyboardY}
        keyboard['size'] = {'height':keyboardHeight, 'width':keyboardWidth}
        print(keyboard)
        
        keys = {}
        qweRow = 'qwertyuiop'
        asdRow = 'asdfghjkl'
        zxcRow = 'zxcvbnm'
        # case : textCaseChangeKey, backspace : Backspace Key, symbols: Symbols Key, regional: regional key, space: spacebar
        keyHeight = keyboard['size']['height']/5
        keyWidth = keyboard['size']['width']/len(qweRow)
        for i in range(len(qweRow)):
            ch = qweRow[i]
            x = keyboard['location']['x']+(i*keyWidth)
            y = keyboard['location']['y']+keyHeight
            width = keyWidth
            height = keyHeight
            keys[ch] = {'x':x, 'y':y, 'height':height, 'width':width}
             
             
        for i in range(len(asdRow[1:-1])):
            ch = asdRow[i+1]
            x = keyboard['location']['x']+(keyWidth*1.5)+(i*keyWidth)
            y = keyboard['location']['y']+(keyHeight*2)
            width = keyWidth
            height = keyHeight
            keys[ch] = {'x':x, 'y':y, 'height':height, 'width':width}
             
        keys[asdRow[0]] = {'x':keyboard['location']['x'], 'y':keyboard['location']['y']+(keyHeight*2), 'height':keyHeight, 'width':(keyWidth*1.5)}
        keys[asdRow[-1]] = {'x':keys[asdRow[-2]]['x']+keys[asdRow[-2]]['width'], 'y':keyboard['location']['y']+(keyHeight*2), 'height':keyHeight, 'width':(keyWidth*1.5)}
        
             
        for i in range(len(asdRow[1:-1])):
            ch = asdRow[i+1]
            zxcCh = zxcRow[i]
            keys[zxcCh] = {'x':keys[ch]['x'], 'y':keys[ch]['y']+keyHeight, 'height':keyHeight, 'width':keyWidth}
            
        keys['case'] = {'x':keys[asdRow[0]]['x'], 'y':keys[asdRow[0]]['y']+keyHeight, 'height':keyHeight, 'width':(keyWidth*1.5)}
        keys['backspace'] = {'x':keys[asdRow[-1]]['x'], 'y':keys[asdRow[-1]]['y']+keyHeight, 'height':keyHeight, 'width':(keyWidth*1.5)}
        
        # bottom row
        
        keys['symbol'] = {'x':keys[asdRow[0]]['x'], 'y':keys[asdRow[0]]['y']+(keyHeight*2), 'height':keyHeight, 'width':(keyWidth*1.5)}
        keys['regional'] = {'x':keys[asdRow[1]]['x'], 'y':keys[asdRow[1]]['y']+(keyHeight*2), 'height':keyHeight, 'width':keyWidth}
        keys['.'] = {'x':keys[asdRow[-3]]['x'], 'y':keys[asdRow[-3]]['y']+(keyHeight*2), 'height':keyHeight, 'width':keyWidth}
        keys[','] = {'x':keys[asdRow[-2]]['x'], 'y':keys[asdRow[-2]]['y']+(keyHeight*2), 'height':keyHeight, 'width':keyWidth}
        keys['enter'] = {'x':keys[asdRow[-1]]['x'], 'y':keys[asdRow[-1]]['y']+(keyHeight*2), 'height':keyHeight, 'width':(keyWidth*1.5)}
        
        keys['spacebar'] = {'x':(keyWidth*2.5), 'y':keys['enter']['y'], 'height':keyHeight, 'width':(keyWidth*6)}
        self.keyboards['en_qwerty_lower'] = keys
        
        print(keys)
        
        
    def click(self, refreshDump=False):
        self.adb.click((self.bounds[0]+self.bounds[2])/2, (self.bounds[1]+self.bounds[3])/2, refreshDump=refreshDump)
        if Cache.currentUIDumpText != Cache.previousUIDumpText:
            self.__reInit(Cache.currentUIDumpText, deviceId=self.deviceId, adbExe=self.adb.adbExe)
        return self
    
    def long_press(self, refreshDump=False):
        self.adb.long_press((self.bounds[0]+self.bounds[2])/2, (self.bounds[1]+self.bounds[3])/2, refreshDump=refreshDump)
        if Cache.currentUIDumpText != Cache.previousUIDumpText:
            self.__reInit(Cache.currentUIDumpText, deviceId=self.deviceId, adbExe=self.adb.adbExe)
        return self
    
    def refresh(self):
        Cache.previousUIDumpText = Cache.currentUIDumpText
        self.__reInit(deviceId=self.deviceId, adbExe=self.adb.adbExe)
        return self
    
    def typeTextByKeyboard(self, text):
        for ch in text:
            key = 'spacebar'
            if ch.lower() in self.keyboards['en_qwerty_lower']:
                key = ch.lower()
            elif ch == ' ':
                key = 'spacebar'
            elif ch == "\n":
                key = 'enter'
            else:
                print('No Cordinates Found for : ', ch)
            
            if ch.istitle():
                print("KeyPress: Case")
                self.adb.click(self.keyboards['en_qwerty_lower']['case']['x']+(self.keyboards['en_qwerty_lower']['case']['width']/2), self.keyboards['en_qwerty_lower']['case']['y']+(self.keyboards['en_qwerty_lower']['case']['height']/2))
                
            
            print("KeyPress: ",key)
            self.adb.click(self.keyboards['en_qwerty_lower'][key]['x']+(self.keyboards['en_qwerty_lower'][key]['width']/2), self.keyboards['en_qwerty_lower'][key]['y']+(self.keyboards['en_qwerty_lower'][key]['height']/2))
    
        
        
    def swipe(self, direction="RIGHT"):
        if direction == "RIGHT":
            y = self.bounds[1]+((self.bounds[3]-self.bounds[1])/2)
            padding = (self.bounds[2]-self.bounds[0])/8
            self.adb.swipe(self.bounds[2]-padding, y, self.bounds[0]+padding, y)
        elif direction == "LEFT":
            y = self.bounds[1]+((self.bounds[3]-self.bounds[1])/2)
            padding = (self.bounds[2]-self.bounds[0])/8
            self.adb.swipe(self.bounds[0]+padding, y, self.bounds[2]-padding, y)
        elif direction == "UP":
            x = self.bounds[0]+((self.bounds[2]-self.bounds[0])/2)
            padding = (self.bounds[3]-self.bounds[1])/8
            self.adb.swipe(x, self.bounds[3]-padding, x, self.bounds[1]+padding)
        elif direction == "DOWN":
            x = self.bounds[0]+((self.bounds[2]-self.bounds[0])/2)
            padding = (self.bounds[3]-self.bounds[1])/8
            self.adb.swipe(x, self.bounds[1]+padding, x, self.bounds[3]-padding)
            
        if Cache.currentUIDumpText != Cache.previousUIDumpText:
            self.__reInit(Cache.currentUIDumpText, deviceId=self.deviceId, adbExe=self.adb.adbExe)
            
        
    def getParent(self):
        return self.parentElement
    
    def inputText(self, text):
        self.adb.inputText(text)
        
    def getText(self):
        return self.text
    
    def home(self):
        self.adb.home()
        if Cache.currentUIDumpText != Cache.previousUIDumpText:
            self.__reInit(Cache.currentUIDumpText, deviceId=self.deviceId, adbExe=self.adb.adbExe)
        
    def back(self):
        self.adb.back()
        if Cache.currentUIDumpText != Cache.previousUIDumpText:
            self.__reInit(Cache.currentUIDumpText, deviceId=self.deviceId, adbExe=self.adb.adbExe)
    
    
    def getChild(self, value=0, attr=None):
        if not attr:
            attr = "resource-id"
        print("CHILD\t"+attr+" "+value)
        if attr == "xpath":
            if not value.startswith("."):
                value = "."+value
            xmlNodes = self.xmlNode.findall(value)
            if len(xmlNodes) > 0:
                element = Element(ET.tostring(xmlNodes[0]), deviceId=self.deviceId)
                return element
            else:
                return None
            
        xmlNodes = self.xmlNode.findall("node")
        for xmlNode in xmlNodes:
            if xmlNode.get(attr) == value:
                element = Element(ET.tostring(xmlNode), deviceId=self.deviceId)
                return element
        
        return None
    
    
    def getChildren(self, value=0, attr=None):
        if not attr:
            attr = "resource-id"
        print("CHILDREN\t"+attr+" "+value)
        elements = []
        if attr == "xpath":
            if not value.startswith("."):
                value = "."+value
            xmlNodes = self.xmlNode.findall(value)
        else:
            xmlNodes = self.xmlNode.findall("node")
        for xmlNode in xmlNodes:
            if xmlNode.get(attr) == value:
                element = Element(ET.tostring(xmlNode), deviceId=self.deviceId)
                elements.append(element)
        return elements
    
    def getNode(self, value=0, attr=None):
        if not attr:
            attr = "resource-id"
        print("NODE\t"+attr+" "+value)
        if attr == "xpath":
            if not value.startswith("."):
                value = "."+value
            xmlNodes = self.xmlNode.findall(value)
            if len(xmlNodes) > 0:
                element = Element(ET.tostring(xmlNodes[0]), deviceId=self.deviceId)
                return element
            else:
                return None
            
        xmlNodes = self.xmlNode.iter("node")
        for xmlNode in xmlNodes:
            #print xmlNode.get(attr)
            if xmlNode.get(attr) == value:
                element = Element(ET.tostring(xmlNode), deviceId=self.deviceId)
                return element
        
        return None
    
    def getNodes(self, value=0, attr=None):
        if not attr:
            attr = "resource-id"
        print("NODES\t"+attr+" "+value)
        elements = []
        if attr == "xpath":
            if not value.startswith("."):
                value = "."+value
            xmlNodes = self.xmlNode.findall(value)
            for xmlNode in xmlNodes:
                element = Element(ET.tostring(xmlNode), deviceId=self.deviceId)
                elements.append(element)
            return elements
        else:
            xmlNodes = self.xmlNode.iter("node")
            
        for xmlNode in xmlNodes:
            if xmlNode.get(attr) == value:
                element = Element(ET.tostring(xmlNode), deviceId=self.deviceId)
                elements.append(element)
        return elements
    
        
class Screen(object):
    
    def __init__(self, driver=None):
        print("Screen Object")
        self.driver = driver
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

def Struct(*args, **kwargs):
    def init(self, *iargs, **ikwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        for i in range(len(iargs)):
            setattr(self, args[i], iargs[i])
        for k, v in ikwargs.items():
            setattr(self, k, v)

    name = kwargs.pop("name", "MyStruct")
    kwargs.update(dict((k, None) for k in args))
    return type(name, (object,), {'__init__': init, '__slots__': kwargs.keys()})        
