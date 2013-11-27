#!/usr/bin/python

import csv, email, imaplib, subprocess

magnetURLs = []

user = 'ab.rasp.pi'
pwd = 'raspberrypi'

m = imaplib.IMAP4_SSL("imap.gmail.com")
print 'Logging into Gmail'
m.login(user,pwd)
m.select('[Gmail]/All Mail')

resp, items = m.search(None, "(UNSEEN)")
items = items[0].split()
if len(items) > 0:
	for emailid in items:
		print 'New email found...fetching'
		resp, data = m.fetch(emailid, "(RFC822)")
		message = email.message_from_string(data[0][1])
		messageParts = message.get_payload()
		for part in messageParts:
			if part.is_multipart() == False and part.get_content_maintype() == 'text':
				url = part.get_payload().replace('\r\n','')
				if url[:6] == 'magnet':
					print 'Magnet link found!'
					magnetURLs.append(url)

	for link in magnetURLs:
		print 'Adding link: ' + link
		subprocess.call(['transmission-remote','-a',link])
else:
	print 'No new emails.'

currTors = str(subprocess.call(['transmission-remote','-l']))
print currTors.strip().split('\t')


