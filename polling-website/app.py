from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
from database import init_db, insert_poll_response
from azure_storage import AzureBlobStorage

azure_blob_storage = AzureBlobStorage(Config.AZURE_STORAGE_CONNECTION_STRING, Config.AZURE_STORAGE_CONTAINER_NAME)

app = Flask(__name__)
app.config.from_object(Config)

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    age = request.form['age']
    gender = request.form['gender']
    education = request.form['education']
    support = request.form['support']
    building_type = request.form.getlist('building_type')
    environment_importance = request.form['environment_importance']
    opinion = request.form.get('opinion', '')
        
    file_url = None
    if 'attachment' in request.files:
        file = request.files['attachment']
        if file and file.filename != '':
            file_url = azure_blob_storage.upload_file(file)


    # Insert data into the database
    try:
        insert_poll_response(age, gender, education, support, building_type, environment_importance, opinion, file_url)
        flash('Your response has been submitted successfully!', 'success')
    except Exception as e:
        flash(str(e), 'danger')

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
