from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError

class MainForm(FlaskForm):
    vehicle_Type = SelectField('Vehicle Type', validators=[DataRequired()],
                               choices=[('Bike', 'Bike'), ('Car', 'Car'), ('Bus', 'Bus'), ('Truck', 'Truck'),
                                        ('Others', 'Others')])
    vehicle_no = StringField('Vehicle Number', validators=[DataRequired()])
    vehicle_model = StringField('Vehicle model')
    register_owner = StringField('Register owner', validators=[DataRequired()])
    current_owner = StringField('Current owner', validators=[DataRequired()])
    phone_number = StringField('Phone number', validators=[DataRequired()])

    # Pollution-related fields
    pollution = RadioField('Pollution', validators=[DataRequired()], choices=[('Yes', 'Yes'), ('No', 'No')])
    pollution_expire = SelectField('Pollution expire', choices=[(12, '1 Year'), (6, '6 Months')],
                                   validators=[Optional()])
    pollution_price = IntegerField('Pollution Price', validators=[Optional()])

    # Insurance-related fields
    insurance = RadioField('Insurance', validators=[DataRequired()], choices=[('Yes', 'Yes'), ('No', 'No')])
    insurance_expire = SelectField('Insurance expire', choices=[(12, '1 Year'), (6, '6 Months')],
                                   validators=[Optional()])
    policy_number = StringField('Policy Number', validators=[Optional()])
    insurance_price = IntegerField('Insurance Price', validators=[Optional()])

    submit = SubmitField('Submit')

    def validate_pollution_expire(self, field):
        if self.pollution.data == 'Yes' and not field.data:
            raise ValidationError('Pollution expire is required when Pollution is Yes.')

    def validate_pollution_price(self, field):
        if self.pollution.data == 'Yes' and not field.data:
            raise ValidationError('Pollution price is required when Pollution is Yes.')

    def validate_insurance_expire(self, field):
        if self.insurance.data == 'Yes' and not field.data:
            raise ValidationError('Insurance expire is required when Insurance is Yes.')

    def validate_insurance_price(self, field):
        if self.insurance.data == 'Yes' and not field.data:
            raise ValidationError('Insurance price is required when Insurance is Yes.')

    def validate_policy_number(self, field):
        if self.insurance.data == 'Yes' and not field.data:
            raise ValidationError('Policy Number is required when Insurance is Yes.')
