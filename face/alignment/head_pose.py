import numpy as np
import cv2
import math
class PoseEstimator:
    """Estimate head pose according to the facial landmarks"""

    def __init__(self, img_size=(480, 640)):
        self.size = img_size

        # 3D model points.
        self.model_points = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, -330.0, -65.0),        # Chin
            (-225.0, 170.0, -135.0),     # Left eye left corner
            (225.0, 170.0, -135.0),      # Right eye right corner
            (-150.0, -150.0, -125.0),    # Mouth left corner
            (150.0, -150.0, -125.0)      # Mouth right corner
        ]) 

        # Camera internals
        # self.focal_length = self.size[1]
        
        self.camera_center = (self.size[1] / 2, self.size[0] / 2)
        focal_length = self.camera_center[0] / np.tan(60/2 * np.pi / 180)
        self.camera_matrix = np.array(
            [[focal_length, 0, self.camera_center[0]],
             [0, focal_length, self.camera_center[1]],
             [0, 0, 1]], dtype="double")

        # Assuming no lens distortion
        self.dist_coeffs = np.zeros((4, 1))

        # Rotation vector and translation vector
        self.r_vec = np.array([[0.01891013], [0.08560084], [-3.14392813]])
        self.t_vec = np.array(
            [[-14.97821226], [-10.62040383], [-2053.03596872]])
        # self.r_vec = None
        # self.t_vec = None
    def face_orientation(self, landmarks):
        v_cx, v_cy = landmarks[2,0] - (landmarks[0,0]+landmarks[1,0])/2, landmarks[2,1] - (landmarks[0, 1]+landmarks[1,1])/2
        image_points = np.array([
                                (landmarks[2,0], landmarks[2,1]),     # Nose tip
                                (landmarks[2,0] + 1.2*v_cx, landmarks[2,1]+ 1.2*v_cy),   # Chin
                                (landmarks[0, 0], landmarks[0, 1]),     # Left eye left corner
                                (landmarks[1,0], landmarks[1,1]),     # Right eye right corne
                                (landmarks[3,0], landmarks[3,1]),     # Left Mouth corner
                                (landmarks[4,0], landmarks[4,1])      # Right mouth corner
                            ], dtype="double")

        (success, rotation_vector, translation_vector) = cv2.solvePnP(self.model_points, image_points, self.camera_matrix, self.dist_coeffs)

        
        rvec_matrix = cv2.Rodrigues(rotation_vector)[0]

        proj_matrix = np.hstack((rvec_matrix, translation_vector))
        eulerAngles = cv2.decomposeProjectionMatrix(proj_matrix)[6] 

        pitch, yaw, roll = [math.radians(_) for _ in eulerAngles]


        pitch = math.degrees(math.asin(math.sin(pitch)))
        roll = -math.degrees(math.asin(math.sin(roll)))
        yaw = math.degrees(math.asin(math.sin(yaw)))

        return int(roll), int(pitch), int(yaw)
