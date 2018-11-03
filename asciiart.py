import numpy as np
from PIL import Image, ImageOps
import argparse


def converter(val):
    index = int(val)
    # len is 65
    artchars = " `^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    return artchars[index]


np_conv = np.vectorize(converter)
np_max = np.vectorize(max)
np_min = np.vectorize(min)

# Parse Input and determine options
parser = argparse.ArgumentParser()
parser.add_argument("in_f", help="input image file")
parser.add_argument(
    "--out_f", help="output image file, default: <input filename>_out.txt")
parser.add_argument("--invert", help="Black/White inversion")
parser.add_argument(
    "--algorithm", help='''
    calculation to average the RGB values to get a brightness value. 
    You can supply any valid python expression with the variables R G B as
    the Red Green and Blue values for the pixel.
        Valid aliases are:                                       
                                 
            
            'avg'        = (R+G+B)/3
            'lightness'  = (max(R, G, B) + min(R, G, B)) / 2
            'luminosity' = 0.21 R + 0.72 G + 0.07 B''')
parser.set_defaults(out_f="_def_out.txt", algorithm='(R+G+B)/3', invert=False)
inf = parser.parse_args()

print(inf)

with Image.open(inf.in_f) as im:
    if inf.invert:
        im = ImageOps.invert(im)
    im_arr = np.asarray(im)
    R = im_arr[:, :, 0].astype(float)
    G = im_arr[:, :, 1].astype(float)
    B = im_arr[:, :, 2].astype(float)

    if inf.algorithm == 'lightness':
        inf.algorithm = '(np_max(R, G, B) + np_min(R, G, B)) / 2'
    elif inf.algorithm == 'luminosity':
        inf.algorithm = '0.21*R + 0.72*G + 0.07*B'
    av = eval(inf.algorithm)

    av = av * 65 / np.max(av)
    av = av.astype(int)
    art = np.transpose(av.astype(str))

art = np_conv(art)
prov = '\n'.join([''.join(art[:, i]) for i in range(art.shape[1])])

if inf.out_f == "_def_out.txt":
    inf.out_f = inf.in_f[:-4] + "_out.txt"

with open(inf.out_f, 'w') as tout:
    print(prov, file=tout)
    pass
