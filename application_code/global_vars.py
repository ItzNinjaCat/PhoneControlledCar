import socket
import cv2
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image


throttle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
steering = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_feed = cv2.VideoCapture()
video_frame = Image()
button_state_dict = {'left' : True, 'right' : True, 'forward' : True, 'backward' : True}

def get_all_states():
	return button_state_dict

def set_all_states(new_states):
	global button_state_dict
	button_state_dict = new_states

def get_button_left_state():
	return button_state_dict['left']

def set_button_left_state(new_state):
	global button_state_dict
	button_state_dict['left'] = new_state

def get_button_right_state():
	return button_state_dict['right']

def set_button_right_state(new_state):
	global button_state_dict
	button_state_dict['right'] = new_state
	
def get_button_forward_state():
	return button_state_dict['forward']

def set_button_forward_state(new_state):
	global button_state_dict
	button_state_dict['forward'] = new_state

def get_button_backward_state():
	return button_state_dict['backward']

def set_button_backward_state(new_state):
	global button_state_dict
	button_state_dict['backward'] = new_state

def get_throttle():
	return throttle

def set_throttle(new_throttle):
	global throttle
	throttle = new_throttle

def get_steering():
	return steering

def set_steering(new_steering):
	global steering
	steering = new_steering
	
	

def get_frame():
	return video_frame

def get_video():
	return video_feed


def hide_widget(wid, dohide=True):
	if hasattr(wid, 'saved_attrs'):
		if not dohide:
			wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
			del wid.saved_attrs
	elif dohide:
		wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
		wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

def error_popup(error_code):
		box = BoxLayout(orientation='vertical')
		box.add_widget(Label(text = error_code, valign = 'middle', halign = 'justify'))
		err_close_btn = Button(text = "OK", size_hint = (0.2,0.3), pos_hint = {'x' : 0.4})
		box.add_widget(err_close_btn)
		err_popup = Popup(title="Error", content=box, size_hint=(0.5, 0.3), auto_dismiss = False)
		err_close_btn.bind(on_press=err_popup.dismiss)
		err_popup.open()