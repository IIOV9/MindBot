from flask import Flask, render_template
from blueprints.MindBot_blueprint import MindBot_blueprint

app = Flask(__name__)

# Register the MindBot blueprint
app.register_blueprint(MindBot_blueprint, url_prefix='/MindBot', endpoint='MindBot.MindBot')

# Define routes for other pages
@app.route('/')
def HomePage():
    return render_template('HomePage.html')

@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/story2')
def story2():
    return render_template('story2.html')

@app.route('/scientific Articale')
def Articale():
    return render_template('scientific Articale.html')

@app.route('/specialist')
def specialist():
    return render_template('specialist.html')

if __name__ == '__main__':
    app.run(debug=True)
