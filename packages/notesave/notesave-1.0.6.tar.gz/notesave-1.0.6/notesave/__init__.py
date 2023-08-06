import datetime
from os import listdir,mkdir
from os.path import isfile, join
import requests
import argparse


class NoteSaver:
  
  def save_note_local(self,title,content):
    try:
      mkdir('notes')
    except FileExistsError:
      pass
    with open(f'notes/{title}','w') as f:
      f.write(content)
  
  def save_note_online(self,title,content):
    url = 'https://pastebin.com/api/api_post.php'
    dev_key = '' #if you want to save notes on pastebin put your key here
    data = {
      'api_dev_key':dev_key,
      'api_option':'paste',
      'api_paste_code':content,
      'api_paste_name':title,}
    x = requests.post(url=url,data=data)
    return x.text

  def fetch_all_notes(self):
    files = [f for f in listdir('notes') if 
    isfile(join('notes',f))]
    return files
  
  def open_note(self,title):
    with open(f'notes/{title}','r') as f:
      return f.read()
  def current_date(self):
    current_time = datetime.datetime.now()
    return current_time.strftime('%Y-%m-%d-%H:%M:%S')
  
  def get_multiline_input(self):
    lines = []
    while True:
      line = input()
      if line:
        lines.append(line)
      else:
        break
    return '\n'.join(lines)

  def gen_id_notes(self,notes,log=True):
    self.ns = {}
    count = 1
    for i in notes:
      self.ns[count] = i
      if log:
        print(count,i.split('--')[1])
      count += 1
  
  def main(self):
    while True:
      op = input('Hello, welcome to the notesaver! Type 1 to view all the notes that you have. Type 2 to create a new one')
      if op == '1':
        notes = self.fetch_all_notes()
        print("Here's your notes")
        self.gen_id_notes(notes)
        id = input('Type the ID of the notes')
        print(self.open_note(self.ns[int(id)]))
      else:
        title = input('Title:')
        print('Contents:')
        note = self.get_multiline_input()
        self.save_note_local(f'{self.current_date()}--{title}',note)
        link = self.save_note_online(title,note)
        print('Your note can be found at '+link)
    
  def cli(self):
    parser = argparse.ArgumentParser(description='Note Saver')
    parser.add_argument('command',help='Command: l,r,c')
    args = parser.parse_args()
    if args.command =='l':
      notes = self.fetch_all_notes()
      if len(notes) == 0:
        print('No notes')
      else:
        print('Notes')
        self.gen_id_notes(notes)
    elif args.command == 'r':
      self.gen_id_notes(self.fetch_all_notes(),log=False)
      id = input('Note ID')
      try:
        print('\nContents:\n')
        print(self.open_note(self.ns[int(id)]))
      except KeyError:
        print('Error')
    elif args.command =='c':
      title = input('Title:')
      print('Content')
      content = self.get_multiline_input()
      self.save_note_local(f'{self.current_date()}--{title}',content)
      link = self.save_note_online(title,content)
      print('Access note online at:',link)
    else:
      print('Invalid')