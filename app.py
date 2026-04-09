from flask import Flask, render_template, request, redirect, session, jsonify
from models import db, User, Task, Job, Material, Electrician
import os

# ✅ FIRST create app
app = Flask(__name__)

app.secret_key = "1234"

# ✅ THEN config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ THEN init db
db.init_app(app)

# ✅ CREATE TABLES
with app.app_context():
    db.create_all()
    db.init_app(app)
# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'],
            password=request.form['password']
        ).first()

        if user:
            session['user'] = user.username
            return redirect('/dashboard')
        else:
            return "❌ Invalid login"

    return render_template('login.html')


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            password=request.form['password']
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/')

    return render_template('register.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    return render_template('dashboard.html',
        t=Task.query.count(),
        j=Job.query.count(),
        m=Material.query.count(),
        e=Electrician.query.count()
    )


# ---------------- TASKS ----------------
@app.route('/tasks', methods=['GET','POST'])
def tasks():
    if request.method == 'POST':
         if not request.form:
            return "Form data missing"
    task = Task(
        description=request.form.get('desc'),
        status=request.form.get('status'),
        job_id=request.form.get('job'),
        electrician_id=request.form.get('electrician')
        )
    db.session.add(task)
    db.session.commit()

    data = Task.query.all()
    jobs = Job.query.all()
    electricians = Electrician.query.all()

    return render_template('tasks.html',
        data=data,
        jobs=jobs,
        electricians=electricians
    )


# ---------------- JOBS ----------------
@app.route('/jobs', methods=['GET','POST'])
def jobs():
    if request.method == 'POST':
        if not request.form:
          return "Form data missing"
        job = Job(
    title=request.form.get('title'),
    location=request.form.get('location'),
    deadline=request.form.get('deadline'),
    electrician_id=request.form.get('electrician')
)
        db.session.add(job)
        db.session.commit()

    data = Job.query.all()
    electricians = Electrician.query.all()

    return render_template('jobs.html', data=data, electricians=electricians)


# ---------------- MATERIALS ----------------
@app.route('/materials', methods=['GET','POST'])
def materials():
    if request.method == 'POST':
        if not request.form:
         return "Form data missing"
        material = Material(
    name=request.form.get('name'),
    quantity=int(request.form.get('qty'))
)
        db.session.add(material)
        db.session.commit()

    data = Material.query.all()
    return render_template('materials.html', data=data)


# ---------------- ELECTRICIANS ----------------
@app.route('/electricians', methods=['GET', 'POST'])
def electricians():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        if not request.form:
         return "Form data missing"
        electrician = Electrician(
    name=request.form.get('name'),
    phone=request.form.get('phone')
)
        db.session.add(electrician)
        db.session.commit()

    data = Electrician.query.all()
    return render_template('electricians.html', data=data)


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


#-----------------Delete-----------------
@app.route('/delete/<type>/<int:id>')
def delete(type, id):

    model_map = {
        "task": Task,
        "job": Job,
        "material": Material,
        "electrician": Electrician
    }

    model = model_map.get(type)

    if model:
        item = model.query.get(id)
        if item:
            db.session.delete(item)
            db.session.commit()

    return redirect(request.referrer)

#-----------------Edit-----------------
@app.route('/edit/<type>/<int:id>', methods=['GET','POST'])
def edit(type, id):

    model_map = {
        "task": Task,
        "job": Job,
        "material": Material,
        "electrician": Electrician
    }

    model = model_map.get(type)
    item = model.query.get(id)

    if request.method == 'POST':

        if type == "task":
            item.description = request.form['desc']
            item.status = request.form['status']

        elif type == "job":
            item.title = request.form['title']
            item.location = request.form['location']

        elif type == "material":
            item.name = request.form['name']
            item.quantity = request.form['qty']

        elif type == "electrician":
            item.name = request.form['name']
            item.phone = request.form['phone']

        db.session.commit()
        return redirect('/' + type + 's')

    return render_template('edit.html', item=item, type=type)

from flask import jsonify

@app.route('/stats')
def stats():
    return jsonify({
        "tasks": Task.query.count(),
        "jobs": Job.query.count(),
        "materials": Material.query.count(),
        "electricians": Electrician.query.count()
    })
    
    
    
if __name__ == '__main__':
    app.run()