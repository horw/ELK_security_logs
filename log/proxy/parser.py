import re


class ProxyParser:

    def __init__(self, re_pattern: str, in_data: list):
        self.in_data = in_data
        self.re_pattern = re_pattern

    def search(self):
        for line in self.in_data:
            result = re.search(self.re_pattern, line)
            yield result.groups()





