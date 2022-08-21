class timeWindow:

    def __init__(self, start_time, end_time):
        self.query = {
            "range": {
              "@timestamp": {
                "gte": start_time,
                "lte": end_time
              }
            }
        }

    def get_query(self):
        return self.query
