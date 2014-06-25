"""upload.py - API for Upload."""
import os
from flask import Blueprint, request, jsonify
from werkzeug import secure_filename
from app import app

upload_api = Blueprint('upload_api', __name__, url_prefix='/api/upload')


# Route that will process the file upload
@upload_api.route('', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files.to_dict()['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        filelocation = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        i = 1
        temp_file = filename
        while(os.path.isfile(filelocation)):
            temp_file = filename.rsplit('.')[0] + '_' + str(i) + '.' + filename.rsplit('.')[1]
            filelocation = os.path.join(app.config['UPLOAD_FOLDER'],
                                        temp_file)
            i += 1
        file.save(filelocation)
        return jsonify(file=temp_file)
    else:
        return jsonify(error="Filetype not supported."), 400


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
