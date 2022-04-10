from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.switch import Switch
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

from threading import Thread
import requests
import json
import cv2
import socket
from os.path import exists
import os

from global_vars import *
from buttons import *
Window.size = (1280, 720)
distance_thread = Thread()
video_thread = Thread()

class Float_layout(FloatLayout):
	def __init__(self, **kwargs):
		global throttle, steering, distance_thread, video_thread
	
		super().__init__(**kwargs)
		
		
		self.keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self.keyboard.bind(on_key_down=self._on_key_down)
		self.keyboard.bind(on_key_up=self._on_key_up)
		get_frame().size = self.size
		get_frame().allow_stretch = True
		get_frame().keep_ratio = False
		

		#switch_AI = Switch(active = False, size_hint = (None, None),size = (83,32), pos_hint = {'x' : 0.88, 'y' : 0.88})
		#self.add_widget(switch_AI)	
		self.add_widget(get_frame())
		hide_widget(get_frame())
		self.add_widget(switch_camera)
		self.add_widget(btn_right)
		self.add_widget(btn_left)
		self.add_widget(btn_forward)
		self.add_widget(btn_backward)
		self.add_widget(btn_settings)
		self.add_widget(display_distance)
		
		
		if not exists(os.path.dirname(os.getcwd()) + '\Assets\data\connections.json'):
			btn_settings.on_press(outside_call_flag = True)
		else:
			dict_list = []
			try:
				with open(os.path.dirname(os.getcwd()) + '\Assets\data\connections.json') as json_file:
					dict_list = json.load(json_file)
				if not len(dict_list):
					btn_settings.on_press(outside_call_flag = True)
			except:
				btn_settings.on_press(outside_call_flag = True)
			if len(dict_list):
				try:
					fail = False
					last_working_dict = None
					for dict in dict_list:
						try:
							try:
								get_throttle().connect((dict['ip'],int(dict['port'])))
								get_steering().connect((dict['ip'],int(dict['port'])))
							except:
								try:
									message = "q"
									get_throttle().send(message.encode())
									get_steering().send(message.encode())
									get_throttle().close()
									get_steering().close()
								except:
									pass
								set_throttle(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
								set_steering(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
								get_throttle().connect((dict['ip'],int(dict['port'])))
								get_steering().connect((dict['ip'],int(dict['port'])))
							set_all_states({'left' : False, 'right' : False, 'forward' : False, 'backward' : False})
							last_working_dict = dict
						except:
							fail = True
							continue
							
						try:
							message = "connection check"
							get_throttle().send(message.encode())
							get_steering().send(message.encode())	
						except:
							btn_settings.on_press(outside_call_flag = True)
							error_popup("Device is not authorized - try to either add it's mac address\nto the trusted.txt file or set security_flag to 0 is connections.txt")
							fail = False
							break
						try:
							get_video().open(dict['video'])
						except:
							pass
						if not get_video().isOpened() and dict['video'] != '':
							error_popup("Unable to connect to given video feed!")
							dict['video'] = ''
						fail = False
						if get_video().isOpened():
							set_flask_url(dict['video'])
							break
					if fail:				
						btn_settings.on_press(outside_call_flag = True)
						btn_settings.settings_error_popup("Unable to connect to given IP and port combination!")
					try:
						get_throttle().connect((last_working_dict['ip'],int(last_working_dict['port'])))
						get_steering().connect((last_working_dict['ip'],int(last_working_dict['port'])))
					except:
						pass

						
					with open(os.path.dirname(os.getcwd()) + '\Assets\data\connections.json', "w") as outfile:
						json.dump(dict_list, outfile, indent=4,  separators=(',',': '))
				except:
					btn_settings.on_press(outside_call_flag = True)

		self.capture = get_video()
		video_thread = Thread(target = Clock.schedule_interval, args = (self.camera_update, 1 / 120))
		video_thread.start()
		distance_thread = Thread(target = Clock.schedule_interval, args=(self.distance_update,  1 / 120))
		distance_thread.start()
		
	def _keyboard_closed(self):
		self.keyboard.unbind(on_key_down=self._on_key_down)
		self.keyboard.unbind(on_key_up=self._on_key_up)
		
		
	def _on_key_down(self, keyboard, keycode, text, modifiers):
		if keycode[1] == 'w' or keycode[1] == 'up':
				btn_forward.on_press()

		elif keycode[1] == 's' or keycode[1] == 'down':
				btn_backward.on_press()
			
		elif keycode[1] == 'a' or keycode[1] == 'left':
				btn_left.on_press()
			
		elif keycode[1] == 'd' or keycode[1] == 'right':
				btn_right.on_press()
		elif keycode[1] == 'escape':
			btn_settings.on_press()
		elif keycode[1] == 'v':
			switch_camera.active = not switch_camera.active
		return True

	def _on_key_up(self, keyboard, keycode):
		if keycode[1] == 'w' or keycode[1] == 'up':
			btn_forward.on_release()
				
		elif keycode[1] == 's' or keycode[1] == 'down':
			btn_backward.on_release()

		elif keycode[1] == 'a' or keycode[1] == 'left':
			btn_left.on_release()
	
		elif keycode[1] == 'd' or keycode[1] == 'right':
			btn_right.on_release()
			
		return True

	def distance_update(self, dt = None):
			try:
				msg = (requests.get(get_flask_url() + "dist")).text
				msg = round(float(msg), 2)
				display_distance.text = "Distance to closest object is {:.2f} cm".format(msg)
			except:
				display_distance.text = "No distance sensor connected!"

	def camera_update(self, dt = None):
		try:
			ret, frame = self.capture.read()
			buf1 = cv2.flip(frame, 0)
			buf = buf1.tobytes()
			texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
			texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
			get_frame().texture = texture1
		except:
			pass
	
	def __del__(self):
		self.capture.release()