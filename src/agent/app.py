"""
Servidor HTTP aiohttp que expone el bot al Bot Framework Emulator.
Arrancar con: python -m src.agent.app
"""
import asyncio
from pathlib import Path

from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from dotenv import load_dotenv

from src.agent.bot import WalmartBot

load_dotenv(Path("config/.env"))

# Para el Emulator local no se necesitan credenciales
SETTINGS = BotFrameworkAdapterSettings(app_id="", app_password="")
ADAPTER = BotFrameworkAdapter(SETTINGS)
BOT = WalmartBot()


async def messages(req: web.Request) -> web.Response:
    if req.content_type != "application/json":
        return web.Response(status=415)

    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return web.json_response(data=response.body, status=response.status)
    return web.Response(status=201)


app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    print("🚀 Bot corriendo en http://localhost:3978/api/messages")
    web.run_app(app, host="localhost", port=3978)