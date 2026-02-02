"""
Enhanced Document Generator Module (Stealth Edition)
"""
import random
import time
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter

COLOR_SCHEMES = [{"primary": (0, 51, 102), "accent": (255, 255, 255), "text": (51, 51, 51)}]

def add_simple_noise(img, intensity=3):
    pixels = img.load()
    for _ in range(img.size[0] * img.size[1] // 10):
        x, y = random.randint(0, img.size[0]-1), random.randint(0, img.size[1]-1)
        r, g, b = pixels[x, y][:3]
        pixels[x, y] = (max(0, min(255, r + random.randint(-intensity, intensity))), 
                        max(0, min(255, g + random.randint(-intensity, intensity))), 
                        max(0, min(255, b + random.randint(-intensity, intensity))) )
    return img

def randomize_position(x, y, v=3): return (x + random.randint(-v, v), y + random.randint(-v, v))

def generate_student_id(first, last, school):
    img = Image.new("RGB", (650, 400), (250, 250, 250))
    draw = ImageDraw.Draw(img)
    draw.rectangle([randomize_position(0, 0), randomize_position(650, 60)], fill=(0, 51, 102))
    draw.text(randomize_position(325, 30), school, fill=(255, 255, 255), anchor="mm")
    draw.text(randomize_position(200, 150), f"Name: {first} {last}", fill=(0, 0, 0))
    img = add_simple_noise(img)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def generate_transcript(first, last, dob, school):
    img = Image.new("RGB", (850, 1100), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text(randomize_position(425, 50), school.upper(), fill=(0, 51, 102), anchor="mm")
    draw.text(randomize_position(425, 100), "ACADEMIC TRANSCRIPT", fill=(0, 0, 0), anchor="mm")
    draw.text(randomize_position(100, 200), f"Student: {first} {last}\nDOB: {dob}", fill=(0, 0, 0))
    img = add_simple_noise(img)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def select_document_type(): return "transcript" if random.random() < 0.8 else "student_id"
