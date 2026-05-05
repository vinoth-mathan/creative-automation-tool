import io
from flask import Flask, request, jsonify, send_from_directory, send_file
import sqlite3
import zipfile
from processor import process_creative

app = Flask(__name__, static_folder='static', static_url_path='')
DB_PATH = 'database.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    conn = get_db_connection()
    accounts = conn.execute('SELECT * FROM accounts').fetchall()
    conn.close()
    return jsonify([dict(row) for row in accounts])

@app.route('/api/dealerships', methods=['GET'])
def get_dealerships():
    account_id = request.args.get('account_id')
    conn = get_db_connection()
    if account_id:
        dealerships = conn.execute('SELECT * FROM dealerships WHERE account_id = ?', (account_id,)).fetchall()
    else:
        dealerships = conn.execute('SELECT * FROM dealerships').fetchall()
    conn.close()
    return jsonify([dict(row) for row in dealerships])

@app.route('/api/generate', methods=['POST'])
def generate():
    if 'background' not in request.files:
        return jsonify({'error': 'No background image uploaded'}), 400
    
    bg_file = request.files['background']
    bg_bytes = bg_file.read()
    
    dealer_ids = request.form.getlist('dealer_ids')
    sizes = request.form.getlist('sizes')
    use_logo = request.form.get('use_logo') == 'true'
    logo_variant = request.form.get('logo_variant', 'light')

    if not dealer_ids or not sizes:
        return jsonify({'error': 'Missing dealers or sizes'}), 400

    conn = get_db_connection()
    size_map = {
        "1080x1080": (1080, 1080),
        "1080x1350": (1080, 1350),
        "1080x1920": (1080, 1920)
    }

    try:
        memory_zip = io.BytesIO()
        with zipfile.ZipFile(memory_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for dealer_id in dealer_ids:
                dealer = conn.execute('SELECT * FROM dealerships WHERE id = ?', (dealer_id,)).fetchone()
                if not dealer: continue

                for size_name in sizes:
                    target_size = size_map.get(size_name)
                    if not target_size: continue

                    out_filename = f"{dealer['name']}_{size_name}.jpg"
                    logo_path = None
                    if use_logo:
                        logo_path = dealer['logo_light_path'] if logo_variant == 'light' else dealer['logo_dark_path']

                    img_bytes = process_creative(bg_bytes, dealer['panel_path'], logo_path, target_size)
                    
                    zipf.writestr(out_filename, img_bytes)

        memory_zip.seek(0)
        return send_file(
            memory_zip,
            mimetype='application/zip',
            as_attachment=True,
            download_name='creatives.zip'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
