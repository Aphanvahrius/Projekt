from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class PollForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    education = SelectField('Education', choices=[('none', 'None'), ('high_school', "High School"), ("bachelor", "Bachelor's Degree"), ('master', "Master's Degree"), ('doctorate', 'Doctorate')], validators=[DataRequired()])
    support = SelectField('Support', choices=[('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
    building_type_hospital = BooleanField('Hospital')
    building_type_school = BooleanField('School')
    building_type_mall = BooleanField('Shopping Mall')
    building_type_park = BooleanField('Park')
    building_type_office = BooleanField('Office Building')
    environment_importance = SelectField('Environment Importance', choices=[('very_important', 'Very Important'), ('somewhat_important', 'Somewhat Important'), ('not_important', 'Not Important')], validators=[DataRequired()])
    opinion = TextAreaField('Opinion', validators=[Length(max=500)])
