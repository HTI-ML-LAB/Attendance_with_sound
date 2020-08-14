import threading
import time
from Connector import *
import random
from face.face_process import face_recognize
from face.utils.config import get_config
from easydict import EasyDict as edict
import time
import speech_recognition as sr
from gtts import gTTS
import playsound
from os import path
import os
class Processor:
    def __init__(self):
        print("Face processs")
        self.config=get_config
        self.face=face_recognize(self.config(net_mode = 'ir_se', threshold = 1.22, detect_id = 1))
        self.queue = []
        self.queue_tem=[]
        self.max_pro = 4
        self.connector=Connector("Face")
        self.sound="sound"
       
        self.threshold_distance=self.config().threshold_distance
        try:
            self.labels,self.features=self.connector.get_users()
            self.features=np.array(self.features)
            self.features=self.features.reshape(self.features.shape[0],512)
        except:
            self.features=np.array([]).reshape(0,512)
            self.labels=[]
        print(self.features.shape)
        

    def identify(self, features):
        if(len(self.features)==0):
            return ["Unknown"]*len(features)
        res=[]
        features= np.array(features)
        features=np.expand_dims(features, 1)
        diff = self.features - features
        dist = np.sum(np.power(diff, 2), axis=2)
        minimum = np.amin(dist, axis=1)
        min_idx = np.argmin(dist, axis=1)
        result = []
        for id,(min, min_id)  in enumerate(zip(minimum, min_idx)):          
            if min < self.threshold_distance:
                # confidence = self.confidence(features[id].reshape(512,), self.features[min_id])
                p_id = self.labels[min_id]
                res.append(p_id)
            else:
                res.append("Unknown")
        return res

    def get_feature(self,image):
        features,boxes =self.face.feature_img(image)
        if(len(features)==1):
            return features[0]
        
        return []

    def process_add_user(self,image,name,year,phone):
        
        feature=self.get_feature(image)
        if(feature!=[]):
            self.connector.add_user(name,year,phone,feature)
            self.labels.append(name)
            self.features=np.concatenate((self.features,feature.reshape(1,512)))
            try:
                if(not path.isfile(os.path.join(self.sound,name+".mp3"))):
                    tts = gTTS(text=name, lang='vi')
                    filename = os.path.join(self.sound,name+".mp3")
                    tts.save(filename)
                playsound.playsound(os.path.join(self.sound,"them"+".mp3"))
                playsound.playsound(os.path.join(self.sound,name+".mp3"))
                
            except Exception as e:
                print(e)

            
            print("add success ful ",name)
        else:
            print("fail length ",len(feature))

    def process_attend(self,image):
        # t1=time.time()
        features,boxes =self.face.feature_img(image)
        # print("time1 ",time.time()-t1)
        if(features.shape[0]!=0):
            names=self.identify(features)
            for x in names:
                if(x!="Unknown"):
                    #visualize with sound
                    if(self.connector.check_recent(x)):
                        try:
                            if(not path.isfile(os.path.join(self.sound,x+".mp3"))):
                                tts = gTTS(text=x, lang='vi')
                                filename = os.path.join(self.sound,x+".mp3")
                                tts.save(filename)
                            playsound.playsound(os.path.join(self.sound,"xin_chao"+".mp3"))
                            playsound.playsound(os.path.join(self.sound,x+".mp3"))
                        except Exception as e:
                            print(e)

                    #add database 
                    self.connector.add_attend(x)

    
    def add_process(self,data,mode):
        # print(mode)
        if(mode=="add"):
            self.queue_tem.append(threading.Thread(target=self.process_add_user,args=(data[0],data[1],data[2],data[3],)))
        if(mode == "attend"):
            self.queue_tem.append(threading.Thread(target=self.process_attend,args=(data[0],)))
            
                

        
    def process_queue(self):
        while 1:
            # print("yes")
            n=len(self.queue)
            if(n>0 or len(self.queue_tem)>0):
                
                for i in range(n-1,max(n-self.max_pro-1,-1),-1):
                    self.queue[i].start()
                    self.queue[i].join()
                    del self.queue[i]
                    time.sleep(1)
                for i in range(len(self.queue_tem)-1,-1,-1):
                    self.queue.append(self.queue_tem[i])
                    del self.queue_tem[i]
            else:
                time.sleep(1)
        

    



