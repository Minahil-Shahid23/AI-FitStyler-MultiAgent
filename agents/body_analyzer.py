import mediapipe as mp
import cv2 

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def analyze_body_from_photo(image_path):
   
    image = cv2.imread(image_path)
    if image is None:
        return "unknown"
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
        results = pose.process(image_rgb)
        
        if not results.pose_landmarks:
            return "unknown" 
        
        landmarks = results.pose_landmarks.landmark
        h, w, _ = image.shape
        
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        shoulder_width = abs(left_shoulder.x * w - right_shoulder.x * w)

        left_leg = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_leg = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        legs_width = abs(left_leg.x * w - right_leg.x * w)
                
        bmi_estimate = (legs_width / shoulder_width)
        if bmi_estimate <= 0.55:
            body_type = "slim"
        elif bmi_estimate > 0.6:
            body_type = "curvy"
        else:
            body_type = "athletic"
        
        mp_drawing.draw_landmarks(image_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imwrite("analyzed_photo.jpg", cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))  # Save for show
        
        return body_type
