

class SocketEntry():
    host:str
    port:int

    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value:str):
        self.__host = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value:int):
        self.__port = value