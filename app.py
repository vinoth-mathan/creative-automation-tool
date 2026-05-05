import io
import os
import sqlite3
import zipfile
import re
from flask import Flask, request, jsonify, send_from_directory, send_file
from processor import process_creative

app = Flask(__name__, static_folder='static', static_url_path='')
DB_PATH = 'database.sqlite'
VALID_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
SIZE_MAP = {
    '1080x1080': (1080, 1080),
    '1080x1350': (1080, 1350),
    '1080x1920': (1080, 1920),
}


def safe_slug(value):
    cleaned = re.sub(r'[^A-Za-z0-9._-]+', '-', (value or '').strip())
    return cleaned.strip('-') or 'item'


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def is_allowed_upload(filename, content_type):
    if not filename:
        return False
    _, ext = os.path.splitext(filename.lower())
    if ext not in VALID_IMAGE_EXTENSIONS:
        return False
    if content_type not in {'image/jpeg', 'image/png'}:
        return False
    return True


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    conn = get_db_connection()
    accounts = conn.execute('SELECT * FROM accounts ORDER BY name').fetchall()
    conn.close()
    return jsonify([dict(row) for row in accounts])


@app.route('/api/dealerships', methods=['GET'])
def get_dealerships():
    account_id = request.args.get('account_id')
    conn = get_db_connection()
    if account_id:
        dealerships = conn.execute(
            'SELECT * FROM dealerships WHERE account_id = ? ORDER BY name',
            (account_id,),
        ).fetchall()
    else:
        dealerships = conn.execute('SELECT * FROM dealerships ORDER BY name').fetchall()
    conn.close()
    return jsonify([dict(row) for row in dealerships])


@app.route('/api/additional-assets', methods=['GET'])
def get_additional_assets():
    assets_dir = os.path.join('assets', 'Logos')
    excluded = {'logo-dark.png', 'logo-light.png'}
    options = []

    if os.path.exists(assets_dir):
        for name in sorted(os.listdir(assets_dir)):
            lower_name = name.lower()
            if lower_name in excluded:
                continue
            full_path = os.path.join(assets_dir, name)
            if os.path.isfile(full_path):
                _, ext = os.path.splitext(lower_name)
                if ext in VALID_IMAGE_EXTENSIONS:
                    options.append(
                        {
                            'label': name,
                            'value': os.path.join('assets', 'Logos', name).replace('\\\\', '/'),
                        }
                    )

    return jsonify(options)


@app.route('/api/generate', methods=['POST'])
def generate_zip():
    if 'background' not in request.files:
        return jsonify({'error': 'No background image uploaded'}), 400

    bg_file = request.files['background']
    if not is_allowed_upload(bg_file.filename, bg_file.content_type):
        return jsonify({'error': 'Background must be JPG or PNG'}), 400

    bg_bytes = bg_file.read()
    dealer_ids = request.form.getlist('dealer_ids')
    sizes = request.form.getlist('sizes')
    use_logo = request.form.get('use_logo') == 'true'
    logo_variant = request.form.get('logo_variant', 'light')
    use_additional_asset = request.form.get('use_additional_asset') == 'true'
    additional_asset_path = request.form.get('additional_asset_path')
    additional_asset_file = request.files.get('additional_asset_file')

    if not dealer_ids or not sizes:
        return jsonify({'error': 'Missing dealers or sizes'}), 400

    additional_asset_bytes = None
    if use_additional_asset and additional_asset_file and additional_asset_file.filename:
        if not is_allowed_upload(additional_asset_file.filename, additional_asset_file.content_type):
            return jsonify({'error': 'Additional asset upload must be JPG or PNG'}), 400
        additional_asset_bytes = additional_asset_file.read()

    conn = get_db_connection()
    try:
        memory_zip = io.BytesIO()
        with zipfile.ZipFile(memory_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for dealer_id in dealer_ids:
                dealer = conn.execute('SELECT * FROM dealerships WHERE id = ?', (dealer_id,)).fetchone()
                if not dealer:
                    continue
                account = conn.execute('SELECT name FROM accounts WHERE id = ?', (dealer['account_id'],)).fetchone()
                account_name = account['name'] if account else 'account'

                for size_name in sizes:
                    target_size = SIZE_MAP.get(size_name)
                    if not target_size:
                        continue

                    logo_path = None
                    if use_logo:
                        logo_path = dealer['logo_light_path'] if logo_variant == 'light' else dealer['logo_dark_path']

                    rendered = process_creative(
                        bg_bytes=bg_bytes,
                        panel_path=dealer['panel_path'],
                        logo_path=logo_path,
                        target_size=target_size,
                        additional_asset_path=additional_asset_path if use_additional_asset else None,
                        additional_asset_bytes=additional_asset_bytes,
                    )

                    filename = (
                        f"{safe_slug(account_name)}_{safe_slug(dealer['name'])}_"
                        f"{dealer['id']}_{size_name}.jpg"
                    )
                    zipf.writestr(filename, rendered)

        memory_zip.seek(0)
        return send_file(memory_zip, mimetype='application/zip', as_attachment=True, download_name='creatives.zip')

    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
    finally:
        conn.close()


@app.route('/api/generate-single', methods=['POST'])
def generate_single():
    if 'background' not in request.files:
        return jsonify({'error': 'No background image uploaded'}), 400

    bg_file = request.files['background']
    if not is_allowed_upload(bg_file.filename, bg_file.content_type):
        return jsonify({'error': 'Background must be JPG or PNG'}), 400

    dealer_id = request.form.get('dealer_id')
    size_name = request.form.get('size')
    use_logo = request.form.get('use_logo') == 'true'
    logo_variant = request.form.get('logo_variant', 'light')
    use_additional_asset = request.form.get('use_additional_asset') == 'true'
    additional_asset_path = request.form.get('additional_asset_path')
    additional_asset_file = request.files.get('additional_asset_file')

    if not dealer_id or not size_name:
        return jsonify({'error': 'Missing dealer or size'}), 400

    target_size = SIZE_MAP.get(size_name)
    if not target_size:
        return jsonify({'error': 'Invalid size'}), 400

    additional_asset_bytes = None
    if use_additional_asset and additional_asset_file and additional_asset_file.filename:
        if not is_allowed_upload(additional_asset_file.filename, additional_asset_file.content_type):
            return jsonify({'error': 'Additional asset upload must be JPG or PNG'}), 400
        additional_asset_bytes = additional_asset_file.read()

    conn = get_db_connection()
    try:
        dealer = conn.execute('SELECT * FROM dealerships WHERE id = ?', (dealer_id,)).fetchone()
        if not dealer:
            return jsonify({'error': 'Dealer not found'}), 404

        logo_path = None
        if use_logo:
            logo_path = dealer['logo_light_path'] if logo_variant == 'light' else dealer['logo_dark_path']

        rendered = process_creative(
            bg_bytes=bg_file.read(),
            panel_path=dealer['panel_path'],
            logo_path=logo_path,
            target_size=target_size,
            additional_asset_path=additional_asset_path if use_additional_asset else None,
            additional_asset_bytes=additional_asset_bytes,
        )

        return send_file(
            io.BytesIO(rendered),
            mimetype='image/jpeg',
            as_attachment=True,
            download_name=f"{dealer['name']}_{size_name}.jpg",
        )

    except Exception as exc:
        return jsonify({'error': str(exc)}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
