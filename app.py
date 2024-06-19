from flask import Flask, render_template, request, redirect, flash
from config import Config
from database import init_db, insert_poll_response
from azure_storage import AzureBlobStorage
from forms import PollForm

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
app.config['SECRET_KEY'] = Config.SECRET_KEY

azure_blob_storage = AzureBlobStorage(Config.AZURE_STORAGE_CONNECTION_STRING, Config.AZURE_STORAGE_CONTAINER_NAME)

@app.route('/')
def index():
    form = PollForm()
    return render_template('index.html', form=form)

@app.route('/submit', methods=['POST'])
def submit():
    form = PollForm()
    if form.validate_on_submit():
        age = form.age.data
        gender = form.gender.data
        education = form.education.data
        support = form.support.data
        building_type = []
        if form.building_type_hospital.data:
            building_type.append('hospital')
        if form.building_type_school.data:
            building_type.append('school')
        if form.building_type_mall.data:
            building_type.append('mall')
        if form.building_type_park.data:
            building_type.append('park')
        if form.building_type_office.data:
            building_type.append('office')
        environment_importance = form.environment_importance.data
        opinion = form.opinion.data

        file_url = None
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename != '':
                file_url = azure_blob_storage.upload_file(file)

        try:
            insert_poll_response(age, gender, education, support, building_type, environment_importance, opinion, file_url)
            flash('Your response has been submitted successfully!', 'success')
        except Exception as e:
            flash(str(e), 'danger')

        return redirect('/')
    else:
        flash('There was an error with your submission. Please check your inputs and try again.', 'danger')
        return render_template('index.html', form=form)

if __name__ == '__main__':
    init_db()
    app.run()
