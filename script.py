from pyrogram import Client
import logging
import os.path
import json
import asyncio
from random import randint



async def send_message():
    while True:
        if os.path.isfile('id.json') == True:
            with open('id.json', 'r') as f:
                id_data = json.load(f)
                current_id = id_data["current_id"]
        else:
            current_id = 2
            id_data = {"current_id": 2}
            logging.info("JSON file doesn't exist, trying to create one")
            with open('id.json', 'w+') as f:
                json.dump(id_data, f)

        target_message = await app.get_messages(target_chanel, current_id)

        while True:
            if (target_message.empty == True
                    or target_message.forward_from != None
                    or target_message.forward_from_chat != None
                    or target_message.media_group_id != None
                    or target_message.photo == None):
                target_message = await app.get_messages(target_chanel, current_id)
                current_id += 1
            else:
                await app.send_photo(main_chanel, target_message.photo.file_id)
                logging.info('Photo is sent. Message id: %s', current_id)
                current_id += 1
                break

        id_data["current_id"] = current_id
        with open('id.json', 'w') as f:
            json.dump(id_data, f)

        await asyncio.sleep(3624)



async def main(main_chanel, target_chanel):
    await app.start()
    task1 = asyncio.create_task(send_message())
    await task1
    await app.stop()



logging.basicConfig(level=logging.INFO, filename="log.log",format="%(asctime)s %(levelname)s %(message)s")

main_chanel = -1
target_chanel = -1

app = Client(
    "my_account",
    api_id=123,
    api_hash="aaa",
    phone_number="+7123
)

logging.info("Script is started")

app.run(main(main_chanel, target_chanel))
