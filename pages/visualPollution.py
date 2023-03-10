import streamlit as st

import torch
from yolov5 import detect
import os
import shutil


from PIL import Image
def load_image(image_file):
    print("Loading ",image_file)
    img = Image.open(image_file)
    img.save(os.path.join("data",image_file.name))
    return img



def app():
    cur_dir=os.getcwd()
    header=st.container()
    result_all = st.container()
    with header:
        st.subheader("Detect visual pollution in image")
        image_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
        if image_file is not None:
            # To See details
            file_details = {"filename":image_file.name, "filetype":image_file.type,
                          "filesize":image_file.size}
            st.write(file_details)

            # To View Uploaded Image
            st.image(load_image(image_file)
                ,width=500
                )
            fname=image_file.name
            image_file=os.path.join("data",fname)
        else:
            fname="test_img.jpg"
            proxy_img_file="data/"+fname
            img = Image.open(proxy_img_file)
            image_file=os.path.join(cur_dir,proxy_img_file)
            st.image(img,width=500)            


    with result_all:     
        weight_path=os.path.join(cur_dir,"yolov5/runs/train/TrainModel/weights/best.pt")
        shutil.rmtree('yolov5/runs/detect/')

        detect.run(weights=weight_path,name="TestModel", source=image_file)  
        image_file_output="yolov5/runs/detect/TestModel/"+fname
        img = Image.open(image_file_output)
        st.subheader("Visual Pollution Detections")    
        st.image(img,width=500)            
        

        