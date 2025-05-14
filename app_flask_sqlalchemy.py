from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo_content = request.form.get('content')
        new_todo = Todo(content=todo_content)
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/')
    else:
        tasks = Todo.query.all()
        return render_template('index.html', todos=tasks)
    

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo_to_delete = Todo.query.get_or_404(todo_id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

# To create the database, run the following commands in Python shell:
# python app_flask_sqlalchemy.py