class eventType:

    def __init__(self, event_type: str="Logon"):
        self.query = {
                "match": {
                    "event.action": event_type
                }
            }

    def get_query(self):
        return self.query
