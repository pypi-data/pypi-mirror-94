
"""
    core/image.py

    this module is responsible for:
        - image to PNG
        - image to ICO
        - image to STRING
        (useful stuff in working with images)

    author: @alexzander
"""


# python
import binascii
import optparse
import pytesseract

# 3rd party
import numpy as np # pip install numpy
from PIL import Image # pip install Pillow

# core package (pip install python-core)
from core.__path import *
from core.system import *
from core.aesthetics import *


# you need to set up in your environment variables TESS = { path your tesseract.exe file }
if "TESS" not in os.environ.keys():
    raise NotFoundError
pytesseract.pytesseract.tesseract_cmd = os.environ["TESS"]


class image_Exception(Exception):
    def __init__(self, message=""):
        self.message = message


class NotAnImageError(image_Exception):
    """ file is not an image """
    pass


def rgb_2_hex(red: int, green: int, blue: int):
    try:
        red = int(red)
        green = int(green)
        blue = int(blue)
    except:
        raise ValueError("@red, @green or @blue cannot be converted to integer")
    return "#{:02x}{:02x}{:02x}".format(red, green, blue)


def decode_qr_bar_code(path):
    """ return Decoded class """

    # validation
    if type(path) != str:
        path = str(path)
    if not is_file(path):
        raise NotAFileError
    # /validation

    img = cv2.imread(path)
    decoded = pyzbar.decode(img)
    return decoded


def hex_2_rgb(hexadecimal: int):
    if type(hexadecimal) != str:
        raise TypeError

    # starting from 1 -> meaning that is excluding the '#'
    return map(ord, hexadecimal[1:].decode("hex"))


def image_to_str(path: str):
    """ return a string from image """
    return pytesseract.image_to_string(Image.open(path))


def save_pdf_from_image(path: str, dst_folder: str):
    """ saves pdf from image to dst specified by user """
    image_name = path.split("\\")[-1].split(".")[0]
    binary_pdf = pytesseract.image_to_pdf_or_hocr(Image.open(path))

    with open(dst_folder + "\\{}.pdf".format(image_name), "wb") as bin_file:
        bin_file.truncate(0)
        bin_file.write(binary_pdf)


def image_to_pdf(path: str):
    """ raw binary content of a pdf file from image file """
    return pytesseract.image_to_pdf_or_hocr(Image.open(path))


def image_to_png(path: str):
    path = get_path_from_absolute(path)
    filename = get_file_name(path)

    img = Image.open(path)
    img.save("{}/{}.png".format(path, filename))


def image_to_ico(path: str):
    img = Image.open(path)
    filename = get_file_name(path)
    path = get_path_from_absolute(path)
    img.save("{}/{}.ico".format(path, filename))

def save_gif(dst, images, fps=1):
    if type(images) != list:
        raise TypeError("param @images should be type list.")
    if type(dst) != str:
        raise TypeError("param @dst should be type str.")

    if not dst.endswith(".gif"):
        raise ValueError("param @destinaion should end with .gif extension.")

    import imageio
    images = [imageio.imread(image_abspath) for image_abspath in images]
    imageio.mimsave(dst, images, fps=fps)


def print_image(path):
    def get_ansi_color_code(r, g, b):
        if r == g and g == b:
            if r < 8:
                return 16
            if r > 248:
                return 231
            return round(((r - 8) / 247) * 24) + 232
        return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)


    def get_color(r, g, b):
        return "\x1b[48;5;{}m \x1b[0m".format(int(get_ansi_color_code(r,g,b)))

    img = Image.open(path)
    print(img.size)

    height = 80
    width = int((img.width / img.height) * height)

    img = img.resize((width, height), Image.ANTIALIAS)
    img_array = np.asarray(img)
    print(img_array.shape)

    for h_index in range(height):
        for w_index in range(width):
            pix = img_array[h_index][w_index]
            print(get_color(pix[0], pix[1], pix[2]), sep='', end='')
        print()

# TODO
def hide_text_in_image(path, text):
    # hide text, trebuie sa vezi daca nu este encrypted deja
    pass

# TODO
def reveal_text_from_image(path):
    # reveal text, trebuie sa vezi daca exista ceva sa poti sa dai reveal
    pass


if __name__ == '__main__':
    pass