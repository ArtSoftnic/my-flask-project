from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from mysql.connector import connect

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'ca-database.cuehjuoht5aa.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'planning'
app.config['MYSQL_DB'] = 'cheynet_planning'

def getusers(txt_search):

    # connection with MySQL 
    cur = mysql.connection.cursor()

    # MySQL SELECT statement 
    sql = "SELECT * FROM hanging_std WHERE greige_ref LIKE %s"
    params = ['%' + txt_search + '%']

    # Execute the SELECT statement and retrieve the search results
    cur.execute(sql, params)
    results = cur.fetchall()
    cur.close()
    return results
    
   

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/hanging-database', methods = ['POST'])
def insert_hanging():    

    if request.method == 'POST':
        reference = request.form['txt_reference']
        length = request.form['txt_length']
        round = request.form['txt_round']

        # Connect to the database
        conn = connect(host='ca-database.cuehjuoht5aa.us-east-2.rds.amazonaws.com', user='root', password='planning', database='cheynet_planning')

        # connection with MySQL 
        cur = conn.cursor()

        # MySQL SELECT statement 
        sql = "INSERT INTO hanging_std (greige_ref, length_per_hang, round_per_hang) VALUES (%s, %s, %s)"

        # Excute the INSERT statement 
        cur.execute(sql, (reference, length, round))

        # Commit the changes to the database 
        conn.commit()      

        # Close the cursor and connection 
        cur.close()       

        return redirect(url_for('add_hanging'))      


@app.route('/hanging-database')
def add_hanging():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hanging_std ORDER BY id DESC")
    add_hanging = cur.fetchall()
    cur.close()
    return render_template('hanging-database.html', usr = add_hanging)


@app.route("/hanging-standard", methods = ["GET", "POST"])
def hanging():
    if request.method == "POST":
        data = dict(request.form)
        users = getusers(data["txt_search"])
        
    else:
        users = []
    
    return render_template("hanging.html", usr = users)


@app.route('/packaging-standard')
def packaging():
    return render_template('packing.html')


@app.route('/bases')
def bases():
    return render_template('bases.html')


@app.route('/wastage')
def wastage():
    return render_template('wastage.html')

# @app.route('/database')
# def wastage():
#     return render_template('wastage.html')


# Error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500


bootstrap = Bootstrap(app)
mysql = MySQL(app)

