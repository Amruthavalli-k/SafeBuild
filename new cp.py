
import streamlit as st

from roboflow import Roboflow
rf = Roboflow(api_key="nB67mc0eYz8FHOWIS0A7")
project = rf.workspace().project("construction-ppe-rdhzo")
model = project.version(1).model

import pandas as pd
from pathlib import Path
import cv2
import streamlit as st

# infer on a local image
#result= model.predict("/content/pexels-everett-bumstead-5434223 (1080p).mp4", confidence=40, overlap=30).json()

def predict_file(file_path, confidence=40, overlap=30):
    # Determine file type based on extension
    file_type = Path(file_path).suffix.lower()

    if file_type in ['.jpg', '.jpeg', '.png']:
        # For images
        result = model.predict(file_path, confidence=40, overlap=30).json()
    elif file_type in ['.mp4', '.avi', '.mov']:
        # For videos
        # Implement video prediction logic here
        result = model.predict_video(file_path)
        pass
    else:
        print("Unsupported file type")

    return result


file1 = st.file_uploader("Upload a Image File")

# Example usage for an image
image_result = predict_file(r""C:\Users\neera\OneDrive\Desktop\CP\testcp3.jpeg"")
print(image_result)

# Example usage for a video (commented out, as the 'predict_video' method is hypothetical)
#video_result = predict_file("/content/pexels-everett-bumstead-5434223 (1080p).mp4")
#print(video_result)

class_list = list(prediction['class'] for prediction in image_result['predictions'])
confidence_list = list(prediction['confidence'] for prediction in image_result['predictions'])

res = pd.DataFrame(list(zip(class_list,confidence_list)), columns=['cat','conf'])
print(res)
n = len(res)
for i in range(0,n):
  if(res.cat[i]=="no hat"):
    if(res.conf[i]>=0.5):
      st.warning("No Hel",icon='⚠️')
    else:
       pass

# visualize your prediction
#model.predict("/content/testcp1.jpeg", confidence=40, overlap=30).save("prediction.jpg")

# infer on an image hosted elsewhere
#print(model.predict("/content/testcp1.jpeg", hosted=True, confidence=40, overlap=30).json())

