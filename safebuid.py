import streamlit as st
from roboflow import Roboflow
import pandas as pd
from pathlib import Path

# Initialize Roboflow
rf = Roboflow(api_key="nB67mc0eYz8FHOWIS0A7")
project = rf.workspace().project("construction-ppe-rdhzo")
model = project.version(1).model

def predict_file(file_path, confidence=40, overlap=30):
    # Determine file type based on extension
    file_type = Path(file_path).suffix.lower()

    if file_type in ['.jpg', '.jpeg', '.png']:
        # For images
        result = model.predict(file_path, confidence=confidence, overlap=overlap).json()
    elif file_type in ['.mp4', '.avi', '.mov']:
        # For videos
        # Implement video prediction logic here
        result = model.predict_video(file_path)
        pass
    else:
        print("Unsupported file type")

    return result
from PIL import Image
logo = Image.open('Sabu1.jpeg')
icon = Image.open('Sabu1.jpeg')

st.set_page_config(page_title="Safe Build", page_icon=icon, layout="wide")
st.image(logo)
st.title("SAFE BUILD-AI at the Helm, Building a Safer Future.")
st.image(icon,width=900)

# Use st.file_uploader to allow users to upload an image file
file1 = st.file_uploader("Upload an Image File", type=["jpg", "jpeg", "png"])

# Check if a file is uploaded
if file1 is not None:
    # Example usage for an image
    image_result = predict_file(file1.name)
    print(image_result)

    # Extract class and confidence lists from the result
    class_list = [prediction['class'] for prediction in image_result['predictions']]
    confidence_list = [prediction['confidence'] for prediction in image_result['predictions']]

    # Create a DataFrame for visualization
    res = pd.DataFrame(list(zip(class_list, confidence_list)), columns=['cat', 'conf'])
    print(res)

    # Display warnings for 'no hat' predictions with confidence >= 0.5
    for i in range(len(res)):
        if res.cat[i] == "no hat" and res.conf[i] >= 0.5:
            st.warning("No Helmet Detected", icon='⚠️')

# Note: The above code assumes that the 'model.predict_video' method is implemented in the Roboflow library.
# You may need to check the Roboflow documentation for the correct usage.
