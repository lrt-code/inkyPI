# Inky Photo Uploader for Raspberry Pi
This project allows you to upload and display images on a Pimoroni Inky Impression ePaper HAT using a Raspberry Pi.

## 📦 Features
- Upload jpg,jpeg,png images through a web interface.
- Use Button A to show the Pi's local IP address on screen.
- Use Button D to safely shut down the Pi.(Working on)
- Option to rotate uploaded image before display.

## 🧰 Requirements
- Raspberry Pi Zero W or later with Raspberry Pi OS
- Pimoroni Inky Impression 4.0" (7-color)
- Python 3.7+
- Flask, Pillow, gpiozero, and Pimoroni Inky library

## 🚀 Setup Instructions
1. **Clone this repo**:
    bash
    git clone https://github.com/YOUR_USERNAME/inky-web.git
    cd inky-web

2. **Install dependencies**:
    bash
    sudo pip3 install flask pillow --break-system-packages
    sudo pip3 install inky[gpio] --break-system-packages

4. **Run the server**:
    bash
    python3 upload_server.py


5. **Access the web UI**:
    Go to `http://<your_pi_ip>:5000` in a browser on the same network.
