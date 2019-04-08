from flask import Flask, session, redirect, render_template, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import UsersModel, DollsModel, DealersModel
from forms import LoginForm, RegisterForm, AddDollForm, SearchPriceForm, SearchDealerForm, AddDealerForm
from db import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
UsersModel(db.get_connection()).init_table()
CarsModel(db.get_connection()).init_table()
DealersModel(db.get_connection()).init_table()


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    if session['username'] == 'admin':
        return render_template('index_admin.html', username=session['username'])
    dolls = DollsModel(db.get_connection()).get_all()
    return render_template('car_user.html', username=session['username'], title='Просмотр базы', dolls=dolls)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        if user_model.exists(user_name)[0] and check_password_hash(user_model.exists(user_name)[1], password):
            session['username'] = user_name
            return redirect('/index')
        else:
            flash('Не верно имя пользователя или пароль')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        users = UsersModel(db.get_connection())
        if form.user_name.data in [u[1] for u in users.get_all()]:
            flash('Такой пользователь уже существует')
        else:
            users.insert(user_name=form.user_name.data, email=form.email.data,
                         password_hash=generate_password_hash(form.password_hash.data))
            return redirect(url_for('index'))
    return render_template("register.html", title='Регистрация пользователя', form=form)


@app.route('/doll_admin', methods=['GET'])
def doll_admin():
    if 'username' not in session:
        return redirect('/login')
    if session['username'] != 'admin':
        flash('Доступ запрещен')
        redirect('index')
    dolls = DollsModel(db.get_connection()).get_all()
    return render_template('doll_admin.html',
                           username=session['username'],
                           title='Просмотр кукол',
                           dolls=dolls)


@app.route('/add_doll', methods=['GET', 'POST'])
def add_doll():
    if 'username' not in session:
        return redirect('login')
    if session['username'] != 'admin':
        return redirect('index')
    form = AddDollForm()
    available_dealers = [(i[0], i[1]) for i in DealersModel(db.get_connection()).get_all()]
    form.dealer_id.choices = available_dealers
    if form.validate_on_submit():
        dolls = DollsModel(db.get_connection())
        dolls.insert(
                    price=form.price.data,
                    color_of_hair=form.color_of_hair.data,
                    rarity=form.rarity.data,
                    dealer_id=form.dealer_id.data)
        return redirect(url_for('doll_admin'))
    return render_template("add_doll.html", title='Добавление куклы', form=form)


@app.route('/doll/<int:doll_id>', methods=['GET'])
def doll(doll_id):
    if 'username' not in session:
        return redirect('/login')
    doll = DollsModel(db.get_connection()).get(doll_id)
    dealer = DealersModel(db.get_connection()).get(doll[5])
    return render_template('doll_info.html',
                           username=session['username'],
                           title='Просмотр кукол',
                           doll=doll,
                           dealer=dealer[1])


@app.route('/search_price', methods=['GET', 'POST'])
def search_price():
    form = SearchPriceForm()
    if form.validate_on_submit():
        dolls = DollsModel(db.get_connection()).get_by_price(form.start_price.data, form.end_price.data)
        return render_template('doll_user.html', username=session['username'], title='Просмотр базы', dolls=dolls)
    return render_template("search_price.html", title='Подбор по цене', form=form)


@app.route('/search_dealer', methods=['GET', 'POST'])
def search_dealer():
    form = SearchDealerForm()
    available_dealers = [(i[0], i[1]) for i in DealersModel(db.get_connection()).get_all()]
    form.dealer_id.choices = available_dealers
    if form.validate_on_submit():
        dolls = DollsModel(db.get_connection()).get_by_dealer(form.dealer_id.data)
        return render_template('doll_user.html', username=session['username'], title='Просмотр базы', dolls=dolls)
    return render_template("search_dealer.html", title='Подбор по цене', form=form)


@app.route('/dealer_admin', methods=['GET'])
def dealer_admin():
    if 'username' not in session:
        return redirect('/login')
    if session['username'] != 'admin':
        flash('Доступ запрещен')
        redirect('index')
    dealers = DealersModel(db.get_connection()).get_all()
    return render_template('dealer_admin.html',
                           username=session['username'],
                           title='Просмотр центров поставщиков',
                           dealers=dealers)


@app.route('/dealer/<int:dealer_id>', methods=['GET'])
def dealer(dealer_id):
    if 'username' not in session:
        return redirect('/login')
    if session['username'] != 'admin':
        return redirect(url_for('index'))
    dealer = DealersModel(db.get_connection()).get(dealer_id)
    return render_template('dealer_info.html',
                           username=session['username'],
                           title='Просмотр информации о центре поставщика',
                           dealer=dealer)


@app.route('/add_dealer', methods=['GET', 'POST'])
def add_dealer():
    if 'username' not in session:
        return redirect('/login')
    if session['username'] == 'admin':
        form = AddDealerForm()
        if form.validate_on_submit():
            dealers = DealersModel(db.get_connection())
            dealers.insert(name=form.name.data, address=form.address.data)
            return redirect(url_for('index'))
        return render_template("add_dealer.html", title='Добавление центра поставщика', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')