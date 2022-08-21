class requiredURL:

    def __init__(self, url: str):
        self.query = {
                "match": {
                    "winlog.event_data.DestAddressURL": url
                }
            }

    def get_query(self):
        return self.query
