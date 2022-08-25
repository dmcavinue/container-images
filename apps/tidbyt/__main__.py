from flask import Flask, abort, jsonify, request, make_response, url_for

from PIL import Image, ImageDraw, ImageFont
from string import ascii_letters
import textwrap

from colour import Color

import base64
from io import BytesIO

import http.client
import os
 
def pil_base64(image):
  img_buffer = BytesIO()
  image.save(img_buffer, format='gif')
  byte_data = img_buffer.getvalue()
  base64_str = base64.b64encode(byte_data)
  return base64_str

def determine_text_size(text: str):
    if len(text) < 5:
        size=20
    elif len(text) < 6:
        size=17
    elif len(text) < 7:
        size=15
    elif len(text) < 8:
        size=12
    elif len(text) < 9:
        size=11
    elif len(text) < 10:
        size=10
    elif len(text) < 12: 
        size=9
    elif len(text) < 14:
        size=15
    elif len(text) < 16:
        size=12
    elif len(text) < 18:
        size=11
    elif len(text) < 20:
        size=10
    elif len(text) <= 34 :
        size=9
    elif len(text) > 34:
        size=14
    return size

def check_color(color):
    if color is None:
        color='red'
    elif color =='':
        color='red'

    try:
        # Converting 'deep sky blue' to 'deepskyblue'
        color = color.replace(" ", "")
        Color(color)
        # if everything goes fine then return True
        return color
    except ValueError: # The color code was not found
        return "red"

def create_image(text: str, size: int, color: str):    
    # Create Image
    img = Image.new('RGB', (64, 32), color = 'black')
    # Load custom font
    font = ImageFont.truetype(font='SourceCodePro-Bold.ttf', size=size)
    # Create DrawText object
    draw = ImageDraw.Draw(im=img)    
    # Calculate the average length of a single character of our font.
    avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
    # Translate this average length into a character count
    max_char_count = int(img.size[0] / avg_char_width)
    # Create a wrapped text object using scaled character count
    text = textwrap.fill(text=text, width=max_char_count)
    ## Add text to the image
    draw.text(xy=(img.size[0]/2, img.size[1] / 2 - .5), text=text, font=font, fill= color, anchor='mm')
    return img

app = Flask(__name__)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
    
@app.route('/msg', methods = ['POST'])
def data():

    tidbyt_deviceid = os.getenv('TIDBYT_DEVICEID')
    tidbyt_token = os.getenv('TIDBYT_TOKEN')

    text = request.args.get('text')
    if len(text) > 34:
        text='TOO BIG'
    size=determine_text_size(text)
    color = request.args.get('color')
    color = check_color(color)
    img =  create_image(text, size, color) 
    #img.show()
    
    #encode image
    image_base64=pil_base64(img)
    image_encoded=image_base64.decode('utf-8')
    
    #API: token 
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer {}".format(tidbyt_token)
        }

    #API: Image-base64 encoded, installationID if you want to save applet, background deploy
    payload = "{\n\"image\":\"" + image_encoded +"\",\n  \"installationID\": \"\",\n  \"background\": false\n}"

    #API: Set address
    conn = http.client.HTTPSConnection("api.tidbyt.com")
    #API: Post to Tidbyt API DeviceID, payload and header
    conn.request("POST", "/v0/devices/{}/push".format(tidbyt_deviceid), payload, headers)

    #API: Response captured    
    res = conn.getresponse()
    data = res.read()

    #Local API Response        
    return jsonify({"color":color,"size":size,"Text":text,"Tidbyt-reply":data.decode("utf-8")})

if __name__ == '__main__':
    app.run(debug=True)
