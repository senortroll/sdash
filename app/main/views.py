from flask import render_template
from . import main
import requests


@main.route('/checks')
def checks():
	response = requests.get('http://ops-sensu01.aws.csdops.net:4567/checks')

	assert response.status_code == 200

	return render_template('checks.html', checks=response.json())

@main.route('/events')
def events():
	response = requests.get('http://ops-sensu01.aws.csdops.net:4567/events')

	assert response.status_code == 200

	return render_template('events.html', events = response.json())

@main.route('/servers')
def servers():
	response = requests.get('http://ops-sensu01.aws.csdops.net:4567/clients')

	assert response.status_code == 200

	return render_template('servers.html', servers = response.json())