from mongoengine import connect
from mongoengine import *
import json
import numpy as np
import datetime 
from datetime import datetime

class User(Document):
    name = StringField(required=True, unique=False)
    year = StringField(required=True,unique=False)
    phone = StringField(required=True,unique=False)
    feature =ListField()

class Attendance(Document):
    name = StringField(required=True, unique=False)
    date = StringField(required=True, unique=False)
    firsttime = StringField(required=True, unique=False)
    lasttime = StringField(required=True, unique=False)


        
class Connector:
    def __init__(self,name):
        connect(name)

    def add_user(self,name,year=0,phone=0,feature=[]):
        User(
            name=name,
            year=year,
            phone=phone,
            feature=feature.tolist()
        ).save()

    def get_users(self):
        names=[]
        features=[]
        user = User.objects()
        for x in user:
            names.append(x.name)
            features.append(np.array(x.feature))
        return names,features

    def add_new_attend(self,name):
        now = datetime.now()
        currtime=now.strftime("%H:%M:%S")
        Attendance(
            name=name,
            date=now.strftime("%d-%m-%Y"),
            firsttime=currtime,
            lasttime=currtime).save()
    
    def add_attend(self,name):
        now = datetime.now()
        date=now.strftime("%d-%m-%Y")
        if(self.get_attend_name(name,date) is not None):
            Attendance.objects(name=name,date=date).get().update(lasttime=now.strftime("%H:%M:%S"))
        else:
            self.add_new_attend(name)

    
    def get_attend_name(self,name,date):
        try:
            att=Attendance.objects(name=name , date=date).get()
            return att.lasttime
        except:
            return None

    def check_recent(self,name):
        now = datetime.now()
        date=now.strftime("%d-%m-%Y")
        t1=self.get_attend_name(name,date)
        t2=now.strftime("%H:%M:%S")
        if(self.subtime(t2,t1)>=15):
            return True
        else:
            return False

    def subtime(self,t2,t1):
        try:
            FMT = '%H:%M:%S'
            tdelta = datetime.strptime(t2, FMT) - datetime.strptime(t1, FMT)
            return tdelta.total_seconds()
        except:
            return 100

# X=Connector("Face")
# # X.add_attend("Hảo")
# # X.get_user()
# # # X.add_user("hao","1234")
# print(X.subtime("17:25:00",X.get_attend_name("Hảo","13-08-2020")))