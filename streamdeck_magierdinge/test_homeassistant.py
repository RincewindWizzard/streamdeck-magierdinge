import json
import time

import requests
from homeassistant_api import Client

from config import load_config


def test_connection():
    config = load_config()
    with Client(
            f'{config.home_assistant.url}/api',
            config.home_assistant.token
    ) as client:
        light = client.get_domain("light")
        light.turn_on(entity_id="light.videoleuchte_licht", rgb_color=[0, 0, 255], brightness=0)




def foo_test_lamp():
    conf = load_config()
    print(get_states(conf))
    turn_light(conf, 255, (255, 0, 0), 0.5)
    time.sleep(1)
    turn_light(conf, 255, (0, 255, 0), 0.5)
    time.sleep(1)
    turn_light(conf, 255, (0, 0, 255), 0.5)
    time.sleep(1)
    turn_light(conf, 0, (255, 0, 0), 0.5)
    assert False


def get_states(conf):
    url = f'{conf.home_assistant.url}/api/states'
    token = conf.home_assistant.token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    return response.text


def turn_light(conf, brightness: int, color: tuple[int, int, int], transition: float = 1):
    url = f'{conf.home_assistant.url}/api/services/light/turn_on'
    token = conf.home_assistant.token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = {
        "entity_id": "light.videoleuchte_licht",
        "rgb_color": color,
        "brightness": min(max(brightness, 0), 255),
        "transition": transition
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
