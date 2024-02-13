import json
import os
from channels.generic.websocket import AsyncWebsocketConsumer


PATH_BASE = "/home/"


class ConsumerReports(AsyncWebsocketConsumer):
    path_now = PATH_BASE

    async def connect(self):
        await self.accept()
        print("select_directory: {}".format(self.path_now))
        rez_html = self.make_html_from_file_list(self.path_now)
        await self.send(text_data=json.dumps({'rez_html': rez_html}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        try:
            msg = json.loads(text_data)
            select_directory = msg["select_directory"]
            print("select_directory: {}".format(select_directory))
            if ".html" in select_directory:
                self.path_now += "{}".format(select_directory)
                await self.send(text_data=json.dumps({'rez_html': "", 'open_link': self.path_now[21:]}))  # delete /usr/share/nginx/html
            elif select_directory == "return_button":
                if self.path_now == PATH_BASE:
                    return
                self.path_now = "/".join(self.path_now[:-1].split("/")[:-1])
                rez_html = self.make_html_from_file_list(self.path_now)
                self.path_now += "/"
                await self.send(text_data=json.dumps({'rez_html': rez_html}))
            else:
                self.path_now += "{}/".format(select_directory)
                rez_html = self.make_html_from_file_list(self.path_now)
                await self.send(text_data=json.dumps({'rez_html': rez_html}))

        except Exception as e:
            print(e)
            await self.send(text_data=json.dumps({'files': str(e)}))

    @staticmethod
    def make_html_from_file_list(path):
        rez_html = ""
        for file in os.listdir(path):
            rez_html += f'<div><input class="input_100_width" onclick="open_directory(this)" readonly id="{file}" value="{file}"></div>'
        return rez_html
