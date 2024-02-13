from channels.generic.websocket import AsyncWebsocketConsumer
from multiprocessing import Queue
import json
import requests
import time
import asyncio


class BcMockConsumer(AsyncWebsocketConsumer):
    qu_perf_start = Queue()
    qu_perf_stop = Queue()

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        try:
            msg = json.loads(text_data)
            service = msg["message"]
            print(service)
            url_base = "http://{}:{}".format(msg["ip"], msg["port"])

            if service == 'start_performance':
                # wait for set config
                time.sleep(1)
                url = url_base + "/start_performance"
                answer = requests.get(url=url, timeout=5)
                await self.send(text_data=json.dumps({'message': str(answer.text)}))

            if service == 'stop_performance':
                url = url_base + "/stop_performance"
                answer = requests.get(url=url, timeout=5)
                await self.send(text_data=json.dumps({'message': str(answer.text)}))

            if service == 'generate_cache':
                url = url_base + "/generate_cache"
                answer = requests.get(url=url, timeout=5)
                await self.send(text_data=json.dumps({'message': str(answer.text)}))

            if service == 'reset_obj_cache':
                url = url_base + "/reset_obj_cache"
                answer = requests.get(url=url, timeout=5)
                await self.send(text_data=json.dumps({'message': str(answer.text)}))

            if service == 'get_config':
                url = url_base + "/get_config"
                answer = requests.get(url=url, timeout=5)
                answer_json = json.loads(answer.text)
                resp = ''
                for key in answer_json.keys():
                    resp += "{}: {}\n".format(key, answer_json[key])
                await self.send(text_data=json.dumps({'message': resp}))

            if service == 'set_config':
                url = url_base + "/set_config"
                answer = requests.post(url=url, data=json.dumps(msg["new_config"]), timeout=5)
                await self.send(text_data=json.dumps({'message': str(answer.text)}))
        except Exception as e:
            print(e)
            await self.send(text_data=json.dumps({'message': str(e)}))
