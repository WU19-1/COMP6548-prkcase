import autopy
import random

random_hex = str(hex(random.randint(1048575,16777216)))[2:] + '.png'

autopy.bitmap.capture_screen().save(random_hex)
