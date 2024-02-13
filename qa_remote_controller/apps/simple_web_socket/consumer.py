import json
import websockets
import asyncio
import re
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from qa_remote_controller.apps.simple_web_socket import compere_jsons
from django.core.cache import cache
from multiprocessing import Queue


class Consumer_simple_socket(AsyncWebsocketConsumer):
    stop_que = Queue()
    work_que = Queue()

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        try:
            msg = json.loads(text_data)
            command_ws = msg["command"]
            print(command_ws)
            cache.set('a-unique-key', 'sdgsdggsdg')

            if command_ws in ['send_msg', 'stop_sub']:
                if not self.work_que.empty():
                    self.stop_que.put("stop")

            if command_ws == 'send_msg':
                url = msg["url"]
                async with websockets.connect(url) as websocket:
                    await websocket.send(json.dumps(json.loads(msg["msg"])))
                    resp = await websocket.recv()
                    await self.send(text_data=json.dumps({'message': str(resp)}))
                    websocket.close()

            if command_ws == 'send_msg_and_sub':
                await self.wait_for_new_msgs(msg)

            if command_ws == 'make_str':
                resp = re.sub(r"\s+|\n|\r|\s+ ", '', msg["msg"])
                await self.send(text_data=json.dumps({'message': str(resp)}))

            if command_ws == 'make_json':
                await self.command_parse_to_json(msg)

            if command_ws == 'dict':
                resp = re.sub('"', "'", msg["msg"])
                resp = re.sub('false', "False", resp)
                resp = re.sub('true', "True", resp)
                resp = re.sub('null', "None", resp)
                await self.send(text_data=json.dumps({'message': str(resp)}))

            if command_ws == 'compare_json':
                await self.compare_jsons(msg)

            if command_ws == 'make_link':
                cache_hash = uuid.uuid4().hex
                cache.set(cache_hash, msg["save_text"])
                await self.send(text_data=json.dumps(
                    {'message': "http://10.22.0.12:9080/simple_web_socket/{}".format(cache_hash)}
                ))

        except Exception as e:
            print(e)
            await self.send(text_data=json.dumps({'message': str(e)}))

    async def wait_for_new_msgs(self, msg):
        url = msg["url"]
        async with websockets.connect(url) as websocket:
            await websocket.send(json.dumps(json.loads(msg["msg"])))
            self.work_que.put("now working")
            resp = ''
            while True:
                try:
                    resp = await asyncio.wait_for(websocket.recv(), 1)
                except Exception:
                    pass
                if not self.stop_que.empty():
                    self.stop_que.get()
                    self.work_que.get()
                    break
                if resp != '':
                    await self.send(text_data=json.dumps({'message': '{}\n'.format(resp)}))
                resp = ''
                await asyncio.sleep(1)
            websocket.close()

    @staticmethod
    def parse_to_json(msg):
        msg_no_html = re.sub("<.*?>", "", msg)
        parse_me = re.sub(r"\s+|\n|\r|\s+ ", '', msg_no_html)
        resp = ''
        spaces = 0

        for char in parse_me:
            if char in ["{", "[", ","]:
                resp += "{}\n".format(char)
                if char in ["{", "["]:
                    spaces += 4
                for _ in range(0, spaces):
                    resp += ' '
            elif char in ["}", "]"]:
                spaces -= 4
                resp += "\n"
                for _ in range(0, spaces):
                    resp += ' '
                resp += char
            else:
                resp += char

        resp = re.sub("'", '"', resp)
        resp = re.sub('False', "false", resp)
        resp = re.sub('True', "true", resp)
        resp = re.sub('None', "null", resp)
        return resp

    async def command_parse_to_json(self, msg):
        resp = self.parse_to_json(msg["msg"])

        try:
            json.loads(resp)
            valid_json = "Valid"
        except Exception as e:
            valid_json = "Invalid: {}".format(e)

        await self.send(text_data=json.dumps({'message': str(resp), "valid_json": valid_json}))

    async def compare_jsons(self, msg):
        tmp_json_1 = self.parse_to_json(msg["json_1"])
        tmp_json_2 = self.parse_to_json(msg["json_2"])

        try:
            tmp_json_1 = re.sub(r"\s+|\n|\r|\s+ ", '', tmp_json_1)
            tmp_json_2 = re.sub(r"\s+|\n|\r|\s+ ", '', tmp_json_2)
            tmp_json_1 = json.loads(tmp_json_1)
            tmp_json_2 = json.loads(tmp_json_2)
            valid_json = 'json valid: compare like jsons'
        except Exception as e:
            tmp_json_1 = self.parse_to_json(msg["json_1"])
            tmp_json_2 = self.parse_to_json(msg["json_2"])
            valid_json = "json invalid compare like strs: {}".format(e)

        if valid_json == 'json valid: compare like jsons':
            rez_json_1, rez_json_2 = compere_jsons.compare_like_jsons(tmp_json_1, tmp_json_2)
        else:
            rez_json_1, rez_json_2 = compere_jsons.compare_like_str(tmp_json_1, tmp_json_2)

        await self.send(text_data=json.dumps(
            {'message': str(rez_json_1), "json_2": str(rez_json_2), 'valid_json': valid_json}
        ))
