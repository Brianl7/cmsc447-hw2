from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/home')

def index():
    return render_template('index.html')

connect = sqlite3.connect('database.db')
connect.execute('CREATE TABLE IF NOT EXISTS USERS (name TEXT, id TEXT, points TEXT)')

@app.route('/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        points = request.form['points']

        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("INSERT INTO USERS (name, id, points) VALUES (?, ?, ?)", (name, id, points))
            users.commit()
        
        return render_template("index.html")
    else:
        return render_template("create.html")

@app.route('/remove', methods = ['GET', 'POST'])
def remove():
    if request.method == 'POST':
        id = request.form['id']
        
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("DELETE FROM users WHERE id = (?)", (id,))
            users.commit()
        
        return render_template("index.html")
    else:
        return render_template("remove.html")

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        name = request.form['name']

        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("SELECT * FROM users WHERE name = (?)", (name,))
            data = cursor.fetchall()

        return render_template("display.html", data = data)
    else:
        return render_template("search.html")

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        points = request.form['points']
        newName = request.form['newName']
        newId = request.form['newId']
        newPoints = request.form['newPoints']
        if newName == "":
            newName = name
        if newId == "":
            newId = id
        if newPoints == "":
            newPoints = points
        connect = sqlite3.connect("database.db")
        cursor = connect.cursor()
        cursor.execute("UPDATE USERS SET name = ?, id = ?, points = ? WHERE name = ? AND id = ? AND points = ?", (newName, newId, newPoints, name, id, points))
        connect.commit()
        return render_template("index.html")
    else:
        return render_template("update.html")

@app.route('/display')
def display():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM USERS')

    data = cursor.fetchall()
    return render_template("display.html", data = data)

if __name__ == '__main__':
    app.run(debug=False)