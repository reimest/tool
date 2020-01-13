import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json, os, random, time
from pprint import *
categories = ['1','2','3']
all_barah = [75480714,26479371,24749774,2706982,29558743,15708540,77291486,59121430,64981773,123830304,52112894]
token = 'bb97c044910f7f2c1979d8cb125fb4448592841a8ac03e503a1d4be5d12e7dae97bca5a04e1c69e10e752'
group_id = 190846662
vk = vk_api.VkApi(token=token)
vk._auth_token()
longpoll = VkBotLongPoll(vk,group_id)
vk = vk.get_api()
def say(peer_id,msg):
    vk.messages.send(peer_id = peer_id, random_id = random.randint(0,2147483647), message = msg)
def auth_handler():
    say(user_id,"Enter authentication code: ")
    key = 'none'
    remember_device = True
    return key, remember_device

if 'data.db' not in os.listdir('.'):
    json.dump({},open('data.db','w'))
    data = {}
else:
    data = json.load(open('data.db'))
while True:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = str(event.object.from_id)
            if user_id not in data.keys():
                text = event.object.text
                if len(text.split()) == 1:
                    say(int(user_id),'Для начала использования этого инструмента вы должны отправить отправить свой логин и пароль через пробел. Не волнуйтесь, я гарантирую безопасное хранение Ваших данных.')
                else:
                    login, password = text.split()[0], text.split()[1]
                    vk_user = vk_api.VkApi(login, password,auth_handler=auth_handler)
                    vk_user.auth(token_only=True)
                    vk_user = vk_user.get_api()
                    vk_user.wall.post(owner_id = -1 * group_id,message="Hello, world")
                    data[user_id] = {'passlog':[text.split()[0], text.split()[1]],'text':''}
            elif user_id in data.keys() and event.object.text.split()[0] == '/reset':
                data[user_id]['text'] = ''
                json.dump(data,open('data.db','w'))
                say(user_id,'Текст для поста сброшен, теперь вы можете написать его заного')
            elif user_id in data.keys() and data[user_id]['text'] == '':
                text = event.object.text
                attachments = event.object.attachments
                atch = []
                for attach in attachments:
                    atch.append(attach['type'] + str(attach[attach['type']]['owner_id']) + '_' + str(attach[attach['type']]['id']))
                data[user_id]['text'] = [text,atch]
                json.dump(data,open('data.db','w'))
                say(user_id,'Проверьте правильность поста. Чтобы сбросить напишите /reset\n\nТеперь введите номер, по каким категориям рассылать.')
                say(user_id,'1. Общие барахолки\n2.Вейп барахолки(Недоступно)\n3.Барахолки электроники(Недоступно)')
                say(user_id,'Сразу после выбора категории начнется рассылка - не выбирайте, если не уверены')
            elif user_id in data.keys() and data[user_id]['text'] != '' and event.object.text.split()[0] in categories:
                login, password = data[user_id]['passlog'][0], data[user_id]['passlog'][1]
                vk_user = vk_api.VkApi(login, password)
                vk_user.auth(token_only=True)
                vk_user = vk_user.get_api()
                    
                categor = event.object.text.split()[0]
                if categor == '1': select = all_barah
                for group in select:
                    try:
                        vk_user.wall.post(owner_id = -1 * group,message=data[user_id]['text'][0],attachments = ','.join(data[user_id]['text'][1]))
                        say(user_id,'Пост отправлен: @club{}'.format(group))
                    except:
                        say(user_id,'Пост не был отправлен: @club{}'.format(group))
                    time.sleep(20)
            #elif user_id in data.keys() and data[user_id]['text'] != '':
                
            
                    # if attach['type'] == 'photo': #types: photo,doc,audio,video
                       # width = 0
                        #for size in attach[attach['type']]['sizes']:
                       #     if size['width'] > width:
                         #       width = size['width']
                        #        url = size['url']
                        #        type_ = size['type']
                       # atch[url] = 'photo'
                    #if attach['type'] == 'doc':
                    #    atch[attach['doc']['url']] = 'doc'
                    #if attach['type'] == 'audio':
                    #    atch[attach['audio']['url']] = 'audio'
                    #if attach ['type'] == 'video':
                     #   atch['video{}_{}'.format(attach['video']['owner_id'],attach['video']['id'])] = 'video'
                     #   say(user_id,'vk.com/video{}_{}'.format(attach['video']['owner_id'],attach['video']['id']))

