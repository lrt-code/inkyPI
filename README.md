 #HEY!!! GPT MADE THIS!!!
I got this hat in the hope of have a simple eink picture display but none of the projects was working, so now im here with gpt...



# Inky Photo Uploader for Raspberry Pi
This project allows you to upload and display images on a Pimoroni Inky Impression ePaper HAT using a Raspberry Pi.

## 📦 Features
- Upload jpg,jpeg,png images through a web interface.
- Option to rotate uploaded image before display.

## 🧰 Requirements
- Raspberry Pi Zero W or later with Raspberry Pi OS
- Pimoroni Inky Impression 4.0" 7-color (this would work with other inky hats but I dont have the mony to buy them yet so if you have one and want to try please tell me if it works)
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


##Things to add##
- Use Button A to show the Pi's local IP address on screen.(working on)
- Use Button D to safely shut down the Pi.(Working on)
- a weather mode on a button
- a way to look at what photos have been uploaded and and it cycles them.
