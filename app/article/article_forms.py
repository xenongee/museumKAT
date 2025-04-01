from wtforms import Form, StringField, TextAreaField


class ArticleForm(Form):
    title = StringField()
    content = TextAreaField()
