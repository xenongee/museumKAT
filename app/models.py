from app import db
from datetime import datetime
from slugify import slugify
from flask_security import UserMixin, RoleMixin


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    fullname = db.Column(db.String(256), nullable=True)
    active = db.Column(db.Boolean())

    roles = db.relationship('Role', secondary=roles_users, backref='users', lazy='dynamic')
    users_articles = db.relationship('Articles', backref='users', lazy='dynamic')
    users_stands = db.relationship('Stands', backref='users', lazy='dynamic')

    def __repr__(self):
        return '<User id: {}, name: {}>'.format(self.id, self.fullname)


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String(128))

    def __repr__(self):
        return '<Role id: {}, name: {}, description: {}>'.format(self.id, self.name, self.description)


class Articles(db.Model):
    __tablename__ = 'articles'
    article_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    img_url = db.Column(db.String, nullable=True)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __init__(self, *args, **kwargs):
        super(Articles, self).__init__(*args, **kwargs)
        self.create_slug()

    def create_slug(self):
        if self.title:
            self.slug = slugify(self.title, to_lower=True)

    def __repr__(self):
        return '<Article id: {}, title: {}>'.format(self.article_id, self.title)


class Stands(db.Model):
    __tablename__ = 'stands'
    stand_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    img_url = db.Column(db.String, nullable=True)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __init__(self, *args, **kwargs):
        super(Stands, self).__init__(*args, **kwargs)
        self.create_slug()

    def create_slug(self):
        if self.title:
            self.slug = slugify(self.title, to_lower=True)

    def __repr__(self):
        return '<Stand id: {}, title: {}>'.format(self.stand_id, self.title)
