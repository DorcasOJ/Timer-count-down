from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import os


app = Flask(__name__)
# 'sqlite:///db.sqlite3'
#app.config.from_pyfile('hello.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://chsvcumebyzuwq:0e0f78fe4f142f4454999e753f5ba9877118314767a86901f9903baa6363208f@ec2-54-87-112-29.compute-1.amazonaws.com:5432/d75og76s42qst1' #'sqlite:///db.sqlite3' os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = 'random_number' #os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Sch_table(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20))
    name = db.Column(db.String(20))
    mins = db.Column(db.Integer)
    default = db.Column(db.Boolean)
    #unique=True, nullable=False
    #db.UniqueConstraint(title)

    def __init__(self, title, name, mins, default):
        self.title = title
        self.name = name
        self.mins = mins
        self.default = default

class Sch_titles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20), )
    default = db.Column(db.Boolean)
    #db.UniqueConstraint(title)

    def __init__(self, title, default):
        self.title = title
        self.default = default

def create(all_keys):
    if 'default' in all_keys:
        for key in range(0, len(all_keys[2:]), 2):
            title, default, mins, name = all_keys[0], all_keys[1], all_keys[2:][key], all_keys[2:][key+1]
            #sch = create(request.form['title'], request.form[name], request.form[minute
            #if request.form[default] == 'True':
            table = Sch_table(request.form[title], request.form[name], request.form[mins], True)
            #else:
            #    table = Sch_table(request.form[title], request.form[name], request.form[mins], False)
            db.session.add(table)
            db.session.commit()
        admin = Sch_table.query.filter(Sch_table.title != request.form[title]).update(dict(default = False))
        db.session.commit()
        admin_title = Sch_titles.query.filter(Sch_titles.title != request.form[title]).update(dict(default=False))
        #admin.default = False
        db.session.commit()

        sch_title = Sch_titles(request.form[title], True)
        db.session.add(sch_title)
        db.session.commit()
    else:
        for key in range(0, len(all_keys[1:]), 2):
            title, mins, name = all_keys[0], all_keys[1:][key], all_keys[1:][key+1]
            #sch = create(request.form['title'], request.form[name], request.form[minute
            table = Sch_table(request.form[title], request.form[name], request.form[mins], False)
            db.session.add(table)
            db.session.commit()
        sch_title = Sch_titles(request.form[title], False)
        db.session.add(sch_title)
        db.session.commit()

    #undefault all formally default if default is true       
    return 'added'

def get_all():
    all_table = Sch_table.query.order_by(Sch_table.title).all()
    #Students.query.filter_by(city = ’Hyderabad’).all()
    all_title = Sch_titles.query.order_by(Sch_titles.title).all()
    #all_title = list(np.unique(all_title))
    return all_table, all_title

def delete(title):
    #if info:
    #    Sch_table.query.filter(Sch_table.name == name)
    #    return 'info deleted'
    Sch_table.query.filter(Sch_table.title == title).delete()
    db.session.commit()
    Sch_titles.query.filter(Sch_titles.title ==title).delete()
    db.session.commit()
    return 'schedule deleted'
    

def mk_default(title):
    admin = Sch_table.query.filter(Sch_table.title == title).update(dict(default = True))
    admin_title = Sch_titles.query.filter(Sch_titles.title == title).update(dict(default=True))
    db.session.commit()

    admin = Sch_table.query.filter(Sch_table.title != title).update(dict(default =False))
    admin_title = Sch_titles.query.filter(Sch_titles.title != title).update(dict(default=False))
    db.session.commit()


@app.route('/')
def home_page():
    all_table, all_title = get_all()
    return render_template('timer_cedar.html', all_table = all_table, all_title = all_title)

@app.route('/show_db')
def show_db():
    all_table, all_title = get_all()
    return render_template('show_db.html', all_table = all_table, all_title = all_title)

@app.route('/create_new_db', methods = ['GET', 'POST'])
def create_new_db():
    if request.method == 'POST':
        #Sch_table.query.delete()
        #flash('Create new schedule')
        f = request.form
        all_keys = [i for i in f.keys()]
        #f = request.form
        #for key in f.keys():
        #    for value in f.getlist(key):
        #        print(key,":",value)
        
        proceed = True
        for key in all_keys:
            if not request.form[key]:
                proceed = False
                flash('Please enter all the fields', 'error')
                break

        if proceed:
            sch = create(all_keys)
            if sch == 'added':
                flash('New Schedule successfully added')
        
            return redirect(url_for('show_db'))
    all_table, all_title = get_all()
    return render_template('create_schedule.html', all_title = all_title)


@app.route('/make_default_true', methods = ['POST'])
def make_default_true():
    def_var = request.form['def_var_key']
    print(def_var)
    #def_var_lst.replace({'Yes': True})
    mk_default(def_var)
    return redirect(url_for('show_db'))


@app.route('/make_default_false', methods = ['POST'])
def make_default_false():
    def_var_false = request.form['def_var_false_kay']
    print(def_var_false)
    admin = Sch_table.query.filter(Sch_table.title == def_var_false).update(dict(default = False))
    admin_title = Sch_titles.query.filter(Sch_titles.title == def_var_false).update(dict(default=False))
    db.session.commit()
    return redirect(url_for('show_db'))


@app.route('/deleteSchd', methods = ['POST'])
def deleteSchd():
    title = request.form['del_var_key']
    out =delete(title)
    flash(out)
    return redirect(url_for('show_db'))

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.cache = {}
    app.run(debug = True, port = 8000) # use_reloader = True, use_debugger= True)
