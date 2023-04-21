from flask import Flask, render_template, redirect, url_for, flash, request, Blueprint, abort
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_migrate import Migrate
from werkzeug.urls import url_parse
from models import *
from forms import *
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
import os
from jinja2 import Environment
import base64



app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static'
db.init_app(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'






@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/home')
def index():
    # with open('D:/market/market/static/images/qaz_thumb.png', 'rb') as f:
    #     image_data = base64.b64encode(f.read()).decode()

    # image = Product(name='xxxxx', description='aaa', price=112, quantity=1, image=image_data, category='sdsd', seller_id=4)
    # db.session.add(image)
    # db.session.commit()

    return render_template('home.html', products=Product.query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильная почта или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('lc'))
        # next_page = request.args.get('next')
        # # if not next_page or url_parse(next_page).netloc != '':
        # #     next_page = url_for('index')
        # # return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/lc')
@login_required
def lc(): 
    return render_template('all.html')

@app.route('/uploadproduct', methods=['GET', 'POST'])
def upload():
    form = ProductForm()
    if form.validate_on_submit():
        image = Product(name=form.name.data, description=form.description.data, price=form.price.data, quantity=form.quantity.data, image=base64.b64encode(form.image.data.read()).decode(), category=form.category.data, seller_id=current_user.id)
        db.session.add(image)
        db.session.commit()
        return redirect(url_for('lc'))
    return render_template('product.html', title='nnn', form=form)




class UserView(ModelView):
    def is_accessible(self):
        return current_user.role == 'admin'


class ProductView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def get_query(self):
        if current_user.role == 'admin':
            return self.session.query(self.model)
        # else:
        #     return self.session.query(self.model).filter_by(seller_id=current_user.id)
        
    def get_count_query(self):
        if current_user.role == 'admin':
            return db.session.query(db.func.count(self.model.id))
        


        

class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(404)  # Forbidden
        return super().index()

    


admin = Admin(app, index_view=CustomAdminIndexView())
admin.add_view(UserView(User, db.session))
admin.add_view(ProductView(Product, db.session, category='Products', name='Edit Products'))



if __name__ == '__main__':
    app.run(debug=True)