import numpy as np
import base64
from PIL import Image
import zlib as zl


def show_image(format, width, height, image):
    image_decoded = base64.b64decode(image)
    print(len(image_decoded))
    print(type(image_decoded))
    #image_data = ... # byte values of the image
    image = Image.frombytes(format, (width,height),image_decoded,'raw')
    image.show()

    # Save to file
    #a=np.asarray(image)
    #im = Image.fromarray(a)
    #image.save("your_file.jpeg")
