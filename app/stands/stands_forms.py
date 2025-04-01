from wtforms import Form, StringField, TextAreaField


class StandsForm(Form):
    title = StringField()
    slug = StringField()
    image_header = StringField()
    content = TextAreaField()
