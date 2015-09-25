from flask import render_template
from flask_table import Table, Col
from . import main
import requests

class EventTable(Table):
	host = Col('Host')
	check = Col('Check')
	allow_sort = True

	def sort_url(self, col_key, reverse=False):
		if reverse:
			direction = 'desc'
		else:
			direction = 'asc'
		return url_for(main.events, direction=direction)

class EventItem(object):
	def __init__(self, host, check):
		self.host = host
		self.check = check

class CheckTable(Table):
	name = Col('Name')
	command = Col('Command')

class CheckItem(object):
	def __init__(self, name, command):
		self.name = name
		self.command = command

@main.route('/checks')
def checks():
	response = requests.get('http://ops-sensu01.aws.csdops.net:4567/checks')

	assert response.status_code == 200
	checks = []

	for check in response.json():
		checks.append(CheckItem(check['name'],check['command']))

	check_table = CheckTable(checks)
	return render_template('checks.html', checks = check_table)

@main.route('/events')
def events():
	response = requests.get('http://ops-sensu01.aws.csdops.net:4567/events')
	events = []

	assert response.status_code == 200

	for event in response.json():
		events.append(EventItem(event['client']['name'],event['check']['name']))

	event_table = EventTable(events)
	return render_template('events.html', events = event_table)

@main.route('/servers')
def servers():
	response = requests.get('http://ops-sensu01.aws.csdops.net:4567/clients')

	assert response.status_code == 200

	return render_template('servers.html', servers = response.json())