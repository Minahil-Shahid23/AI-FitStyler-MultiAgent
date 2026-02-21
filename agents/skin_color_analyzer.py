import mediapipe as mp
import cv2 
import numpy as np

# --- Smart Import Logic (Local vs Cloud Fix) ---
try:
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
except AttributeError:
    # Local/Alternative import
    import mediapipe.python.solutions.face_mesh as mp_face_mesh
    import mediapipe.python.solutions.drawing_utils as mp_drawing

def detect_skin_tone_and_palette(image_path):
    """
    Detect skin tone from face image and return fashion color palette
    """
    image = cv2.imread(image_path)
    if image is None:
        return "unknown", []

    height, width, _ = image.shape

    # Standard initialization
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as face_mesh:

        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.multi_face_landmarks:
            return "unknown", []

        face_landmarks = results.multi_face_landmarks[0]

        # Cheek landmarks for skin color sampling
        LEFT_CHEEK = [234, 93, 132, 58]
        RIGHT_CHEEK = [454, 323, 361, 288]

        cheek_points = []
        for idx in LEFT_CHEEK + RIGHT_CHEEK:
            x = int(face_landmarks.landmark[idx].x * width)
            y = int(face_landmarks.landmark[idx].y * height)
            cheek_points.append((x, y))

        cheek_points = np.array(cheek_points, dtype=np.int32)

        # Skin tone area mask
        mask = np.zeros((height, width), dtype=np.uint8)
        cv2.fillConvexPoly(mask, cheek_points, 255)

        skin_pixels = image[mask == 255]
        if len(skin_pixels) == 0:
            return "unknown", []

        avg_bgr = np.mean(skin_pixels, axis=0).astype(np.uint8)

        # Convert to LAB space for reliable lightness (L) detection
        lab = cv2.cvtColor(avg_bgr.reshape(1, 1, 3), cv2.COLOR_BGR2LAB)[0][0]
        L = lab[0]

        if L < 60:
            skin_tone = "dark"
        elif L > 85:
            skin_tone = "fair"
        else:
            skin_tone = "wheatish"

    # Fashion Palettes
    palettes = {
        "fair": ["#A8D5BA", "#D6E4F0", "#E8F4F8", "#F0E6EF", "#E8E8E8", "#D4AF37"],
        "wheatish": ["#C7B198", "#D2B48C", "#B0C4DE", "#D8BFD8", "#F5F5DC", "#8FBC8F"],
        "dark": ["#4682B4", "#708090", "#5F9EA0", "#7B68EE", "#696969", "#2F4F4F"]
    }

    palette = palettes.get(skin_tone, palettes["wheatish"])
    
    # Annotated image logic
    annotated_image = image.copy()
    annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    
    if results.multi_face_landmarks:
        mp_drawing.draw_landmarks(
            annotated_image_rgb, 
            results.multi_face_landmarks[0], 
            mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
        )
    
    cv2.imwrite("analyzed_skin_photo.jpg", cv2.cvtColor(annotated_image_rgb, cv2.COLOR_RGB2BGR))

    return skin_tone, palette
