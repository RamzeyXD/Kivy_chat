from typing import Optional

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.properties import StringProperty

from twisted.internet import reactor
from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint


class User(Protocol):
    # def __init__(self):
    #     reactor.callInThread(self.send_data)

    def connectionMade(self):
        self.factory.app.print_message("Welcome")
        print("Enter your name")

    def dataReceived(self, data: bytes):
        self.factory.app.print_message(data.decode('utf-8'))
        print(data.decode('utf-8'))


class UserFactory(ReconnectingClientFactory):
    protocol = User

    def __init__(self, app):
        self.app = app

    # def buildProtocol(self, addr: IAddress) -> Optional[User]:
    #     return User()

    def clientConnectionFailed(self, connector, reason):
        print(reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, unused_reason):
        print(unused_reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, unused_reason)


Window.size = (320, 600)


class WindowManager(ScreenManager):
    """A window manager to manage switching between screens"""
    pass


class ChatScreen(Screen):
    """A screen that display chat"""
    chat_text = StringProperty()

    def print_message(self, msg):
        self.chat_text += "{}\n".format(msg)


class MainApp(MDApp):
    connection = None

    def build(self):
        """Initialize the application and return the root widget"""
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.accent_hue = '400'
        self.title = "SimpleChat"

        # Storing screens in a list.
        screens = [
            ChatScreen(name="chat")
        ]

        self.wm = WindowManager(transition=FadeTransition())
        for screen in screens:
            self.wm.add_widget(screen)

        self.connect_to_server()

        return self.wm

    def connect_to_server(self):
        # connection = TCP4ClientEndpoint(reactor, 'localhost', 8000)
        # connection.connect(UserFactory(app=self))
        reactor.connectTCP('localhost', 8000, UserFactory(self))
        print('pre')
        print('run')

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def send_message(self, msg):
        print(msg)
        if msg and self.connection:
            print('s')
            self.connection.write(msg.encode('utf-8'))

    def print_message(self, msg):
        self.wm.current_screen.print_message(msg)


if __name__ == '__main__':
    MainApp().run()
