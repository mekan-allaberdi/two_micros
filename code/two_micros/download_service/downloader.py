#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import json
import threading
import configparser
from kafka import KafkaProducer
from two_micros.util.helper import read_csv, download_file, get_file_extension, check_local_dir


class DLS(threading.Thread):
	"""
	Downloader Service

	Attributes:
		csv_file_path : path of input csv file
		image_local_path : local path to store images.
		producer : kafka producer
		stop_event : controller to stop thread process
	"""
	daemon = True
	def __init__(self, topic):
		self.topic = topic
		config = configparser.ConfigParser()
		config.read('config.ini')
		config_attrs = config[self.topic]
		self.csv_file_path = config_attrs['csv_file_path']
		self.image_local_path = os.getcwd() + '/' + config_attrs['image_local_path']
		self.producer = KafkaProducer(bootstrap_servers='localhost:9092',
									value_serializer=lambda v: json.dumps(v).encode('utf-8'))
		threading.Thread.__init__(self)
		self.stop_event = threading.Event()
        
	def stop(self):
	    self.stop_event.set()

	def run(self):
		# Check if local dir is created before or not.
		# If directory does not exist, create it.
		check_local_dir(self.image_local_path)

		records = read_csv(self.csv_file_path)
		for record in records:
			id = record['id']
			url = record['path']
			ext = get_file_extension(url)
			local_path = ''.join([self.image_local_path, id, ext])
			download_file(url, local_path)

			record['path'] = local_path
			self.producer.send(self.topic, record)
			self.producer.flush()
		self.producer.close()
		self.stop()

class SuperHeros(DLS):
	def __init__(self):
		super().__init__('super_heros')

class AlterEgos(DLS):
	def __init__(self):
		super().__init__('alter_egos')
