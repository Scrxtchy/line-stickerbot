from flask import Flask, request, redirect, abort, send_file
import re
import json
import logging
import shutil
import urllib.request
import urllib.parse
import requests
import cssutils
import tempfile
from bs4 import BeautifulSoup
#from wand.image import Image
from zipfile import ZipFile
#from OpenSSL import SSL
import os


regex = re.compile(r'v1\/sticker\/(\d+)\/\w+\/sticker\.(.+)')
cssutils.log.setLevel(logging.CRITICAL)


app = Flask(__name__)

@app.route("/line/<int:stickerId>", methods=['GET'])
def getStickers(stickerId):
	stickerId = str(stickerId)
	print('request ' + stickerId)
	stickerUrl = "https://store.line.me/stickershop/product/" + stickerId
	request = requests.get(stickerUrl).text
	stickerpage = BeautifulSoup(request, "html.parser")
	stickertitle = stickerpage.title.string
	if os.path.isfile(stickerId + ".zip") == False:
		with tempfile.TemporaryDirectory() as tmpdirname:
			send_stickers(stickerpage, stickerId, tmpdirname)
	return send_file(stickerId + '.zip', mimetype='application/zip', as_attachment=True, attachment_filename=stickertitle + '.zip')


def send_stickers(page, sid, tmpdirname):
	dl_stickers(page, tmpdirname)
	
	with ZipFile(sid + '.zip', 'w') as stickerzip:
		for root, dirs, files in os.walk(tmpdirname + '/'):
			for file in files:
				stickerzip.write(os.path.join(root, file), file)
				os.remove(os.path.join(root, file))


def dl_stickers(page, tmpdirname):
	images = page.find_all('span', attrs={"style": not ""})
	for i in images:
		imageurl = i['style']
		imageurl = cssutils.parseStyle(imageurl)
		imageurl = imageurl['background-image']
		imageurl = imageurl.replace('url(', '').replace(')', '')
		imageurl = imageurl[1:-15]
		match = regex.search(imageurl)
		response = requests.get(imageurl.replace("sticker.png", "sticker_popup.png"), stream=True)
		filen = match.group(1) + '.' + match.group(2)
		with open(tmpdirname +'/' + filen, "wb") as file:
			shutil.copyfileobj(response.raw, file)

		response = requests.get(imageurl, stream=True)
		filen = 'thumb-' + filen
		with open(tmpdirname +'/' + filen, "wb") as file:
			shutil.copyfileobj(response.raw, file)

		#resize_sticker(response, imageurl)
"""
def resize_sticker(image, filename):
	filen = filename[-7:]
	with Image(file=image) as img:
		ratio = 1
		if img.width > img.height:
			ratio = 512.0/img.width
		else:
			ratio = 512.0/img.height
		img.resize(int(img.width*ratio), int(img.height*ratio), 'mitchell')
		img.save(filename=("downloads/" + filen))
"""
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000)
