import json
import requests


def get_stiket(ID):
    try:
        if int(ID) > 0:
            gets = requests.get('https://paladinbot.pythonanywhere.com/dbu/?method=get_stiker&id={}'.format(ID)).json()
            return gets
        else:
            'DBU_EROR: user_id должен быть больше 0'
    except Exception as e:
        print(e)
        return 'DBU_EROR: user_id должен быть числом.'

def get_keys(txt = ''):
    gets = requests.get('https://paladinbot.pythonanywhere.com/dbu/?method=get_genetator&text={}'.format(str(txt))).json()
    return gets

def get_short(urls = ''):
    gets = requests.get('https://paladinbot.pythonanywhere.com/dbu/?method=get_shortlink&url={}'.format(str(urls))).json()
    return gets

def get_check(urls = ''):
    gets = requests.get('https://paladinbot.pythonanywhere.com/dbu/?method=get_check_link&url={}'.format(str(urls))).json()
    return gets

def get_trans_emj(text = 'котик в воде'):
    gets = requests.get('https://paladinbot.pythonanywhere.com/dbu/?method=get_emoji_transl&text={}'.format(str(text).lower())).json()
    return gets

def get_stiket_info(ID,tokens = ''):
    try:
        if int(ID) > 0:
            if tokens != '':
                url = "https://paladinbot.pythonanywhere.com/dbu/"

                querystring = {"method":"get_stiker_info","id":str(ID),"token":tokens}

                payload = ""
                headers = {'Authorization': 'Basic Og=='}

                gets = requests.request("GET", url, data=payload, headers=headers, params=querystring).json()
                return gets
            else:
                return 'DBU_EROR: Второй параметр, должен быть ваш Токен!Так как mess_id для каждого пользователя разный.'
        else:
            'DBU_EROR: packs_id должен быть больше 0'
    except Exception as e:
        return 'DBU_EROR: packs_id должен быть числом.'
