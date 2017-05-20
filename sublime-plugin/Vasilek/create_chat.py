import sublime, sublime_plugin
import urllib, urllib.parse
import webbrowser

HOST = "http://127.0.0.1:5000"
TYPES = {'py': "Python",
		 'cpp': "C++",
		 'html': "Html"}

def create_chat(name):
	global window, code, code_type
	#data = urllib.parse.urlencode({'login': 'sublime-bot'}).encode()
	#req = urllib.request.Request('http://127.0.0.1:5000/', data)
	#f = urllib.request.urlopen(req)
	#cookie = f.headers['Set-Cookie'][:f.headers['Set-Cookie'].find(';')]
	#print(cookie)
	#print(f.read())
	data = urllib.parse.urlencode({'code': code,
								   'code_type': code_type,
								   'name': name}).encode()
	req = urllib.request.Request(HOST + '/api/create_chat', data)
	f = urllib.request.urlopen(req)
	chat = HOST + f.read().decode()
	#print(chat)
	webbrowser.open_new_tab(chat)

class CreateChatCommand(sublime_plugin.WindowCommand):
	def run(self):
		view = self.window.active_view()
		if view is None:
			self.window.status_message("No active view found")
			return
		file_name = view.file_name()
		if file_name is None:
			self.window.status_message("Save your file before sending code")
			return
		global window, code, code_type
		window = self.window
		with open(file_name, "r") as f:
			code = f.read()
		ext = file_name.split('.')[-1]
		if ext in TYPES:
			code_type = TYPES[ext]
		else:
			code_type = "Unknown"
		self.window.show_input_panel("Enter chat name", "", on_done=create_chat, \
							on_cancel=None, on_change = None)
