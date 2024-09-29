import datetime
from telethon import TelegramClient
from telethon import functions, types

api_id=21551348
api_hash="6567877864887ac2a1e19c239c20df06"
Shortname="KAscrap"

client = TelegramClient(Shortname, api_id, api_hash)

async def main():
    # Now you can use all client methods listed below, like for example...
    try:
        result = await client(functions.messages.GetDialogsRequest(
            offset_date=datetime.datetime(2024,10,20),
            offset_id=42,
            offset_peer='username',
            limit=100,
            hash=-12398745604826,
            # folder_id=42
        ))
        print(result.stringify())
        # print("main",await client.getmes())
    except Exception as e:
        print("error", e)

with client:
    client.loop.run_until_complete(main())