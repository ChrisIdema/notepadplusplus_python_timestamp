from Npp import editor, notepad, NOTIFICATION
import time
import os

def add_now_to_new():
	"""add current timestamp to newly created empty document (same as creation timestamp)"""
	# Only act on new/untitled empty documents
	#print("add_creation_timestamp")
	filename = notepad.getCurrentFilename()
	if (filename.startswith("new ") or filename == "") and editor.getLength() == 0:
		timestamp = time.strftime("%Y-%m-%d_%H%M%S")  # e.g. 2011-12-13_141516        
		editor.addText(timestamp + "\n")
		
# Register the callback so it runs every time a new buffer (tab) is activated
notepad.callback(add_now_to_new, [NOTIFICATION.BUFFERACTIVATED])

def add_now():
	"""insert now timestamp"""
	timestamp = time.strftime("%Y-%m-%d_%H%M%S")  # e.g. 2011-12-13_141516    
	editor.addText(timestamp)
	   
def add_creation():  
	"""add creation timestamp of current unsaved document to top of document"""
	# if saved file_name is an absolute path, else it's 'new \d+'
	file_name = notepad.getCurrentFilename() 
	if (file_name.startswith("new ")): # 'new \d+'

		session_xml_path = os.path.join(os.getenv('APPDATA'), 'Notepad++', 'session.xml')         
		if not os.path.exists(session_xml_path):
			notepad.messageBox("session.xml not found:\n" + session_xml_path, "Error", 0)
			return False
		
		timestamp = ''
		with open(session_xml_path,'r') as f:
			for line in f.readlines():
				loc = line.find(f"backup\\{file_name}@")
				if loc >= 0:
					timestamp = line[loc:].split('@')[1].split('"')[0]
					break     

		if len(timestamp) == 0:
			notepad.messageBox(f"date not found for {file_name}", "Error", 0)
			return False
		else:       
			content = editor.getText()

			# check if timestamp is already at top of file 
			if content.startswith(timestamp):
				print(f'file "{file_name}" already has timestamp {timestamp}')
				return False
			else:
				print(f'file "{file_name}" would have gotten timestamp {timestamp}')
				#editor.insertText(0, timestamp + "\n")
				return True     
	return False 


def add_creation_to_all():
	session_xml_path = os.path.join(os.getenv('APPDATA'), 'Notepad++', 'session.xml')       
	if not os.path.exists(session_xml_path):
		notepad.messageBox("session.xml not found:\n" + session_xml_path, "Error", 0)
		return False

	open_files = notepad.getFiles()
	updated = 0
	skipped = 0
	total = len(open_files)

	current_open_file = notepad.getCurrentFilename()
	
	for file in open_files:
		path = file[0]
		notepad.activateFile(path) # switch to this tab
		if add_creation():
			updated += 1
		else:
			skipped += 1
	
	notepad.activateFile(current_open_file) # go back file that was open
	
	notepad.messageBox(
		"Batch processing finished!\n\n"
		"Total tabs processed: {}\n"
		"Timestamps added: {}\n"
		"Skipped (already had timestamp or no backup): {}".format(total, updated, skipped),
		"Batch Retroactive Timestamp",
		0
	)
