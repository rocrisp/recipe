from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import create_connection
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM recipes')
        recipes = cursor.fetchall()  # This should return a list of dictionaries
    return render_template('index.html', recipes=recipes)

@app.route('/recipes/<int:recipe_id>', methods=['GET', 'POST'])
def get_recipe_by_id(recipe_id):
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE recipes
                SET title = %s, ingredients = %s, instructions = %s, updated_at = %s
                WHERE id = %s
            ''', (title, ingredients, instructions, datetime.now(), recipe_id))
            conn.commit()
        return redirect(url_for('index'))
    else:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM recipes WHERE id = %s', (recipe_id,))
            recipe = cursor.fetchone()
        return render_template('edit_recipe.html', recipe=recipe)

@app.route('/recipes/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        with create_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO recipes (title, ingredients, instructions, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (title, ingredients, instructions, datetime.now(), datetime.now()))
                conn.commit()
        return redirect(url_for('index'))
    return render_template('add_recipe.html')

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM recipes WHERE id = %s', (recipe_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
