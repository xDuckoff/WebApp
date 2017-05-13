import sublime, sublime_plugin
import urllib, urllib.parse

def create_chat(name):
	global window, code
	data = urllib.parse.urlencode({'login': 'sublime-bot'}).encode()
	req = urllib.request.Request('http://127.0.0.1:5000/', data)
	f = urllib.request.urlopen(req)
	cookie = f.headers['Set-Cookie'][:f.headers['Set-Cookie'].find(';')]
	print(cookie)
	print(f.read())
	data = urllib.parse.urlencode({'code': code,
								   'codetype':"Python",
								   'name': name}).encode()
	req = urllib.request.Request('http://127.0.0.1:5000/create_chat', data, {"Cookie":cookie})
	f = urllib.request.urlopen(req)
	print(f.read())

class ExampleCommand(sublime_plugin.WindowCommand):
	def run(self):
		view = self.window.active_view()
		if view is None:
			self.window.status_message("No active view found")
			return
		file_name = view.file_name()
		if file_name is None:
			self.window.status_message("Save your file before sending code")
			return
		global window, code
		window = self.window
		with open(file_name, "r") as f:
			code = f.read()
		create_chat('kek')
		#self.window.show_input_panel("Enter chat name", "", on_done=create_chat, \
							#on_cancel=None, on_change = None)
