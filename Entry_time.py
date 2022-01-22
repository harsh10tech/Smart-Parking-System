import cv2 as cv
import pytesseract
import os
import time
import class_thres
from PIL import Image
from datetime import date
import datetime
import pymongo as db

#connecting to mongoDB
client = db.MongoClient("mongodb://localhost:27017/")

#calling of needed software
pytesseract.pytesseract.tesseract_cmd=(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
yes = '0'

sence = input('Type 0 to enter: ')

if sence == yes :
    
   
    date=date.today().strftime('%d-%B-%Y')
    x= datetime.datetime.now()
    entry_time = x.strftime("%H:%M")
    
    #will create new text file for every new day with their title as date
    new_day = date+'.txt'
    
    #Capturing the image of the plate
    #num_plate = cv.VideoCapture(0) 
    img = cv.imread(r'Smart-Parking-System\Number_plate2.jpg',1) #reading the image
    plate = cv.resize(img, (int(img.shape[1]/3),int(img.shape[0]/3)))
    
    gray = cv.cvtColor(plate, cv.COLOR_BGR2GRAY) #changing image into grayscale
    
    cv.imshow('number_plate',plate) #opening a window to show the image
    
    #A class for thresholld and creating temporary file
    gray = class_thres.thres.thres2(gray) 
    temp = "{}.png".format(os.getpid())
    cv.imwrite(temp,gray)
    
    #Extracting the text from the image in string form
    number = pytesseract.image_to_string(gray)
    
    #deleting the temporary file
    os.remove(temp)
    
    time.sleep(3)
    
    data = '\n' + number + '   ' + entry_time
    
    #A text file to keep permanent record of the entries for future record
    entry = open(new_day,"a")

    entry.write(data)
    entry.close()
    
    #Using MongoDB to create a database
    cardb = client["Car-Parking"]
    carcol = cardb["Cars"]
    cardata = {"_id":number,"Entry Time":entry_time,"Exit_time":"xxxx","Duration":"xxxx"}
    carcol.insert_one(cardata)
    
cv.waitKey(0)

cv.destroyAllWindows()
