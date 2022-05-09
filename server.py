from typing import Optional

from twisted.internet import reactor
from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import ServerFactory, connectionDone, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint


class UserServer(Protocol):
    def __init__(self, users):
        self.users = users
        self.name = ""

    def connectionMade(self):
        print("New Connection")

    def connectionLost(self, reason=connectionDone):
        if self in self.users:
            del self.users[self]
            print(f"Removed connection: {self}")

    def dataReceived(self, data: bytes):
        data = data.decode('utf-8')
        print(data)
        if not self.name:
            self.add_user(data)

        for protocol in self.users.keys():
            protocol.transport.write(f"{self.name}: {data}".encode('utf-8'))

    def add_user(self, name):
        if name not in self.users:
            self.users[self] = name
            self.name = name
        else:
            self.transport.write("This name has already used. Try another one!".encode('utf-8'))


class UserServerFactory(ServerFactory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr: IAddress) -> Optional[UserServer]:
        return UserServer(self.users)


if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, 8000)
    endpoint.listen(UserServerFactory())
    reactor.run()
