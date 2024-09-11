from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

# create database

class Todo(db.Model):
   sno=db.Column(db.Integer , primary_key=True)
   title=db.Column(db.String (200), nullable=False)
   dsc=db.Column(db.String(500), nullable=False)
   date_now = db.Column(db.DateTime, default=datetime.utcnow)
#    action=db.Column(db.)


    # koi cheez dekhni hai toh yha se dekh skte hai is method se
   def __repr__(self) -> str:
      return f"{self.sno}-{self.title}"
   

#  jab bhi hum koi post karte hai toh hume route me methods ki list banakr likhna pdta hai

@app.route("/" , methods=['get' , 'POST']) 
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        dsc = request.form['dsc']

        todo = Todo(title=title, dsc=dsc)
        db.session.add(todo)
        db.session.commit()
    
    # for search functionality
    search_query=request.args.get('search' , '')
    totalTodos=db.session.query(Todo).count()
    if search_query:
        # Filter todos based on the search query
        show_all = Todo.query.filter(
            Todo.title.contains(search_query) | 
            Todo.dsc.contains(search_query)
        ).all()
        
    else:
        # Show all todos if no search query is provided
        show_all = Todo.query.all()
        
        
    return render_template("index.html", show_all=show_all,totalTodos=totalTodos)


# Route to display all todos
@app.route("/show")
def products():
    show_all=Todo.query.all()
    print(show_all)
    return 'this is products page'

# Route to delete a todo

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()  # Fetch the todo item
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# update todo

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first_or_404()  # Fetch the todo item
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.dsc = request.form['dsc']
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # This creates the tables when the script is run
    app.run(debug=True, port=8000)