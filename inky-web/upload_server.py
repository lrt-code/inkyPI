import os
import socket
from flask import Flask, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto
from gpiozero import Button
from signal import pause
import subprocess

UPLOAD_FOLDER = '/home/pi/inky_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ROTATION_FILE = '/tmp/inky_rotation.txt'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

inky = auto()
inky.set_border(inky.WHITE)

try:
    button_a = Button(5)
    button_d = Button(6)
except Exception as e:
    print(f"[Warning] Button A or D could not be initialized: {e}")
    button_a = None
    button_d = None

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    s.close()
    return ip

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def display_image(filepath, rotate=0):
    img = Image.open(filepath)
    img = img.convert("RGB")

    w, h = inky.resolution
    if rotate:
        img = img.rotate(rotate, expand=True)

    if img.width > w or img.height > h:
        img.thumbnail((w, h), Image.LANCZOS)

    bg = Image.new("RGB", (w, h), (255, 255, 255))
    x = (w - img.width) // 2
    y = (h - img.height) // 2
    bg.paste(img, (x, y))
    inky.set_image(bg)
    inky.show()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    rotation = int(request.form.get('rotation', 0))

    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        with open(ROTATION_FILE, 'w') as f:
            f.write(str(rotation))
        display_image(filepath, rotate=rotation)
        return redirect('/')
    return 'Invalid file type'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def show_ip():
    ip = get_ip()
    w, h = inky.resolution
    img = Image.new("P", (w, h))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 18)
    except:
        font = ImageFont.load_default()
    text_w, text_h = draw.textsize(ip, font=font)
    draw.text(((w - text_w) / 2, (h - text_h) / 2), ip, fill=0, font=font)
    inky.set_image(img)
    inky.show()

def shutdown_pi():
    subprocess.call(["sudo", "shutdown", "now"])

if button_a:
    button_a.when_pressed = show_ip

if button_d:
    button_d.when_pressed = shutdown_pi

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
