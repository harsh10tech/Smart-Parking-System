import cv2 as cv
import pytesseract
import os
import time
import class_thres
from PIL import Image
from datetime import date
import datetime
import pymongo as db

client = db.MongoClient("mongodb://localhost:27017/")

pytesseract.pytesseract.tesseract_cmd=(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
yes = '0'

sence = input('Type 0 to enter: ')


if sence == yes :
    
    date=date.today().strftime('%d-%B-%Y')
    extime= datetime.datetime.now()
    exit_time = extime.strftime('%H:%M')
    
    #will create the existing text file with same date
    new_day = date+'.txt'
    
    #num_plate = cv.VideoCapture(0)
    #check,plate = num_plate.read()
    img = cv.imread(r'Smart-Parking-System\Number_plate2.jpg',1) #reading the image
    plate = cv.resize(img, (int(img.shape[1]/3),int(img.shape[0]/3)))
    
    gray = cv.cvtColor(plate, cv.COLOR_BGR2GRAY)
    
    cv.imshow('number_plate',plate)
    
    gray = class_thres.thres.thres2(gray)
    temp = "{}.png".format(os.getpid())
    cv.imwrite(temp,gray)
    
    number = pytesseract.image_to_string(Image.open(temp))
    
    os.remove(temp)
    
    time.sleep(3)
    
    cardb = client["Car-Parking"]
    carcol = cardb["Cars"]
    reffdata = {"_id":number}
    cardata = {"$set":{"Exit_time":exit_time}}
    carcol.update_one(reffdata,cardata)

    entime = carcol.find_one({"_id":number},{"_id":0,"Entry Time":1})
    entry = entime["Entry Time"]
    #print(entry)
    #print(exit_time)
    entry_time = datetime.datetime.strptime(entry,'%H:%M')
    duration = datetime.datetime.strptime(exit_time,'%H:%M')-entry_time
    #duration = datetime.datetime.strftime(duration,"%H:%M")
    cardata2 = {"$set":{"Duration":str(duration)}}
    carcol.update_one(reffdata,cardata2)

    print(duration)


cv.waitKey(0)


cv.destroyAllWindows()    
