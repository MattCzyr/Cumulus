class Color:
    name = ''
    hue = -1

    def __init__(self, name, hue):
        self.name = name
        self.hue = hue
        all.append(self)


all = []

red = Color('red', 0)
orange = Color('orange', 30)
yellow = Color('yellow', 60)
green = Color('green', 120)
blue = Color('blue', 210)
purple = Color('purple', 270)


def from_name(name):
    for color in all:
        if color.name == name:
            return color
    return None

def is_color(name):
    for color in all:
        if color.name == name:
            return True
    return False