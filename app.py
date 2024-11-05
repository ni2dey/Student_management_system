from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/studentDB"
mongo = PyMongo(app)


@app.route('/')
def index():
    students = mongo.db.students.find()
    return render_template('index.html', students=students)


@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    age = request.form.get('age')
    grade = request.form.get('grade')
    email = request.form.get('email')
    
    if name and age and grade and email:
        mongo.db.students.insert_one({
            'name': name,
            'age': age,
            'grade': grade,
            'email': email
        })
    return redirect(url_for('index'))


@app.route('/edit_student/<id>', methods=['GET', 'POST'])
def edit_student(id):
    student = mongo.db.students.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        grade = request.form.get('grade')
        email = request.form.get('email')

        mongo.db.students.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'name': name, 'age': age, 'grade': grade, 'email': email}}
        )
        return redirect(url_for('index'))
    return render_template('update.html', student=student)


@app.route('/delete_student/<id>')
def delete_student(id):
    mongo.db.students.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
