from app.gateway.event import TagChangedEvent

class AlarmService:
    async def on_tag_changed(self, event: TagChangedEvent):
        print("[ALARM CHECK]", event.variable_id, event.new_value)
