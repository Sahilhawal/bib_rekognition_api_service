import base64
from flask import Flask, current_app

import json
from crypt import methods
from email import message
from email.mime import image

import boto3
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from flaskr.db import get_db

# from flaskr.bib_functions import get_photos_for_bib
from .bib_functions import get_bib_to_photo_mappings, get_list_of_photos_from_s3bucket, get_photos_for_bib, get_texts_in_image, map_images_to_bib_number

bp = Blueprint('bib_photos', __name__)

@bp.route('/test/', defaults={'bib_number': None})
@bp.route('/test/<bib_number>')
def get_photos(bib_number):
    # test_function()
    print( current_app.config,)
    print( current_app.name,)
    bib_to_photo_mappings=get_bib_to_photo_mappings(bib_number)
    return render_template('bib_photos/index.html', bib_to_photo_mappings=bib_to_photo_mappings)

@bp.route('/create-mapping',methods=('POST',))
def create_mappings_for_S3_images():
    S3_bucket_images = get_list_of_photos_from_s3bucket()
    map_images_to_bib_number(S3_bucket_images)
    return {'message': 'Created'},201

@bp.route('/detect-image-text', methods=('POST',))
def detect_image_text():
    image = request.files["photo"]
    image_bytes = image.read()
    textDetections=get_texts_in_image(image_bytes)
    encoded_string = base64.b64encode(image_bytes).decode()   
    request_data = {
      'img_data':encoded_string,
      'textDetections':textDetections
    }
    return render_template('bib_photos/index.html', **request_data)

