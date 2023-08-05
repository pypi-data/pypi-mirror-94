import colorsys
import random

def hsl_to_hex(hue, sat, lum, *, max_value=255):
    rgb = colorsys.hls_to_rgb(hue/max_value,lum/max_value,sat/max_value)
    return '#%02x%02x%02x'%(round(rgb[0]*255),round(rgb[1]*255),round(rgb[2]*255))

def generate_random_pastel_hex(seed=None) -> str:
    if seed:
        random.seed(seed)

    SAT = 125
    LUM = 194

    hue = random.randint(0,255)

    return hsl_to_hex(hue, SAT, LUM)