from flask import Flask, render_template, redirect, request, g
import sqlite3

# データベースの名前を格納
DATABASE="recipe.db"

app = Flask(__name__)

# トップページ
@app.route("/")
def index():
    return render_template("index.html")

# 材料からレシピ検索
@app.route("/food-recipe", methods=['GET', 'POST'])
def food_recipe():
    if request.method == 'POST':
        # 入力された材料を変数に格納
        material1 = request.form.get('material1')

        if not material1:
            return redirect('food-recipe')
        
        material2 = request.form.get('material2')
        material3 = request.form.get('material3')

        # 材料からレシピ情報を取得
        if not material2 and not material3:
            recipes = get_db().execute("SELECT * FROM recipe WHERE recipe_material LIKE ? GROUP BY recipe_title LIMIT 20", ('%'+material1+'%',)).fetchall()
            
        elif material2 and not material3:
            recipes = get_db().execute("SELECT * FROM recipe WHERE recipe_material LIKE ? AND recipe_material LIKE ? GROUP BY recipe_title LIMIT 20", ('%'+material1+'%', '%'+material2+'%', )).fetchall()

        elif material2 and material3:
            recipes = get_db().execute("SELECT * FROM recipe WHERE recipe_material LIKE ? AND recipe_material LIKE ? AND recipe_material LIKE ? GROUP BY recipe_title LIMIT 20", ('%'+material1+'%', '%'+material2+'%', '%'+material3+'%', )).fetchall()

        return render_template("search-recipe.html", recipes=recipes)
    else:
        return render_template("food-recipe.html")

# 料理名から買い物リスト
@app.route("/recipe-food", methods=['GET', 'POST'])
def recipe_food():
    if request.method == 'POST':
        # 送信された料理名を格納している
        cooking = request.form.get('cooking')

        # 送信された料理名が入っているrecipe_titleを一件取得
        cookings = get_db().execute("SELECT * FROM recipe WHERE recipe_title LIKE ? GROUP BY recipe_title LIMIT 1", ('%'+cooking+'%',)).fetchall()
        
        # recipe_titleをrecipe_title変数に格納
        recipe_url = cookings[0]['recipe_url']

        # 材料のリストを作っている
        materials = cookings[0]['recipe_material']
        materials = materials.replace('[', '')
        materials = materials.replace(' ', '')
        materials = materials.replace(']', '')
        materials = materials.replace('\'', '')
        materials = materials.replace('☆', '')
        materials = materials.split(',')

        return render_template('search-food.html', recipe_url=recipe_url, materials=materials, cooking=cooking)
    return render_template("recipe-food.html")

#database
def connect_db():
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv
def get_db():
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db