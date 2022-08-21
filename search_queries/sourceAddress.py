
class sourceAddressQuery:

    def __init__(self, saddr: str):
        self.query = {
                "bool": {
                    "must": {
                        "term": {"winlog.event_data.SourceAddress": saddr},
                    },
                    "filter": [
                        {
                            "exists": {
                                "field": "winlog.event_data.DestAddress"
                            }
                        },
                        {
                            "exists": {
                                "field": "winlog.event_data.SourceAddress"
                            }
                        }

                    ]
                }
        }

    def get_query(self):
        return self.query
