from PIL import Image
import inspect
import requests

DRAWING_CHARS = ['#', '#', '#', '#', '#', '#', '#', ';', ':', ',', '.']


def resize_image(image,new_width=50):
    width,height = image.size
    ratio = height//width
    new_height = int(new_width*ratio*0.80)
    resized_image = image.resize((new_width,new_height))
    return(resized_image)

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([DRAWING_CHARS[pixel//27] for pixel in pixels])
    return(characters)
    

def main(new_width=50):
    path =  inspect.getfile(requests)[:-20]+"m1key/profile.jpeg"
    image = Image.open(path)
    new_image = pixels_to_ascii((resize_image(image)).convert("L"))
    pixel_count = len(new_image)
    ascii_image = "\n".join(new_image[i:(i+new_width)] for i in range(0,pixel_count,new_width))
    print(ascii_image)
    print()
    print("""Hello, it's Mithilesh Tiwari , aka m1key. Welcome to m1key world.""")