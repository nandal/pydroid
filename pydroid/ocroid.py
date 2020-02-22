'''
Created on Jan 15, 2018

@author: nandal-pc
'''

from datetime import datetime
import os


tesseractExePath = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
adbExePath = "D:\\android\\sdk-tools-windows-3859397\\platform-tools\\adb.exe"

suggestionTextColor = (107,119,124, 255)
keyboardTextColor = (55,71,79,255)
black = (0,0,0,255)
white = (255,255,255,255)

class Ocroid(object):
    
    def __init__(self, tesseractExe=None, adb=None, dataDir="ocroid_data"):
        self.tesseractExe = tesseractExe
        self.adb = adb
        self.dataDir = dataDir
        
        self.suggestionsOcrScreenshot = None
        self.suggestionsRowOcrScreenshot = None

        self.keyboardsOcrScreenshot = None
        self.keyboardsRowOneOcrScreenshot = None
        self.keyboardsRowTwoOcrScreenshot = None
        self.keyboardsRowThreeOcrScreenshot = None
        self.keyboardsRowFourOcrScreenshot = None
        
        if self.adb.deviceId:
            self.resultFile = self.dataDir+"/result_"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+"_"+self.adb.deviceId+"_.txt";
        else:
            self.resultFile = self.dataDir+"/result_"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+"_.txt";
            
        self.keys = {}
        self.suggestions = {}
        
        os.environ['TESSDATA_PREFIX'] = 'C:\\Program Files (x86)\\Tesseract-OCR\\tessdata'
        print("OCR Class Initialized.")
        
    def colorRangeCompare(self, colorOne, colorTwo, freedom=None):
        if freedom:
            for i in range(3):
                if colorOne[i] < colorTwo[i]+freedom and colorOne[i] > colorTwo[i]-freedom:
                    pass
                else:
                    return False
        else:
            for i in range(3):
                if colorOne[i] == colorTwo[i]:
                    pass
                else:
                    return False
        return True
    
    def cleanDir(self):
        import os, shutil
        folder = self.androidTempDir
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        
        folder = self.ocrTempDir
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        
    def getScreenshot(self):
        self.mobileScreenshotFilepath = "sdcard/screenshot.png"
        self.localScreenshotFilepath = self.androidTempDir+"/screenshot.png"
        self.adb.screencap(self.mobileScreenshotFilepath)
        self.adb.pull(self.mobileScreenshotFilepath, self.localScreenshotFilepath)
        print("Screenshot is Collected from Device")
        
    def processScreenShotSuggestions(self, screenShotFilePath):
        from PIL import Image
        suggestionFound = False
        # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
        #img = Image.new( 'RGB', (100,250), "black") # create a new black image
        suggestionY1 = 770
        suggestionY2 = 820
        img = Image.open(screenShotFilePath)
        self.screensize = img.size
        img = img.crop((0, suggestionY1, self.screensize[0], suggestionY2))
       
        pixels = img.load() # create the pixel map
        
        
        for row in range(img.size[1]-1, -1, -1):
            for col in range(img.size[0]):
                #print pixels[col, row]
                if self.colorRangeCompare(pixels[col, row], suggestionTextColor):
                    pixels[col, row] = black
                    suggestionFound = True
                else:
                    pixels[col, row] = white
  
        
        sug_row_width = suggestionY2 - suggestionY1

        if sug_row_width < 0 :
            import sys
            sys.exit()
        
        self.sug_row_height = sug_row_width
        
        self.suggestionsRowY = suggestionY1

        self.suggestionMinY = suggestionY1
        self.suggestionMaxY = suggestionY2
        
        self.suggestionsRowOcrScreenshot = self.ocrTempDir+"/suggestions_row.png"
        
        img.save(self.suggestionsRowOcrScreenshot,"PNG")
        
        print("Screenshot is processed for OCR - Suggestions")
        return suggestionFound
        
    
    def processScreenShotForKeyboard(self, screenShotFilePath):
        from PIL import Image
        # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
        #img = Image.new( 'RGB', (100,250), "black") # create a new black image
        keyboardY1 = 865
        keyboardY2 = 1150
        
        img = Image.open(screenShotFilePath)
        self.screensize = img.size
        
        print("Image size before crop:",img.size)
        img = img.crop((0, keyboardY1, img.size[0], keyboardY2))
        print("Image size after crop:",img.size)
        pixels = img.load() # create the pixel map
        
        for row in range(img.size[1]-1, -1, -1):
            for col in range(img.size[0]):
                if self.colorRangeCompare(pixels[col, row], keyboardTextColor, 10):
                    pixels[col, row] = black
                else:
                    pixels[col, row] = white
            

        key_row_width = (keyboardY2-keyboardY1)/3

        self.key_row_height = key_row_width
        
        self.keyboardsRowOneY = keyboardY1
        self.keyboardsRowTwoY = self.keyboardsRowOneY+key_row_width
        self.keyboardsRowThreeY = self.keyboardsRowTwoY+key_row_width
        
        self.keyboardsOcrScreenshot = self.ocrTempDir+"/keyboard_rows_"+str(self.keyboardsRowOneY)+".png"
        self.keyboardsRowOneOcrScreenshot = self.ocrTempDir+"/keyboard_row_1_"+str(self.keyboardsRowOneY)+".png"
        self.keyboardsRowTwoOcrScreenshot = self.ocrTempDir+"/keyboard_row_2_"+str(self.keyboardsRowTwoY)+".png"
        self.keyboardsRowThreeOcrScreenshot = self.ocrTempDir+"/keyboard_row_3_"+str(self.keyboardsRowThreeY)+".png"
        
        img.save(self.keyboardsOcrScreenshot,"PNG")
        img.crop((0, 0, self.screensize[0], self.key_row_height)).save(self.keyboardsRowOneOcrScreenshot,"PNG")
        img.crop((0, self.key_row_height, self.screensize[0], self.key_row_height*2)).save(self.keyboardsRowTwoOcrScreenshot,"PNG")
        img.crop((0, self.key_row_height*2, self.screensize[0], self.key_row_height*3)).save(self.keyboardsRowThreeOcrScreenshot,"PNG")
        
        print("Screenshot is processed for OCR - Keyboard")
        
    def runTesseract(self):
        self.suggestionsRowOcrText = self.ocrTempDir+"/suggestions_row"
        self.adb.cmdShell([self.tesseractExe, self.suggestionsRowOcrScreenshot, "-psm", "6", self.suggestionsRowOcrText])
        self.adb.cmdShell([self.tesseractExe, self.suggestionsRowOcrScreenshot, "-psm", "6", self.suggestionsRowOcrText, "makebox"])
        
        self.keyboardsRowOneOcrText = self.ocrTempDir+"/keyboard_row_1"
        self.keyboardsRowTwoOcrText = self.ocrTempDir+"/keyboard_row_2"
        self.keyboardsRowThreeOcrText = self.ocrTempDir+"/keyboard_row_3"
        self.keyboardsRowFourOcrText = self.ocrTempDir+"/keyboard_row_4"
        self.keyboardsRowFiveOcrText = self.ocrTempDir+"/keyboard_row_5"
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowOneOcrScreenshot, "-psm", "6", self.keyboardsRowOneOcrText])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowOneOcrScreenshot, "-psm", "6", self.keyboardsRowOneOcrText, "makebox"])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowTwoOcrScreenshot, "-psm", "6", self.keyboardsRowTwoOcrText])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowTwoOcrScreenshot, "-psm", "6", self.keyboardsRowTwoOcrText, "makebox"])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowThreeOcrScreenshot, "-psm", "6", self.keyboardsRowThreeOcrText])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowThreeOcrScreenshot, "-psm", "6", self.keyboardsRowThreeOcrText, "makebox"])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowFourOcrScreenshot, "-psm", "6", self.keyboardsRowFourOcrText])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowFourOcrScreenshot, "-psm", "6", self.keyboardsRowFourOcrText, "makebox"])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowFiveOcrScreenshot, "-psm", "6", self.keyboardsRowFiveOcrText])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowFiveOcrScreenshot, "-psm", "6", self.keyboardsRowFiveOcrText, "makebox"])
        
        print("Tesseract Run Completed")
        
        
    def runTesseractSuggestionsOnly(self):
        self.suggestionsRowOcrText = self.ocrTempDir+"/suggestions_row"
        print [self.tesseractExe, self.suggestionsRowOcrScreenshot, "-psm", "6", self.suggestionsRowOcrText]
        self.adb.cmdShell([self.tesseractExe, self.suggestionsRowOcrScreenshot, "-psm", "6", self.suggestionsRowOcrText])
        self.adb.cmdShell([self.tesseractExe, self.suggestionsRowOcrScreenshot, "-psm", "6", self.suggestionsRowOcrText, "makebox"])
        
        print("Tesseract Run - Suggestions Only")
        
        
    def runTesseractKeyboardOnly(self):
        
        self.keyboardsRowOneOcrText = self.ocrTempDir+"/keyboard_row_1"
        self.keyboardsRowTwoOcrText = self.ocrTempDir+"/keyboard_row_2"
        self.keyboardsRowThreeOcrText = self.ocrTempDir+"/keyboard_row_3"
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowOneOcrScreenshot, "-psm", "7", self.keyboardsRowOneOcrText])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowOneOcrScreenshot, "-psm", "7", self.keyboardsRowOneOcrText, "makebox"])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowTwoOcrScreenshot, "-psm", "7", self.keyboardsRowTwoOcrText])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowTwoOcrScreenshot, "-psm", "7", self.keyboardsRowTwoOcrText, "makebox"])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowThreeOcrScreenshot, "-psm", "7", self.keyboardsRowThreeOcrText])
        self.adb.cmdShell([self.tesseractExe, self.keyboardsRowThreeOcrScreenshot, "-psm", "7", self.keyboardsRowThreeOcrText, "makebox"])

        
        print("Tesseract Run - Keyboard Only")
        
    def collectKeysLowerCase(self):
        self.keys = {}
        with open(self.keyboardsRowOneOcrText+".box") as fd:
            lines = fd.readlines()
            for line in lines:
                values = line.strip().split()
                if len(values) >= 6:
                    key = values[0].strip()
                    x1 = int(values[1].strip())
                    y1 = int(values[2].strip())
                    x2 = int(values[3].strip())
                    y2 = int(values[4].strip())
                    if x1 == self.screensize[0] and x2 == self.screensize[0] and y1 == 0 and y2 == 0:
                        pass
                    else:
                        if key == '-':
                            key = 'l'
                        self.keys[key] = (x1, self.keyboardsRowOneY+y1, x2, self.keyboardsRowOneY+y2)
                        
        with open(self.keyboardsRowTwoOcrText+".box") as fd:
            lines = fd.readlines()
            for line in lines:
                values = line.strip().split()
                if len(values) >= 6:
                    key = values[0].strip()
                    x1 = int(values[1].strip())
                    y1 = int(values[2].strip())
                    x2 = int(values[3].strip())
                    y2 = int(values[4].strip())
                    if x1 == self.screensize[0] and x2 == self.screensize[0] and y1 == 0 and y2 == 0:
                        pass
                    else:
                        if key == '-':
                            key = 'l'
                        self.keys[key] = (x1, self.keyboardsRowTwoY+y1, x2, self.keyboardsRowTwoY+y2)
                        
        with open(self.keyboardsRowThreeOcrText+".box") as fd:
            lines = fd.readlines()
            for line in lines:
                values = line.strip().split()
                if len(values) >= 6:
                    key = values[0].strip()
                    x1 = int(values[1].strip())
                    y1 = int(values[2].strip())
                    x2 = int(values[3].strip())
                    y2 = int(values[4].strip())
                    if x1 == self.screensize[0] and x2 == self.screensize[0] and y1 == 0 and y2 == 0:
                        pass
                    else:
                        if key == '2':
                            key = 'z'
                        self.keys[key] = (x1, self.keyboardsRowThreeY+y1, x2, self.keyboardsRowThreeY+y2)
                        
        
                    
    def collectKeysUpperCase(self):
        self.keys = {}
        
        with open(self.keyboardsRowOneOcrText+".box") as fd:
            lines = fd.readlines()
            for line in lines:
                values = line.strip().split()
                if len(values) >= 6:
                    key = values[0].strip()
                    x1 = int(values[1].strip())
                    y1 = int(values[2].strip())
                    x2 = int(values[3].strip())
                    y2 = int(values[4].strip())
                    if x1 == self.screensize[0] and x2 == self.screensize[0] and y1 == 0 and y2 == 0:
                        pass
                    else:
                        print("Key:",key) #"Code:",key.encode('utf-8')
                        if key == '|':
                            key = 'I'
                        elif key == '�':
                            key = "Y"
                        self.keys[key] = (x1, self.keyboardsRowOneY+y1, x2, self.keyboardsRowOneY+y2)
                        
        print("Keyboard Keys are Mapped.")
        
        with open(self.keyboardsRowTwoOcrText+".box") as fd:
            lines = fd.readlines()
            for line in lines:
                values = line.strip().split()
                if len(values) >= 6:
                    key = values[0].strip()
                    x1 = int(values[1].strip())
                    y1 = int(values[2].strip())
                    x2 = int(values[3].strip())
                    y2 = int(values[4].strip())
                    if x1 == self.screensize[0] and x2 == self.screensize[0] and y1 == 0 and y2 == 0:
                        pass
                    else:
                        self.keys[key] = (x1, self.keyboardsRowTwoY+y1, x2, self.keyboardsRowTwoY+y2)
                        
        with open(self.keyboardsRowThreeOcrText+".box") as fd:
            lines = fd.readlines()
            for line in lines:
                values = line.strip().split()
                if len(values) >= 6:
                    key = values[0].strip()
                    x1 = int(values[1].strip())
                    y1 = int(values[2].strip())
                    x2 = int(values[3].strip())
                    y2 = int(values[4].strip())
                    if x1 == self.screensize[0] and x2 == self.screensize[0] and y1 == 0 and y2 == 0:
                        pass
                    else:
                        self.keys[key] = (x1, self.keyboardsRowThreeY+y1, x2, self.keyboardsRowThreeY+y2)
                        
        print("Keyboard Upper Keys are Mapped.")
        self.keysMapFilepath = self.ocrTempDir+"/keysMap.txt"
        with open(self.keysMapFilepath, "w") as fd:
            lines = []
            for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if ch in self.keys:
                    line = ch+" "+str(self.keys[ch][0])+" "+str(self.keys[ch][1])+" "+str(self.keys[ch][2])+" "+str(self.keys[ch][3])
                    lines.append(line+"\n")
            fd.writelines(lines)
            print("KeyMapping written to",self.keysMapFilepath)
            
    def loadKeyMapDictionary(self):
        self.keys = {}
        with open(self.keysMapFilepath, "r") as fd:
            lines = fd.readlines()
            for line in lines:
                values = line.strip().split()
                if len(values) >= 5:
                    key = values[0].strip()
                    x1 = int(values[1].strip())
                    y1 = int(values[2].strip())
                    x2 = int(values[3].strip())
                    y2 = int(values[4].strip())
                    self.keys[key] = (x1, y1, x2, y2)
        print("All Keys are Loaded to Dictionary.")
        
    def collectSuggestions(self):
        self.getScreenshot()
        suggestionsFound = self.processScreenShotSuggestions(self.localScreenshotFilepath)
        if not suggestionsFound:
            self.suggestions = {}
            print("Suggestions Not Found.")
            return
        
        self.runTesseractSuggestionsOnly()
        self.suggestions = {}

        suggestionsBoxList = []
        skippedIndexes = []
        with open(self.suggestionsRowOcrText+".txt", "r") as fd:
            data = fd.readlines()
            data = " ".join(data)
            suggestionsList = data.split()
            
        with open(self.suggestionsRowOcrText+".box", "r") as fd:
            lines = fd.readlines()
            lineNo = 0
            for line in lines:
                values = line.strip().split()
                if len(values) >= 6:
                    key = values[0].strip()
                    x1 = int(values[1].strip())
                    y1 = int(values[2].strip())
                    x2 = int(values[3].strip())
                    y2 = int(values[4].strip())
                    if x1 == self.screensize[0] and x2 == self.screensize[0] and y1 == 0 and y2 == 0:
                        suggestionsBoxList.append([False, key, 0, 0, 0, 0])
                        skippedIndexes.append(lineNo)
                    else:
                        suggestionsBoxList.append([True, key, x1, self.suggestionsRowY+y1, x2, self.suggestionsRowY+y2])
                lineNo += 1
        suggestionsString = " ".join(suggestionsList)
        print("Suggestions:",suggestionsString)
        
        
        lineNo = 0
        for word in suggestionsList:
            if len(word) > 0:
                processedWord = ""
                processedWordMap = []
                for ch in word:
                    if lineNo < len(suggestionsBoxList) and suggestionsBoxList[lineNo][0] and ch == suggestionsBoxList[lineNo][1]:
                        processedWord += ch
                        processedWordMap.append(suggestionsBoxList[lineNo])
                    lineNo += 1
                if len(processedWord) > 0:
                    key = processedWord.strip()
                    x1 = int(processedWordMap[0][2])
                    x2 = int(processedWordMap[-1][4])
                    y1 = int(processedWordMap[0][3])
                    y2 = int(processedWordMap[-1][5])
                    self.suggestions[key] = (x1, y1, x2, y2)

        print("Suggestions Coordinates are collected:",self.suggestions)
        
        
    def saveScreen(self):
        import sys
        from datetime import datetime
        from PIL import Image, ImageDraw
        im = Image.open(self.localScreenshotFilepath)
        draw = ImageDraw.Draw(im)
        for key in self.suggestions.keys():
            x1 = self.suggestions[key][0]
            y1 = self.suggestionsRowY
            x2 = self.suggestions[key][2]
            y2 = self.suggestionsRowY+self.sug_row_height
            draw.rectangle((x1, y1, x2, y2), outline=128)
            
        x1 = 0
        y1 = self.suggestionMinY
        x2 = self.screensize[0]
        y2 = self.suggestionMaxY
        draw.rectangle((x1,y1,x2,y2), outline="red")
        del draw
        # write to stdout
        im.save(self.androidTempDir+"/"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+".png", "PNG")
                    
        
    def markScreen(self, x, y):
        import sys
        from PIL import Image, ImageDraw
        im = Image.open(self.localScreenshotFilepath)
        draw = ImageDraw.Draw(im)
        r = 5
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(255,0,0,255))
        del draw
        # write to stdout
        im.save(self.androidTempDir+"/"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+"_clicked.png", "PNG")
        


if __name__ == '__main__':
    pass