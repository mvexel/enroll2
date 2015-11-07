#!/usr/bin/env python

import requests
import os
import json
import time
from sys import exit

previous_results_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'previous.json')
class_of_interest = 17574
tos = ['jessen.kelly@utah.edu', 'm@rtijn.org']
subject = 'enrollment update for {}'.format(class_of_interest)
body_template = 'Your enrollment has changed for class {class_number}. It was {previous} and now it is {current}!'

def send_email(content, tos=tos, subject=subject):

	mailgun_api_key = os.environ.get('MAILGUN_API_KEY')
	if not mailgun_api_key:
		print 'please set MAILGUN_API_KEY'
		exit(1)
	return requests.post(
		"https://api.mailgun.net/v3/maproulette.org/messages",
		auth=("api", mailgun_api_key),
		data={	"from": "Martijn <martijn@maproulette.org>",
				"to": tos,
				"subject": subject,
				"text": content})

def get_enrollment_for_class(enrollment_dict, class_number):
	for row in enrollment_dict['results']:
		if row['class_number'] == class_number:
			return int(row.get('currently_number'))
	return None
 

def get_current_enrollment(class_number):
	api_url = "https://api.import.io/store/data/560aab2b-2e32-4fee-92da-c362f4f6b2e7/_query?input/webpage/url=https%3A%2F%2Fstudent.apps.utah.edu%2Fuofu%2Fstu%2FClassSchedules%2Fmain%2F1164%2Fseating_availability.html%3Fsubject%3DARTH&_user=f1b8969f-164a-4b8a-8b84-6b5a4a2effe5&_apikey=f1b8969f164a4b8a8b846b5a4a2effe5eded0a4c7992bf34467145454e4cf22edc902dba420eac8f824572546157855b1df614bf3c41819567a4fc9cdcca5d7ed3077b6d658a3c744fadebd13d586de2&class_number="

	r = requests.get(api_url)
	current_enrollment = r.json()

	if not os.path.isfile(previous_results_file):
		if os.path.exists(previous_results_file):
			# out_file exists as a directory
			print 'there is a directory named {}. Please move it out of the way. We need a file there with that name'.format(out_file)
			exit(1)
		
	print 'writing current enrollment to {}'.format(previous_results_file)

	with open(previous_results_file, 'w') as fh:
		json.dump(current_enrollment, fh)

	return {'enrolled': get_enrollment_for_class(current_enrollment, class_number)}

def get_previous_enrollment(class_number):
	if not os.path.isfile(previous_results_file):
		return {}
	last_mod_time = time.ctime(os.path.getmtime(previous_results_file))
	previous = None
	with open(previous_results_file, 'r') as fh:
		previous = json.load(fh)
	return {'enrolled': get_enrollment_for_class(previous, class_of_interest), 'asof': last_mod_time}

if __name__ == '__main__':
	print time.ctime()
	previous = get_previous_enrollment(class_of_interest)
	current = get_current_enrollment(class_of_interest)
	if current.get('enrolled') != previous.get('enrolled'):
		print 'enrollment changed, sending email'
		send_email(body_template.format(
			class_number=class_of_interest,
			previous=previous.get('enrolled'),
			current=current.get('enrolled')))
	else:
		print 'enrollment the same'