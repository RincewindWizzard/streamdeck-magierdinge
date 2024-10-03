import threading
from typing import Callable

import homeassistant_api
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.Devices.StreamDeck import StreamDeck
from StreamDeck.ImageHelpers import PILHelper
from colour import Color

from icon_loader import load_icon
from ux_ui import LightSwitch, Button, State
from loguru import logger
from config import load_config


def shutdown_join(fun: Callable[[], None]):
    def join_all():
        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                pass

    def closure():
        fun()
        join_all()

    return closure()


def setup_streamdeck(deck: StreamDeck, buttons: list[Button]):
    if not deck.is_visual():
        raise ValueError('Streamdeck has no displays!')

    deck.open()
    deck.reset()

    logger.debug("Opened '{}' device (serial number: '{}', fw: '{}')".format(
        deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
    ))

    deck.set_brightness(100)

    for key in range(min(len(buttons), deck.key_count())):
        with deck:
            button = buttons[key]
            deck.set_key_image(key, PILHelper.to_native_key_format(deck, button.draw_image()))

    def on_key_pressed(deck, key, state):
        logger.debug(f'{deck}, {key}, {state}')
        if key < len(buttons):
            buttons[key].on_pressed(deck, key, state)

    deck.set_key_callback(on_key_pressed)


@shutdown_join
def main():
    config = load_config()

    with homeassistant_api.Client(
            f'{config.home_assistant.url}/api',
            config.home_assistant.token
    ) as client:
        light = client.get_domain("light")

        def turn_light(btn: LightSwitch):
            logger.debug(f'Color: {btn.primary_color.rgb}')

            light.turn_on(
                entity_id="light.videoleuchte_licht",
                rgb_color=[int(x * 255) for x in btn.primary_color.rgb],
                brightness=255 if btn.state == State.ON else 0)

        buttons = [
            LightSwitch(color=Color('red'), on_pressed=turn_light),
            LightSwitch(color=Color('green'), on_pressed=turn_light),
            LightSwitch(color=Color('blue'), on_pressed=turn_light),
            LightSwitch(color=Color('white'), on_pressed=turn_light),
            LightSwitch(color=Color('yellow'), on_pressed=turn_light),
        ]

        streamdecks = DeviceManager().enumerate()
        logger.debug("Found {} Stream Deck(s).\n".format(len(streamdecks)))
        for index, deck in enumerate(streamdecks):
            if deck.is_visual():
                setup_streamdeck(deck, buttons=buttons)


if __name__ == '__main__':
    main()
