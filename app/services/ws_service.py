from app.gateway.event import TagChangedEvent

class WebSocketService:
    async def on_tag_changed(self, event: TagChangedEvent):
        print("[WS]", event.variable_id, event.new_value)
