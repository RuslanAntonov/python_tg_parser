from pyrogram import Client
import logging
import os.path
import json
import asyncio
import datetime



async def send_message():
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

    for i in range(1, 25):
        while True:
            if (target_message.empty == True
                    or target_message.forward_from != None
                    or target_message.forward_from_chat != None
                    or target_message.media_group_id != None
                    or target_message.photo == None):
                current_id += 1
                target_message = await app.get_messages(target_chanel, current_id)
            else:
                post_date = datetime.datetime.today() + datetime.timedelta(hours=i)
                await app.send_photo(main_chanel, target_message.photo.file_id, schedule_date=post_date)
                logging.info('Photo was send. Message id: %s', current_id)
                current_id += 1
                target_message = await app.get_messages(target_chanel, current_id)
                break

    id_data["current_id"] = current_id
    with open('id.json', 'w') as f:
        json.dump(id_data, f)


async def main(main_chanel, target_chanel):
    await app.start()
    task1 = asyncio.create_task(send_message())
    await task1
    await app.stop()



logging.basicConfig(level=logging.INFO, filename="log.log",format="%(asctime)s %(levelname)s %(message)s")

main_chanel = -123
target_chanel = -123

app = Client(
    "my_account",
    api_id=123,
    api_hash="123",
    phone_number="123"
)

logging.info("Script is started")

app.run(main(main_chanel, target_chanel))
