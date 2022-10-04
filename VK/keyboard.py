import json

def get_button(text, color):
    return {
        "action": {
            # "type": "callback",
            "type": "text",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


def send_kb (user_id, text):
    from VK.main import vkapp
    keyboard = {
        "one_time": False,
        "inline": False,
        "buttons": [
            [get_button('search', 'primary')],
            [get_button('back', 'secondary'),
             get_button('view_favorite', 'secondary'),
             get_button('view_black', 'secondary'),
             get_button('next', 'secondary')]
        ]
    }
    vkapp.vk.method('messages.send', {'user_id': user_id,
                                      'message': text,
                                      'random_id': 0,
                                      'keyboard': encode(keyboard)})


def send_kb_in_message(user_id, text, user_id_search):
    from VK.main import vkapp
    keyboard = {
        "one_time": False,
        "inline": True,
        "buttons":
            [[get_button(f'black_{user_id_search}', 'negative'), get_button(f'favorite_{user_id_search}', 'positive')]]
    }
    vkapp.vk.method('messages.send', {'user_id': user_id,
                                      'message': text,
                                      'random_id': 0,
                                      'keyboard': encode(keyboard)})


def encode(keyboard):
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    return str(keyboard.decode('utf-8'))
