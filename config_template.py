import os

path = {
	'previous_results': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'previous.json')
}

email = {
	'tos': [], # list of email addresses
	'subject': 'enrollment update for {}'.format(class_of_interest),
	'body_template', 'Your enrollment has changed for class {class_number}. It was {previous} and now it is {current}!'
}

enrollment_source = {
	'url': '', # user import.io to create an api based on a class schedule web page
	'class_of_interest': 17574
}