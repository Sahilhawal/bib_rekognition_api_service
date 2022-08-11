from flaskr.db import get_db
from flask import Flask, current_app, Blueprint


# test_bp = Blueprint('test_bp', __name__)

def get_photos_for_bib(bib_number):
    db = get_db()
    bib_to_photo_mappings = db.execute(
        'SELECT *'
        ' FROM photo_to_bib_mapping p'
    ).fetchall()

    print('======== Prinitng test function')
    print(bib_to_photo_mappings)
    return bib_to_photo_mappings  

def test_function():
    print('======== Prinitng test function')


# with app.app_context():
#     # within this block, current_app points to app.
#     print(current_app.config,)