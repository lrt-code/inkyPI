from flask import Flask, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto
from gpiozero import Button
from signal import pause
import os
import socket
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = '/home/pi/inky-web/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

inky = auto()
inky.set_border(inky.WHITE)

# Button setup with safe error handling
try:
    button_a = Button(5)
    button_a_ok = True
except Exception as e:
    print(f"[Warning] Button A could not be initialized: {e}")
    button_a_ok = False

try:
    button_d = Button(6)
    button_d_ok = True
except Exception as e:
    print(f"[Warning] Button D could not be initialized: {e}")
    button_d_ok = False

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "Unavailable"
    s.close()
    return ip

def display_text(text):
    img = Image.new("P", inky.resolution)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    w, h = draw.textsize(text, font=font)
    draw.text(((inky.width - w) / 2, (inky.height - h) / 2), text, inky.BLACK, font=font)
    inky.set_image(img)
    inky.show()

def display_image(path, rotate):
    img = Image.open(path)
    if rotate == 'cw':
        img = img.rotate(-90, expand=True)
    elif rotate == 'ccw':
        img = img.rotate(90, expand=True)
    elif rotate == 'flip':
        img = img.rotate(180, expand=True)

    img.thumbnail(inky.resolution, Image.LANCZOS)
    bg = Image.new("RGB", inky.resolution, (255, 255, 255))
    x = (bg.width - img.width) // 2
    y = (bg.height - img.height) // 2
    bg.paste(img, (x, y))
    inky.set_image(bg)
    inky.show()

@app.route("/", methods=["GET"])
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect("/")
    file = request.files["file"]
    rotate = request.form.get("rotate", "none")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        display_image(filepath, rotate)
        return redirect("/")
    return "Invalid file type"

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if button_a_ok:
    button_a.when_pressed = lambda: display_text(get_ip())

if button_d_ok:
    button_d.when_pressed = lambda: subprocess.call(["sudo", "shutdown", "now"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
