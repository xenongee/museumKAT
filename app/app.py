import os.path as op

from flask import Flask, request, redirect, url_for
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_security import SQLAlchemyUserDatastore, Security, current_user
from flask_babelex import Babel

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


# Admin
from models import Articles, Stands, Users, Role


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class MainMixin:
    def is_accessible(self):
        return (current_user.has_role('admin') or current_user.has_role('redactor'))

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.create_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class UsersView(AdminView):
    excluded_list_columns = ('password')


class HomeAdminView(MainMixin, AdminIndexView):
    pass


class ArticleView(MainMixin, BaseModelView):
    excluded_list_columns = ('content', 'img_url')
    form_columns = ['title', 'content', 'img_url', 'users']
    pass


class StandsView(MainMixin, BaseModelView):
    excluded_list_columns = ('content', 'img_url')
    form_columns = ['title', 'content', 'img_url', 'users']
    pass


## Create directory
path = op.join(op.dirname(__file__), 'static/files')

## Create admin interface
admin = Admin(app, 'Музей профессионального образования', url='/', index_view=HomeAdminView(name='Главная'), base_template='layout/layout.html', template_mode='bootstrap3')
admin.add_view(ArticleView(Articles, db.session, 'Статьи'))
admin.add_view(StandsView(Stands, db.session, 'Стенды'))
admin.add_view(UsersView(Users, db.session, 'Пользователи'))
admin.add_view(AdminView(Role, db.session, 'Роли пользователей'))
admin.add_view(FileAdmin(path, '/static/files/', name='Файлы'))


# Flask Security
user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
security = Security(app, user_datastore)

babel = Babel(app, 'ru')