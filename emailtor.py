#!/usr/bin/python

import getpass, email, imaplib, subprocess, transmissionrpc

magnetURLs = []

user = 'ab.rasp.pi'

ip = '192.168.1.105'
port = 9091

mediaDirectory = '/home/pi/media/'

m = imaplib.IMAP4_SSL("imap.gmail.com")
print 'Logging into Gmail'
m.login(user,getpass.getpass())
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
else:
	print 'No new emails.'

tc = transmissionrpc.Client(ip,port=port)
if len(magnetURLs) > 0:
    for url in magnetURLs:
        tc = transmissionrpc.Client(ip,port=port)
        torrent = tc.add_torrent(url,timeout=None)
        print 'Added torrent: '+ torrent.name

currTorrents = tc.get_torrents()

for torrent in currTorrents:
    if torrent.percentDone >= 1:
        print 'Torrent: ' + torrent.name + ' completed.  Moving to ' + mediaDirectory + ' and removing from list.'
        torrent.move_data(mediaDirectory, timeout=None)
        tc.remove_torrent(torrent.id,delete_data=False,timeout=None)

