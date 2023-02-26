from flask import Flask, render_template, request, session, redirect
from DB import Mysql
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(30)


@app.route('/')
def hello():
    # 欢迎页面
    return render_template('hello.html')


@app.route('/talk')
def talk():
    user = session.get('userinfo')
    if user is None:
        return redirect('/login')
    return render_template('talk.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # GET 请求，展示静态页面
    if request.method == 'GET':
        session['userinfo'] = None
        return render_template('login.html')
    else:
        # POST 处理登录逻辑
        # 获取用户名
        user_name = request.form.get('username')
        sql = f'select * from user where 学号 = "{user_name}"'
        db = Mysql()
        db.cursor.execute(sql)
        user = db.cursor.fetchone()
        if user is None:
            return '<script>alert("该学号未注册");location. href="/login"</script>'
        # 获取密码
        password = request.form.get('password')
        # 拼凑 sql 语句
        sql = f'select * from user where 学号 = "{user_name}"  and password = "{password}"'
        # 执行 sql 语句
        db.cursor.execute(sql)
        # 获取查询到的单挑数据
        user = db.cursor.fetchone()
        # 说明密码错误
        if user is None:
            return '<script>alert("密码错误");location.href="/login"</script>'
        session['userinfo'] = user;
        # 跳转到talk
        return redirect('/talk')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 1 展示注册页面 GET (获取)
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 接受表单提交过来的 学号
        user_name = request.form.get('username')
        # 判断是否已经注册
        db = Mysql()
        sql = f'select * from user where 学号 = "{user_name}"'
        db.cursor.execute(sql)
        user = db.cursor.fetchone()
        # 如果用户不为 None 说明已经注册了。
        # 需要停止程序的运行，并告诉用户
        if user is not None:
            return '<script>alert("该学号已注册");location.href="/login"</script>'
        password = request.form.get('password')
        m1 = request.form.get('密保1')
        m2 = request.form.get('密保2')
        m3 = request.form.get('密保3')
        # 拼凑 sql 语句
        sql = f'insert into user (学号,password,密保1,密保2,密保3) values ("{user_name}","{password}","{m1}","{m2}","{m3}")'
        # 创建数据库对象
        # 执行 sql 语句
        add_result = db.cursor.execute(sql)
        # 保存数据库的修改
        db.conn.commit()
        if add_result > 0:
            return '<script>alert("恭喜您注册成功");location.href="/login"</script>'
        else:
            return '<script>alert("抱歉您注册失败了");location.href="/register"</script>'


@app.route('/forget', methods=['GET', 'POST'])
def forget():
    if request.method == 'GET':
        return render_template('forget.html')
    else:
        user_name = request.form.get('username')
        # 判断是否已经注册
        db = Mysql()
        sql = f'select * from user where 学号 = "{user_name}"'
        db.cursor.execute(sql)
        user = db.cursor.fetchone()
        # 如果用户为 None 说明未注册了。
        # 需要停止程序的运行，并告诉用户
        if user is None:
            return '<script>alert("该学号未注册");location.href="/forget"</script>'
        m = request.form.get('a')
        password = request.form.get('password')
        # 拼凑sql语句
        sql = f'select * from user where 学号 = "{user_name}" and {m} = "{password}"'
        # 执行sql语句
        db.cursor.execute(sql)
        add_result = db.cursor.fetchone()
        if add_result is None:
            return '<script>alert("密保错误");location.href="/forget"</script>'
        else:
            session['use'] = user_name;
            return redirect('/rebuild')


@app.route('/rebuild', methods=['GET', 'POST'])
def rebuild():
    if request.method == 'GET':
        return render_template('rebuild.html')
    else:
        password = request.form.get('password')
        user = session.get('use')
        db = Mysql()
        sql = f'update user set password = "{password}" where 学号 = "{user}"'
        db.cursor.execute(sql)
        db.conn.commit()
        # 检测是否成功修改
        sql = f'select * from user where 学号 = "{user}" and password = "{password}"'
        # 执行sql语句
        db.cursor.execute(sql)
        add_result = db.cursor.fetchone()
        if add_result is None:
            return '<script>alert("修改失败");location.href="/rebuild"</script>'
        else:
            return '<script>alert("修改成功");location.href="/login"</script>'


if __name__ == '__main__':
    app.run()