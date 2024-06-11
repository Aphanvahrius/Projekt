from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
from database import init_db, insert_poll_response
from azure_storage import AzureBlobStorage

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
    attachment = request.files['attachment']

    # Handle file upload
    if attachment:
        filename = secure_filename(attachment.filename)
        attachment.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = None

    # Insert data into the database
    try:
        insert_poll_response(age, gender, education, support, building_type, environment_importance, opinion, filename)
        flash('Your response has been submitted successfully!', 'success')
    except Exception as e:
        flash(str(e), 'danger')

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
