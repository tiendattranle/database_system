from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
import psycopg2
from logging.config import dictConfig
import logging
import sys
import base64
from io import BytesIO
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'



books = [
    {
        "id": 1,
        "title": "The Little Prince",
        "price": 150000,
        "sales": 100,
        "image": "static/images/book1.png"
    },
    {
        "id": 2,
        "title": "Tuesdays with Morrie",
        "price": 210000,
        "sales": 75,
        "image": "static/images/book2.png"
    },
    {
        "id": 3,
        "title": "7 Habits of Highly Effective People",
        "price": 300000,
        "sales": 45,
        "image": "static/images/book3.png"
    },
    {
        "id": 3,
        "title": "7 Habits of Highly Effective People",
        "price": 300000,
        "sales": 45,
        "image": "static/images/book3.png"
    },
    {
        "id": 3,
        "title": "7 Habits of Highly Effective People",
        "price": 300000,
        "sales": 45,
        "image": "static/images/book3.png"
    },
    {
        "id": 3,
        "title": "7 Habits of Highly Effective People",
        "price": 300000,
        "sales": 45,
        "image": "static/images/book3.png"
    }
]


# Kết nối cơ sở dữ liệu
def get_db_connection():
    return psycopg2.connect(database="CNPM", user="postgres", password="123456", host="localhost", port="5432")

# Yêu cầu đăng nhập
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login_for_customer'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/index')
@login_required
def index():
    username = session.get('username')
    logger.debug(f"Session username: {username}")  # Thêm dòng log này

    if not username:
        return redirect(url_for('login_for_customer'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, profile_picture FROM "User" WHERE username = %s', (username,))
    user = cur.fetchone()
    logger.debug(f"User fetched: {user}")  # Thêm dòng log này

    cur.close()
    conn.close()

    if user:
        name = user[0]
        profile_picture2 = user[1]
        logger.debug(f"Name: {name}")  # Thêm dòng log này
        logger.debug(f"Fetched profile picture for {username}: {name}")  # Log ảnh đại diện đã được lấy
        if profile_picture2:
            profile_picture2_base64 = base64.b64encode(profile_picture2).decode('utf-8')  # Chuyển sang chuỗi base64
        else:
            profile_picture2_base64 = None
        return render_template('index.html', name=name, profile_picture2_base64=profile_picture2_base64)
    else:
        return "User not found", 404
   
@app.route('/product/<int:item_id>')
@login_required
def product(item_id):
    username = session.get('username')
    logger.debug(f"Session username: {username}")  # Thêm dòng log này

    if not username:
        return redirect(url_for('login_for_customer'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, profile_picture FROM "User" WHERE username = %s', (username,))
    user = cur.fetchone()
    logger.debug(f"User fetched: {user}")  # Thêm dòng log này

    cur.close()
    conn.close()

    if user:
        name = user[0]
        profile_picture2 = user[1]
        logger.debug(f"Name: {name}")  # Thêm dòng log này
        logger.debug(f"Fetched profile picture for {username}: {name}")  # Log ảnh đại diện đã được lấy
        if profile_picture2:
            profile_picture2_base64 = base64.b64encode(profile_picture2).decode('utf-8')  # Chuyển sang chuỗi base64
        else:
            profile_picture2_base64 = None
        return render_template('product.html', name=name, profile_picture2_base64=profile_picture2_base64, item_id=item_id)
    else:
        return "User not found", 404
@app.route('/account')
@login_required
def account():
    username = session.get('username')
    logger.debug(f"Session username: {username}")  # Thêm dòng log này

    if not username:
        return redirect(url_for('login_for_customer'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, profile_picture FROM "User" WHERE username = %s', (username,))
    user = cur.fetchone()
    logger.debug(f"User fetched: {user}")  # Thêm dòng log này

    cur.close()
    conn.close()

    if user:
        name = user[0]
        profile_picture2 = user[1]
        logger.debug(f"Name: {name}")  # Thêm dòng log này
        logger.debug(f"Fetched profile picture for {username}: {name}")  # Log ảnh đại diện đã được lấy
        if profile_picture2:
            profile_picture2_base64 = base64.b64encode(profile_picture2).decode('utf-8')  # Chuyển sang chuỗi base64
        else:
            profile_picture2_base64 = None
        return render_template('account.html', name=name, profile_picture2_base64=profile_picture2_base64)
    else:
        return "User not found", 404

@app.route('/account-update')
@login_required
def account_update():
    username = session.get('username')
    logger.debug(f"Session username: {username}")  # Thêm dòng log này

    if not username:
        return redirect(url_for('login_for_customer'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, profile_picture FROM "User" WHERE username = %s', (username,))
    user = cur.fetchone()
    logger.debug(f"User fetched: {user}")  # Thêm dòng log này

    cur.close()
    conn.close()

    if user:
        name = user[0]
        profile_picture2 = user[1]
        logger.debug(f"Name: {name}")  # Thêm dòng log này
        logger.debug(f"Fetched profile picture for {username}: {name}")  # Log ảnh đại diện đã được lấy
        if profile_picture2:
            profile_picture2_base64 = base64.b64encode(profile_picture2).decode('utf-8')  # Chuyển sang chuỗi base64
        else:
            profile_picture2_base64 = None
        return render_template('account_update.html', name=name, profile_picture2_base64=profile_picture2_base64)
    else:
        return "User not found", 404

@app.route("/get_products", methods=["GET"])
def get_books():
    return jsonify(books)

@app.route('/book/<string:book_id>')
def get_book(book_id):
    book = {
        "id": 1,
        "title": "The Little Prince",
        "price": 150000,
        "category": "Mom and baby",
        "publishingYear": 2022,
        "publisher": "",
        "cover": "soft",
        "author": "",
        "sales": 100,
        "image": "static/images/book1.png"
    }
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

@app.route('/')
def login_for_customer():
    return render_template('login_for_customer.html') 

@app.route('/register')
def register():
    return render_template('register.html') 

@app.route('/login_for_admin')
def login_for_admin():
    return render_template('login_for_admin.html') 


@app.route('/cart')
@login_required
def cart():
    username = session.get('username')  # Lấy username từ session
    if not username:
        return redirect(url_for('login_for_customer'))  # Nếu không có session, chuyển hướng đến trang login
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Truy vấn tên người dùng từ bảng "User"
    cur.execute('SELECT name, profile_picture FROM "User" WHERE username = %s', (username,))
    user = cur.fetchone()
    if user:
        name = user[0]  # Lấy tên từ kết quả truy vấn
        profile_picture3 = user[1] 
        logger.debug(f"Fetched name for user {username}: {name}")
        logger.debug(f"Fetched profile picture for {username}: {name}")  # Log ảnh đại diện đã được lấy
        if profile_picture3:
            profile_picture3_base64 = base64.b64encode(profile_picture3).decode('utf-8')  # Chuyển sang chuỗi base64
        else:
            profile_picture3_base64 = None
    else:
        cur.close()
        conn.close()
        return "User not found", 404

    cur.close()
    conn.close()
    data = request.get_json()  # Parse JSON body
    user_id = data.get('user_id')
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_name, quantity, price, discounted_price, image_url
        FROM Cart
        WHERE user_id = %s;
    """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    
    # Truyền dữ liệu vào template
    return render_template('cart.html', name=name, profile_picture3_base64=profile_picture3_base64, rows=rows)
 

@app.route('/order')
@login_required
def order():
    username = session.get('username')  # Lấy username từ session
    if not username:
        return redirect(url_for('login_for_customer'))  # Nếu không có session, chuyển hướng đến trang login
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Truy vấn tên người dùng từ bảng "User"
    cur.execute('SELECT name, profile_picture FROM "User" WHERE username = %s', (username,))
    user = cur.fetchone()
    if user:
        name = user[0]  # Lấy tên từ kết quả truy vấn
        profile_picture4 = user[1]
        logger.debug(f"Fetched name for user {username}: {name}")
        logger.debug(f"Fetched profile picture for {username}: {name}")  # Log ảnh đại diện đã được lấy
        if profile_picture4:
            profile_picture4_base64 = base64.b64encode(profile_picture4).decode('utf-8')  # Chuyển sang chuỗi base64
        else:
            profile_picture4_base64 = None
    else:
        cur.close()
        conn.close()
        return "User not found", 404

    cur.close()
    conn.close()
    
    # Truyền dữ liệu vào template
    return render_template('order.html', name=name, profile_picture4_base64=profile_picture4_base64) 

@app.route('/homescreen_admin')
@login_required
def homescreen_admin():
    username = session.get('username')  # Lấy username từ session
    if not username:
        return redirect(url_for('login_for_customer'))  # Nếu không có session, chuyển hướng đến trang login
    conn = get_db_connection()
    cur = conn.cursor()
    # Truy vấn tên người dùng từ cơ sở dữ liệu
    cur.execute('SELECT name, profile_picture FROM "User" WHERE username = %s', (username,))
    user = cur.fetchone()
     # Lấy thông báo của người dùng
    cur.execute('SELECT content, time FROM "Notification" WHERE username = %s ORDER BY time DESC', (username,))
    notifications = cur.fetchall()  # Lấy tất cả thông báo của người dùng
    if user:
        name = user[0]  # Lấy tên từ kết quả truy vấn
        profile_picture5 = user[1]  # Lấy ảnh từ cơ sở dữ liệu (dạng bytea)
        logger.debug(f"Fetched profile picture for {username}: {name}")  # Log ảnh đại diện đã được lấy
        if profile_picture5:
            profile_picture5_base64 = base64.b64encode(profile_picture5).decode('utf-8')  # Chuyển sang chuỗi base64
        else:
            profile_picture5_base64 = None
    else:
        cur.close()
        conn.close()
        return "User not found", 404
    cur.close()
    conn.close()
    return render_template('homescreen_admin.html', name=name, profile_picture5_base64=profile_picture5_base64, notifications=notifications) 


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html') 

@app.route('/admin_printing_history')
@login_required
def admin_printing_history():
    username = session.get('username')  # Lấy username từ session
    if not username:
        return redirect(url_for('login_for_customer'))
    conn = get_db_connection()
    cur = conn.cursor()
    # Truy vấn tên người dùng từ cơ sở dữ liệu
    cur.execute('SELECT name, profile_picture FROM "User" WHERE username = %s', (username,))
    user = cur.fetchone()
     # Lấy thông báo của người dùng
    cur.execute('SELECT content, time FROM "Notification" WHERE username = %s ORDER BY time DESC', (username,))
    notifications = cur.fetchall()
    # Truy vấn dữ liệu từ bảng admin_printinghistory
    logger.debug("Fetching admin printing history")
    cur.execute('SELECT name, printer_id, file_name, file_size, no_pages, status, time, paper_orientation, print_sides, num_copies, file_type, user_id FROM admin_printinghistory')
    admin_history = cur.fetchall()  # Lấy tất cả kết quả
    
    logger.debug(f"admin printing history fetched: {admin_history}")
    if user:
        name = user[0]  # Lấy tên từ kết quả truy vấn
        profile_picture7 = user[1]  # Lấy ảnh từ cơ sở dữ liệu (dạng bytea)
        logger.debug(f"Fetched profile picture for {username}: {name}")  # Log ảnh đại diện đã được lấy
        if profile_picture7:
            profile_picture7_base64 = base64.b64encode(profile_picture7).decode('utf-8')  # Chuyển sang chuỗi base64
        else:
            profile_picture7_base64 = None
    else:
        cur.close()
        conn.close()
        return "User not found", 404
    cur.close()
    conn.close()
    
    # Truyền dữ liệu vào template
    return render_template('admin_printing_history.html', admin_history=admin_history, name=name,notifications=notifications,profile_picture7_base64=profile_picture7_base64)


@app.route('/login_customer', methods=['POST'])
def login_customer():
    conn = get_db_connection()
    cur = conn.cursor()
    username = request.form['username']
    password = request.form['password']
    logger.debug(f"Login attempt: username={username}, password={password}")  # Log input

    cur.execute('SELECT * FROM "User" WHERE username = %s AND password = %s', (username, password))
    user = cur.fetchone()
    logger.debug(f"User found: {user}")  # Log result from database

    cur.close()
    conn.close()

    if user:
        session['username'] = username
        logger.debug(f"Session saved: {session['username']}")  # Log session
        return redirect(url_for('index'), )
    else:
        return redirect(url_for('login_for_customer', wrongpw='true'))

@app.route('/login_admin', methods=['POST'])
def login_admin():
    conn = get_db_connection()
    cur = conn.cursor()
    username = request.form['username']
    password = request.form['password']
    # Kiểm tra thông tin đăng nhập
    cur.execute('SELECT username FROM "User" WHERE username = %s AND password = %s', (username, password))
    user = cur.fetchone()
    if user:
        # Kiểm tra vai trò của tài khoản
        cur.execute('SELECT username FROM "admin" WHERE username = %s', (username,))
        admin_account = cur.fetchone()
        if admin_account:
            # Nếu là admin
            session['username'] = username
            cur.close()
            conn.close()
            return redirect(url_for('homescreen_admin'))  # Trang chủ admin
        # Nếu không phải admin, kiểm tra xem có phải customer
        cur.execute('SELECT username FROM "customer" WHERE username = %s', (username,))
        customer_account = cur.fetchone()
        if customer_account:
            # Nếu là customer
            session['username'] = username
            cur.close()
            conn.close()
            return redirect(url_for('index'))  # Trang chủ customer
        # Nếu không thuộc bảng nào khác
        cur.close()
        conn.close()
        return redirect(url_for('system_error'))  # Lỗi nếu tài khoản không hợp lệ
    else:
        # Nếu username hoặc password không đúng
        cur.close()
        conn.close()
        return redirect(url_for('login_for_admin', wrongpw='false'))

if __name__ == '__main__':
    app.run(debug=True)
