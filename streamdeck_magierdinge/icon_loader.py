import io
from importlib.resources import files, as_file

import cairosvg
from PIL import Image
from xml.etree import ElementTree as ET

ICON_DIMENSION = 72


def style_svg(svg: bytes) -> str:
    tree = ET.ElementTree(ET.fromstring(svg))
    root = tree.getroot()

    style = ET.Element("style")
    style.text = """
        svg { background-color: black; }
        line, path, rect, circle, polygon, polyline, ellipse {
            stroke: white; 
            fill: none;      
        }
        rect, circle, polygon, polyline, ellipse {
            fill: white;   
        }
    """
    root.insert(0, style)

    xml_str = ET.tostring(root, encoding='unicode')
    return xml_str.replace('ns0:', '').replace(':ns0', '')


def load_icon(name: str, style: str = 'outline'):
    print(f'{name}')
    path = files(__name__).joinpath(f'material-icons/svg/{name}/{style}.svg')
    svg_content = style_svg(path.read_bytes())
    print(svg_content)

    png_data = cairosvg.svg2png(bytestring=svg_content, output_width=ICON_DIMENSION, output_height=ICON_DIMENSION)
    image = Image.open(io.BytesIO(png_data)).convert("RGB")
    image = image.resize((ICON_DIMENSION, ICON_DIMENSION))

    return image


def list_icons():
    path = files(__name__).joinpath(f'material-icons/svg/')
