import digitalio
import busio
import board
from adafruit_epd.epd import Adafruit_EPD
from datetime import datetime
from adafruit_epd.ssd1675 import Adafruit_SSD1675
from PIL import Image, ImageDraw, ImageFont

# First define some color constants
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)
RED = (0xFF, 0x00, 0x00)

# Next define some constants to allow easy resizing of shapes and colors
BORDER = 20
FONTSIZE = 24
BACKGROUND_COLOR = BLACK
FOREGROUND_COLOR = WHITE
TEXT_COLOR = BLACK

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)
srcs = None
cnt = 0

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

def random_fill(display):
	print("*** Updating screen with random fil")
	display.fill(Adafruit_EPD.WHITE)
	 
	display.fill_rect(0, 0, 50, 60, Adafruit_EPD.BLACK)
	display.hline(80, 30, 60, Adafruit_EPD.BLACK)
	display.vline(80, 30, 60, Adafruit_EPD.BLACK)
	 
	display.display()
	print('*** Printing Display Done')

def write_text(display, text):
	print("Generating Text")
	print("Generating Text - Rotation")
	display.rotation = 3
	print("Generating Text - Create Image")
	image = Image.new("RGB", (display.width, display.height))
	print("Generating Text - Draw")
	draw = ImageDraw.Draw(image)
	print("Generating Text - rectangle Fil")
	draw.rectangle((0, 0, display.width - 1, display.height - 1), fill=BACKGROUND_COLOR)
	print("Generating Text - rectangle border")
	draw.rectangle(
	    (BORDER, BORDER, display.width - BORDER - 1, display.height - BORDER - 1),
	    fill=FOREGROUND_COLOR,
	)
	print("Generating Text - Font size")
	(font_width, font_height) = font.getsize(text)
	print("Generating Text - text")
	draw.text(
	    (display.width // 2 - font_width // 2, display.height // 2 - font_height // 2),
	    text,
	    font=font,
	    fill=TEXT_COLOR,
	)

	# Display image.
	print("Generating Text - Display Image display.image")
	display.image(image)
	print("Generating Text - Display Image display.display")
	display.display()
	print("Generating Text Done")

def detect_button(up, down, display, status):
	if status["up"] and not up.value:
		print("Up Button Pushed")
		status["up"] = False
		status["down"] = True
		write_text(display, 'Hello')
	elif not status["up"] and up.value:
		status["up"] = True
		print("Up Button Status Reset")

	if status["down"] and not down.value:
		status["up"] = True
		status["down"] = False
		print("Down Button Pushed")
		write_text(display, 'World')
	elif not status["down"] and down.value:
		status["down"] = True
		print("Down Button Status Reset")


def main():
	print("*** Main init")
	print('*** Init Display')
	display = Adafruit_SSD1675(122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=srcs,
                          rst_pin=rst, busy_pin=busy)
	# fill_display()

	up_button = digitalio.DigitalInOut(board.D5)
	up_button.switch_to_input()
	down_button = digitalio.DigitalInOut(board.D6)
	down_button.switch_to_input()

	status = {
		"up" : True,
		"down": True
	}

	while True:
		detect_button(up_button, down_button, display, status)

main()
