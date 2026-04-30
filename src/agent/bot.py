"""
Adaptador Bot Framework que envuelve el agente de Semantic Kernel.
"""
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from src.agent.chat import build_agent


class WalmartBot(ActivityHandler):
    def __init__(self):
        self.agent = build_agent()

    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text
        if not user_input or not user_input.strip():
            return

        await turn_context.send_activity(
            MessageFactory.text("⏳ Consultando modelos...")
        )

        respuesta = ""
        async for response in self.agent.invoke(messages=user_input):
            respuesta = response.message.content

        await turn_context.send_activity(MessageFactory.text(respuesta))

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        "🤖 Hola, soy el Agente Walmart Insights.\n"
                        "Puedo predecir ventas y analizar segmentos de tiendas.\n"
                        "¿En qué te puedo ayudar?"
                    )
                )