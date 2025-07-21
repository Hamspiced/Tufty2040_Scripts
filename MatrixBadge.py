from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pimoroni import Button
from random import randint, choice
import time
import jpegdec
import qrcode

# Init
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
button_c = Button(9, invert=False)
WIDTH, HEIGHT = display.get_bounds()

# ---- COLORS ----
LIGHTEST = display.create_pen(245, 242, 232)  # Beige
LIGHT     = display.create_pen(200, 200, 200) # Light Gray
DARK      = display.create_pen(80, 80, 80)    # Charcoal (Matrix area background)
DARKEST   = display.create_pen(0, 0, 0)       # Black

# ---- TEXT CONTENT ----
COMPANY_NAME = "MidwestGadgets"
NAME = "Hamspiced"
BLURB1 = "Nick Gambino"
BLURB2 = "Owner/Maker"
BLURB3 = "@Hamspiced"
QR_TEXT = "MidwestGadgets.com"
IMAGE_NAME = "squirrel.jpg"

# ---- Matrix Rain Configuration ----
MATRIX_CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789"
MATRIX_BG_COLOR = DARK                       # Background inside badge behind Matrix
#MATRIX_CHAR_COLOR = display.create_pen(180, 255, 180)  # Greenish Matrix characters
MATRIX_CHAR_COLOR = display.create_pen(0, 0, 0)  # Greenish Matrix characters


# ---- LAYOUT ----
BORDER_SIZE = 4
PADDING = 10
COMPANY_HEIGHT = 40
FONT_SIZE = 2
CHAR_WIDTH = 8 * FONT_SIZE
CHAR_HEIGHT = 8 * FONT_SIZE
COLS = WIDTH // 6  # Increased column density
ROWS = HEIGHT // CHAR_HEIGHT
MATRIX_X = BORDER_SIZE
MATRIX_Y = COMPANY_HEIGHT + BORDER_SIZE
MATRIX_W = WIDTH - (BORDER_SIZE * 2)
MATRIX_H = HEIGHT - COMPANY_HEIGHT - (BORDER_SIZE * 2)
drops = [randint(0, ROWS) for _ in range(COLS)]

def draw_matrix_overlay():
    for i in range(COLS):
        x = int(i * WIDTH / COLS)
        y = drops[i] * CHAR_HEIGHT
        if MATRIX_X <= x < MATRIX_X + MATRIX_W and MATRIX_Y <= y < MATRIX_Y + MATRIX_H:
            display.set_pen(MATRIX_CHAR_COLOR)
            display.set_font("bitmap6")
            display.text(choice(MATRIX_CHARSET), x, y, WIDTH, FONT_SIZE)
        drops[i] += 1
        if drops[i] * CHAR_HEIGHT > HEIGHT or randint(0, 100) > 97:
            drops[i] = 0

def draw_badge(shift=0):
    display.set_pen(LIGHTEST)
    display.clear()
    display.set_pen(MATRIX_BG_COLOR)
    display.rectangle(MATRIX_X, MATRIX_Y, MATRIX_W, MATRIX_H)

def draw_overlay_content(shift=0):
    display.set_pen(DARKEST)
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), COMPANY_HEIGHT)

    display.set_pen(LIGHT)
    display.set_font("bitmap6")
    display.text(COMPANY_NAME, BORDER_SIZE + PADDING + shift, BORDER_SIZE + PADDING, WIDTH, 3)

    display.set_pen(LIGHTEST)
    display.set_font("bitmap8")
    display.text(NAME, BORDER_SIZE + PADDING + shift, BORDER_SIZE + PADDING + COMPANY_HEIGHT, WIDTH, 5)

    display.set_pen(DARKEST)
    display.text("*", BORDER_SIZE + PADDING + 120 + PADDING, 105, 160, 2)
    display.text("*", BORDER_SIZE + PADDING + 120 + PADDING, 140, 160, 2)
    display.text("*", BORDER_SIZE + PADDING + 120 + PADDING, 175, 160, 2)

    display.set_pen(LIGHTEST)
    display.text(BLURB1, BORDER_SIZE + PADDING + 135 + PADDING, 105, 160, 2)
    display.text(BLURB2, BORDER_SIZE + PADDING + 135 + PADDING, 140, 160, 2)
    display.text(BLURB3, BORDER_SIZE + PADDING + 135 + PADDING, 175, 160, 2)

def show_photo():
    j = jpegdec.JPEG(display)
    j.open_file(IMAGE_NAME)
    display.set_pen(DARKEST)
    display.rectangle(PADDING, HEIGHT - ((BORDER_SIZE * 2) + PADDING) - 120, 120 + (BORDER_SIZE * 2), 120 + (BORDER_SIZE * 2))
    j.decode(BORDER_SIZE + PADDING, HEIGHT - (BORDER_SIZE + PADDING) - 120)
    display.set_pen(LIGHTEST)
    display.text("QR", 240, 215, 160, 2)

def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size

def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.set_pen(LIGHTEST)
    display.rectangle(ox, oy, size, size)
    display.set_pen(DARKEST)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)

def show_qr():
    display.set_pen(DARK)
    display.clear()
    code = qrcode.QRCode()
    code.set_text(QR_TEXT)
    size, module_size = measure_qr_code(HEIGHT, code)
    left = int((WIDTH // 2) - (size // 2))
    top = int((HEIGHT // 2) - (size // 2))
    draw_qr_code(left, top, HEIGHT, code)

def glitch_animation():
    for _ in range(2):
        display.set_pen(choice([LIGHT, DARK, LIGHTEST]))
        display.clear()
        display.update()
        time.sleep(0.02)
    for _ in range(25):
        y = randint(MATRIX_Y, MATRIX_Y + MATRIX_H - 1)
        h = randint(1, 2)
        display.set_pen(choice([LIGHTEST, LIGHT, DARK]))
        display.rectangle(0, y, WIDTH, h)
    display.update()
    time.sleep(0.03)
    for shift in [-2, 3, -1, 0]:
        draw_badge(shift)
        draw_matrix_overlay()
        draw_overlay_content(shift)
        if badge_mode == "photo":
            show_photo()
        else:
            show_qr()
        display.update()
        time.sleep(0.03)

# ---- RENDER LOOP ----
badge_mode = "photo"
draw_badge()
draw_matrix_overlay()
draw_overlay_content()
show_photo()
display.update()

last_matrix_time = time.ticks_ms()
matrix_interval = 50

last_glitch_time = time.ticks_ms()
glitch_interval = 15000

while True:
    current_time = time.ticks_ms()

    if time.ticks_diff(current_time, last_matrix_time) > matrix_interval:
        draw_badge()
        draw_matrix_overlay()
        draw_overlay_content()
        if badge_mode == "photo":
            show_photo()
        else:
            show_qr()
        display.update()
        last_matrix_time = current_time

    if time.ticks_diff(current_time, last_glitch_time) > glitch_interval:
        glitch_animation()
        last_glitch_time = current_time

    if button_c.is_pressed:
        if badge_mode == "photo":
            badge_mode = "qr"
            show_qr()
        else:
            badge_mode = "photo"
            draw_badge()
            draw_matrix_overlay()
            draw_overlay_content()
            show_photo()
        display.update()
        time.sleep(1)