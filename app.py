import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 数据库文件名
DATABASE = 'todos.db'

def init_db():
    """初始化数据库，创建 todos 表"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()

def get_todos():
    """从数据库获取所有待办事项"""
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row  # 使结果可以通过列名访问
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todos ORDER BY id')
        return [dict(row) for row in cursor.fetchall()]

def add_todo(task):
    """添加新的待办事项"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO todos (task, completed) VALUES (?, ?)', (task, False))
        conn.commit()

def complete_todo(index):
    """将指定 ID 的待办事项标记为完成"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE todos SET completed = ? WHERE id = ?', (True, index))
        conn.commit()

def delete_todo(index):
    """删除指定 ID 的待办事项"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM todos WHERE id = ?', (index,))
        conn.commit()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            add_todo(task)
        return redirect(url_for('home'))

    todos = get_todos()
    return render_template('index.html', todos=todos)

@app.route('/complete/<int:index>')
def complete(index):
    complete_todo(index)
    return redirect(url_for('home'))

@app.route('/delete/<int:index>')
def delete(index):
    delete_todo(index)
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()  # 在启动应用前初始化数据库
    app.run(debug=True)