from app.gateway.event import TagChangedEvent

class MQTTService:
    async def on_tag_changed(self, event: TagChangedEvent):
        print("[MQTT]", event.variable_id, event.new_value)
