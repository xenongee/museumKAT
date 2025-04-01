from app import db
from flask import Blueprint, render_template, request, redirect, url_for
from flask_security import login_required
from models import Stands, Users
from .stands_forms import StandsForm
from lib.ListPrepare import ListPrepare
from lib.StandsMenu import StandsMenu


stands = Blueprint('museumstands', __name__, template_folder='templates')


@stands.route('/create_stand', methods=['POST', 'GET'])
@login_required
def create_stand():
    standsMenu = StandsMenu.standslist
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        try:
            stand = Stands(title=title, content=content)
            db.session.add(stand)
            db.session.commit()
        except:
            print('Something wrong')
        return redirect(url_for('museumstands.stands_index'))

    form = StandsForm()
    return render_template(
        'create_or_update_stand.html',
        title=True,
        standsMenu=standsMenu,
        create=True,
        form=form,
        author='Иван Иванович'
    )


@stands.route('/<slug>/edit_stand', methods=['POST', 'GET'])
@login_required
def edit_stand(slug):
    standsMenu = StandsMenu.standslist
    stands = Stands.query.filter(Stands.slug == slug).first_or_404()

    if request.method == 'POST':
        form = StandsForm(formdata=request.form, obj=stands)
        form.populate_obj(stands)
        db.session.commit()

        return redirect(url_for('museumstands.stand_page', slug=stands.slug))

    form = StandsForm(obj=stands)
    return render_template(
        'create_or_update_stand.html',
        title=True,
        standsMenu=standsMenu,
        update=True,
        slug=stands.slug,
        form=form
    )


@stands.route('/')
def stands_index():
    standsMenu = StandsMenu.standslist
    stands_list = Stands.query.order_by(Stands.stand_id)

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    paginate = stands_list.paginate(page=page, per_page=6)
    stands = ListPrepare(paginate.items, 'stand_id')
    stands = stands.get_list()
    return render_template(
        'stands/index.html',
        activeButtonState=2,
        title=True,
        standsMenu=standsMenu,
        pageName='Стенды музея',
        stands=stands,
        paginate=paginate
    )


@stands.route('/<slug>')
def stand_page(slug):
    standsMenu = StandsMenu.standslist
    stand = Stands.query.filter(Stands.slug == slug).first_or_404()
    if stand.user_id_fk:
        user = Users.query.filter(Users.id == stand.user_id_fk).first()
        user = user.fullname
    else:
        user = ''

    return render_template(
        'stand.html',
        activeButtonState=2,
        title=True,
        standsMenu=standsMenu,
        stand=stand,
        author=user,
        slug=slug
    )
