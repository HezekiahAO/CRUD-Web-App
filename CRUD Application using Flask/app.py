from flask import Flask, render_template, request, redirect, url_for
import sqlite3 # Used to handle database interactionand queriesI. 



app = Flask(__name__)
 

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def add_user(name, age):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
    conn.commit()
    conn.close()

def update_user(user_id, name, age):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET name = ?, age = ? WHERE id = ?', (name, age, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn=sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

@app.route('/')              #routing this home page to index function
def index():
    users = get_users()
    return render_template('frontend.html', users=users)  # Render the template with user data

@app.route('/add_user', methods=['POST'])   # routing this add_user page to add function
def add():
    name = request.form['name']    #request object is used to handle form data and form allows us to get the data from the form.
    age = request.form['age']
    add_user(name, age)
    return redirect(url_for('index'))

@app.route('/update', methods=['POST', 'GET'])
def update(user_id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        update_user(user_id, name, age)
        return redirect(url_for('index'))
    
    # If GET request, fetch user data to pre-fill the form  
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('update.html', user=user)

@app.route('/delete/<int:user_id>')
def delete(user_id):
    delete_user(user_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(host='0.0.0.0', port = 5000, debug = True) # Run the Flask application