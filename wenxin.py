import json
import random
import requests
import eel
@eel.expose
def unit_chat(chat_input, user_id="user"):
    client_id = "P4q1cZ2YdKzkyt1n3ICBUGkH"
    client_secret = "LEspy4oAFmjNcr3vMSB0IF5sdLHMGWf4"
    chat_reply = "系统繁忙，请稍后重试"
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s" % (client_id, client_secret)

    ret = requests.get(url)

    access_token = eval(ret.text)['access_token']

    post_data = {
        "log_id": str(random.random()),
        "request": {
            "query": chat_input,
            "user_id": user_id
        },
        "session_id": "",
        "service_id": "S78544",
        "version": "2.0"
    }
    unit_chatbot_url = "https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=" + access_token
    res = requests.post(unit_chatbot_url, json=post_data)
    unit_chat_obj = json.loads(res.content)
    # result-response_list-schema-intent_confidence-action_list-say
    if unit_chat_obj['error_code'] != 0:
        return chat_reply
    unit_chat_result = unit_chat_obj['result']
    unit_chat_response_list = unit_chat_result['response_list']
    unit_chat_response_obj = random.choice([unit_chat_response for unit_chat_response in unit_chat_response_list if unit_chat_response['schema']['intent_confidence'] > 0.0])
    unit_chat_action = unit_chat_response_obj['action_list']
    unit_chat_action_obj = random.choice(unit_chat_action)
    unit_chat_say = unit_chat_action_obj['say']
    return unit_chat_say


if __name__ == '__main__':
    while True:
        chat_input = input('请输入>>')
        if chat_input == '退出':
            break
        result_say = unit_chat(chat_input)
        print("unit输出", result_say)