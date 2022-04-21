from urllib import response
from telethon import TelegramClient
import json

api_id = 12230482
api_hash = "3913f537691ebf3d3720519560dc1981"
client = TelegramClient('anon', api_id, api_hash)


async def main():
    me = await client.get_me()
    # print(me.stringify())
    dialogs = await client.get_dialogs(5)
    response = []
    for d in dialogs:
        print(d.entity)
        print(d.title)
        response.append(d.title)
    print(response)
    print(json.dumps(response, ensure_ascii=False))
    # dialogs = await client.get_dialogs(5)
    # for dialog in dialogs:
    # print(dialog.name + ":")
    # print(dialog.message.message)

    # dialog = (await client.get_dialogs())[2]
    # messages = await client.get_messages(dialog, 10)
    # for m in messages:
    # print()
    # print(m.message)


with client:
    client.loop.run_until_complete(main())
