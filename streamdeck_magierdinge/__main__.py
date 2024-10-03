import threading

from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

from icon_loader import load_icon
from ux_ui import LightSwitch
from loguru import logger

ICON_NAMES = [
    'local_florist',
    'lens',
    'kitesurfing',
    'iron',
    'headset',
    'tapas'
]

BUTTONS = [
    LightSwitch()
]


def on_key_pressed(deck, key, state):
    logger.debug(f'{deck}, {key}, {state}')
    if key < len(BUTTONS):
        BUTTONS[key].on_pressed(deck, key, state)


def shutdown_join():
    # Wait until all application threads have terminated (for this example,
    # this is when all deck handles are closed).
    for t in threading.enumerate():
        try:
            t.join()
        except RuntimeError:
            pass


def main():
    streamdecks = DeviceManager().enumerate()

    print("Found {} Stream Deck(s).\n".format(len(streamdecks)))

    for index, deck in enumerate(streamdecks):
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
            deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        ))

        # Set initial screen brightness to 30%.
        deck.set_brightness(30)

        for key in range(min(len(BUTTONS), deck.key_count())):
            with deck:
                button = BUTTONS[key]
                deck.set_key_image(key, PILHelper.to_native_key_format(deck, button.draw_image()))

        deck.set_key_callback(on_key_pressed)

    shutdown_join()


if __name__ == '__main__':
    main()
