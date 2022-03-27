from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.config import Config 
from kivy.lang.builder import Builder
from kivy.uix.camera import Camera
from kivy.core.window import Window
#import cv2
#import time



import socket

host = '192.168.75.163'  # as both code is running on same pc
port = 5000  # socket server port number

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
client_socket.connect((host, port))  # connect to the server








class Button_left(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(Button_left, self).__init__(**kwargs)
        self.always_relese = False
        self.source = 'left.png'
        self.pos_hint = {'x' : 0.1, 'y' : 0.1}
        self.size_hint = (None, None)
    def on_press(self):
        self.source = 'left_down.png'

    def on_release(self):
        self.source = 'left.png'

class Button_right(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(Button_right, self).__init__(**kwargs)
        self.source = 'right.png'
        self.pos_hint = {'x' : 0.25, 'y' : 0.1}
        self.size_hint = (None, None)
    def on_press(self):
        message = 'right'
        client_socket.send(message.encode())  # send message
        self.source = 'right_down.png'

    def on_release(self):
        self.source = 'right.png'
class Button_forward(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(Button_forward, self).__init__(**kwargs)
        self.source = 'forward.png'
        self.pos_hint = {'x' : 0.85, 'y' : 0.25}
        self.size_hint = (None, None)
    def on_press(self):
        self.source = 'forward_down.png'

    def on_release(self):
        self.source = 'forward.png'

class Button_backward(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(Button_backward, self).__init__(**kwargs)
        self.source = 'backward.png'
        self.pos_hint = {'x' : 0.85, 'y' : 0.05}
        self.size_hint = (None, None)
    def on_press(self):
        self.source = 'backward_down.png'

    def on_release(self):
        self.source = 'backward.png'

#cam = Camera(resolution=(Window.width, Window.height))

class Float_layout(FloatLayout):
	def hide_widget(self, wid, dohide=True):
		if hasattr(wid, 'saved_attrs'):
			if not dohide:
				wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
				del wid.saved_attrs
		elif dohide:
			wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
			wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True


	def switch_callback(self, switchObject, switchValue):
		print("here")
		if(switchValue):
			cam.play = True
			self.hide_widget(cam, False)
		else:
			cam.play = False
			self.hide_widget(cam)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		#self.add_widget(cam)
		#cam.play = False
		#self.hide_widget(cam)
		switch_camera = Switch(active = False, pos_hint = {'x' : 0.43, 'y' : 0.45})
		self.add_widget(switch_camera)
		switch_camera.bind(active = self.switch_callback)
		switch_AI = Switch(active = False, pos_hint = {'x' : -0.43, 'y' : 0.45})
		self.add_widget(switch_AI)
		self.add_widget(Button_right())
		self.add_widget(Button_left())
		self.add_widget(Button_forward())
		self.add_widget(Button_backward())
		

class DemoApp(App):
	def build(self):
		return Float_layout()
	
DemoApp().run()
client_socket.close()  # close the connection