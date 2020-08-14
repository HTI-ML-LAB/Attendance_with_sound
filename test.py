from face.face_process import face_recognize
from face.utils.config import get_config
config=get_config
face=face_recognize(config(net_mode = 'ir_se', threshold = 1.22, detect_id = 1))