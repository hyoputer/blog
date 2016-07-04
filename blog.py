from flask import Flask, render_template, request, url_for, flash, redirect
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = "jwjkwi"
r = redis.Redis('localhost', port = '6379')

class comments:
    def __init__(self, name, comment):
        self.name = name
        self.comment= comment

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/write', methods = ['POST', 'GET'])
def write():
    if request.method == 'POST':
        if not request.form['name']:
            flash('닉네임을 적어주세요')
        elif not request.form['comment']:
            flash('글을 적어주세요')

        else:
            comment = comments(request.form['name'], request.form['comment'])
            count = int(r.hget('Comments', 'Count'))
            r.hset('Comments', '%d' % (count + 1), comment)
            r.hincrby('Comments', 'Count', 1)
            flash('글이 저장되었습니다', 'success')
            return redirect(url_for('post'))
    return render_template('write.html')

@app.route('/post')
def post():
    count = int(r.hget('Comments', 'Count'))
    return render_template('post.html', count = count)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True, port = 55555)
