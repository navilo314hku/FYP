from const import *
import sys
from datetime import datetime
import numpy as np 
import cv2
import os 
from time import sleep
from threading import *
class ReadThread(Thread):
    def arrayFromFile(self,file_name):
        arr=[]
        with open(file_name,'r') as f:
            for line in f.readlines(): #line is a string
                line_arr=[float(x) for x in line.split(",")]
                arr.append(line_arr)
        arr=np.array(arr)
        return arr
    def __init__(self,txtFileName):
        super(ReadThread, self).__init__()
        self.txtFileName=txtFileName

    def run(self):
        #return numpy array
        print("ReadThread.run()")
        img_array=self.arrayFromFile(self.txtFileName)
        return img_array

    def start(self):
        return self.run()
class WriteThread(Thread):
    def __init__(self,output_path,img_array):
        super(WriteThread, self).__init__()
        self.output_path=output_path
        self.img_array=img_array
    def run(self):
        cv2.imwrite(self.output_path,self.img_array)
        return 

def threadStoreTxtToJpg(TXT_PATH,IMAGE_PATH,label):

    def isEmptyTxt(file_name):
        return os.stat(f"{file_name}").st_size == 0
    def currentTimeInfo():
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    #convert all txt files from {TXT_PATH} into jpg images and store them in {IMAGE_PATH}
    #1. list all files name with txt extension
    destination_folder= os.path.join(IMAGE_PATH,f"{label}")
    for file in os.listdir(TXT_PATH):
        if file.endswith(".txt"):
            file_name=os.path.join(TXT_PATH,file)
            if not isEmptyTxt(file_name): 
                print(file_name)
                t1=ReadThread(file_name)#init thread object
                t1.start()
                t1.join()
                #img_array=arrayFromFile(file_name)
                #sleep(0.8)
               
                output_path=os.path.join(destination_folder,currentTimeInfo()+".jpg")
                Writethread=WriteThread(output_path,img_array)
                Writethread.start()
                Writethread.join()
#                cv2.imwrite(output_path,img_array)
def storeTxtToJpg(TXT_PATH,IMAGE_PATH,label):
    def arrayFromFile(file_name):
        arr=[]
        with open(file_name,'r') as f:
            for line in f.readlines(): #line is a string
                line_arr=[float(x) for x in line.split(",")]
                arr.append(line_arr)
        arr=np.array(arr)
        return arr
    def isEmptyTxt(file_name):
        return os.stat(f"{file_name}").st_size == 0
    def currentTimeInfo():
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    #convert all txt files from {TXT_PATH} into jpg images and store them in {IMAGE_PATH}
    #1. list all files name with txt extension
    destination_folder= os.path.join(IMAGE_PATH,f"{label}")
    for file in os.listdir(TXT_PATH):
        if file.endswith(".txt"):
            file_name=os.path.join(TXT_PATH,file)
            if not isEmptyTxt(file_name): 
                print(file_name)
                img_array=arrayFromFile(file_name)
                sleep(1)
                #cv2.imwrite(img_)
                #path=os.path.join("images","your_file.jpg")
                output_path=os.path.join(destination_folder,currentTimeInfo()+".jpg")
                cv2.imwrite(output_path,img_array)

if __name__=='__main__':
    if len(sys.argv)!=3:#test 0
        print("MISSING ARGUMENT(S)!!!")
        print("QUITTED")
        quit()
    if not (sys.argv[1]=='test' or sys.argv[1]=='train'):
        print("NO SUCH MODE, PLEASE ENTER test or train as mode")
        print("QUIT")
        quit()
        
    
    #print("the argument is ")
    #print(sys.argv[1])
    if sys.argv[1]=='test':
        path=TEST_IMAGE_PATH
    elif sys.argv[1]=='train':
        path=TRAIN_IMAGE_PATH
    storeTxtToJpg(TXT_PATH,path,sys.argv[2])
