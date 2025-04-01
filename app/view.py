from app import app, security
from flask import render_template, request, redirect, url_for
from flask_security import login_required
from models import Users, Role, Articles, Stands
from lib.ListPrepare import ListPrepare
from lib.StandsMenu import StandsMenu


@app.route('/index')
@app.route('/')
def index_page():
    standsMenu = StandsMenu.standslist
    articles_list = Articles.query.order_by(Articles.article_id.desc())

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    paginate = articles_list.paginate(page=page, per_page=8)
    articles = ListPrepare(paginate.items, 'article_id', reverse=True)
    articles = articles.get_list(articlepage=True)


    return render_template(
        'index.html',
        activeButtonState=1,
        jumbotron_img_url='files/images/stands-headers/kat-front-fasad.jpg',
        title=False,
        standsMenu=standsMenu,
        pageName='Добро пожаловать в Музей профессионального образования!',
        articles=articles,
        paginate=paginate
    )


@app.route('/adminpanel')
@login_required
def admin_redirect():
    return redirect('admin/')


@app.route('/about')
def about_page():
    standsMenu = StandsMenu.standslist
    article = Articles.query.filter(Articles.slug == 'o-muzee').first()
    user = Users.query.filter(Users.id == article.user_id_fk).first()

    return render_template(
        'about.html',
        pageName=article.title,
        activeButtonState=3,
        title=True,
        standsMenu=standsMenu,
        contents=article.content,
        author=user.fullname
    )


@app.route('/search')
def search_page():
    standsMenu = StandsMenu.standslist
    q = request.args.get('q')
    rendertemplate = render_template(
        'search.html',
        activeButtonState=4,
        title=True,
        standsMenu=standsMenu,
        notfound=True,
        pageName='Ничего не найдено!',
        contents='''
            По вашему запросу "{}" ничего не нашлось. <br><br>
            Рекомендации: <br>
            <ul>
                <li>Убедитесь, что все слова написаны без ошибок.</li>
                <li>Попробуйте использовать другие ключевые слова.</li>
                <li>Попробуйте использовать более популярные ключевые слова.</li>
            </ul>
        '''.format(q)
    )
    if q is not None and len(q) == 0:
        return rendertemplate
    else:
        qc = q.capitalize()
        ql = q.lower()
        print(qc, ql)
        articlesCapital = Articles.query.filter(Articles.title.contains(qc) | Articles.content.contains(qc)).all()
        articlesLower = Articles.query.filter(Articles.title.contains(ql) | Articles.content.contains(ql)).all()
        standsCapital = Stands.query.filter(Stands.title.contains(qc) | Stands.content.contains(qc)).all()
        standsLower = Stands.query.filter(Stands.title.contains(ql) | Stands.content.contains(ql)).all()

        searchResult = []
        if len(articlesCapital) >= 1:
            searchResult.extend(articlesCapital)
        if len(articlesLower) >= 1:
            searchResult.extend(articlesLower)
        if len(standsCapital) >= 1:
            searchResult.extend(standsCapital)
        if len(standsLower) >= 1:
            searchResult.extend(standsLower)

        searchResult = ListPrepare(searchResult, sortkey='', reverse=True)
        searchResult = searchResult.get_list(articlepage=True)
        searchResult = list(set(searchResult))
        # searchResult = [el for el, _ in groupby(searchResult)]
        print(searchResult)
        if searchResult and len(searchResult) >= 1:
            return render_template(
                'search.html',
                activeButtonState=4,
                notfound=False,
                standsMenu=standsMenu,
                searchResult=searchResult,
                pageName='Результаты поиска по запросу: {}'.format(q)
            )
        else:
            return rendertemplate


# errors
@app.errorhandler(404)
def page_not_found(e):
    standsMenu = StandsMenu.standslist
    return render_template(
        'error.html',
        error=True,
        pageName='Ошибка 404, страница отсуствует',
        standsMenu=standsMenu,
        contents=e
    ), 404


@app.errorhandler(403)
def page_forbidden(e):
    standsMenu = StandsMenu.standslist
    return render_template(
        'error.html',
        error=True,
        customImageURL='images/placeholders/placeholder_700x500.jpg',
        pageName='Ошибка 403, доступ запрещен',
        standsMenu=standsMenu
    ), 403


@app.errorhandler(500)
def page_internal_server_error(e):
    standsMenu = StandsMenu.standslist
    return render_template(
        'error.html',
        error=True,
        customImageURL='images/placeholders/placeholder_700x500.jpg',
        pageName='Ошибка 500, ошибка сервера',
        standsMenu=standsMenu
    ), 500
