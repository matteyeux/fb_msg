#!/usr/bin/python
import sys
import os
from bs4 import BeautifulSoup

def init_bs(in_file):
	file = open(in_file, 'rb')
	soup = BeautifulSoup(file, 'html.parser')
	return soup

def messages_info(htmlfile, print_out=0):
	msginfo = init_bs(htmlfile)
	messages = ''
	messages = msginfo.findAll('p')
	convo_name = msginfo.title.text.encode('utf-8')
	msg = 0
	if print_out == 1:
		print(convo_name)
	for i in range(0, len(messages)):
		msg += 1
		out = messages[i]
		out = out.text.encode('utf-8')
		if out == "":
			msg -= 1
		# if print_out == 1 and out != '\x00' :
		# 	print(out)
	if print_out == 1:
		print("found %d messages in %s" % (msg, convo_name))
	return msg

# add "/" at the end of the path - too lazy to fix
def total_messages(msg_dir, print_out=0):
	total = 0
	for files in os.listdir(msg_dir):
		if files.endswith(".html"):
			files = msg_dir + files
			msg_number = messages_info(files, 0)
			total += msg_number
			if print_out == 1:
				print("Total messages : %s" % total)
	return total

def event_info(event_file, print_out=0):
	event = init_bs(event_file)
	info_event = event.findAll('p')
	event_nb = 0
	for i in range(0, len(info_event)):
		if print_out == 1:
			print(info_event[i].text)
		event_nb += 1
	if print_out:
		print(event_nb)
	return event_nb

# I assume you facebook_data_dir 
# is the root of the folder you unziped
def all(facebook_data_dir):
	msg_dir = facebook_data_dir + "/messages/"
	event_dir = facebook_data_dir + "/html/events.htm"
	# this part may take a while 
	# if you have a lot a of messages per conversation
	print("Looking for messages...")
	print("Total messages : %d" % total_messages(msg_dir))
	print("Total events : %d" % event_info(event_dir))

def usage(toolname):
	print("usage : %s [file]" % toolname)
	print(" -a [dir]\tall stats")
	print(" -c [dir]\tmessages count")
	print(" -m [file]\tmessage info")
	print(" -e [file]\tevent info")

if __name__ == '__main__':
	argc = len(sys.argv)
	argv = sys.argv

	if argc < 2:
		usage(argv[0])
		sys.exit(1)

	for i in range(0, argc):
		if argv[i] == "-c":
			directory = argv[i + 1]
			total_messages(directory, 1)

		elif argv[i] == "-m" :
			msg_file = argv[i + 1]
			messages_info(msg_file, 1)

		elif argv[i] == "-e" :
			event_info(argv[i + 1])

		elif argv[i] == "-a":
			all(argv[i + 1])
		elif argv[i] == "-h":
			usage(argv[0])
			exit(0)
