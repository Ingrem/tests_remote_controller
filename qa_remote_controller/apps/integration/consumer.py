from channels.generic.websocket import AsyncWebsocketConsumer
import json
import aioredis
import requests
import redis
import asyncio
import uuid


REDIS_HOST = "0.0.0.0"
REDIS_PORT = "5173"
redis_db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)


class Consumer(AsyncWebsocketConsumer):
    flag = False
    topic = str(uuid.uuid4())

    async def connect(self):
        self.flag = False
        await self.accept()

    async def disconnect(self, _):
        self.flag = False
        redis_db.publish('stop_tests', json.dumps({"REDIS_TOPIC": self.topic}))

    async def receive(self, text_data=None, bytes_data=None):
        try:
            # liveness probe
            try:
                http_resp = requests.get('http://0.0.0.0:9081/liveness')
            except requests.exceptions.RequestException:
                await self.send(text_data=json.dumps({"message": "backend liveness probe fail", "lvl": "ERROR"}))
                return

            if http_resp.status_code != 200:
                await self.send(text_data=json.dumps({"message": "backend liveness probe fail", "lvl": "ERROR"}))
                return

            json_data = json.loads(text_data)
            print(json_data["cmd"])

            if not self.flag:
                self.topic = str(uuid.uuid4())
                self.flag = True
                await self.receive_msgs()

            if json_data["cmd"] == 'start_visibility_diff':
                redis_db.publish('start_visibility_diff', json.dumps(
                    {
                        "REDIS_TOPIC": self.topic,
                        "FEED_TIMEOUT": json_data["FEED_TIMEOUT"],
                        "TESTS_ITER_COUNT": json_data["TESTS_ITER_COUNT"]
                    }))

            if json_data["cmd"] == 'start_price_diff':
                redis_db.publish('start_price_diff', json.dumps(
                    {
                        "REDIS_TOPIC": self.topic,
                        "FEED_TIMEOUT": json_data["FEED_TIMEOUT"],
                        "TESTS_ITER_COUNT": json_data["TESTS_ITER_COUNT"]
                    }))

            if json_data["cmd"] == 'stop_tests':
                self.flag = False
                redis_db.publish('stop_tests', json.dumps({"REDIS_TOPIC": self.topic}))

            if json_data["cmd"] == 'start_e2e':
                if json_data["PASSWORD"] == "***":
                    json_data["PASSWORD"] = "Parol123"

                redis_db.publish('start_e2e', json.dumps(
                    {
                        "REDIS_TOPIC": self.topic,
                        "LOGIN": json_data["LOGIN"],
                        "PASSWORD": json_data["PASSWORD"]
                    }))

            if json_data["cmd"] == 'start_e2e_android':
                if json_data["PASSWORD"] == "***":
                    json_data["PASSWORD"] = "Parol123"

                redis_db.publish('start_e2e_android', json.dumps(
                    {
                        "REDIS_TOPIC": self.topic,
                        "LOGIN": json_data["LOGIN"],
                        "PASSWORD": json_data["PASSWORD"]
                    }))

            if json_data["cmd"] == 'start_e2e_ios':
                if json_data["PASSWORD"] == "***":
                    json_data["PASSWORD"] = "Parol123"

                redis_db.publish('start_e2e_ios', json.dumps(
                    {
                        "REDIS_TOPIC": self.topic,
                        "LOGIN": json_data["LOGIN"],
                        "PASSWORD": json_data["PASSWORD"]
                    }))

        except Exception as e:
            print("exception: {}".format(e))
            await self.send(text_data=json.dumps({'message': str(e), 'lvl': 'ERROR'}))

    async def receive_msgs(self):
        redis_db_async = await aioredis.create_redis(f"redis://{REDIS_HOST}:{REDIS_PORT}")
        channel1, = await redis_db_async.subscribe(self.topic)

        async def async_reader(channel):
            while await channel.wait_message() and self.flag:
                msg_redis = await channel.get(encoding='utf-8')
                if msg_redis[0] == "I":
                    await self.send(text_data=json.dumps({"message": msg_redis, "lvl": "INFO"}))
                if msg_redis[0] == "D":
                    await self.send(text_data=json.dumps({"message": msg_redis, "lvl": "DEBUG"}))
                if msg_redis[0] == "E":
                    await self.send(text_data=json.dumps({"message": msg_redis, "lvl": "ERROR"}))
                if msg_redis[0] == "S" and msg_redis[1] == "Y":
                    await self.send(text_data=json.dumps({"message": msg_redis, "lvl": "SYSTEM"}))
                if msg_redis[0] == "S" and msg_redis[1] == "U":
                    await self.send(text_data=json.dumps({"message": msg_redis, "lvl": "SUCCESS"}))

        asyncio.ensure_future(async_reader(channel1))
