from flask import Flask, render_template

app = Flask(__name__)

# Define routes for each page
@app.route('/')
def HomePage():
    return render_template('HomePage.html')

@app.route('/MindBot')
def MindBot():
    return render_template('MindBot.html')


if __name__ == '__main__':
    app.run(debug=True)
