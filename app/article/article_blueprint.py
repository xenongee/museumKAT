from app import db
from flask import Blueprint, render_template, request, redirect, url_for
from flask_security import login_required
from models import Articles, Users
from .article_forms import ArticleForm
from lib.StandsMenu import StandsMenu


article = Blueprint('article', __name__, template_folder='templates')


@article.route('/create_article', methods=['POST', 'GET'])
@login_required
def create_article():
    standsMenu = StandsMenu.standslist
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        try:
            article = Articles(title=title, content=content)
            db.session.add(article)
            db.session.commit()
        except:
            print('Something wrong')
        return redirect(url_for('index_page'))

    form = ArticleForm()
    return render_template(
        'create_or_update_article.html',
        title=True,
        standsMenu=standsMenu,
        create=True,
        form=form,
        author='Иван Иванович'
    )


@article.route('/<slug>/edit_article', methods=['POST', 'GET'])
@login_required
def edit_article(slug):
    standsMenu = StandsMenu.standslist
    article = Articles.query.filter(Articles.slug == slug).first_or_404()

    if request.method == 'POST':
        form = ArticleForm(formdata=request.form, obj=article)
        form.populate_obj(article)
        db.session.commit()

        return redirect(url_for('article.article_index', slug=article.slug))

    form = ArticleForm(obj=article)
    return render_template(
        'create_or_update_article.html',
        title=True,
        standsMenu=standsMenu,
        update=True,
        slug=article.slug,
        form=form
    )


@article.route('/<slug>')
def article_index(slug):
    standsMenu = StandsMenu.standslist
    article = Articles.query.filter(Articles.slug == slug).first_or_404()
    if article.user_id_fk:
        user = Users.query.filter(Users.id == article.user_id_fk).first()
        user = user.fullname
    else:
        user = ''

    return render_template(
        'article/index.html',
        title=True,
        standsMenu=standsMenu,
        article=article,
        author=user,
        slug=slug,
        date='05.09.78',
        time='12:42'
    )
