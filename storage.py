"""Simple CSV persistence; single user, no concurrent edits."""
import csv
import os
import tempfile
from pathlib import Path

SCHEMA = {
 'players':['player_id','name','age'],
 'puzzles':['puzzle_id','title','category','difficulty'],
 'results':['result_id','player_id','puzzle_id','played_on','score','time_seconds','completed']
}
class Store:
 def __init__(self,path=None):
  self.path=Path(path) if path else Path(__file__).resolve().parent/'data'
  self.path.mkdir(parents=True,exist_ok=True)
 def read(self,table):
  file=self.path/f'{table}.csv'
  if not file.exists():return []
  with file.open(encoding='utf-8',newline='') as f:
   reader=csv.DictReader(f)
   if reader.fieldnames!=SCHEMA[table]:raise ValueError(f'Invalid header in {file.name}')
   rows=list(reader)
   if any(None in row or None in row.values() for row in rows):raise ValueError(f'Malformed row in {file.name}')
   return rows
 def save(self,table,rows):
  tmp=None
  try:
   with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',newline='',dir=self.path,delete=False) as f:
    tmp=f.name; writer=csv.DictWriter(f,fieldnames=SCHEMA[table]);writer.writeheader();writer.writerows(rows)
   os.replace(tmp,self.path/f'{table}.csv')
  finally:
   if tmp and os.path.exists(tmp):os.unlink(tmp)
