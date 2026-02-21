import cv2
import numpy as np

def detect_skin_tone_and_palette(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return "wheatish", ["#C7B198", "#D2B48C"]

    # Image ke center se aik chota area sample karna
    h, w, _ = image.shape
    sample = image[h//3:h//2, w//3:2*w//3]
    avg_bgr = np.mean(sample, axis=(0, 1)).astype(np.uint8)
    
    # LAB space conversion for lightness
    lab = cv2.cvtColor(avg_bgr.reshape(1, 1, 3), cv2.COLOR_BGR2LAB)[0][0]
    L = lab[0]

    if L < 60:
        skin_tone = "dark"
    elif L > 85:
        skin_tone = "fair"
    else:
        skin_tone = "wheatish"

    palettes = {
        "fair": ["#A8D5BA", "#D6E4F0", "#E8F4F8", "#F0E6EF", "#E8E8E8", "#D4AF37"],
        "wheatish": ["#C7B198", "#D2B48C", "#B0C4DE", "#D8BFD8", "#F5F5DC", "#8FBC8F"],
        "dark": ["#4682B4", "#708090", "#5F9EA0", "#7B68EE", "#696969", "#2F4F4F"]
    }
    
    palette = palettes.get(skin_tone, palettes["wheatish"])
    return skin_tone, palette
