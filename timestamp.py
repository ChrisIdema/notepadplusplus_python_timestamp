from Npp import editor, notepad, NOTIFICATION
import time
import os

def add_now(args):
    # Only act on new/untitled empty documents
    print("add_creation_timestamp")
    filename = notepad.getCurrentFilename()
    if (filename.startswith("new ") or filename == "") and editor.getLength() == 0:
        # Change the format here if you want something different
        timestamp = time.strftime("%Y-%m-%d_%H%M%S")  # e.g. 2026-06-02_181530        
        editor.addText(timestamp + "\n")
        
# Register the callback so it runs every time a new buffer (tab) is activated
notepad.callback(add_now, [NOTIFICATION.BUFFERACTIVATED])


       
def add_creation():  
    file_name = notepad.getCurrentFilename()
    #print(file_name)
    if (file_name.startswith("new ")):

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
                backup_timettamp = backup_full_name.split('@')[1]
                
                if backup_base_name == file_name:
                   candidates.append({'path': f.path, 'timestamp': backup_timettamp}) 
               

        if len(candidates) == 0:
            notepad.messageBox("file not found in backup folder", "Error", 0)
            return False
        elif len(candidates) > 1:
            candidates_string = "\n".join([c["path"] for c in candidates])
            notepad.messageBox(candidates_string, "Error", 0)
            return False 
        else:
            editor.insertText(0, candidates[0]["timestamp"] + "\n")
            return True 
    
    return False 


def run_on_all_open_files():
    backup_dir = os.path.join(os.getenv('APPDATA'), 'Notepad++', 'backup')
    if not os.path.exists(backup_dir):
        notepad.messageBox("Backup folder not found:\n" + backup_dir, "Error", 0)
        return False

    open_files = notepad.getFiles()
    updated = 0
    skipped = 0
    total = len(open_files)
    
    for file in open_files:
        path = file[0]
        notepad.activateFile(path)          # switch to this tab
        if add_creation():
            updated += 1
        else:
            skipped += 1
    
    notepad.messageBox(
        "Batch processing finished!\n\n"
        "Total tabs processed: {}\n"
        "Timestamps added: {}\n"
        "Skipped (already had timestamp or no backup): {}".format(total, updated, skipped),
        "Batch Retroactive Timestamp",
        0
    )
