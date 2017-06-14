# line-stickerweb
A website for downloading Line stickers. It takes a store ID sent to the server, downloads the page, and finds the relevant image links. Then, it downloads the images and sends them all back to the user in a .zip archive.

## How do I use it?
Run it yourself, with `main.py`.
Open `http://localhost/line/<page id>`

## Dependencies

This page uses a few modules to make my life easier. Run `pip install` if you don't have them.

* `bs4` for parsing the HTML of the sticker page.
* `cssutils` for getting the url of the sticker image.
* `flask` for running the server
* `requests` for making web requests
