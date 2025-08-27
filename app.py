# app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 简单的 todo list 存储在内存中
todos = []


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # 获取表单数据
        task = request.form.get('task')
        if task:
            todos.append({"task": task, "completed": False})
        return redirect(url_for('home'))

    return render_template('index.html', todos=todos)


@app.route('/complete/<int:index>')
def complete(index):
    if 0 <= index < len(todos):
        todos[index]["completed"] = True
    return redirect(url_for('home'))


@app.route('/delete/<int:index>')
def delete(index):
    if 0 <= index < len(todos):
        todos.pop(index)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)