from kivy.uix.switch import Switch
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.app import App

from global_vars import *

import errno
import json
import cv2
import socket
from os.path import exists
import os

class Button_left(ButtonBehavior, Image):
	def __init__(self, **kwargs):
		super(Button_left, self).__init__(**kwargs)
		self.always_relese = False
		self.source = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\left.png'
		self.pos_hint = {'x' : 0.04, 'y' : 0.1}
		self.size_hint = (0.1, 0.1)

	def on_press(self):
		if not get_button_right_state():
			set_button_left_state(True)
			self.source = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\left_down.png'
			message = "leftON"
			get_steering().send(message.encode())

	def on_release(self):
		if not get_button_right_state():
			set_button_left_state(False)
			self.source = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\left.png'
			message = "leftOFF"
			get_steering().send(message.encode())

class Button_right(ButtonBehavior, Image):
	def __init__(self, **kwargs):
		super(Button_right, self).__init__(**kwargs)
		self.source = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\right.png'
		self.pos_hint = {'x' : 0.12, 'y' : 0.1}
		self.size_hint = (0.1, 0.1)

	def on_press(self):
		if not get_button_left_state():
			set_button_right_state(True)
			self.source = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\right_down.png'
			message = "rightON"
			get_steering().send(message.encode())
			
	def on_release(self):
		if not get_button_left_state():
			set_button_right_state(False)
			self.source = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\right.png'
			message = "rightOFF"
			get_steering().send(message.encode())	

class Button_forward(ButtonBehavior, Image):
	def __init__(self, **kwargs):
		super(Button_forward, self).__init__(**kwargs)
		self.source = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\forward.png'
		self.pos_hint = {'x' : 0.85, 'y' : 0.22}
		self.size_hint = (0.1, 0.1)

	def on_press(self):
		if not get_button_backward_state():
			set_button_forward_state(True)
			self.source = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\forward_down.png'
			message = "forwardON"
			get_throttle().send(message.encode())
			
	def on_release(self):
		if not get_button_backward_state():
			set_button_forward_state(False)
			self.source = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\forward.png'
			message = "forwardOFF"
			get_throttle().send(message.encode())

class Button_backward(ButtonBehavior, Image):
	def __init__(self, **kwargs):
		super(Button_backward, self).__init__(**kwargs)
		self.source = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\backward.png'
		self.pos_hint = {'x' : 0.85, 'y' : 0.07}
		self.size_hint = (0.1, 0.1)

	def on_press(self):
		if not get_button_forward_state():
			set_button_backward_state(True)
			self.source = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\backward_down.png'
			message = "backwardON"
			get_throttle().send(message.encode())
			
	def on_release(self):
		if not get_button_forward_state():
			set_button_backward_state(False)
			self.source = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\backward.png'
			message = "backwardOFF"
			get_throttle().send(message.encode())

class Distance_display(Label):
	def __init__(self, **kwargs):
		super(Distance_display, self).__init__(**kwargs)
		self.pos_hint = {'x' : 0.45, 'y' : 0.87}
		self.size_hint = (0.1, 0.1)
		self.text = "Distance sensor is not connected"
		self.color = "red"
		self.font_size = 35
		
class Switch_camera(Switch):
	def __init__(self, **kwargs):
		super(Switch_camera, self).__init__(**kwargs)
		self.active = False
		self.size_hint = (None, None)
		self.size = (83,32)
		self.pos_hint = {'x' : 0.89, 'y' : 0.89}
		self.bind(active=self.switch_callback)
	
	def switch_callback(self, switchObject, switchValue):
		if get_video().isOpened():
			if switchValue:
				hide_widget(get_frame(), False)
			else:
				hide_widget(get_frame())
		else:
			if switchValue:
				error_popup("Unable to connect to given video feed!")

btn_right = Button_right()
btn_left = Button_left()
btn_forward = Button_forward()
btn_backward = Button_backward()
switch_camera = Switch_camera()
display_distance = Distance_display()


class Button_settings(ButtonBehavior, Image):
	def __init__(self, **kwargs):
		super(Button_settings, self).__init__(**kwargs)
		
		self.always_relese = False
		self.source = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\settings.png'
		self.pos_hint = {'x' : 0.01, 'y' : 0.87}
		self.size_hint = (0.1, 0.1)
		self.float = FloatLayout(size = (600, 400))
		
		self.close_btn = Button(size_hint = (None, None), size = (50, 50), pos_hint = {'x' : 0.93, 'y' : 0.85}, background_normal = os.path.dirname(os.getcwd()) + '\\Assets\\sprites\\close.png')
		hide_widget(self.close_btn)
		self.close_btn.bind(on_press=self.close_btn_callback)
		self.conn_btn = Button(text = 'Connect', size_hint = (0.8, 0.25), pos_hint = {'x' : 0.1 , 'y' : 0.1})
		self.conn_btn.bind(on_press = self.popup_btn)
		self.ip_textinput = TextInput(hint_text = 'IP Adress - Ipv4 adress of the Rpi', size_hint = (0.6,0.1), pos_hint = {'x' : 0.2, 'y' : 0.7})
		self.port_textinput = TextInput(hint_text = 'Port - The port on which the socket server is running', size_hint = (0.6,0.1), pos_hint = {'x' : 0.2, 'y' : 0.6})
		self.video_server_url_textinput = TextInput(hint_text = 'Video stream URL - URL for the flask server', size_hint = (0.6,0.1), pos_hint = {'x' : 0.2, 'y' : 0.5})
		if exists(os.path.dirname(os.getcwd()) + "\Assets\data\connections.json"):	
			try:
				dict_list = []
				try:
					with open(os.path.dirname(os.getcwd()) + '\Assets\data\connections.json') as json_file:
						dict_list = json.load(json_file)
					dict = dict_list[-1]
					self.ip_textinput.text = dict['ip']
					self.port_textinput.text = dict['port']
					self.video_server_url_textinput.text = dict['video']
				except:
					pass
			except:
				pass
		self.float.add_widget(self.ip_textinput)
		self.float.add_widget(self.port_textinput)
		self.float.add_widget(self.video_server_url_textinput)
		self.float.add_widget(self.conn_btn)
		self.float.add_widget(self.close_btn)
		
		self.popup = Popup(title="Enter ip and port of the Raspberry Pi", content=self.float, size_hint=(0.8, 0.6), auto_dismiss = False)
		
	def settings_error_popup(self, error_code):
		error_popup(error_code)
		try:
			if exists(os.path.dirname(os.getcwd()) + '\Assets\data\connections.json'):
				dict_list = []
				try:
					with open(os.path.dirname(os.getcwd()) + '\Assets\data\connections.json') as json_file:
						dict_list = json.load(json_file)
					dict = dict_list[-1]
					self.ip_textinput.text = dict['ip']
					self.port_textinput.text = dict['port']
					self.video_server_url_textinput.text = dict['video']
				except:
					pass
				
		except:
			pass

	def close_btn_callback(self, dt = None):
		global button_state_dict
		try:
			hide_widget(switch_camera, False)
			hide_widget(btn_left, False)
			hide_widget(btn_right, False)
			hide_widget(btn_forward, False)
			hide_widget(btn_backward, False)
			hide_widget(self, False)
			hide_widget(display_distance, False)
			set_all_states({'left' : False, 'right' : False, 'forward' : False, 'backward' : False})
			self.popup.dismiss()
			self.disabled = False
			self.ip_textinput.focus = False
			self.port_textinput.focus = False
			self.video_server_url_textinput.focus = False
			app = App.get_running_app()
			app.layout.keyboard.focus = True
			app.layout.keyboard.bind(on_key_down=app.layout._on_key_down)
			app.layout.keyboard.bind(on_key_up=app.layout._on_key_up)
		except:
			pass

	def popup_btn(self, dt = None):
		global button_state_dict, throttle, steering

		if self.ip_textinput.text == '' or self.port_textinput.text == '':
			self.settings_error_popup("IP address and port number are required to use the app!")
		else:

			dict = {
				'ip' : self.ip_textinput.text.strip(),
				'port' : self.port_textinput.text.strip(),
				'video' : self.video_server_url_textinput.text.strip()
			}
			try:
				try:
					get_throttle().connect((dict['ip'],int(dict['port'])))
					get_steering().connect((dict['ip'],int(dict['port'])))
				except Exception as e:
					if e == ConnectionRefusedError:
						self.settings_error_popup("Device is not authorized - try to either add it's mac address\nto the trusted.txt file or set security_flag to 0 is connections.txt")
						return
					try:
						message = "q"
						get_throttle().send(message.encode())
						get_steering().send(message.encode())
						get_throttle().close()
						get_steering().close()
					except Exception as e:
						if e.errno == 10053:
							self.settings_error_popup("Device is not authorized - try to either add it's mac address\nto the trusted.txt file or set security_flag to 0 is connections.txt")
							return
					set_throttle(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
					set_steering(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
					get_throttle().connect((dict['ip'],int(dict['port'])))
					get_steering().connect((dict['ip'],int(dict['port'])))
				try:
					message = "connection check"
					get_throttle().send(message.encode())
					get_steering().send(message.encode())
				except:
					self.settings_error_popup("Device is not authorized - try to either add it's mac address\nto the trusted.txt file or set security_flag to 0 is connections.txt")
					return
			except:
				self.settings_error_popup("Unable to connect to given IP and port combination!")
				return
		
			try:
				get_video().open(dict['video'])
			except:
				pass
			
			if not get_video().isOpened() and dict['video'] != '':
				error_popup("Unable to connect to given video feed!")
			elif get_video().isOpened():
				set_flask_url(dict['video'])
			try:
				dict_list = []
				try:
					with open(os.path.dirname(os.getcwd()) + '\Assets\data\connections.json') as json_file:
						dict_list = json.load(json_file)
					flag = False
					for i in range(len(dict_list)):
						if dict_list[i]['ip'] == dict['ip'] and dict_list[i]['port'] == dict['port']:
							dict_list[i] = dict
							flag = True
							break
					if not flag:
						dict_list.append(dict)
				except:
					dict_list.append(dict)
				with open(os.path.dirname(os.getcwd()) + '\Assets\data\connections.json', "w") as outfile:
					json.dump(dict_list, outfile, indent=4,  separators=(',',': '))
			except:
				pass
			
			try:
				hide_widget(switch_camera, False)
				hide_widget(btn_left, False)
				hide_widget(btn_right, False)
				hide_widget(btn_forward, False)
				hide_widget(btn_backward, False)
				hide_widget(self, False)
				hide_widget(display_distance, False)
				set_all_states({'left' : False, 'right' : False, 'forward' : False, 'backward' : False})
				self.popup.dismiss()
				self.disabled = False
				self.ip_textinput.focus = False
				self.port_textinput.focus = False
				self.video_server_url_textinput.focus = False
				app = App.get_running_app()
				app.layout.keyboard.focus = True
				app.layout.keyboard.bind(on_key_down=app.layout._on_key_down)
				app.layout.keyboard.bind(on_key_up=app.layout._on_key_up)
			except:
				pass
		
	def on_press(self, outside_call_flag = False):
		try:
			hide_widget(switch_camera)
			hide_widget(btn_left)
			hide_widget(btn_right)
			hide_widget(btn_forward)
			hide_widget(btn_backward)
			hide_widget(self)
			hide_widget(display_distance)
			self.disabled = True

			if not outside_call_flag:
				hide_widget(self.close_btn, False)
			else:
				hide_widget(self.close_btn)
			self.popup.open()
		except:
			pass
		
		
		
btn_settings = Button_settings()
