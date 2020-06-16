# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 07:49:57 2020

@author: adars
"""


import tkinter as tk
import cv2,os
import csv
import numpy as np
import pandas as pd
import datetime
import time
from playsound import playsound
from PIL import ImageTk, Image


window = tk.Tk()
window.title("Face Recognization Attendence System")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
 
window.geometry('1440x900')
window.configure(background='gray91')

#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)


message = tk.Label(window, text="Face-Recognition Attendence System" ,fg="gold"  ,width=63  ,height=1,font=('times', 30, 'italic bold ')) 
message.place(x=0, y=0)





from tkinter import *
from PIL import Image, ImageTk



image = Image.open("face.png")
photo = ImageTk.PhotoImage(image)


label = Label(image=photo)
label.image = photo # keep a reference!
label.pack()
label.place(x=0, y=50)
        # labels can be text or images 



lbl = tk.Label(window, text="Student ID",width=20  ,height=1  ,fg="white"  ,bg="saddle brown" ,font=('times', 20, ' bold ') ) 
lbl.place(x=350, y=150)

txt = tk.Entry(window,width=30 ,bg="white" ,fg="black",font=('times', 20, ' bold '))
txt.place(x=700, y=150)

lbl2 = tk.Label(window, text="Student Full Name",width=20  ,fg="white"  ,bg="saddle brown"    ,height=1 ,font=('times', 20, ' bold ')) 
lbl2.place(x=350, y=250)

txt2 = tk.Entry(window,width=30  ,bg="white"  ,fg="black",font=('times', 20, ' bold ')  )
txt2.place(x=700, y=250)

lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="white"  ,bg="saddle brown"  ,height=1 ,font=('times', 20, ' bold ')) 
lbl3.place(x=350, y=350)

message = tk.Label(window, text="" ,bg="white"  ,fg="black"  ,width=70  ,height=2, activebackground = "green") 
message.place(x=700, y=347)
message.config(font=("Courier", 13, 'bold'))

lbl3 = tk.Label(window, text="Attendance Sheet: ",width=20  ,fg="white"  ,bg="saddle brown"  ,height=1 ,font=('times', 20, ' bold ')) 
lbl3.place(x=10, y=650)




 
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages(): 
    if (len(txt.get()) != 0) and (len(txt2.get()) != 0):
        Id=(txt.get())
        name=(txt2.get())
        final=name.replace(" ", "")
        if(is_number(Id) and final.isalpha()):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector=cv2.CascadeClassifier(harcascadePath)
            sampleNum=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                    #incrementing sample number 
                    sampleNum=sampleNum+1
                    #saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("/Trainer/ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    #display the frame
                    cv2.imshow('frame',img)
                #wait for 100 miliseconds 
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum>200:
                    break
            cam.release()
            cv2.destroyAllWindows() 
            
            
            header = ['Student Id', 'Student Name']
            exists = os.path.isfile('/Studentdetails.csv')
            if exists:
                    #Id = e1.get()
                    #name = e2.get()
                    some_list = [Id , name]
                    with open('/Studentdetails.csv', 'a+') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow(some_list)
                    csvFile.close()     
    
            else:        
                    header = ['Student Id', 'Student Name']
                    #Id = e1.get()
                    #name = e2.get()
                    some_list = [Id , name]
                    with open('/Studentdetails.csv', 'a+') as csvFile:
                            
                        writer = csv.writer(csvFile)
                        writer.writerow(i for i in header)
                        writer.writerow(some_list)
                        
                    csvFile.close()         
            
            """
            res = "Student Id : " + Id +"    " " Name : "+ name
            row = [Id , name]
            with open('/Face_recognization.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            """
                  
            message.configure(text= res)
        else:
            if(Id.isalpha()):
                res = "Please enter numeric student id"
                message.configure(text= res)
            elif(is_number(name)):
                res = "Please enter alphabetical name of student"
                message.configure(text= res)
            else:
                print("")
    else:
        res = "Please enter full data of student to proceed further"
        message.configure(text= res)           


def TrainImages():
    if  os.listdir('E:/python_file2020/Face_recognization/trainer') :
    # Store configuration file values
        print("File is present")
        #recognizer = cv2.face_LBPHFaceRecognizer.create()
        recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
        harcascadePath = "/haarcascade_frontalface_default.xml"
        detector =cv2.CascadeClassifier(harcascadePath)
        faces,Id = getImagesAndLabels("/TrainingImageLabel")
        recognizer.train(faces, np.array(Id))
        recognizer.write("/TrainingImage/trainer.yml")
        res = "Image Trained"#+",".join(str(f) for f in Id)
        message.configure(text= res)             
    else:
         res = "Data not available for training "
         message.configure(text= res)         
 
from PIL import Image
def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

global aa

def Track():
    exists = os.path.isfile('/TrainingImage/trainer.yml')
    if exists:
        #recognizer = cv2.face.createLBPHFaceRecognizer()
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        #cv2.createLBPHFaceRecognizer()
        recognizer.read("/TrainingImage/trainer.yml")
        harcascadePath = "/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);    
        df=pd.read_csv("/StudentDetails/StudentsDetails.csv")
        #cam = cv2.VideoCapture('rtsp://admin:123456789@192.168.1.8')
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX        
        col_names =  ['Id','Name','Date','Entry_Time']
        attendance = pd.DataFrame(columns = col_names)    
        while(cam.isOpened()):
            ret, im =cam.read()
            if ret:
                gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                faces=faceCascade.detectMultiScale(gray, 1.3,5)    
                for(x,y,w,h) in faces:
                    cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                    Id, conf = recognizer.predict(gray[y:y+h,x:x+w]) 
                    print(Id)                                  
                    if(conf < 40):
                        ts = time.time()      
                        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        global aa 
                        aa=df.loc[df['Id'] == Id]['Name'].values
                        tt=str(Id)+"-"+aa
                        name=(", ".join(aa))
                        #tt=str(Id)+"-"+aa
                        attendance.loc[len(attendance)] = [Id,name,date,timeStamp]
                    else:
                        Id='Unknown'                
                        tt=str(Id)
                        #playsound('beep.mp3')
                        #name=(", ".join(aa))
                    if(conf > 55):
                        #temp=(", ".join(aa))
                        name=(", ".join(aa))
                        noOfFile=len(os.listdir("/ImagesUnknown"))+1
                        cv2.imwrite("/ImagesUnknown"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])     
                    cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
                attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
                cv2.imshow('im',im) 
            if (cv2.waitKey(1)==ord('q')):
                break
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        exists = os.path.isfile('/StudentDetails/StudentsDetails.csv')
        if exists: 
            fileName="/StudentDetails/StudentsDetails.csv"
            with open(fileName, 'a') as f:
                attendance.to_csv(f, header=False)
       
            print("Exists")
        else:    
            fileName="/StudentDetails/StudentsDetails.csv"
            attendance.to_csv(fileName,index=False)
        cam.release()
        cv2.destroyAllWindows()
        if(Id=='Unknown'):
            res = "Student is Unknown"
        else:    
            res = "Succesfully Filled the Attendence"#+",".join(str(f) for f in Id)
        message.configure(text= res)
        playsound('thankyou.mp3')
        #print(attendance)
        attendance = attendance.to_string(index=False)
        res=attendance
        
        S = Scrollbar(window)
        T = Text(window,state='disabled',height=6, width=85)
        T.configure(state='normal')
        T.place(x=375,y=650)
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        #message2.configure(text= res)
        T.insert(END, res)
        T.configure(state='disabled')
    else:
        res = "Data not available for tracking"
        message.configure(text= res)     
        

clearButton = tk.Button(window, text="Clear", command=clear  ,fg="red"  ,bg="white"  ,width=10  ,height=1 ,activebackground = "grey" ,font=('times', 10, ' bold '))
clearButton.place(x=1150, y=150)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="red"  ,bg="white"  ,width=10  ,height=1, activebackground = "grey" ,font=('times', 10, ' bold '))
clearButton2.place(x=1150, y=250)    
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="white"  ,bg="orange2"  ,width=20  ,height=3, activebackground = "grey" ,font=('times', 20, ' bold '))
takeImg.place(x=10, y=480)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="white"  ,bg="orange2"  ,width=20  ,height=3, activebackground = "grey" ,font=('times', 20, ' bold '))
trainImg.place(x=370, y=480)
trackImg = tk.Button(window, text="Track Entry", command=Track  ,fg="white"  ,bg="orange2"  ,width=20  ,height=3, activebackground = "grey" ,font=('times', 20, ' bold '))
trackImg.place(x=730, y=480)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="white"  ,bg="orange2"  ,width=20  ,height=3, activebackground = "grey" ,font=('times', 20, ' bold '))
quitWindow.place(x=1090, y=480)
copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 30, 'italic bold underline'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.configure(state="disabled",fg="red")
copyWrite.pack(side="left")
copyWrite.place(x=800, y=750)
 
window.mainloop()
