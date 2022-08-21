class destAddressQuery:

    def __init__(self, daddr: str):
        self.daddr = daddr
        self.query = {
                "bool": {
                    "must": {
                        "term": {"winlog.event_data.DestAddress": daddr},
                    }
                }
        }

    def get_query(self):
        return self.query

    def update_by(self, durl_value: str):
        return[
            {
                "term": {
                    "winlog.event_data.DestAddress": self.daddr
                }
            },
            {
                "source": f"ctx._source.winlog.event_data.DestAddressURL = '{durl_value}'",
                "lang": "painless"
            }
        ]