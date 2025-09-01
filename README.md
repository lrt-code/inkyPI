from pathlib import Path

readme_content = """
# Inky Photo Uploader for Raspberry Pi

This project allows you to upload and display images on a Pimoroni Inky Impression ePaper HAT using a Raspberry Pi.

## 📦 Features

- Upload `.jpg`, `.jpeg`, or `.png` images through a web interface.
- Automatically rotate and fit the image to the display.
- Use Button A to show the Pi's local IP address on screen.
- Use Button D to safely shut down the Pi.
- Option to rotate uploaded image before display.

## 🧰 Requirements

- Raspberry Pi Zero W or later with Raspberry Pi OS
- Pimoroni Inky Impression 5.7" 7-color ePaper display
- Python 3.7+
- Flask, Pillow, gpiozero, and Pimoroni Inky library

## 🚀 Setup Instructions

1. **Clone this repo**:

    ```bash
    git clone https://github.com/YOUR_USERNAME/inky-web.git
    cd inky-web
    ```

2. **Install dependencies**:

    ```bash
    sudo pip3 install flask pillow --break-system-packages
    sudo pip3 install inky[gpio] --break-system-packages
    ```

3. **Run the server**:

    ```bash
    python3 upload_server.py
    ```

4. **Access the web UI**:
    Go to `http://<your_pi_ip>:5000` in a browser on the same network.

## 🔧 Hardware Notes

- Make sure SPI is enabled in `raspi-config`.
- Buttons A and D are mapped to GPIO 5 and GPIO 6 respectively.

## 📁 Project Structure

