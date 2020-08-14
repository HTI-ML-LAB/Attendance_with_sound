import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import torch
import numpy as np
from PIL import Image
from torchvision import transforms as trans
import math
import time
from .utils.utils import compare
from .utils.constants import WEIGHT_DIR, WEIGHT_PATH, URL
from .src.backbone.model import SE_IR, MobileFaceNet, l2_norm
from .alignment.detector import Retinaface_Detector
# from smoofing.Smoofing import Smoofing
class face_recognize(object):
    def __init__(self, conf):
        self.setup(conf)
    def setup(self, conf):
        self.conf = conf
        if self.conf.use_mobile_facenet:
            self.model = MobileFaceNet(512).to(conf.device)
        else:
            self.model = SE_IR(50, 0.4, conf.net_mode).to(conf.device)
        self.use_tensor = conf.use_tensor     #If False: su dung numpy dung cho tuong lai khi trien khai qua Product Quantizers cho he thong lon
        self.weight = WEIGHT_PATH[conf.net_mode]
        self.model.eval()
        
        self.threshold = conf.threshold
        self.test_transform = conf.test_transform

        self.mtcnn = Retinaface_Detector(device = conf.device, thresh = 0.7, scales = [320, 320])
        # self.anti_spoofing = Smoofing()

        self.tta = False

        self.limit = conf.face_limit
        self.min_face_size = conf.min_face_size
        self.load_state(self.conf.device.type)

    def load_state(self, device='cpu'): 
        if not os.path.isfile(self.weight):
            if not os.path.exists(WEIGHT_DIR):
                os.mkdir(WEIGHT_DIR)
            os.system(URL[self.conf.net_mode])
            os.system('mv %s %s'%(URL[self.conf.net_mode].split(' ')[-1], WEIGHT_DIR))

        if device == 'cpu':        
            self.model.load_state_dict(torch.load(self.weight, map_location='cpu'))
        else:
            self.model.load_state_dict(torch.load(self.weight))

    def load_single_face(self, image, name='Unknow'):
        embeddings = []
        names = ['Unknown']
        embs = []
        assert not image is None, 'None is not image, please enter image path!'
        try:
            if isinstance(image, np.ndarray):
                img = Image.fromarray(image)
            elif isinstance(image, str):
                assert os.path.isfile(image), 'No such image name: %s'%image
                img = Image.open(image)
            else:
                    img = image   
        except:
            pass
        if img.size != (112, 112):
            b,img = self.mtcnn.align(img)
        with torch.no_grad():
            if self.tta:
                mirror = trans.functional.hflip(img)
                emb = self.model(self.test_transform(img).to(self.conf.device).unsqueeze(0))
                emb_mirror = self.model(self.test_transform(mirror).to(self.conf.device).unsqueeze(0))
                if self.use_tensor:
                    embs.append(l2_norm(emb + emb_mirror))
                else:
                    embs.append(l2_norm(emb + emb_mirror).data.cpu().numpy())
                
            else:                        
                embs.append(self.model(self.test_transform(img).to(self.conf.device).unsqueeze(0)).data.cpu().numpy())
        if not len(embs) == 0:
            names=[]
            names.append(name)
            names = np.array(names)
          
            if self.use_tensor:
                embedding = torch.cat(embs).mean(0,keepdim=True)
                embeddings.append(embedding)
                embeddings = torch.cat(embeddings)
            else:
                embedding = np.mean(embs,axis=0)
                embeddings.append(embedding[0])
        return embeddings, names



    def align_multi(self, img):
        bboxes, faces = self.mtcnn.align_multi(img, self.limit, self.min_face_size)
        return bboxes, faces

    def align(img):
        face = self.mtcnn.align(img)
        return face
    def feature_img(self, img):
        
        try:
         bboxes, faces  = self.align_multi(img)
        # bboxes, faces = dict_output["bboxs"], dict_output["faces"]

         embs = []
         for im in faces:
            embs.append(self.model(self.test_transform(im).to(self.conf.device).unsqueeze(0)).data.cpu().numpy()[0])
         return np.array(embs), bboxes
        except Exception as e:
            print(e)
            return np.array([]),[]
    
   
