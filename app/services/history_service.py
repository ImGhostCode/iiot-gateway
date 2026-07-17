from app.gateway.event import TagChangedEvent

class HistoryService:
    async def on_tag_changed(self, event: TagChangedEvent):
        print("[HISTORY]", event.variable_id, event.new_value)
