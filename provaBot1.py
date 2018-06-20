import requests  
import datetime

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update



annoying_bot = BotHandler("581632988:AAEXhdWcAoAQU1y8oOqEjaNDBElm-AEzAMY")  


def main():  
    new_offset = None

    while True:
        annoying_bot.get_updates(new_offset)
       
        last_update = annoying_bot.get_last_update()
        chat_type = last_update['message']['chat']['type']

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['from']['first_name']
        words_n = len(last_chat_text.split()) +1
        insult_text="No, " + last_chat_name +",  I don't think you meant \""+last_chat_text +"\".\nIf you were more intelligent, you'd have sent a message with at least " + str(words_n) + " words. You're not welcome in this "
        if chat_type == "private":
            insult_text += "conversation"
        elif chat_type == "group":
            insult_text+="group"
        
        annoying_bot.send_message(last_chat_id,insult_text)

        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()