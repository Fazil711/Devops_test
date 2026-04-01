import sqlite3
import bcrypt
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- DATABASE SETUP ---
conn = sqlite3.connect('data/users.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')
conn.commit()
# ----------------------

@app.get("/", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # 1. Look up the user in the database by their username
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    user_record = cursor.fetchone()

    # 2. Check if the user actually exists
    if user_record is None:
        return {"status": "error", "message": "Invalid username or password"}
    
    # 3. Extract the hashed password from the database record
    stored_hash = user_record[0]
    
    # 4. Compare the typed password with the stored hash
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode('utf-8')
    
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return {"status": "success", "message": f"Welcome back, {username}!"}
    else:
        return {"status": "error", "message": "Invalid username or password"}

@app.get("/signup", response_class=HTMLResponse)
async def get_signup(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html")

@app.post("/signup")
async def signup(username: str = Form(...), password: str = Form(...)):
    # 1. Hash the password
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # 2. Save to the database
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return {"status": "success", "message": f"User {username} created! You can now log in."}
    except sqlite3.IntegrityError:
        
        return {"status": "error", "message": "Username already exists. Choose another."}


