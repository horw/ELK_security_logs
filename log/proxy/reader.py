class ProxyFileReader:

    def __init__(self, path):
        self.path = path
        try:
            with open(path) as file:
                self.data = file.read().split('\n')
        except FileNotFoundError:
            print("File don't exists, please, choose another one!")
            self.data = []

    def get_data(self) -> list:
        return self.data
