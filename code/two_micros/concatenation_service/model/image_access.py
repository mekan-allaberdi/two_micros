#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from two_micros.concatenation_service.model import db, Img
from two_micros.util.constants import IDLE, READY, MERGED
from datetime import datetime

def get(id):
	return db.session.query(Img).get(id)

def some_filter(path):
	q = db.session.query(Img)
	q = q.filter(Img.super_hero_path==path)
	q.all()

def new_image(id, super_hero_path=None, alter_egos_path=None):
	image = get(id)
	if image is not None:
		image.super_hero_path = image.super_hero_path or super_hero_path
		image.alter_egos_path = image.alter_egos_path or alter_egos_path
		image.check_state_to_ready()
	else:
		image = Img(id=id,
			super_hero_path=super_hero_path,
			alter_egos_path=alter_egos_path,
			state=IDLE)
		db.session.add(image)
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		raise e

def get_ready_images():
	q = db.session.query(Img).filter(Img.state==READY)
	return q.all()

def state_to_finished(id):
	image = get(id)
	if image is not None:
		image.state = MERGED
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			raise e
	else:
		print('Error: No image found with id:%s ' % id)
