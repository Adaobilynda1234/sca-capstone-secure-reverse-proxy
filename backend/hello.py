import os
from flask import Flask, jsonify
import mysql.connector
from prometheus_client import Counter, generate_latest
from prometheus_flask_exporter import PrometheusMetrics

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# Prometheus metric
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Student Records Portal', version='1.0.0')

# -------------------------
# Database Manager Class
# -------------------------
class DBManager:
    def __init__(self):
        password_file = '/run/secrets/db-password'
        with open(password_file, 'r') as pf:
            password = pf.read().strip()

        self.connection = mysql.connector.connect(
            user="root",
            password=password,
            host="db",  # Docker service name
            database="example",
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()

    def init_db(self):
        """Create table and seed data"""
        self.cursor.execute("DROP TABLE IF EXISTS students")
        self.cursor.execute("""
            CREATE TABLE students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                course VARCHAR(255)
            )
        """)

        students = [
            ('Ada', 'Computer Science'),
            ('John', 'Engineering'),
            ('Mary', 'Medicine'),
            ('David', 'Mathematics')
        ]

        self.cursor.executemany(
            "INSERT INTO students (name, course) VALUES (%s, %s)",
            students
        )
        self.connection.commit()

    def get_students(self):
        self.cursor.execute("SELECT name, course FROM students")
        return self.cursor.fetchall()


# -------------------------
# Helper: Get DB Connection
# -------------------------
def get_db():
    return DBManager()


# -------------------------
# Routes
# -------------------------

@app.route('/')
def home():
    logger.info("GET / - serving student records")
    db = get_db()
    db.init_db()
    students = db.get_students()
    logger.info(f"Fetched {len(students)} students from DB")
    html = """
    <html>
    <head>
        <title>Student Records Portal</title>
    </head>
    <body style="font-family: Arial; padding:20px;">
        <h2 style="color: blue;">Student Records Portal</h2>
    """

    for name, course in students:
        html += f"""
        <div style="
            padding:10px;
            margin:10px 0;
            border:1px solid #ccc;
            border-radius:5px;
            background:#f9f9f9;
        ">
            <b>Name:</b> {name} <br>
            <b>Course:</b> {course}
        </div>
        """

    html += "</body></html>"
    return html


@app.route('/health')
def health():
    logger.info("GET /health - OK")
    return jsonify({"status": "ok"}), 200


@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


# -------------------------
# App Runner
# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)