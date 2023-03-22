from flask import Flask, jsonify, request, render_template, send_file, make_response, Response
from translate import Translator
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import io
from io import BytesIO
import requests
from psaw import PushshiftAPI
import random
import jokepie
import json

app = Flask(__name__)
bytes = BytesIO()
client = jokepie.Client()

class CustomError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        return f"{super().__str__()}. Error code: {self.error_code}"



@app.route('/')
def index():
    return 'Welcome to the Technua API. Dont write []! \n ———— \n Routes: \n  /avatar?nick=[your nickname] \n /blur?image=[image link] \n  /countryball?image=[image link]'


@app.route('/avatar')
def avatar():
   if not request.args.get('nick'):
        w = {
            'error': 'Missing argument(s)!'
        }
        return jsonify(w), 400
   response = requests.get("https://source.unsplash.com/random/1000x1000/?dark%20neon%20background")
   b = Image.open(BytesIO(response.content))
   bg = b.filter(ImageFilter.GaussianBlur(radius=10))

# Создаем объект для рисования на изображении
   draw = ImageDraw.Draw(bg)
   font = ImageFont.truetype("3701-font.ttf", 100)
   text_size = font.getsize(request.args.get('nick'))
   x = (1000 - text_size[0]) // 2
   y = (1000 - text_size[1]) // 2
# Загружаем шрифт Arial.ttf размера 24
   

# Рисуем текст на изображении, используя загруженный шрифт
   draw.text((x, y), request.args.get('nick'), font=font)

# Сохраняем измененное изображение
   
    
    # Преобразуем изображение в байты и отправляем его в ответе
   img_bytes = BytesIO()
   bg.save(img_bytes, format='PNG')
   img_bytes.seek(0)
    
   return img_bytes, 200, {'Content-Type': 'image/png'}


@app.route('/blur')
def blur():
  image = request.args.get('image')
  if not image:
        w = {
            'error': 'Missing argument(s)!'
        }
        return jsonify(w), 400
  b = BytesIO()
  h = requests.get(image)
  mg = Image.open(BytesIO(h.content))
  img = mg.filter(ImageFilter.GaussianBlur(radius=10))
  img.save(b, format='PNG')
  b.seek(0)
  return b, 200, {'Content-Type': 'image/png'}


@app.route('/countryball')
def countryball():
  if not request.args.get('image'):
        w = {
            'error': 'Missing argument(s)!'
        }
        return jsonify(w), 400
  a = Image.open('ball.png').convert('RGBA')
  d = BytesIO()
  c = Image.new('RGBA', (1280, 1280), (0, 0, 0, 0))
  r = requests.get(request.args.get('image'))
  p = Image.open(BytesIO(r.content)).convert('RGBA')
  g = p.resize((1280, 1280))
  g.paste(a, (0, 0), mask=a)
  g.save(d, format='PNG')
  d.seek(0)
  return d, 200, {'Content-Type': 'image/png'}


# создаем новый путь в Flask
@app.route('/jokes')
def jokes():
  joke = client.get_joke()
  j = joke.joke
  a = {
    'joke': j
  }
  response = make_response(json.dumps(a, ensure_ascii=False))
  response.headers['Content-Type'] = 'application/json'
  return response


@app.route('/translator')
def translator():
    b = BytesIO()
    tolang = request.args.get('tolang')
    text = request.args.get('text')
    
    if not text or not tolang:
        w = {
            'error': 'Missing argument(s)!'
        }
        return jsonify(w), 400
    
    translator = Translator(to_lang=tolang)
    t = translator.translate(text)
    
    
    l = {
        'translated': t
    }
  
    response = make_response(json.dumps(l, ensure_ascii=False))
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/imagesearch')
def randomanimals():
  b = request.args.get('prompt')
  if not b:
        w = {
            'error': 'Missing argument(s)!'
        }
        return jsonify(w), 400
  a = requests.get(f'https://source.unsplash.com/random/1000x1000/?{b}')
  c = BytesIO()
  d = Image.open(BytesIO(a.content))
  d.save(c, format='PNG')
  c.seek(0)
  return c, 200, {'Content-Type': 'image/png'}

@app.route('/twodomers')
def twodomers():
  if not request.args.get('image'):
        w = {
            'error': 'Missing argument(s)!'
        }
        return jsonify(w), 400
  a = Image.open('guys.png').convert('RGBA')
  d = BytesIO()
  c = Image.new('RGBA', (2048, 1619), (0, 0, 0, 0))
  r = requests.get(request.args.get('image'))
  p = Image.open(BytesIO(r.content)).convert('RGBA')
  g = p.resize((2048, 1619))
  g.paste(a, (0, 0), mask=a)
  g.save(d, format='PNG')
  d.seek(0)
  return d, 200, {'Content-Type': 'image/png'}


@app.route('/whathow')
def whathow():
  if not request.args.get('image'):
        w = {
            'error': 'Missing argument(s)!'
        }
        return jsonify(w), 400
  a = Image.open('whathow.png').convert('RGBA')
  d = BytesIO()
  c = Image.new('RGBA', (1160, 870), (0, 0, 0, 0))
  r = requests.get(request.args.get('image'))
  p = Image.open(BytesIO(r.content)).convert('RGBA')
  g = p.resize((1160, 870))
  g.paste(a, (0, 0), mask=a)
  g.save(d, format='PNG')
  d.seek(0)
  return d, 200, {'Content-Type': 'image/png'}


app.run(host='0.0.0.0', port=81)