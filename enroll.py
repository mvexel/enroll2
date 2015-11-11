#!/usr/bin/env python

import requests
import os
import json
import time
from sys import exit
import config

def send_email(
	content,
	tos=config.email.get('tos'),
	subject=config.email.get('subject')):

	mailgun_api_key = os.environ.get('MAILGUN_API_KEY')
	if not mailgun_api_key:
		print 'please set MAILGUN_API_KEY'
		exit(1)
	return requests.post(
		"https://api.mailgun.net/v3/maproulette.org",
		auth=("api", mailgun_api_key),
		data={	"from": "Martijn <martijn@maproulette.org>",
				"to": config.email.get('tos'),
				"subject": config.email.get('subject'),
				"text": config.email.get('content')})

def get_enrollment_for_class(enrollment_dict, class_number):
	for row in enrollment_dict.get('results'):
		if row.get('class_number') == class_number:
			return int(row.get('currently_number'))
	return None
 

def get_current_enrollment(class_number):
	r = requests.get(config.enrollment_source.get('url'))
	current_enrollment = r.json()

	if not os.path.isfile(config.path.get('previous_results')):
		if os.path.exists(config.path.get('previous_results')):
			# out_file exists as a directory
			print 'there is a directory named {}. Please move it out of the way. We need a file there with that name'.format(out_file)
			exit(1)
		
	print 'writing current enrollment to {}'.format(config.path.get('previous_results'))

	with open(config.path.get('previous_results'), 'w') as fh:
		json.dump(current_enrollment, fh)

	return {'enrolled': get_enrollment_for_class(current_enrollment, class_number)}

def get_previous_enrollment(class_number):
	if not os.path.isfile(config.path.get('previous_results')):
		return {}
	last_mod_time = time.ctime(os.path.getmtime(config.path.get('previous_results')))
	previous = None
	with open(config.path.get('previous_results'), 'r') as fh:
		previous = json.load(fh)
	return {'enrolled': get_enrollment_for_class(previous, config.enrollment_source.get('class_of_interest')), 'asof': last_mod_time}

if __name__ == '__main__':
	print time.ctime()
	previous = get_previous_enrollment(config.enrollment_source.get('class_of_interest'))
	current = get_current_enrollment(config.enrollment_source.get('class_of_interest'))
	if current.get('enrolled') != previous.get('enrolled'):
		print 'enrollment changed, sending email'
		send_email(config.email.get('body_template').format(
			class_number=config.enrollment_source.get('class_of_interest'),
			previous=previous.get('enrolled'),
			current=current.get('enrolled')))
	else:
		print 'enrollment the same'