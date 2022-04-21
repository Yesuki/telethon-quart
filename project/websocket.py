import hypercorn
from quart import Quart, request
from quart_cors import route_cors
from telethon import TelegramClient
import asyncio
from hypercorn.asyncio import serve
import json


api_id = 12230482
api_hash = "3913f537691ebf3d3720519560dc1981"

# Telethon Client
client = TelegramClient('anon', api_id, api_hash)

# Quart App
app = Quart(__name__)
app.secret_key = 'CHANGE THIS TO SOMETHING SECRET'

loop = asyncio.get_event_loop()

# Connect the client before we start serving with Quart


@app.before_serving
async def startup():
    await client.connect()

# After we're done serving (near shutdown), clean up the client


@app.after_serving
async def cleanup():
    await client.disconnect()


@app.route('/', methods=["GET"])
@route_cors(
    allow_origin=["http://localhost:3000"])
async def hello():
    return "Hello World"


@app.route('/requestCode', methods=["POST"])
@route_cors(allow_headers=["content-type"],
            allow_methods=["POST"], allow_origin=["http://localhost:3000"])
async def sendCode():
    data = await request.get_json()
    global phone
    phone = data["phone"]
    if 'phone' in data:
        try:
            await client.send_code_request(phone)
        except:
            return "Phone Number incorrect", 400
        return "Code Sent", 201


@app.route('/messages', methods=["GET"])
@route_cors(
    allow_origin=["http://localhost:3000"],
    allow_headers=["content-type"],
    allow_methods=["GET"],)
async def getMessage():
    if await client.is_user_authorized():
        dialogs = await client.get_dialogs(5)
        response = []
        for d in dialogs:
            print(d)
            print(d.title)
            response.append(d.title)
        return json.dumps(response, ensure_ascii=False), 200


@app.route('/signin', methods=["POST"])
@route_cors(allow_headers=["content-type"],
            allow_methods=["POST"],
            allow_origin=["http://localhost:3000"])
async def signInAttempt():
    data = await request.get_json()
    code = data["code"]
    global phone

    if not await client.is_user_authorized():
        if 'code' in data:
            try:
                await client.sign_in(phone, code)
            except:
                return "Unauthorized", 401
            me = await client.get_me()

            response = {}
            response["id"] = me.id
            response["username"] = me.username
            response["access_hash"] = me.access_hash
            response["first_name"] = me.first_name
            response["last_name"] = me.last_name
            response["phone"] = me.phone
            json_data = json.dumps(response, ensure_ascii=False)

            return json_data, 200
    return "Already Logged in", 406


@app.route('/logout', methods=["POST"])
@route_cors(allow_headers=["content-type"],
            allow_methods=["POST"],
            allow_origin=["http://localhost:3000"])
async def logout():
    try:
        await client.log_out()
    except:
        return "Logout failed", 401

    return "Logout Success", 200


loop.run_until_complete(serve(app, hypercorn.Config()))
