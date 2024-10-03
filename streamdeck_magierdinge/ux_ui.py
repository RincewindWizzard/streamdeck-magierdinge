from importlib.resources import files

import cairosvg
from PIL.ImageFile import ImageFile
from icon_loader import load_icon
from colour import Color
from xml.etree import ElementTree as ET
from enum import Enum
from loguru import logger

ICON_DIMENSION = 72  # Width and height of a streamdeck button display


def load_svg_icon(name: str, style: str = 'outline') -> ET:
    path = files(__name__).joinpath(f'material-icons/svg/{name}/{style}.svg')
    tree = ET.ElementTree(ET.fromstring(path.read_bytes()))
    return tree


def style_svg(tree: ET.ElementTree, style: str) -> ET.ElementTree:
    root = tree.getroot()
    existing_style_tag = root.find("{http://www.w3.org/2000/svg}style")
    if existing_style_tag is not None:
        existing_style_tag.text = style
    else:
        style_tag = ET.Element("style")
        style_tag.text = style
        root.insert(0, style_tag)
    return tree


def style_with(stroke: Color, background: Color, fill: Color):
    return f"""
        svg {{ 
            background-color: {background}; 
        }}
        line, path, rect, circle, polygon, polyline, ellipse {{
            stroke: {stroke.hex}; 
            fill: none;      
        }}
        rect, circle, polygon, polyline, ellipse {{
            fill: {fill.hex};   
        }}
        """


class Button(object):
    def __init__(self):
        ...

    def draw_image(self) -> ImageFile:
        ...

    def on_pressed(self):
        ...


class State(Enum):
    ON = 1
    OFF = 2


class LightSwitch(object):
    def __init__(self, color: Color = Color('red')):
        self._icon_lightbulb = load_svg_icon('lightbulb')
        self._icon_light_off = load_svg_icon('light_off')
        self.state = State.OFF

        self.icons = {
            State.OFF: style_svg(
                self._icon_lightbulb,
                style_with(
                    stroke=color,
                    background=Color('black'),
                    fill=color)),
            State.ON: style_svg(
                self._icon_light_off,
                style_with(
                    stroke=Color('#555555'),
                    background=Color('black'),
                    fill=Color('#555555')))

        }

        ...

    def draw_image(self) -> ImageFile:
        svg = self.icons[self.state]

        return cairosvg.svg2png(
            bytestring=svg,
            output_width=ICON_DIMENSION,
            output_height=ICON_DIMENSION)

    def on_pressed(self):
        logger.debug('Light Switch pressed')

        if self.state == State.ON:
            self.state = State.OFF
        elif self.state == State.OFF:
            self.state = State.ON
