# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Resource, Api, reqparse, request
import pandas as pd
import csv
import os
import io
from google.cloud import vision
#from google.cloud import storage
from PIL import Image
import numpy as np
from dotenv import load_dotenv
import waitress


app = Flask(__name__)
api = Api(app)


# google vision access key
gvision_access_json = "client_secret_698428564418-u9q0hmtd5t2ggm14rbvsrotph76ni8u8.apps.googleusercontent.com.json"

# AWS access key
load_dotenv()
access_key_id = os.getenv('access_key_id')
secret_access_key = os.getenv('secret_access_key')


def cross_match(det_OCR_list):

    #####Setting up Harmful Chemicals Dataset as List#####

    with open("dataset/harmful_chemicals_cosmetics.csv", newline='', encoding='latin-1') as f:
        reader1 = csv.reader(f)
        chemicals = list(reader1)
        chemicals.pop(0)

    chemicals_list=[]
    for i in range(len(chemicals)):
        chemicals_list.append(chemicals[i][0])

    #Converting list to dict for faster operation, 6.6x faster
    chemicals_dict = {}
    for b in chemicals_list:
        chemicals_dict[b] = chemicals_list.index(b) 
    #print(chemicals_list)

    #Dict. chemical_detected = TRUE or FALSE, if TRUE, chemical_names = [list of chemicals]
    detected_chemicals = {'chemical_detected': "", 'chemical_names': []}


    #Cross-matching detected chemicals with chemicals_dict
    for det in det_OCR_list:
        if (det in chemicals_dict.keys()) and (det not in detected_chemicals['chemical_names']):
            detected_chemicals["chemical_names"].append(det) 
        else:
            pass
    #Check if chemical_names list is populated
    if bool(detected_chemicals["chemical_names"]):
        detected_chemicals['chemical_detected'] = True
    else:
        detected_chemicals['chemical_detected'] = False
    
        
    #Output
    if ( (detected_chemicals['chemical_detected'] == True) ):
        return(detected_chemicals)
    else:
        return str(False)

@app.route('/chems/', methods = ['POST'])
def detect_text_uri(uri):
    if request.method != 'POST':
        return("Error 405 - Method Not Allowed")
    else:

        """Detects text in the file located in Google Cloud Storage or on the Web.
        """
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = uri

        response = client.text_detection(image=image)
        texts = response.text_annotations
        print('Texts:')

        det_OCR_list = []

        for text in texts:
            if text in det_OCR_list:
                pass
            else:
                det_OCR_list.append(text.description)

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        #return str(logo_list)
        return cross_match(det_OCR_list)