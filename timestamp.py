from Npp import editor, notepad, NOTIFICATION
import time
import os

def add_now_to_new(args=None):
	"""add current timestamp to newly created empty document (same as creation timestamp)"""

	file_name = notepad.getCurrentFilename()
	# if saved file_name is an absolute path and won't start with "new ", else it's 'new \d+'
	if (file_name.startswith("new ") or file_name == "") and editor.getLength() == 0:
		timestamp = time.strftime("%Y-%m-%d_%H%M%S")  # e.g. 2011-12-13_141516        
		editor.addText(timestamp + "\n")
		
# Register the callback so it runs every time a new buffer (tab) is activated
notepad.callback(add_now_to_new, [NOTIFICATION.BUFFERACTIVATED])


def add_now():
	"""insert now timestamp at current cursor location"""
	timestamp = time.strftime("%Y-%m-%d_%H%M%S")  # e.g. 2011-12-13_141516    
	editor.addText(timestamp)
	   
def add_creation():  
	"""add creation timestamp of current unsaved non-empty document to top of document"""
	
	file_name = notepad.getCurrentFilename()	

	if editor.getLength() == 0:
		print("won't add creation date to empty file, that's what add_now_to_new() is used for")
		return False
	
	# if saved file_name is an absolute path and won't start with "new ", else it's 'new \d+'
	if not (file_name.startswith("new ") or file_name == ""):
		print("won't add creation date to saved file as notepad++ doesn't track that and file dates are not reliable")
		return False
		
	# first look in backup dir:
	backup_dir = os.path.join(os.getenv('APPDATA'), 'Notepad++', 'backup')        
	if not os.path.exists(backup_dir):
		notepad.messageBox("Backup folder not found:\n" + backup_dir, "Error", 0)
		return False
	
	# loop through backup folder for file candidates
	candidates = []
	for f in os.scandir(backup_dir):
		if f.is_file():                
			backup_full_name = os.path.split(f)[1]                
			backup_base_name = backup_full_name.split('@')[0]
			backup_timestamp = backup_full_name.split('@')[1]
			
			if backup_base_name == file_name:
				candidates.append({'path': f.path, 'timestamp': backup_timestamp}) 

	timestamp = ''
	if len(candidates) == 0:
		notepad.messageBox(f"date not found for {file_name}", "Error", 0)
		return False
	elif len(candidates) == 1:
		timestamp = candidates[0]["timestamp"]
	else:
		print("multiple candidates, checking session.xml...")	
		session_xml_path = os.path.join(os.getenv('APPDATA'), 'Notepad++', 'session.xml')         
		if not os.path.exists(session_xml_path):
			notepad.messageBox("session.xml not found:\n" + session_xml_path, "Error", 0)
			return False
				
		with open(session_xml_path,'r') as f:
			for line in f.readlines():
				loc = line.find(f"backup\\{file_name}@")
				if loc >= 0:
					timestamp = line[loc:].split('@')[1].split('"')[0]
					break     

	if len(timestamp) == 0:
		notepad.messageBox(f"date not found for {file_name}", "Error", 0)
		return False

	content = editor.getText()

	# check if timestamp is already at top of file 
	if content.startswith(timestamp):
		print(f'file "{file_name}" already has timestamp {timestamp}')
		return False
	else:
		editor.insertText(0, timestamp + "\n")
		return True     


def add_creation_to_all():
	"""call add_creation() on all open files"""
	session_xml_path = os.path.join(os.getenv('APPDATA'), 'Notepad++', 'session.xml')       
	if not os.path.exists(session_xml_path):
		notepad.messageBox("session.xml not found:\n" + session_xml_path, "Error", 0)
		return False
	
	backup_dir = os.path.join(os.getenv('APPDATA'), 'Notepad++', 'backup')        
	if not os.path.exists(backup_dir):
		notepad.messageBox("Backup folder not found:\n" + backup_dir, "Error", 0)
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
	
	notepad.activateFile(current_open_file) # switch to tab that was open initially
	
	notepad.messageBox(
		"Batch processing finished!\n\n"
		"Total tabs processed: {}\n"
		"Timestamps added: {}\n"
		"Skipped (already had timestamp or no backup): {}".format(total, updated, skipped),
		"Batch Retroactive Timestamp",
		0
	)
