from flask_wtf import FlaskForm
from wtforms.validators import InputRequired,Length,Email
from wtforms import StringField,TextAreaField,PasswordField,EmailField,SubmitField,ValidationError,SelectField,DateField

class RegisterForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(),Length(min=4,max=15)])
    email = EmailField("email", validators=[InputRequired(), Length(max=150)])
    password = PasswordField("password",validators=[InputRequired(),Length(min=6,max=15)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField("email", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    submit = SubmitField("Login")

class TaskForm(FlaskForm):
    title = StringField("Task Title", validators=[InputRequired(), Length(max=150)])
    description = TextAreaField("Description")
    due_date = DateField("Due Date", format='%Y-%m-%d', validators=[InputRequired()])

    priority = SelectField("Priority", choices=[
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low')
    ])

    category = SelectField("Category", choices=[
        ('Work', 'Work'),
        ('Personal', 'Personal'),
        ('Health', 'Health'),
        ('Study', 'Study')
    ])

    submit = SubmitField("Create Task")

class UpdateForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
    email = EmailField("email", validators=[InputRequired(), Length(max=150)])
    submit = SubmitField("Update")