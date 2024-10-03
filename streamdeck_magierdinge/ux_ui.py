import io
from importlib.resources import files
from typing import TypeVar, Callable, Any

import cairosvg
from PIL.ImageFile import ImageFile
from PIL import Image
from StreamDeck.ImageHelpers import PILHelper

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
            background-color: {background.get_web()}; 
        }}
        line, path, rect, circle, polygon, polyline, ellipse {{
            stroke: {stroke.get_web()}; 
            fill: none;      
        }}
        rect, circle, polygon, polyline, ellipse {{
            fill: {fill.get_web()};   
        }}
        """


def render_svg(fun: Callable[[Any], ET.Element]) -> Callable[[Any], ImageFile]:
    def svg_to_image(svg: ET) -> ImageFile:
        # TODO: Namespaces korrekt entfernen
        svg_str = ET.tostring(svg.getroot(), encoding='unicode').replace('ns0:', '').replace(':ns0', '')
        logger.trace(svg_str)

        png_data = cairosvg.svg2png(
            bytestring=svg_str,
            output_width=ICON_DIMENSION,
            output_height=ICON_DIMENSION)

        image = Image.open(io.BytesIO(png_data)).convert("RGB")
        image = image.resize((ICON_DIMENSION, ICON_DIMENSION))
        return image

    return lambda self: svg_to_image(fun(self))


class Button(object):
    def __init__(self):
        ...

    def draw_image(self) -> ImageFile:
        ...

    def on_pressed(self, deck, key, state):
        ...


class State(Enum):
    ON = 1
    OFF = 2


class LightSwitch(Button):
    def __init__(self, color: Color = Color('red'), on_pressed: Callable[[Button], None] = lambda _: None):
        super().__init__()
        self.primary_color = color
        self.on_pressed_cb = on_pressed
        self._icon_lightbulb = load_svg_icon('lightbulb')
        self._icon_light_off = load_svg_icon('link_off')
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

    @render_svg
    def draw_image(self) -> ET:
        svg = self.icons[self.state]

        return svg

    def on_pressed(self, deck, key, state):
        logger.debug('Light Switch pressed')

        if state:
            if self.state == State.ON:
                self.state = State.OFF
            elif self.state == State.OFF:
                self.state = State.ON

        deck.set_key_image(
            key,
            PILHelper.to_native_key_format(deck, self.draw_image()))

        self.on_pressed_cb(self)
