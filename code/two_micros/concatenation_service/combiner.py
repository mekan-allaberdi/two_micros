#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import time
import threading
import configparser

from two_micros.concatenation_service.model import image_access
from two_micros.util.helper import concat_two_images, get_file_extension, check_local_dir

class Combiner(threading.Thread):
	"""
	Combiner Service : Concatenate images

	Attributes:
		image_local_path : local path to store images.
		stop_event : controller to stop thread process
	"""
	
	daemon = True
	def __init__(self):
		config = configparser.ConfigParser()
		config.read('config.ini')
		self.image_local_path = os.getcwd() + '/' + config['cs']['image_local_path']
		threading.Thread.__init__(self)
		self.stop_event = threading.Event()

	def stop(self):
		self.stop_event.set()

	def run(self):
		check_local_dir(self.image_local_path)

		while not self.stop_event.is_set():
			image_list = image_access.get_ready_images()
			if not image_list:
				# if no images to proceed, wait 5 secs.
				time.sleep(5)

			for image in image_list:
				id = image.id
				ext = get_file_extension(image.super_hero_path)
				img_final_path = ''.join([self.image_local_path, id, ext])
				try:
					concat_two_images(img_left_path=image.super_hero_path,
									img_right_path=image.alter_egos_path, 
									img_final_path = img_final_path)
				except:
					print('Error in concatenating image id:%s' % id)
				image_access.state_to_finished(id)