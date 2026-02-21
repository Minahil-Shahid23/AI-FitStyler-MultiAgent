import cv2
import mediapipe as mp

def analyze_body_from_photo(image_path):
    # MediaPipe ko function ke andar initialize karna zyada stable hai
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    image = cv2.imread(image_path)
    if image is None:
        return "unknown"
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Pose Detection logic
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
        results = pose.process(image_rgb)
        
        if not results.pose_landmarks:
            return "unknown" 
        
        landmarks = results.pose_landmarks.landmark
        h, w, _ = image.shape
        
        # Landmarks ki values (Shoulder and Hip)
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        shoulder_width = abs(left_shoulder.x * w - right_shoulder.x * w)

        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        hip_width = abs(left_hip.x * w - right_hip.x * w)
                
        # Body type calculation
        ratio = (hip_width / shoulder_width)
        if ratio <= 0.75:
            body_type = "slim"
        elif ratio > 0.95:
            body_type = "curvy"
        else:
            body_type = "athletic"
        
        # Drawing landmarks on image
        mp_drawing.draw_landmarks(image_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imwrite("analyzed_photo.jpg", cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))

        return body_type

