from layout_widget import Float_layout, distance_thread
from global_vars import *
from kivy.app import App
from kivy.config import Config 
import os
Config.set('graphics', 'resizable', True)
Config.set('kivy','window_icon',os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\app_icon.ico')

class RcCarApplication(App):
	def build(self):
		self.icon = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\app_icon.png'
		return Float_layout()

	def on_stop(self):
		try:
			message = "q"
			get_throttle().send(message.encode())
			get_steering().send(message.encode())
			get_throttle().close()
			get_steering().close()
		except:
			pass
		try:
			get_video().release()
		except:
			pass
		try:
			distance_thread._stop()
		except:
			pass
