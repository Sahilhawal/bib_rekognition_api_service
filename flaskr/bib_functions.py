from flaskr.db import get_db
from flask import Flask, current_app, Blueprint



def detect_text_and_create_mapping(photo, bucket):
    client=boto3.client('rekognition', region_name='ap-south-1')
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    textDetections=response['TextDetections']
    for text in textDetections:
        if text['Type'] == 'WORD':
            bib_number = text['DetectedText'];
            insert_bib_photo_mapping(bib_number, photo)

def get_photos_for_bib(bib_number):
    db = get_db()
    bib_to_photo_mappings = db.execute(
        'SELECT *'
        ' FROM photo_to_bib_mapping p'
        ' WHERE p.bib_number = ?',
        (bib_number,)
    ).fetchall()

    return bib_to_photo_mappings        

def get_all_photos():
    db = get_db()
    bib_to_photo_mappings = db.execute(
        'SELECT *'
        ' FROM photo_to_bib_mapping p'
    ).fetchall()

    return bib_to_photo_mappings        

def insert_bib_photo_mapping(bib_number, photo):
    db = get_db()
    db.execute(
        'INSERT INTO photo_to_bib_mapping (bib_number, photo)'
        ' VALUES (?, ?)',
        (bib_number, photo )
    )
    db.commit()

def get_bib_to_photo_mappings(bib_number):    
    if bib_number is not None:
        bib_to_photo_mappings = get_photos_for_bib(bib_number)
    else: 
        bib_to_photo_mappings = get_all_photos()

    return bib_to_photo_mappings

def get_list_of_photos_from_s3bucket():
    s3client=boto3.client('s3', region_name='ap-south-1')
    S3_bucket_images = s3client.list_objects(Bucket='mysecondawsbucketsahil')['Contents']
    return S3_bucket_images

def map_images_to_bib_number(image_list):
    for image in image_list:
        bucket='mysecondawsbucketsahil'
        photo=image['Key']
        detect_text_and_create_mapping(photo,bucket)

def get_texts_in_image(image_bytes):
    client=boto3.client('rekognition')
    response = client.detect_text(Image={'Bytes': image_bytes})
    textDetections=response['TextDetections']
    return textDetections

def test_function():
    print('======== Prinitng test function')


# with app.app_context():
#     # within this block, current_app points to app.
#     print(current_app.config,)