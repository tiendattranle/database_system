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
idx = 6



# Kết nối cơ sở dữ liệu
def get_db_connection():
    return psycopg2.connect(database="DBS", user="postgres", password="123456", host="localhost", port="5432")

# Yêu cầu đăng nhập
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login_for_customer'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/index')
@login_required
def index():
    email = session.get('email')
    Fname = session.get('Fname')
    logger.debug(f"Session email: {email}")  # Thêm dòng log này
    books = get_books()
    if not email:
        return redirect(url_for('login_for_customer'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.close()
    conn.close()

    name = Fname
    logger.debug(f"Name: {name}")  # Thêm dòng log này
    logger.debug(f"Fetched profile picture for {email}: {name}")  # Log ảnh đại diện đã được lấy

    return render_template('index.html', name=name, books=books)
   
@app.route('/product/<string:item_id>')
@login_required
def product(item_id):
    Fname = session.get('Fname')
    session['itemID'] = item_id
    name = Fname
    return render_template('product.html', name=name)

@app.route('/account')
@login_required
def account():
    email = session.get('email')
    Fname = session.get('Fname')
    logger.debug(f"Session email: {email}")  # Thêm dòng log này

    if not email:
        return redirect(url_for('login_for_customer'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.close()
    conn.close()

    name = Fname
    logger.debug(f"Name: {name}")  # Thêm dòng log này
    logger.debug(f"Fetched profile picture for {email}: {name}")  # Log ảnh đại diện đã được lấy

    return render_template('account.html', name=name)

@app.route('/account-update')
@login_required
def account_update():
    email = session.get('email')
    Fname = session.get('Fname')
    logger.debug(f"Session email: {email}")  # Thêm dòng log này

    if not email:
        return redirect(url_for('login_for_customer'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.close()
    conn.close()

    name = Fname
    logger.debug(f"Name: {name}")  # Thêm dòng log này
    logger.debug(f"Fetched profile picture for {email}: {name}")  # Log ảnh đại diện đã được lấy

    return render_template('account_update.html', name=name)

@app.route("/get_products", methods=["GET"])
def get_books():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM Book''')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(books)

@app.route("/delete-account")
def delete_account():
    userID = session.get('userID')
    email = session.get('email')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'''DELETE FROM Customer WHERE customerID = '{userID}';''')
    cur.execute(f'''DELETE FROM AppUser WHERE userID = '{userID}';''')
    cur.execute(f'''DELETE FROM UserAccount WHERE email = '{email}';''')
    cur.close()
    conn.commit()
    conn.close()
    return jsonify({"message": "Delete successfully"})

def retrive_books():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM Book''')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

@app.route('/book')
def get_book():
    books = retrive_books()
    book_id = session.get('itemID')
    logger.debug(f'book_id: {book_id}')
    for book in books:
        if book[0] == book_id:
            return jsonify({"bookID": book[0], "category": book[1], "name": book[2], "author": book[3], "price": book[4], "noStock": book[5], "cover": book[6], "publisher": book[7], "publishYear": book[8], "noPages": book[9], "size": book[10], "img": book[11]}), 200
    return jsonify({"error": "Book not found"}), 404

@app.route('/get-info')
def get_info():
    userID = session.get('userID')
    email = session.get('email')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Using parameterized query to avoid SQL injection
        cur.execute(f'''SELECT * FROM Customer WHERE customerID = '{userID}';''')
        info = cur.fetchone()

        if not info:
            return jsonify({"error": "User not found"}), 404
        
        cur.close()
        conn.close()
        if info[2] == 'M': info[2] = "Male"
        if info[2] == 'F': info[2] = "Female"
        print("bi cai gi vay troi")
        return jsonify({
            "message": "success",
            "userID": info[0],
            "fullName": info[1],
            "gender": info[2],
            "dob": info[3],
            "phoneNumber": info[4],
            "email": email,
            "points": info[5]
        }), 200
    except Exception as e:
        # Log the error and return a generic server error
        print(f"Error: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

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
    email = session.get('email')  # Lấy email từ session
    Fname = session.get('Fname')
    logger.debug(f"Session email: {email}")
    if not email:
        return redirect(url_for('login_for_customer'))  # Nếu không có session, chuyển hướng đến trang login
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Truy vấn tên người dùng từ bảng "User"
    
    # cur.execute("""
    #             SELECT product_name, quantity, price, discounted_price, image_url
    #             FROM Cart
    #             WHERE user_id = %s;
    #         """, (email,))
    rows = 1#cur.fetchall()
    cur.close()
    conn.close()
    
    # Truyền dữ liệu vào template
    return render_template('cart.html', name=Fname, rows=rows)
 

@app.route('/order')
@login_required
def order():
    Fname = session.get('Fname')  # Lấy email từ session
    # Truyền dữ liệu vào template
    return render_template('order.html', name=Fname) 

@app.route('/submit', methods=['POST'])
def submit():
    global idx
    full_name = request.form.get('full_name')
    phone_number = request.form.get('phone_number')
    dob = request.form.get('dob')
    gender = request.form.get('gender')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password != confirm_password: return redirect(url_for(register))

    userID = 'US000'+str(idx)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'''INSERT INTO UserAccount
            VALUES ('{email}', '{password}');
                ''')
    cur.execute(f'''INSERT INTO AppUser
            VALUES ('{userID}', '{email}');
                ''')
    if gender == "male": gender = 'M'
    if gender == "female": gender = 'F'
    cur.execute(f'''
            INSERT INTO Customer
            VALUES ('{userID}', '{full_name}', '{gender}', '{dob}', '{phone_number}', 0);''')
    idx+=1
    print (f"index: {idx}")
    cur.close()
    conn.commit()
    conn.close()
    return redirect(url_for('login_for_customer'))

@app.route('/homescreen_admin')
@login_required
def homescreen_admin():
    email = session.get('email')  # Lấy email từ session
    if not email:
        return redirect(url_for('login_for_customer'))  # Nếu không có session, chuyển hướng đến trang login
    conn = get_db_connection()
    cur = conn.cursor()
    # Truy vấn tên người dùng từ cơ sở dữ liệu
    cur.execute('SELECT name, profile_picture FROM "User" WHERE email = %s', (email,))
    user = cur.fetchone()
    if user:
        name = user[0]  # Lấy tên từ kết quả truy vấn
        profile_picture5 = user[1]  # Lấy ảnh từ cơ sở dữ liệu (dạng bytea)
        logger.debug(f"Fetched profile picture for {email}: {name}")  # Log ảnh đại diện đã được lấy
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
    return render_template('homescreen_admin.html', name=name, profile_picture5_base64=profile_picture5_base64) 


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html') 

@app.route('/admin_printing_history')
@login_required
def admin_printing_history():
    email = session.get('email')  # Lấy email từ session
    if not email:
        return redirect(url_for('login_for_customer'))
    conn = get_db_connection()
    cur = conn.cursor()
    # Truy vấn tên người dùng từ cơ sở dữ liệu
    cur.execute('SELECT name FROM "User" WHERE email = %s', (email,))
    user = cur.fetchone()
    # Truy vấn dữ liệu từ bảng admin_printinghistory
    logger.debug("Fetching admin printing history")
    cur.execute('SELECT name, printer_id, file_name, file_size, no_pages, status, time, paper_orientation, print_sides, num_copies, file_type, user_id FROM admin_printinghistory')
    admin_history = cur.fetchall()  # Lấy tất cả kết quả
    
    logger.debug(f"admin printing history fetched: {admin_history}")
    if user:
        name = user[0]  # Lấy tên từ kết quả truy vấn
        profile_picture7 = user[1]  # Lấy ảnh từ cơ sở dữ liệu (dạng bytea)
        logger.debug(f"Fetched profile picture for {email}: {name}")  # Log ảnh đại diện đã được lấy
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
    return render_template('admin_printing_history.html', admin_history=admin_history, name=name, profile_picture7_base64=profile_picture7_base64)


@app.route('/login_customer', methods=['POST'])
def login_customer():
    conn = get_db_connection()
    cur = conn.cursor()
    email = request.form['email']
    password = request.form['password']
    logger.debug(f"Login attempt: email={email}, password={password}")  # Log input

    cur.execute(f'''SELECT * FROM UserAccount WHERE email = '{email}' AND pswrd = '{password}';''')
    user = cur.fetchall()
    cur.execute(f'''SELECT FName, userID FROM Customer JOIN (SELECT userID FROM AppUser WHERE usEmail = '{email}') ON customerID = userID;''')
    logger.debug(f"User found: {user}")  # Log result from database
    results = cur.fetchall()
    if results: 
        FName = results[0][0]
        userID = results[0][1]
        cur.close()
        conn.close()
    else:
        cur.close()
        conn.close()
        return redirect(url_for('login_for_customer', wrongpw='true'))
    if user:
        session['email'] = email
        session['Fname'] = FName
        session['userID'] = userID
        logger.debug(f"Session saved: {session['email']}")  # Log session
        return redirect(url_for('index'), )
    else:
        return redirect(url_for('login_for_customer', wrongpw='true'))

@app.route('/login_admin', methods=['POST'])
def login_admin():
    conn = get_db_connection()
    cur = conn.cursor()
    email = request.form['email']
    password = request.form['password']
    # Kiểm tra thông tin đăng nhập
    cur.execute(f'''SELECT * FROM UserAccount WHERE email = '{email}' AND pswrd = '{password}';''')
    user = cur.fetchone()
    if user:
        # Kiểm tra vai trò của tài khoản
        cur.execute('SELECT email FROM "admin" WHERE email = %s', (email,))
        admin_account = cur.fetchone()
        if admin_account:
            # Nếu là admin
            session['email'] = email
            cur.close()
            conn.close()
            return redirect(url_for('homescreen_admin'))  # Trang chủ admin
        # Nếu không phải admin, kiểm tra xem có phải customer
        cur.execute('SELECT email FROM "customer" WHERE email = %s', (email,))
        customer_account = cur.fetchone()
        if customer_account:
            # Nếu là customer
            session['email'] = email
            cur.close()
            conn.close()
            return redirect(url_for('index'))  # Trang chủ customer
        # Nếu không thuộc bảng nào khác
        cur.close()
        conn.close()
        return redirect(url_for('system_error'))  # Lỗi nếu tài khoản không hợp lệ
    else:
        # Nếu email hoặc password không đúng
        cur.close()
        conn.close()
        return redirect(url_for('login_for_admin', wrongpw='false'))

if __name__ == '__main__':
    app.run(debug=True)
