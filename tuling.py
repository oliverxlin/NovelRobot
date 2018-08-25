import json
import urllib.request


class tuling(object):
    def __init__(self):
        self.api_url = "http://openapi.tuling123.com/openapi/api/v2"

        self.data = {
            "reqType": 0,
            "perception":
            {
                "inputText":
                {
                    "text": "几点了"
                },

                "selfInfo":
                {
                    "location":
                    {
                        "city": "上海",
                        "province": "上海",
                        "street": "文汇路"
                    }
                }
            },

            "userInfo":
            {
                "apiKey": "ce56485710c64ac38f884b9b0fa357b7",
                "userId": "Richado"
            }
        }

    def con_tuling(self, text):
        self.data["perception"]["inputText"]["text"] = text
        data = json.dumps(self.data).encode('utf8')
        
        http_post = urllib.request.Request(self.api_url, data = data, headers={
            'content-type': 'application/json'})
        response = urllib.request.urlopen(http_post)
        response_str = response.read().decode('utf8')

        response_dic = json.loads(response_str)

        intent_code = response_dic['intent']['code']
        results_text = response_dic['results'][0]['values']['text']
        print('Turing的回答：')
        print('code：' + str(intent_code))
        print('text：' + results_text)
        return results_text
