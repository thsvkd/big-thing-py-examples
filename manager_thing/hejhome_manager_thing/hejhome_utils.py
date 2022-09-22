from big_thing_py.utils import *


def find_homeid(home_list, home_name):
    for home in home_list:
        if home['hame'] == home_name:
            return home['homeId']


# def rgb_to_xy(r, g, b):
#     rNorm = r / 255.0
#     gNorm = g / 255.0
#     bNorm = b / 255.0

#     rFinal = enhance_color(rNorm)
#     gFinal = enhance_color(gNorm)
#     bFinal = enhance_color(bNorm)

#     X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
#     Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
#     Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763

#     if X + Y + Z == 0:
#         return (0, 0)
#     else:
#         xFinal = X / (X + Y + Z)
#         yFinal = Y / (X + Y + Z)

#         return [xFinal, yFinal]
