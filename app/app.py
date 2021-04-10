from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('timer_cedar.html')
   

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.cache = {}
    app.run(debug = True, port = 8000) # use_reloader = True, use_debugger= True)
