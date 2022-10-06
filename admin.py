from flask import Flask
from flask_admin import Admin
from models import db, Rubricator, Resources, Class, Subject
from flask_admin.contrib.peewee import ModelView
#from forms import ContactForm, LoginForm
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from flask_babelex import Babel
from model_views import MyView


app = Flask(__name__)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = 'gfgfgghghgfhgfhgfhgfhfgghghghghghg'

babel = Babel(app)

@babel.localeselector
def get_locale():
        # Put your logic here. Application can store locale in
        # user profile, cookie, session, etc.
        return 'ru'

admin = Admin(app, name='database', template_mode='bootstrap4')
admin.add_view(ModelView(Resources, name='Ресурсы'))
admin.add_view(ModelView(Rubricator, name='Рубрикатор'))
admin.add_view(ModelView(Class, name="Класс"))
admin.add_view(ModelView(Subject, name="Предмет"))
admin.add_view(MyView(Resources, name='Ресурсы'))

# Add administrative views here

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


app.run()
