#    This is a utility to use Telegram's unlimited storage for backup. 	
#    Copyright (C) 2021  Rohit T P
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/

from datetime import datetime
from os.path import relpath
from pathlib import Path
import speedtest
import time
try :
	from utils import getNewFiles,printProgressBar
except :
	from .utils	import getNewFiles,printProgressBar

def getUploadedFiles(tg,chat_id) :	
	last_id = 0
	files = set([])
	
	while True :
		messages = tg.call_method(
			"getChatHistory",
			{
				"chat_id": chat_id,
				"offset": 0,
				"limit": 100,
				"only_local": False,
				"from_message_id": last_id
			}
		)
		
		messages.wait()
		if not messages.update or len(messages.update["messages"]) == 0 : break
		for message in messages.update["messages"] :
			if "document" in message["content"] and message["content"]["document"]["document"]["local"]["can_be_downloaded"] :
				files.add(message["content"]["document"]["document"]["local"]["path"])
			last_id = message["id"]
	
	return files

def sendFile(tg,chat_id,file_path,parent_folder="/") :
		param= {
			'chat_id': chat_id,
			'input_message_content': {
				'@type':'inputMessageDocument',
				'document': {
					'@type':'inputFileLocal',
					'path': file_path
				},
				'caption' : {
					'@type': 'formattedText', 
					'text': str(relpath(file_path,parent_folder))
				},
				'disable_content_type_detection': True
			},
			'@extra': {
				'path': file_path
			}
		}
		return tg.call_method("sendMessage",param)
		
def showResults(done,failed,errors) :
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print(f"Total files to upload {done+failed}")
	print(f"{done} files uploaded")
	print(f"{failed} files failed to upload")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
	
	if failed > 0 and input("Do you wan't to see the error log (y/N) ? : ").lower() == "y" :
		print(errors) 
	
	print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	print("Press crtl+c once you recive all files\n\n") 
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	
	return None	
		
def backup(tg,chat_id,back_up_folders):
	print("\nGetting list of uploaded files")
	old_files = getUploadedFiles(tg,chat_id)
	
	new_files = []
	print("Getting list of files to upload")
	
	for folder in back_up_folders :
		new_files.extend(getNewFiles(folder,old_files))
	
	if len(new_files) == 0 : return showResults(0,0,"")	
		
	print("Measuring internet speed")	
	total_files = len(new_files)
	net_speed = speedtest.Speedtest().upload()/8
	(done,failed,errors) = (0,0,"")
	
	printProgressBar(0,total_files, autosize = True)	
	tg.send_message(chat_id=chat_id,text=f"Backup started on {datetime.today().strftime('%Y-%m-%d %I:%M %p')}")
	tg.send_message(chat_id=chat_id,text=f"\nBacking up {total_files} files @ {net_speed/1000000} MBps.");
		
	for (new_file,folder) in new_files : 
		task = sendFile(tg,chat_id,new_file,folder)
		task.wait();
		if(task.error_info == None ) : 
			time.sleep(task.update["content"]["document"]["document"]["size"]/net_speed)   
			done += 1
		else :
			failed += 1
			errors += str(task.error_info) + "\n\n"
		printProgressBar(done+failed, total_files, prefix = 'Uploading:', suffix = 'Complete', autosize = True)
	
	tg.send_message(chat_id=chat_id, text=f"Backup ended on {datetime.today().strftime('%Y-%m-%d %I:%M %p')}");
		
	showResults(done,failed,errors)		   
	if done > 0 : tg.idle()
