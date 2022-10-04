from VK.class_VKapp import VKapp
import config
import json
from vk_api.longpoll import VkEventType
from pprint import pprint
from VK.keyboard import send_kb, send_kb_in_message


vkapp = VKapp(token_user=config.vk_token_prog, tokenVK_Group=config.vk_token_my)





if __name__ == '__main__':
    # bot = VKapp(token_user=config.vk_token_prog, tokenVK_Group=config.vk_token_my)
    # a = vkapp.total_dict(1)
    # print(a)
    b = vkapp.foto_dict(159538953)
    print (b)
    # print(list(bot.total_dict(54934926))[0])
    def create_file(total_dict):
        with open(f"total.json", "w",encoding='UTF-8') as write_file:
            json.dump(total_dict, write_file)
        print(f'Создан файл: total.json')
    for event in vkapp.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text.lower()
                user_id = event.user_id
                send_kb(user_id, msg.lower())
                if msg == 'hi':
                    vkapp.send_msg(user_id, 'hellow froend')
                    vkapp.send_msg(user_id, 'how a u?')
                if msg == 'ok':
                    vkapp.send_msg(user_id, 'tell the amoun of 5 and 5)')
                    vkapp.send_msg(user_id, user_id)
                if msg == 'name':
                    vkapp.send_msg(user_id, vkapp.get_name(user_id))
                if msg == 'adge':
                    vkapp.send_msg(user_id, vkapp.get_age(user_id))
                if msg == 'city':
                    vkapp.send_msg(user_id, vkapp.get_id_city(user_id))
                if msg == 'sex':
                    vkapp.send_msg(user_id, vkapp.get_reverse_sex(user_id))
                if msg == 'search':
                    total_dict = vkapp.total_dict(user_id)
                    vkapp.send_msg(user_id, f'https://vk.com/id{(list(total_dict)[0])}')
                    send_kb_in_message(user_id, msg.lower(),(list(total_dict)[0]))
                    vkapp.send_foto(user_id=user_id, user_id_foto=(list(total_dict)[0]))
                    vkapp.send_msg(user_id, f'https://vk.com/id{(list(total_dict)[1])}')
                    vkapp.send_foto(user_id=user_id, user_id_foto=(list(total_dict)[1]))
                    vkapp.send_msg(user_id, f'https://vk.com/id{(list(total_dict)[2])}')
                    vkapp.send_foto(user_id=user_id, user_id_foto=(list(total_dict)[2]))
                    print(total_dict)
                    create_file(total_dict)
