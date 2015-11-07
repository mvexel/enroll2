previous_results_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'previous.json')
class_of_interest = 17574
tos = ['jessen.kelly@utah.edu', 'm@rtijn.org']
subject = 'enrollment update for {}'.format(class_of_interest)
body_template = 'Your enrollment has changed for class {class_number}. It was {previous} and now it is {current}!'
