from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, default=1, nullable=False)



with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo_content = request.form.get('content')
        due_date_str = request.form.get('due_date')

        if not todo_content.strip() or not due_date_str:
            return redirect('/')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        # Set the priority to the next available number (highest priority + 1)
        max_priority = db.session.query(db.func.max(Todo.priority)).scalar() or 0
        new_todo = Todo(content=todo_content, due_date=due_date, priority=max_priority + 1)
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/')
    else:
        # Fetch tasks sorted by priority
        tasks = Todo.query.order_by(Todo.priority).all()
        current_date = datetime.now().date()
        return render_template('index.html', todos=tasks, current_date=current_date)
    
@app.route('/update-priority', methods=['POST'])
def update_priority():
    # Get the new order of IDs from the request
    new_order = request.json.get('order', [])
    for index, todo_id in enumerate(new_order):
        todo = Todo.query.get(todo_id)
        if todo:
            todo.priority = index + 1  # Update priority based on the new order
    db.session.commit()
    return {'status': 'success'}

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