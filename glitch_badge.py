# Monochrome badge with glitch flicker and text shift (Tufty2040)
from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pimoroni import Button
from random import randint, choice
import time
import jpegdec
import qrcode

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
button_c = Button(9, invert=False)

WIDTH, HEIGHT = display.get_bounds()

# Midwest Gadgets Monochrome Palette
LIGHTEST = display.create_pen(245, 242, 232)   # Beige
LIGHT    = display.create_pen(200, 200, 200)   # Light Gray
DARK     = display.create_pen(80, 80, 80)      # Charcoal
DARKEST  = display.create_pen(0, 0, 0)         # Black

GLITCH_COLORS = [LIGHTEST, LIGHT, DARK, DARKEST]

# Badge content
COMPANY_NAME = "MidwestGadgets"
NAME = "BIG NAME"
BLURB1 = "Firstname Lastname"
BLURB2 = "Title"
BLURB3 = "Website"
QR_TEXT = "QRCODE_WEBSITE_ADDRESS"
IMAGE_NAME = "squirrel.jpg"

# Layout constants
BORDER_SIZE = 4
PADDING = 10
COMPANY_HEIGHT = 40


def draw_badge(shift=0):
    display.set_pen(LIGHTEST)
    display.clear()

    display.set_pen(DARK)
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), HEIGHT - (BORDER_SIZE * 2))

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
    # Step 1: Flash flicker
    for _ in range(3):
        display.set_pen(choice(GLITCH_COLORS))
        display.clear()
        display.update()
        time.sleep(0.02)

    # Step 2: Horizontal glitch lines
    for _ in range(30):
        y = randint(0, HEIGHT - 2)
        h = randint(1, 2)  # thinner glitch
        display.set_pen(choice(GLITCH_COLORS))
        display.rectangle(0, y, WIDTH, h)
    display.update()
    time.sleep(0.03)

    # Step 3: Text shift flicker
    for shift in [-2, 3, -1, 0]:
        draw_badge(shift)
        show_photo()
        display.update()
        time.sleep(0.03)


# Initial screen
badge_mode = "photo"
draw_badge()
show_photo()
display.update()

# Glitch timer
last_glitch_time = time.ticks_ms()
glitch_interval = 15000  # 15 seconds

while True:
    current_time = time.ticks_ms()

    if time.ticks_diff(current_time, last_glitch_time) > glitch_interval:
        glitch_animation()
        if badge_mode == "photo":
            draw_badge()
            show_photo()
        else:
            show_qr()
        display.update()
        last_glitch_time = current_time

    if button_c.is_pressed:
        if badge_mode == "photo":
            badge_mode = "qr"
            show_qr()
        else:
            badge_mode = "photo"
            draw_badge()
            show_photo()
        display.update()
        time.sleep(1)
