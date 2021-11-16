#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import json
import threading
from kafka import KafkaConsumer
from two_micros.concatenation_service.model import image_access

class Receiver(threading.Thread):
	"""
	Downloader Service

	Attributes:
		consumer : kafka consumer
		stop_event : controller to stop thread process
	"""
	daemon = True
	def __init__(self, topic):
		self.topic = topic
		self.consumer = KafkaConsumer(self.topic,
									bootstrap_servers='localhost:9092',
		            				group_id=self.topic,
		            				value_deserializer=lambda m: json.loads(m.decode('utf-8')))
		threading.Thread.__init__(self)
		self.stop_event = threading.Event()
		print(topic, 'is started')
 
	def stop(self):
	    self.stop_event.set()

	def valid_json(self, json_msg):
		return 'id' in json_msg and 'path' in json_msg

	def run(self):
		while not self.stop_event.is_set():
			for msg in self.consumer:
				json_val = msg.value
				if self.valid_json(json_val):
					id = json_val['id']
					path = json_val['path']
					self.new_image(id, path)
				if self.stop_event.is_set():
					break

		self.consumer.close()
		self.stop()


class SuperHeroReceiver(Receiver):
	def __init__(self):
		super().__init__('super_heros')

	def new_image(self, id, path):
		image_access.new_image(id=id, super_hero_path=path)

class AlterEgosReceiver(Receiver):
	def __init__(self):
		super().__init__('alter_egos')

	def new_image(self, id, path):
		image_access.new_image(id=id, alter_egos_path=path)

