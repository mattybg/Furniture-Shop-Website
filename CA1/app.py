#admin username : password
#      Admin : 04K13!D04K13

from flask import Flask, render_template, session, redirect, url_for, g, request  
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, SortForm, ProductForm, DeleteForm
from functools import wraps

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.config["SESSION_TYPE"] = "filesystem" 
app.config["SESSION_PERMANENT"] = False
Session(app)




@app.before_request
def logged_in_user():
    g.user = session.get("user_id", None)
    g.admin = session.get("adminLogged", False)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url)) 
        return view(*args, **kwargs)
    return wrapped_view 


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data 
        db = get_db()
        possible_clashing_user = db.execute("""SELECT * FROM users
        WHERE user_id =?;""", (user_id,)).fetchone()
        if possible_clashing_user is not None:
            form.user_id.errors.append("User id already taken!")
        else:
            db.execute("""INSERT INTO users (user_id, password) VALUES (?, ?);""",
                (user_id, generate_password_hash(password)))
            db.commit()
            return redirect( url_for("login") )
    return render_template("register.html", form=form)
 
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        possible_clashing_user = db.execute("""SELECT * FROM users
        WHERE user_id = ?;""", (user_id,)).fetchone()
        if possible_clashing_user is None:
            form.user_id.errors.append("No such user!")
        elif not check_password_hash(possible_clashing_user["password"], password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["user_id"] = user_id
            if user_id == "Admin":
                session["adminLogged"] = True            
            next_page = request.args.get("next")
            if not next_page:
                next_page=url_for("index")
            return redirect(next_page)
    return render_template("login.html", form=form) 

@app.route("/logout")
def logout():
    session.clear()
    return redirect( url_for("index") ) 

@app.route("/products", methods=["GET", "POST"])
def products():
    db = get_db()
    form = SortForm()
    if form.validate_on_submit():
        sort_order = request.form.get("sort_by", "asc") #yt link hereeeee <--------
        if sort_order == "asc":
            products = db.execute("""SELECT * FROM products 
                                    ORDER BY price ASC""").fetchall()
        else:
            products = db.execute("""SELECT * FROM products 
                                    ORDER BY price DESC""").fetchall()
    else:
        products = db.execute("""SELECT * FROM products""").fetchall()
    return render_template("products.html", products=products, form=form)
 
@app.route("/product/<int:product_id>")
def product(product_id):  
    db = get_db()
    product = db.execute("""SELECT * FROM products
                            WHERE product_id = ?;""", (product_id,)).fetchone()
    return render_template("product.html", product=product)

@app.route("/add_to_cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = {}
    if product_id not in session["cart"]:
        session["cart"][product_id] = 1
    return redirect(url_for("cart"))



@app.route("/cart")
@login_required
def cart():
    if "cart" not in session:
        session["cart"] = {}
    names = {}
    db = get_db()
    cart_items = []
    for product_id in session["cart"]:
        product = db.execute("""SELECT * FROM products
                    WHERE product_id = ?;""", (product_id,)).fetchone()
        name = product["name"]
        names[product_id] = name
        cart_items.append({"product": product, "quantity": session["cart"][product_id], "price": product["price"], "total": product["price"] * session["cart"][product_id]})
    total_price = sum([item["total"] for item in cart_items])
    return render_template("cart.html", cart=cart_items, names=names, total_price=total_price)


@app.route("/checkout")
@login_required
def checkout():
    if "cart" not in session or not session["cart"]:
        return redirect(url_for("cart"))
    db = get_db()
    user_id = g.user
    total_price = 0
    for product_id, quantity in session["cart"].items():
        product = db.execute("""SELECT * FROM products
                                WHERE product_id = ?;""", (product_id,)).fetchone()
        total_price += product["price"] * quantity
    db.execute("""INSERT INTO orders (user_id, total_price)
                   VALUES (?, ?);""", (user_id, total_price))
    order_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    for product_id, quantity in session["cart"].items():
        product = db.execute("""SELECT * FROM products
                                WHERE product_id = ?;""", (product_id,)).fetchone()
    session["cart"] = {}
    db.commit()
    return render_template("checkout.html", order_id=order_id, total_price=total_price)

@app.route("/myaccount")
@login_required
def myaccount():
    user_id = g.user
    db = get_db()
    orders = db.execute(
        """SELECT * FROM orders WHERE user_id = ?""", (user_id,)).fetchall()
    return render_template("myaccount.html", orders=orders)


@app.route("/admin")
@login_required
def admin():
    if g.admin:
        user_id = g.user
        db = get_db()
        orders = db.execute(
            """SELECT * FROM orders""",).fetchall()
        return render_template("admin.html", orders=orders)
    else:
        return redirect(url_for("login"))

@app.route("/admin/delete<int:order_id>")
@login_required
def delete(order_id):
    if g.admin:
        db = get_db()
        db.execute("""DELETE FROM orders WHERE order_id = ?""", (order_id,))
        db.commit()
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("login"))
    
    


@app.route("/admin/addproduct", methods=["GET", "POST"])
@login_required
def add_product(): 
    if g.admin:
        form = ProductForm()
        message = ""
        if form.validate_on_submit():
            name = form.name.data
            price = form.price.data
            description = form.description.data
            image = form.image.data
            db = get_db() 
            clashing_product = db.execute("""SELECT * FROM products where name = ?;""", (name,)).fetchone()
            if clashing_product is not None: 
                form.name.errors.append("Product already exists")
            else: 
                db.execute("""INSERT INTO products (name, price, description, image) VALUES (?, ?, ?,?);""", (name, price, description, image))
                db.commit()
                message = "New product added to catalog!" 
        return render_template("addproduct.html", form=form, message=message)
    else:
        return redirect(url_for("login"))
    

# idea for file field https://stackoverflow.com/questions/30279473/get-an-uploaded-file-from-a-wtforms-field
