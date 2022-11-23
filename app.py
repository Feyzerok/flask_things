import os
from flask import Flask
from flask_admin import Admin, form
from exts import db
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from flask_babelex import Babel
from flask_admin.babel import gettext
from views import ThemeView, ResView, BuildsView, ProductView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = 'gfgfgghghgfhgfhgfhgfhfgghghghghghg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                                    "data/em_resources.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['STORAGE'] = os.path.abspath('data/temp')

app_context = app.app_context()
app_context.push()

db.init_app(app)


babel = Babel(app)
migrate = Migrate(app, db)

"""Локализация админ панели"""
@babel.localeselector
def get_locale():
    # Put your logic here. Application can store locale in
    # user profile, cookie, session, etc.
    return 'ru'


"""Administrative views"""
from models import Resources, Grade, Subject, Themes, Series, Builds, Products


admin = Admin(app, name='database', template_mode='bootstrap4')
admin.add_view(ResView(Resources, db.session, name='Ресурсы'))
admin.add_view(ModelView(Grade, db.session, name='Классы'))
admin.add_view(ModelView(Subject, db.session, name='Предметы'))
admin.add_view(ThemeView(Themes, db.session, name='Темы'))
admin.add_view(ModelView(Series, db.session, name='Серии'))
admin.add_view(BuildsView(Builds, db.session, name='Сборки'))
admin.add_view(ProductView(Products, db.session, name='Продукты'))


""" Здесь будет функция login """
#@app.route('/login/', methods=['post', 'get'])
#def login():
#    form = LoginForm()
#    if form.validate_on_submit():
#	user = db.session.query(User).filter(User.username == form.username.data).first()
#	if user and user.check_password(form.password.data):
#	    login_user(user, remember=form.remember.data)
#	    return redirect(url_for('admin'))
#
#	flash("Invalid username/password", 'error')
#	return redirect(url_for('login'))
#    return render_template('login.html', form=form)

if __name__ == '__main__':
    db.create_all()
    db.session.commit()

    #from data.constant_subjects_grades_series import subjects, grades, series
    #from db_worker import prepare_const_data, fill_products_data
    #path_to_json = os.path.join('data', 'products.json')
    #prepare_const_data(db, subjects, grades, series)
    #fill_products_data(db, path_to_json)


    app.run(host='0.0.0.0')
