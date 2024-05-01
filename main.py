from flask import Flask, render_template

app = Flask(__name__)



@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('index.html',
                           title=title)


@app.route('/promotion')
def promotion():
    return render_template('promotion.html')


@app.route('/image_mars')
def imgmars():
    return render_template('mars.html')

@app.route('/ss')
def imrs():
    return render_template('11.html')



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')