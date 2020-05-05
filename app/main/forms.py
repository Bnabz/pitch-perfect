from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    post = TextAreaField('Your pitch', validators=[Required()])
    category = SelectField('Category', choices=[('product', 'product'), ('pickup_line', 'pickup_line'), ('business', 'business')],
                           validators=[Required()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    comment = TextAreaField('Post a comment', validators=[Required()])
    submit = SubmitField('Post')


