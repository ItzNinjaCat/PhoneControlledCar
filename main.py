from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.config import Config 
from kivy.lang.builder import Builder
from kivy.uix.camera import Camera
from kivy.core.window import Window
<<<<<<< Updated upstream:main.py
#import cv2
#import time
=======
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from threading import Thread
import requests
import time
import json
import cv2
import socket
from os.path import exists

Window.size = (1600, 900)
distance_thread = None
throttle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
steering = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_connection_status = False
video_feed = cv2.VideoCapture()

button_state_dict = {'left' : True, 'right' : True, 'forward' : True, 'backward' : True}


def hide_widget(wid, dohide=True):
	if hasattr(wid, 'saved_attrs'):
		if not dohide:
			wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
			del wid.saved_attrs
	elif dohide:
		wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
		wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

>>>>>>> Stashed changes:kivy_tests/main.py



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
		self.pos_hint = {'x' : 0.04, 'y' : 0.1}
		self.size_hint = (0.1, 0.1)

	def on_press(self):
		if not button_state_dict['right']:
			button_state_dict['left'] = True
			self.source = 'left_down.png'
			message = "leftON"
			steering.send(message.encode())

	def on_release(self):
		if not button_state_dict['right']:
			button_state_dict['left'] = False
			self.source = 'left.png'
			message = "leftOFF"
			steering.send(message.encode())

class Button_right(ButtonBehavior, Image):
<<<<<<< Updated upstream:main.py
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
=======
	def __init__(self, **kwargs):
		super(Button_right, self).__init__(**kwargs)
		self.source = 'right.png'
		self.pos_hint = {'x' : 0.12, 'y' : 0.1}
		self.size_hint = (0.1, 0.1)

	def on_press(self):
		if not button_state_dict['left']:
			button_state_dict['right'] = True
			self.source = 'right_down.png'
			message = "rightON"
			steering.send(message.encode())
			
	def on_release(self):
		if not button_state_dict['left']:
			button_state_dict['right'] = False
			self.source = 'right.png'
			message = "rightOFF"
			steering.send(message.encode())	

>>>>>>> Stashed changes:kivy_tests/main.py
class Button_forward(ButtonBehavior, Image):
	def __init__(self, **kwargs):
		super(Button_forward, self).__init__(**kwargs)
		self.source = 'forward.png'
		self.pos_hint = {'x' : 0.85, 'y' : 0.22}
		self.size_hint = (0.1, 0.1)

	def on_press(self):
		if not button_state_dict['backward']:
			button_state_dict['forward'] = True
			self.source = 'forward_down.png'
			message = "forwardON"
			throttle.send(message.encode())
			
	def on_release(self):
		if not button_state_dict['backward']:
			button_state_dict['forward'] = False
			self.source = 'forward.png'
			message = "forwardOFF"
			throttle.send(message.encode())

class Button_backward(ButtonBehavior, Image):
<<<<<<< Updated upstream:main.py
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
=======
	def __init__(self, **kwargs):
		super(Button_backward, self).__init__(**kwargs)
		self.source = 'backward.png'
		self.pos_hint = {'x' : 0.85, 'y' : 0.07}
		self.size_hint = (0.1, 0.1)
>>>>>>> Stashed changes:kivy_tests/main.py

	def on_press(self):
		if not button_state_dict['forward']:
			button_state_dict['backward'] = True
			self.source = 'backward_down.png'
			message = "backwardON"
			throttle.send(message.encode())
			
	def on_release(self):
		if not button_state_dict['forward']:
			button_state_dict['backward'] = False
			self.source = 'backward.png'
			message = "backwardOFF"
			throttle.send(message.encode())

<<<<<<< Updated upstream:main.py
	def switch_callback(self, switchObject, switchValue):
		print("here")
		if(switchValue):
			cam.play = True
			self.hide_widget(cam, False)
		else:
			cam.play = False
			self.hide_widget(cam)
=======
class Distance_display(Label):
	def __init__(self, **kwargs):
		super(Distance_display, self).__init__(**kwargs)
		self.pos_hint = {'x' : 0.45, 'y' : 0.87}
		self.size_hint = (0.1, 0.1)
		self.text = "Distance sensor is not connected"
		self.color = "red"
		self.font_size = 35
		
btn_right = Button_right()
btn_left = Button_left()
btn_forward = Button_forward()
btn_backward = Button_backward()
switch_camera = Switch(active = False, size_hint = (None, None),size = (83,32), pos_hint = {'x' : 0.89, 'y' : 0.89})
display_distance = Distance_display()
flask_url = ""
frames_per_second = 1 / 30
distance_update_timer = 6

class Button_settings(ButtonBehavior, Image):
	def __init__(self, **kwargs):
		super(Button_settings, self).__init__(**kwargs)
		
		self.always_relese = False
		self.source = 'settings.png'
		self.pos_hint = {'x' : 0.01, 'y' : 0.87}
		self.size_hint = (0.1, 0.1)
		box = FloatLayout(size = (600, 400))
		

		close_btn = Button(text='Connect', size_hint=(0.8, 0.25), pos_hint= {'x' : 0.1 , 'y' : 0.1})
		close_btn.bind(on_press=self.popup_bttn)
		self.ip_textinput = TextInput(hint_text='IP Adress - Ipv4 adress of the Rpi', size_hint =(0.6,0.1), pos_hint = {'x' : 0.2, 'y' : 0.7})
		self.port_textinput = TextInput(hint_text='Port - The port on which the socket server is running', size_hint =(0.6,0.1), pos_hint = {'x' : 0.2, 'y' : 0.6})
		self.video_server_url_textinput = TextInput(hint_text='Video stream URL - URL for the flask server', size_hint =(0.6,0.1), pos_hint = {'x' : 0.2, 'y' : 0.5})
		if exists("connections.json"):	
			try:
				dict_list = []
				with open('connections.json') as json_file:
					dict_list = json.load(json_file)
				dict = dict_list[-1]
				self.ip_textinput.text = dict['ip']
				self.port_textinput.text = dict['port']
				self.video_server_url_textinput.text = dict['video']
			except:
				pass
		box.add_widget(self.ip_textinput)
		box.add_widget(self.port_textinput)
		box.add_widget(self.video_server_url_textinput)
		box.add_widget(close_btn)
		
		self.popup = Popup(title="Enter ip and port of the Raspberry Pi", content=box, size_hint=(0.8, 0.6), auto_dismiss = False)
		
	def error_popup(self, error_code):
		box = BoxLayout(orientation='vertical')
		box.add_widget(Label(text = error_code, valign = 'middle', halign = 'justify'))
		err_close_btn = Button(text = "OK", size_hint = (0.2,0.3), pos_hint = {'x' : 0.4})
		box.add_widget(err_close_btn)
		err_popup = Popup(title="Error", content=box, size_hint=(0.5, 0.3), auto_dismiss = False)
		err_close_btn.bind(on_press=err_popup.dismiss)
		err_popup.open()
		try:
			if exists("connections.json"):
				dict_list = []
				with open('connections.json') as json_file:
					dict_list = json.load(json_file)
				dict = dict_list[-1]
				self.ip_textinput.text = dict['ip']
				self.port_textinput.text = dict['port']
				self.video_server_url_textinput.text = dict['video']

				
		except:
			pass
>>>>>>> Stashed changes:kivy_tests/main.py

	def popup_bttn(self, dt = None):
		global socket_connection_status, button_state_dict, throttle, steering, frames_per_second, distance_update_timer
		
		if self.ip_textinput.text == '' or self.port_textinput.text == '':
			self.error_popup("IP address and port number are required to use the app!")
		else:

			dict = {
				'ip' : self.ip_textinput.text.strip(),
				'port' : self.port_textinput.text.strip(),
				'video' : self.video_server_url_textinput.text.strip()
			}
			try:
				if socket_connection_status:
					message = "q"
					throttle.send(message.encode())
					steering.send(message.encode())
					throttle.close()
					steering.close()
					throttle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					steering = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

					
				throttle.connect((dict['ip'],int(dict['port'])))
				steering.connect((dict['ip'],int(dict['port'])))
				socket_connection_status = True
			except:
				self.error_popup("Unable to connect to given IP and port combination!")
				return
		
			try:
				video_feed.open(dict['video'])
			except:
				pass
			
			if not video_feed.isOpened() and dict['video'] != '':
				self.error_popup("Unable to connect to given video feed!")
			elif video_feed.isOpened():
				flask_url = dict['video']
	
			try:
				dict_list = []
				with open('connections.json') as json_file:
					dict_list = json.load(json_file)
				flag = False
				for i in range(len(dict_list)):
					if dict_list[i]['ip'] == dict['ip'] and dict_list[i]['port'] == dict['port']:
						dict_list[i] = dict
						flag = True
						break
				if not flag:
					dict_list.append(dict)
				with open("connections.json", "w") as outfile:
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
				button_state_dict = {'left' : False, 'right' : False, 'forward' : False, 'backward' : False}
				self.popup.dismiss()
				self.disabled = False
			except:
				pass
		
	def on_press(self):
		self.popup.open()
		
		hide_widget(switch_camera)
		hide_widget(btn_left)
		hide_widget(btn_right)
		hide_widget(btn_forward)
		hide_widget(btn_backward)
		hide_widget(self)
		hide_widget(display_distance)
		self.disabled = True
		
btn_settings = Button_settings()


class Float_layout(FloatLayout):
	def __init__(self, **kwargs):
		global socket_connection_status, button_state_dict, throttle, steering, flask_url, distance_thread
	
		super().__init__(**kwargs)
<<<<<<< Updated upstream:main.py
		#self.add_widget(cam)
		#cam.play = False
		#self.hide_widget(cam)
		switch_camera = Switch(active = False, pos_hint = {'x' : 0.43, 'y' : 0.45})
=======
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_key_down)
		self._keyboard.bind(on_key_up=self._on_key_up)
		self.img = Image()
		self.img.size = self.size
		self.img.allow_stretch = True
		self.img.keep_ratio = False
		self.ids['image_source'] = self.img
		

		#switch_AI = Switch(active = False, size_hint = (None, None),size = (83,32), pos_hint = {'x' : 0.88, 'y' : 0.88})
		#self.add_widget(switch_AI)	

		self.add_widget(self.img)
		hide_widget(self.img)
>>>>>>> Stashed changes:kivy_tests/main.py
		self.add_widget(switch_camera)
		self.add_widget(btn_right)
		self.add_widget(btn_left)
		self.add_widget(btn_forward)
		self.add_widget(btn_backward)
		self.add_widget(btn_settings)
		self.add_widget(display_distance)
		
		
		if not exists("connections.json"):
			btn_settings.on_press()
		else:
			dict_list = []
			with open('connections.json') as json_file:
				dict_list = json.load(json_file)
			if not len(dict_list):
				btn_settings.on_press()
			else:
				try:
					dict_list = []
					with open('connections.json') as json_file:
						dict_list = json.load(json_file)
					
					fail = False
					last_working_dict = None
					for dict in dict_list:
						try:
							if socket_connection_status:
								message = "q"
								throttle.send(message.encode())
								steering.send(message.encode())

								throttle.close()
								steering.close()
								throttle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
								steering = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							throttle.connect((dict['ip'],int(dict['port'])))
							steering.connect((dict['ip'],int(dict['port'])))
							socket_connection_status = True
							button_state_dict = {'left' : False, 'right' : False, 'forward' : False, 'backward' : False}
							last_working_dict = dict
						except:
							fail = True
							continue
							
						try:
							video_feed.open(dict['video'])
						except:
							pass
						if not video_feed.isOpened() and dict['video'] != '':
							btn_settings.error_popup("Unable to connect to given video feed!")
							dict['video'] = ''
						fail = False
						if video_feed.isOpened():
							flask_url = dict['video']
							break
					if fail:				
						btn_settings.on_press()
						btn_settings.error_popup("Unable to connect to given IP and port combination!")
					elif not socket_connection_status:
							throttle.connect((last_working_dict['ip'],int(last_working_dict['port'])))
							steering.connect((last_working_dict['ip'],int(last_working_dict['port'])))
							socket_connection_status = True
					with open("connections.json", "w") as outfile:
						json.dump(dict_list, outfile, indent=4,  separators=(',',': '))
				except:
					btn_settings.on_press()

		switch_camera.bind(active = self.switch_callback)
<<<<<<< Updated upstream:main.py
		switch_AI = Switch(active = False, pos_hint = {'x' : -0.43, 'y' : 0.45})
		self.add_widget(switch_AI)
		self.add_widget(Button_right())
		self.add_widget(Button_left())
		self.add_widget(Button_forward())
		self.add_widget(Button_backward())
=======
		self.capture = video_feed
		Clock.schedule_interval(self.camera_update, 1 / 120)
		distance_thread = Thread(target = Clock.schedule_interval, args=(self.distance_update,  1 / 120))
		distance_thread.start()
		
	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_key_down)
		self._keyboard.unbind(on_key_up=self._on_key_up)
		self._keyboard = None
>>>>>>> Stashed changes:kivy_tests/main.py
		
	def _on_key_down(self, keyboard, keycode, text, modifiers):
		if keycode[1] == 'w' or keycode[1] == 'up':
			if not button_state_dict['backward'] and not button_state_dict['forward'] :
				btn_forward.on_press()

<<<<<<< Updated upstream:main.py
class DemoApp(App):
	def build(self):
		return Float_layout()
	
DemoApp().run()
client_socket.close()  # close the connection
=======
		elif keycode[1] == 's' or keycode[1] == 'down':
			if not button_state_dict['forward'] and not button_state_dict['backward']:
				btn_backward.on_press()
			
		elif keycode[1] == 'a' or keycode[1] == 'left':
			if not button_state_dict['right'] and not button_state_dict['left']:
				btn_left.on_press()
			
		elif keycode[1] == 'd' or keycode[1] == 'right':
			if not button_state_dict['left'] and not button_state_dict['right']:
				btn_right.on_press()

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
				msg = (requests.get(flask_url + "dist")).text
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
			self.img.texture = texture1
		except:
			pass

	def switch_callback(self, switchObject, switchValue):
		if video_feed.isOpened():
			if switchValue:
				hide_widget(self.img, False)
			else:
				hide_widget(self.img)
		else:
			if switchValue:
				Button_settings.error_popup(Button_settings, "Unable to connect to given video feed!")

class RcCarApplication(App):
	def build(self):
		return Float_layout()

	def on_stop(self):
	
		message = "q"
		throttle.send(message.encode())
		steering.send(message.encode())
		throttle.close()
		steering.close()
		video_feed.release()
		distance_thread._stop()

def main():
	RcCarApplication().run()

if __name__ == "__main__":
	main()
>>>>>>> Stashed changes:kivy_tests/main.py
