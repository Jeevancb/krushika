#Flask WTForms tools
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField, SelectField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Length, NumberRange, ValidationError

#Soil Test Analysis Page - Form Implementation
class SoilTestForm(FlaskForm):
    #PH Field
    ph_value = IntegerField('PH', validators=[
        DataRequired(), 
        NumberRange(min=0,max=14)
        ])
    
    #Macronutrients Fields
    magnesium_value = IntegerField('Magnesium', validators=[DataRequired()])
    phosphorus_value = IntegerField('Phosphorus', validators=[DataRequired()])
    potassium_value = IntegerField('Potassium', validators=[DataRequired()])
    calcium_value = IntegerField('Calcium', validators=[DataRequired()])
    
    #Micronutrients Fields
    boron_value = IntegerField('Boron', validators=[DataRequired()])
    iron_value = IntegerField('Iron', validators=[DataRequired()])
    zinc_value = IntegerField('Zinc', validators=[DataRequired()])
    manganese_value = IntegerField('Manganese', validators=[DataRequired()])

    #Soil Type Field
    soil_type = SelectField('Soil Type', choices=[
        ('aluvial','Aluvial Soil'),
        ('black','Black Soil'),
        ('red','Red Soil'),
        ('lateral','Lateral Soil'),
        ('mountain','Mountain Soil')])

    #Submit Button
    submitbutton = SubmitField("Verify & Submit")

#Expenditure Analysis Page - Form Implementation
class ExpenditureForm(FlaskForm):
    year_field = IntegerField('⌚Year', validators=[
        DataRequired(),
        NumberRange(min=1800, max=2100)
    ])
    seed_cost = IntegerField('🌾Seed Cost', validators=[
        DataRequired(),
        NumberRange(min=0, max=None)
    ])
    fertilizer_cost = IntegerField('🧪Fertilizer Cost', validators=[
        DataRequired(),
        NumberRange(min=0, max=None)
    ])
    irrigation_cost = IntegerField('💧Irrigation Cost', validators=[
        DataRequired(),
        NumberRange(min=0, max=None)
    ])
    labour_cost = IntegerField('🧑‍🌾Labour Cost', validators=[
        DataRequired(),
        NumberRange(min=0, max=None)
    ])
    transportation_cost = IntegerField('🚚Transportation Cost', validators=[
        DataRequired(),
        NumberRange(min=0, max=None)
    ])
    other_cost = IntegerField('🧾Other Costs', validators=[
        DataRequired(),
        NumberRange(min=0, max=None)
    ])
    yield_amount = IntegerField('🪶Yield Amount (in KGs)', validators=[
        DataRequired(),
        NumberRange(min=0, max=None)
    ])
    crop_price = IntegerField('🌿Crop Price (per KG)', validators=[
        DataRequired(),
        NumberRange(min=0, max=None)
    ])    


    submitbutton = SubmitField("Submit")

