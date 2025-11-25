from flask import Flask, send_from_directory, redirect, request, url_for, jsonify, abort
import os
import json
import sqlite3

BASE_DIR = os.path.dirname(__file__)
HTML_DIR = os.path.join(BASE_DIR, 'html')
CSS_DIR = os.path.join(BASE_DIR, 'css')
IMG_DIR = os.path.join(BASE_DIR, 'img')
DB_PATH = os.path.join(BASE_DIR, 'logo.db')
GAMES_DIR = os.path.join(BASE_DIR, 'static', 'games')

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/bytearena')


@app.route('/bytearena')
def bytearena():
    return send_from_directory(HTML_DIR, 'ByteArena.html')


@app.route('/biblioteka')
def biblioteka():
    return send_from_directory(HTML_DIR, 'biblioteka.html')


@app.route('/about')
def about():
    return send_from_directory(HTML_DIR, 'about.html')


@app.route('/portfolio')
def portfolio():
    return send_from_directory(HTML_DIR, 'portfolio.html')


@app.route('/news')
def news():
    return send_from_directory(HTML_DIR, 'news.html')


@app.route('/login')
def login():
    return send_from_directory(HTML_DIR, 'login.html')


@app.route('/register')
def register():
    return send_from_directory(HTML_DIR, 'Registe.html')

@app.route('/test_download')
def test_download():
    return send_from_directory(HTML_DIR, 'test_download.html')

@app.route('/Uncharted')
def Uncharted():
    return send_from_directory(HTML_DIR, 'Uncherted.html') 

@app.route('/GodofWar')
def GodOfWar():
    return send_from_directory(HTML_DIR, 'GodofWar.html')

@app.route('/Spider-Man')
def SpiderMan():
    return send_from_directory(HTML_DIR, 'Spider-Man.html')

@app.route('/TheLastofUs')
def TheLastofUs():
    return send_from_directory(HTML_DIR, 'TheLastOfUs.html')

@app.route('/HorizonZeroDawn')
def HorizonZeroDawn():
    return send_from_directory(HTML_DIR, 'HorizonZeroDawn.html')

@app.route('/DeathStranding')
def DeathStranding():
    return send_from_directory(HTML_DIR, 'DeathStranding.html')

@app.route('/DemonSouls')
def DemonSouls():
    return send_from_directory(HTML_DIR, 'DemonSouls.html')

@app.route('/GostOfTsusima')
def GostOfTsusima():
    return send_from_directory(HTML_DIR, 'GostOfTsusima.html') 

@app.route('/profil')
def profil(): 
    return send_from_directory(HTML_DIR, 'profil.html')

@app.route('/basket')
def basket():
    return send_from_directory(HTML_DIR, 'basket.html') 

@app.route('/do_basket', methods=['GET'])
def do_basket():
    return send_from_directory(HTML_DIR, 'basket.html')

@app.route('/do_logout', methods=['GET'])
def do_logout():
    return send_from_directory(HTML_DIR, 'login.html')

USERS_FILE = os.path.join(BASE_DIR, 'users.json')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS basket (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            game TEXT NOT NULL,
            count INTEGER NOT NULL DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/do_register', methods=['POST'])
def do_register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    if not username or not password:
        return redirect(url_for('register') + '?msg=missing')

    users = _load_users()
    if username in users:
        return redirect(url_for('register') + '?msg=exists')

    users[username] = {'password': password}
    _save_users(users)
    return redirect(url_for('login') + '?msg=created')


@app.route('/do_login', methods=['POST'])
def do_login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    if not username or not password:
        return redirect(url_for('login') + '?msg=missing')

    users = _load_users()
    entry = users.get(username)
    if entry and entry.get('password') == password:
        resp = redirect('/profil?msg=logged')
        resp.set_cookie('user', username, max_age=60*60*24*7)
        return resp
    else:
        return redirect(url_for('login') + '?msg=failed')

@app.route('/do_profil', methods=['POST'])
def do_profil():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    if not username or not password:
        return redirect(url_for('profil') + '?msg=missing')
    if username == "alex_thndr" and password == "alex_thndr":
        return redirect(url_for('profil') + '?msg=logged')
    else:
        return redirect(url_for('profil') + '?msg=failed')

@app.route('/logout', methods=['GET'])
def logout():
    resp = redirect('/login?msg=logged_out')
    resp.delete_cookie('user')
    return resp

@app.route('/css/<path:filename>')
def css_files(filename):
    return send_from_directory(CSS_DIR, filename)


@app.route('/img/<path:filename>')
def img_files(filename):
    return send_from_directory(IMG_DIR, filename)


@app.route('/api/basket', methods=['GET'])
def api_basket():
    user = request.cookies.get('user')
    if not user:
        return jsonify({'error':'not logged in'}), 401
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, game, count FROM basket WHERE user=?', (user,))
    items = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(items)

@app.route('/api/basket/add', methods=['POST'])
def api_basket_add():
    user = request.cookies.get('user')
    if not user:
        return jsonify({'error':'not logged in'}), 401
    game = request.form.get('game') or (request.get_json() or {}).get('game')
    if not game:
        return jsonify({'error':'missing game'}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, count FROM basket WHERE user=? AND game=?', (user, game))
    row = cur.fetchone()
    if row:
        cur.execute('UPDATE basket SET count=count+1 WHERE id=?', (row['id'],))
    else:
        cur.execute('INSERT INTO basket (user, game, count) VALUES (?, ?, 1)', (user, game))
    conn.commit()
    conn.close()
    return jsonify({'ok':True})

@app.route('/api/basket/remove', methods=['POST'])
def api_basket_remove():
    user = request.cookies.get('user')
    if not user:
        return jsonify({'error':'not logged in'}), 401
    basket_id = request.form.get('basket_id') or (request.get_json() or {}).get('basket_id')
    if not basket_id:
        return jsonify({'error':'missing basket_id'}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM basket WHERE id=? AND user=?', (basket_id, user))
    conn.commit()
    conn.close()
    return jsonify({'ok':True})

def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return {}

@app.route('/download/<filename>')
def download(filename):
    # Prevent path traversal and ensure the file exists
    # Normalize and build absolute path
    safe_games_dir = os.path.normpath(GAMES_DIR)
    file_path = os.path.normpath(os.path.join(safe_games_dir, filename))

    # Ensure the resolved path is inside the games directory
    if not file_path.startswith(safe_games_dir + os.sep) and file_path != safe_games_dir:
        abort(400)

    if not os.path.isfile(file_path):
        abort(404)

    # send_from_directory expects the directory and the filename (not a full path)
    return send_from_directory(safe_games_dir, os.path.relpath(file_path, safe_games_dir), as_attachment=True)

def _save_users(d):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True, threaded=True)
