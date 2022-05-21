import os
from flask import Flask, render_template,flash,redirect, render_template_string,url_for,session,logging,request
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'static/images'

# user login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session :
            return f(*args, **kwargs)
        else:
            flash("login for this page","danger")
            return redirect(url_for("login"))
    return decorated_function


# user Register form
class RegisterForm(Form):
    name = StringField("Name Surname",validators=[validators.Length(min = 4,max = 25)])
    username = StringField("Username",validators=[validators.Length(min = 5,max = 35)])
    email = StringField("Email ",validators=[validators.Email(message = "Please enter a correct email...")])
    password = PasswordField("Password:",validators=[
        validators.DataRequired(message = "Creat password"),
        validators.EqualTo(fieldname = "confirm",message="invalid password ...")
    ])
    confirm = PasswordField("Success Password")
    isAdmin = StringField("isAdmin",validators=[validators.Length(min = 0,max = 1)])


class ProfileForm(Form):
    name = StringField("Name Surname",validators=[validators.Length(min = 4,max = 25)])
    username = StringField("Username",validators=[validators.Length(min = 5,max = 35)])
    email = StringField("Email ",validators=[validators.Email(message = "Please enter a correct email...")])
    password = PasswordField("Password:",validators=[
        validators.DataRequired(message = "Creat password"),
        validators.EqualTo(fieldname = "confirm",message="invalid password ...")
    ])
    confirm = PasswordField("Success Password")
    isAdmin = StringField("isAdmin",validators=[validators.Length(min = 0,max = 1)])    


class LoginForm(Form):
    email = StringField("Email")
    password = PasswordField("Password")


class AddNewProductForm(Form):
    title = StringField("Title",validators=[validators.Length(min = 1)])
    category = StringField("Category",validators=[validators.Length(min = 1)])
    url = StringField("Url",validators=[validators.Length(min = 1)])
    product_code = StringField("Product Code",validators=[validators.Length(min = 1)])
    price = StringField("Price",validators=[validators.Length(min = 1)])
    description = StringField("Description",validators=[validators.Length(min = 0)])
    quantity = StringField("Quantity",validators=[validators.Length(min = 0)])\


class EditProductForm(Form):
    title = StringField("Title",validators=[validators.Length(min = 1)])
    category = StringField("Category",validators=[validators.Length(min = 1)])
    url = StringField("Url",validators=[validators.Length(min = 1)])
    product_code = StringField("Product Code",validators=[validators.Length(min = 1)])
    price = StringField("Price",validators=[validators.Length(min = 1)])
    description = StringField("Description",validators=[validators.Length(min = 0)])
    quantity = StringField("Quantity",validators=[validators.Length(min = 0)])



app = Flask(__name__)
#important! KEY
app.secret_key= "project"
 # mysql 
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "project"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
#app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql = MySQL(app)
#apps to do
@app.route("/")
def index():
   return render_template("index.html")

#products
@app.route("/products", methods = ["GET"])
def products():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        qry = "Select * From product"
        result = cursor.execute(qry)

        if result > 0:
            products = cursor.fetchall()
            return render_template("products.html",products = products)
        else:
            return render_template("products.html")
#products2
@app.route("/products2", methods = ["GET"])
def products2():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        qry = "Select * From product_2"
        result = cursor.execute(qry)

        if result > 0:
            products = cursor.fetchall()
            return render_template("products2.html",products = products)
        else:
            return render_template("products2.html")

#Dashboard
@app.route("/dashboard", methods = ["GET"])
def dashboard():
    
    if session["isAdmin"] == 1:   

        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            qry = "Select * From users"
            result = cursor.execute(qry)
    
            if result > 0 :
                user = cursor.fetchall()
                return render_template("dashboard.html",user = user)
            else:
                return render_template("dashboard.html")
    else:
        return redirect(url_for("index"))

#top-3
@app.route("/top3", methods = ["GET"])
def top3():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        qry = "Select * From users ORDER BY count DESC"
        result = cursor.execute(qry)

        if result > 0 :
            user = cursor.fetchall()
            return render_template("top3.html",user = user)
        else:
            return render_template("top3.html")


#product edit 1

@app.route("/product-edit/<int:id>", methods = ["GET","POST"])
@login_required
def productEdit(id):
    form = EditProductForm(request.form)
    if request.method == 'POST'and form.validate():
        baseId = id
        title = form.title.data
        category = form.category.data
        url = form.url.data
        product_code = form.product_code.data
        price = form.price.data
        description = form.description.data
        quantity = form.quantity.data

        # connect to database
        cursor = mysql.connection.cursor()
        qry = """
                Update product Set title = %s,
                            category = %s,
                            url = %s,
                            product_code = %s,
                            price = %s,
                            description = %s,
                            quantity = %s
                            WHERE id = %s
            """
        cursor.execute(
            qry,(
                title,
                category,
                url,
                product_code,
                price,
                description,
                quantity,
                baseId,
            )
        )
        
        mysql.connection.commit()
        cursor.close()
        
        flash("Product editted successfully","success")
        return redirect(url_for("products"))
    else:
        return render_template("editproduct.html",form = form)        


#product edit 2

@app.route("/product2-edit/<int:id>", methods = ["GET","POST"])
@login_required
def product2Edit(id):
    form = EditProductForm(request.form)
    if request.method == 'POST'and form.validate():
        baseId = id
        title = form.title.data
        category = form.category.data
        url = form.url.data
        product_code = form.product_code.data
        price = form.price.data
        description = form.description.data
        quantity = form.quantity.data

        # connect to database
        cursor = mysql.connection.cursor()
        qry = """
                Update product_2 Set title = %s,
                            category = %s,
                            url = %s,
                            product_code = %s,
                            price = %s,
                            description = %s,
                            quantity = %s
                            WHERE id = %s
            """
        cursor.execute(
            qry,(
                title,
                category,
                url,
                product_code,
                price,
                description,
                quantity,
                baseId,
            )
        )
        
        mysql.connection.commit()
        cursor.close()
        
        flash("Product editted successfully","success")
        return redirect(url_for("products2"))
    else:
        return render_template("editproduct2.html",form = form)  

#edit user



#register
@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        isAdmin = form.isAdmin.data
        password = sha256_crypt.encrypt(form.password.data)
        createdAt = datetime.now()
        count = 0
                    
        cursor = mysql.connection.cursor()
                    
        qry = "Insert into users(name,email,username,password,createdAt,isAdmin,count) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(qry,(name,email,username,password,createdAt,isAdmin,count))
        
        mysql.connection.commit()

        cursor.close()
        
        flash( "Registered...","success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form = form)


#update profile

@app.route("/profile/<int:id>",methods = ["GET","POST"])
def profile(id):
    userId = id

    cursor = mysql.connection.cursor()
    qry = "Select * From users where id = %s"
    result =  cursor.execute(qry,(userId,))
    if result > 0:
        data = cursor.fetchone()
        session["profileimage"] = data["img_url"]
        session["profilename"] = data["name"]
        session["profileisAdmin"] = data["isAdmin"]
        session["profileemail"] = data["email"]
        session["profileusername"] = data["username"]


        form = ProfileForm(request.form)
        if request.method == "POST" and form.validate():
            name = form.name.data
            username = form.username.data
            email = form.email.data            
            password = sha256_crypt.encrypt(form.password.data)
            isAdmin = form.isAdmin.data
          

            cursor = mysql.connection.cursor()
            qry = "Update users Set name = %s ,username = %s ,email = %s ,password = %s ,isAdmin = %s  where id = %s"             
            cursor.execute(qry,(name,username,email,password,isAdmin,userId))
            mysql.connection.commit()
            cursor.close()

            flash( "Registered...","success")
            if session["isAdmin"] == 1:   
                return redirect(url_for("dashboard"))
            else:
                return redirect(url_for("index"))
            
        else:
            return render_template("profile.html",form = form)


#Login
@app.route("/login", methods = ["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        email = form.email.data
        password_entered = form.password.data
        updatedAt = datetime.now()
        cursor = mysql.connection.cursor()
        qry = "Select * From users where email = %s"
        result =  cursor.execute(qry,(email,))

        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password_entered, real_password):
                    flash("success enter","success")                    



                    cursor.execute("SELECT * FROM users WHERE email = '%s'" % email)
                    rows1 = cursor.fetchall()

                    count = rows1[0]["count"]+1  
                    isLogin = 1  # if its for login = 1 if someone login the system  

                  

                    qry3 = "Update users Set isLogin = %s, count = %s,updatedAt = %s where email =%s"             
                    cursor.execute(qry3,(isLogin,count,updatedAt,email))

                    mysql.connection.commit()


                    session["logged_in"] = True
                    session["userId"] = rows1[0]["id"]
                    session["username"] = rows1[0]["username"]
                    session["isAdmin"] = rows1[0]["isAdmin"]                      
                    session["email"] = rows1[0]["email"]   
                    cursor.close()

                    return redirect(url_for("index"))
            else:
                    flash("invalid password...", "danger")
                    return redirect(url_for("login")) 
        else:
            flash("has no users....","danger")
            return redirect(url_for("login"))    

    return render_template("login.html",form=form)


#log out
@app.route("/logout")
def logout():
    cursor = mysql.connection.cursor()                    
    email = session["email"]     
    isLogin = 0  # if its for login = 1 if someone login the system  
    qry = "Update users Set isLogin = %s where email =%s"             
    cursor.execute(qry,(isLogin,email))
    mysql.connection.commit()
    cursor.close()

    session.clear()
    return redirect(url_for("index"))

#add-product 1
@app.route("/add-product",methods = ["GET","POST"])
def productSave():
    form = AddNewProductForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        category = form.category.data
        url = form.url.data
        product_code = form.product_code.data
        price = form.price.data
        description = form.description.data
        quantity = form.quantity.data
        whoIsAdd = session["email"]
        rank = 1
        isActive = 1

        cursor = mysql.connection.cursor()
        
        qry = """
                Insert into product(
                    quantity,
                    whoIsAdd,
                    title,
                    category,
                    url,
                    product_code,
                    price,
                    description,
                    rank,
                    isActive
                    ) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
              """ 
        
        cursor.execute(
            qry, 
            (
                quantity,
                whoIsAdd,
                title,
                category,
                url,
                product_code,
                price,
                description,
                rank,
                isActive,
            )
        )
        mysql.connection.commit()
        cursor.close()
        
        flash("Product added successfully","success")
        return redirect(url_for("products"))
    else:
        return render_template("addproduct.html", form=form)

#add-product 2
@app.route("/add-product2",methods = ["GET","POST"])
def product2Save():
    form = AddNewProductForm(request.form)
    if request.method== "POST" and form.validate():
        title = form.title.data
        category = form.category.data
        url = form.url.data
        product_code = form.product_code.data
        price = form.price.data
        description = form.description.data
        quantity = form.quantity.data
        whoIsAdd = session["email"]
        rank = 1
        isActive = 1

        cursor = mysql.connection.cursor()
        
        qry = """
                Insert into product_2(
                    quantity,
                    whoIsAdd,
                    title,
                    category,
                    url,
                    product_code,
                    price,
                    description,
                    rank,
                    isActive
                    ) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
              """ 
        
        cursor.execute(
            qry, 
            (
                quantity,
                whoIsAdd,
                title,
                category,
                url,
                product_code,
                price,
                description,
                rank,
                isActive,
            )
        )
        mysql.connection.commit()
        cursor.close()
        
        flash("Product added successfully","success")
        return redirect(url_for("products2"))
    else:
        return render_template("addproduct2.html", form=form)





    





@app.route("/uploadimage/<int:id>/<string:tableName>",methods = ["GET","POST"])
def upload_file(id,tableName):
    
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)


        product_id = id
        tableName = tableName
        url = file1.filename
        updatedAt = datetime.now()

        cursor = mysql.connection.cursor()
        if tableName == "product":
            qry = "Update product Set img_url = %s,updatedAt = %s where id = %s"     
            cursor.execute(qry,(url,updatedAt,product_id))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("products"))
        elif tableName == "products":            
            qry = "Update product_2 Set img_url = %s,updatedAt = %s where id = %s"   
            cursor.execute(qry,(url,updatedAt,product_id))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("products2"))
        elif tableName == "users":   
            qry = "Update users Set img_url = %s,updatedAt = %s where id = %s"   
            cursor.execute(qry,(url,updatedAt,product_id))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("index"))

        return 'ok'
    return '''

    '''




#delete 1
@app.route("/product-delete/<int:id>", methods = ["GET","POST"])
@login_required
def productDelete(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        qry = "delete from product where id = %s"
        cursor.execute(qry,(id,))
        mysql.connection.commit()
        cursor.close()
        flash("Product deleted successfully","danger")
        return redirect(url_for("products"))


#delete 2
@app.route("/product2-delete/<int:id>", methods = ["GET","POST"])
@login_required
def product2Delete(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        qry = "delete from product_2 where id = %s"
        cursor.execute(qry,(id,))
        mysql.connection.commit()
        cursor.close()
        flash("Product deleted successfully","danger")
        return redirect(url_for("products2"))


#delete user
@app.route("/user-delete/<int:id>", methods = ["GET","POST"])
def dashUserdelete(id):        
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        qry = "delete from users where id = %s"
        cursor.execute(qry,(id,))
        mysql.connection.commit()
        cursor.close()
        flash("User deleted successfully","danger")
        return redirect(url_for("dashboard")) 

if __name__ == "__main__":
    app.run(debug=True)
