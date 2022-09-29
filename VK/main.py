import json
from VK.class_VK import VK
from vk_api.longpoll import VkLongPoll, VkEventType
import config
from pprint import pprint
# from keyboard import sended_keybord
# with open('token/tokenVK_Group.txt', 'r', ) as fileYA:
#     tokenVK_Group = fileYA.read()
# with open('token/tokenVK.txt', 'r', ) as fileVK:
#     tokenVK = fileVK.read()


if __name__ == '__main__':
    bot = VK(token_user=config.vk_token_prog, tokenVK_Group=config.vk_token_my)
    # a = bot.foto_dict(481468488)
    # print(a)
    # print(list(bot.total_dict(54934926))[0])
    def create_file(total_dict):
        with open(f"total.json", "w",encoding='UTF-8') as write_file:
            json.dump(total_dict, write_file)
        print(f'Создан файл: total.json')
    for event in bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text.lower()
                user_id = event.user_id
                # sended_keybord(user_id, msg.lower())
                if msg == 'hi':
                    bot.send_msg(user_id, 'hellow froend')
                    bot.send_msg(user_id, 'how a u?')
                if msg == 'ok':
                    bot.send_msg(user_id, 'tell the amoun of 5 and 5)')
                    bot.send_msg(user_id, user_id)
                if msg == 'name':
                    bot.send_msg(user_id, bot.get_name(user_id))
                if msg == 'adge':
                    bot.send_msg(user_id, bot.get_age(user_id))
                if msg == 'city':
                    bot.send_msg(user_id, bot.get_id_city(user_id))
                if msg == 'sex':
                    bot.send_msg(user_id, bot.get_reverse_sex(user_id))
                if msg == 'search':
                    total_dict = bot.total_dict(user_id)
                    bot.send_msg(user_id, f'https://vk.com/id{(list(total_dict)[0])}')
                    bot.send_msg(user_id, f'https://vk.com/id{(list(total_dict)[1])}')
                    bot.send_msg(user_id, f'https://vk.com/id{(list(total_dict)[2])}')
                    print(total_dict)
                    create_file(total_dict)