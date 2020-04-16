
import sys,time,os,vk_api, requests, json

def auth_handler():
    key = input("enter authentication code: ")
    remember_device = True
    return key, remember_device

def main():
    interval = 40
    #----login----
    while True:
        try:
            print('  >>> log in please\n')
            login = input('login: ')
            passw = input('password: ')
            sys.stdout.write('\rlogining with ur account...')
            vk_user = vk_api.VkApi(login, passw,auth_handler=auth_handler)
            vk_user.auth(token_only=True)
            vk = vk_user.get_api()
            sys.stdout.write('\rlogining with ur account...[done]\n\n')
            break
        except:
            sys.stdout.write('\rlogining with ur account...[failed]\n\n')
            print('uncorrect vk_data \ncheck your login or password\n\n')
    print('account: {} {}\n'.format(vk.account.getProfileInfo()['first_name'],vk.account.getProfileInfo()['last_name']))
    time.sleep(2)
    
    #----ids_of_groups----
    ids = {}
    sys.stdout.write('\rparsing ids of groups from DIR ids...')
    try:
        for txt_name in os.listdir('ids'):
            ids[os.listdir('ids').index(txt_name)+1] = [txt_name.replace('.txt',''),json.loads(open('ids/{}'.format(txt_name),'rb').read())]
        sys.stdout.write('\rparsing ids of groups from DIR ids...[done]\n')
    except:
        sys.stdout.write('\rparsing ids of groups from DIR ids...[failed]\n')
    time.sleep(2)
    #----text----
    sys.stdout.write('\rgetting text from text.txt...')
    try:
        with open('text.txt', 'rb') as f:
            text = f.read()
        sys.stdout.write('\rgetting text from text.txt...[done]\n')
    except:
        sys.stdout.write('\rgetting text from text.txt...[failed]\n')
    time.sleep(2)


        
     #----photos----
    sys.stdout.write('\rcheching photos from DIR photos...')
    try:
        files = os.listdir('photos')
        photos_ = []
        for name in files:
            try:
                form = name[name.index('.',-4):]
            except:
                continue
            if form in ['.png','.jpg']:
                photos_.append(name)
        sys.stdout.write('\rcheching photos from DIR photos...[done]\n\n\n')
        print('count of photos: {}\n\n'.format(len(photos_)))
        time.sleep(2)
        if len(photos_) != 0:
            print('list of photos:\n\n   > {}\n'.format('\n   > '.join(photos_)))
            time.sleep(2)
    except:
        sys.stdout.write('\rcheching photos from DIR photos...[failed]\n')
        time.sleep(2)

        
    #uploading_photos
    if len(photos_) != 0:
        sys.stdout.write('\ruploading photos on server...')
        try:
            uploaded_photos = []
            for ph in photos_:
                upload_url = vk.photos.getWallUploadServer()
                post = requests.post(url=upload_url["upload_url"], files={"photo": open('photos/'+ph, "rb")}).json()
                attch = vk.photos.saveWallPhoto(photo=post['photo'],server=post['server'],hash=post['hash'])[0]
                uploaded_photos.append('photo'+str(attch['owner_id'])+'_'+str(attch['id']))
            sys.stdout.write('\ruploading photos on server...[done]\n\n')
        except:
            sys.stdout.write('\ruploading photos on server...[failed]')
            return
        
    #start_posting
    print('choose kit of groups to posting:\n ')
    for i in ids.keys():
        print('\t{}) {}'.format(str(i),ids[i][0]) )
    print('\t0) exit')
    print()
    while True:
        try:
            ch = int(input('> '))
        except:
            print('!!!invalid input!!!')
            continue
        if ch == 0:
            print('goodbye.')
            return
        elif ch in ids.keys():
            break
        else:
            print('!!!invalid input!!!')
    if input('start posting?[y/n]').lower() in ['y','д','yes','ye','да']:     
        for group_id in ids[ch][1]:
            try:
                vk.wall.post(owner_id = -1 * group_id,message=text.decode('Windows-1251'),attachments = uploaded_photos)
                print('[done] https://vk.com/club{} '.format(group_id))
            except:
                print('[!!!][failed] https://vk.com/club{} '.format(group_id))
            time.sleep(interval)
    else:
        return
            
if __name__ == '__main__':
    main()
