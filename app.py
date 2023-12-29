from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Todo.db"
db = SQLAlchemy(app)


class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.id } , {self.task}"


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        task_content = request.form['task']
        new_task = TodoList(task=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "An error occurred"

    else:
        tasks = TodoList.query.order_by("date").all()
        return render_template('home.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete_task(id):
    # del_task = TodoList.query.filter_by(id=id).first()
    del_task = TodoList.query.get_or_404(id)
    try:
        db.session.delete(del_task)
        db.session.commit()
        return redirect('/')
    except:
        return "Something went wrong"


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update_task(id):

    updated_task = TodoList.query.get_or_404(id)
    if request.method == 'POST':

        # update_task = TodoList.query.filter_by(id=id).first()
        updated_task.task = request.form['task']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Something went wrong"

    else:
        return render_template('update.html', task=updated_task)


if __name__ == "__main__":
    app.run(debug=True)
