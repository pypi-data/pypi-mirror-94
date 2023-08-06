import string
import pyttsx3
import speech_recognition as sr
import pyautogui
import time
import os
def ParseList(array):
    if type(array) != list:
        raise Exception(f"The parameter passed should be list not {type(array)}")
    newArray = []
    for i in range (len(array)):
        realWord = array[i].split("\n")[0]
        newArray.append(realWord)
    return newArray
def reverse(string):
    if type(string) != str:
        string = int(string)

    i = len(string)
    newString = ""
    for i in range(len(string)-1, -1, -1):
        newString+=string[i]
    return newString   
def allPossibleKeys():
    lowercase = list(string.ascii_lowercase)
    uppercase = list(string.ascii_uppercase)
    digits = list(string.digits)
    punc = list(string.punctuation)

    listFinal = []
    listFinal.extend(lowercase)
    listFinal.extend(uppercase)
    listFinal.extend(digits)
    listFinal.extend(punc)
    listFinal.append(f" ")
    return listFinal
def speak(audio, rate):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty("rate", rate)
    engine.say(audio)
    engine.runAndWait()

def listen(err="Sorry we could not listen to that, please try saying again", voice=False, repeat=True):
    query = ""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 0.8
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
        except:
            if voice:
                speak(err)
            if repeat:
                listen(err, voice, repeat)
            print(err)
    return query
def Capitalize(string):
    string = string.split(" ")
    g1=False
    if len(string) > 1:
        g1 = True
    stringName = ""
    for i in string:
        for j in i:
            if i.index(j)==0:
                stringName+=j.upper()
            else:
                stringName+=j
            if string.index(i) == -1:
                break
        if g1:
            stringName+=" "
            
    return stringName.strip()
def remove_last_lines(string, index):
    if type(string) != str:
        raise Exception("Expected string but found {}".format(type(string)))
    string = string.split("\n")
    string = string[:-index]    
    toJoin = "\n"
    string = toJoin.join(string)
    return string
def remove_and_add_last_line(string, index, string2):
    if type(string) != str:
        raise Exception("Expected string but found {}".format(type(string)))
    string = string.split("\n")
    string = string[:-index]   
    # print(string)
    # print(string)
    string3 = string2.split("\n")
    # print(string3)
    string.extend(string3)
    toJoin = "\n"
    string = toJoin.join(string) 
    # print(string)
    return string

def add_last(string, toadd):
    string = string.split("\n")
    toadd = toadd.split("\n")
    string.extend(toadd)
    toJoin = "\n"
    string = toJoin.join(string)
    return string

def img_to_text(filename):
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'
    return(pytesseract.image_to_string(filename))
    


def getFiles(arr):
    if type(arr) != list:
        raise Exception("Required {} found {}".format(list, type(arr)))
    files = []
    try:
        for i in arr:
            if os.path.isfile(i):
                files.append(i)
    except Exception as e:
        print(e)
    return files

def getFolders(arr):
    if type(arr) != list:
        raise Exception("Required {} found {}".format(list, type(arr)))
    files = []
    try:
        for i in arr:
            if not os.path.isfile(i):
                files.append(i)
    except Exception as e:
        print(e)
    return files
def filterList(array, difference, right=False):
    if type(array) != list:
        raise Exception(f"The parameter passed should be list not {type(array)}")
    newArray = []
    for i in range (len(array)):
        if right:
            realWord = array[i].split(f"{difference}")[1]
        else:
            realWord = array[i].split(f"{difference}")[0]
        newArray.append(realWord)
    return newArray

def getPath(path):
    if path == "":
        raise Exception("The part are empty")
    path = str(path)
    path = path.split("\'")[1]
    return path

def removeLastElement(string, differ):
    if string == "" or differ=="":
        raise Exception("The vlaues are empty")
    main = string.split(differ)[-1]
    mainthing = string.split(differ)
    mainthing.remove(main)
    dif = differ
    mainthing = dif.join(mainthing)

    return mainthing
def removeFirstElement(string, differ):
    if string == "" or differ=="":
        raise Exception("The vlaues are empty")
    main = string.split(differ)[0]
    mainthing = string.split(differ)
    mainthing.remove(main)
    dif = differ
    mainthing = dif.join(mainthing)

    return mainthing
def removeNElement(string, differ, index):
    if string == "" or differ=="":
        raise Exception("The vlaues are empty")
    main = string.split(differ)[index]
    mainthing = string.split(differ)
    mainthing.remove(main)
    dif = differ
    mainthing = dif.join(mainthing)

    return mainthing

def get_all_drives():
    available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
    return available_drives
def randaLastElement(string, differ, wtadd):
    if string == "" or differ=="" or wtadd == "":
        raise Exception("The vlaues are empty")
    main = string.split(differ)[-1]
    mainthing = string.split(differ)
    mainthing.remove(main)
    mainthing.append(wtadd)
    dif = differ
    mainthing = dif.join(mainthing)

    return mainthing
def randaFirstElement(string, differ, wtadd):
    if string == "" or differ=="" or wtadd == "":
        raise Exception("The vlaues are empty")
    main = string.split(differ)[0]
    mainthing = string.split(differ)
    mainthing.remove(main)
    mainthing.append(wtadd)
    dif = differ
    mainthing = dif.join(mainthing)

    return mainthing
def randaNElement(string, differ,wtadd,index=0):
    if string == "" or differ=="" or wtadd == "":
        raise Exception("The vlaues are empty")
    main = string.split(differ)[index]
    mainthing = string.split(differ)
    mainthing.remove(main)
    mainthing.append(wtadd)
    dif = differ
    mainthing = dif.join(mainthing)

    return mainthing


class Arrays:
    def linear_search(self, element, array):
        if element in array:
            return True
        else:
            return False
    def binary_search(self, element, array):
        if element in array:
            return array.index(element)
        else:
            return False
    
    def sort(self, array):
        array.sort()
        return array
class Automation:
    def type(self, issue, pause = 0):
        time.sleep(pause)
        pyautogui.typewrite(issue)
    def click(self, x=0, y=0, clicks=1, interval=0, pause=0):
        time.sleep(pause)
        pyautogui.click(x=x, y=y, clicks=clicks, interval=interval)
    def hit(self, key="enter", pause=0):
        time.sleep(pause)
        pyautogui.press(key)
