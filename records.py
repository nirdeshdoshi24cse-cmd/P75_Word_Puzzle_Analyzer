"""Validated CRUD for players, puzzles, and attempt results."""
from datetime import date
from uuid import uuid4
import math
from storage import Store

CATEGORIES=('Crossword','Word Search','Anagram','Cryptogram','Word Ladder','Other')
DIFFICULTIES=('Easy','Medium','Hard')

def date_value(value):
 try:
  if len(value)!=10 or date.fromisoformat(value).isoformat()!=value:raise ValueError
  d=date.fromisoformat(value)
  if d>date.today():raise ValueError
  return value
 except ValueError:raise ValueError('Date must be a valid non-future YYYY-MM-DD date') from None

def number(value,label,lo=0,hi=None,integer=False):
 try:
  val=int(value) if integer else float(value)
  if integer and str(val)!=str(value).strip():raise ValueError
  if not math.isfinite(val) or val<lo or (hi is not None and val>hi):raise ValueError
  return val
 except (ValueError,TypeError,OverflowError):raise ValueError(f'{label} must be {"an integer" if integer else "a number"} from {lo}'+(f' to {hi}' if hi is not None else '')) from None

class Records:
 def __init__(self,store=None):self.store=store or Store()
 def all(self,table):return self.store.read(table)
 def put(self,table,data,identifier=None):
  rows=self.all(table); pk={'players':'player_id','puzzles':'puzzle_id','results':'result_id'}[table]
  if identifier and not any(row[pk]==identifier for row in rows):raise ValueError('Selected record no longer exists')
  data={k:str(v).strip() for k,v in data.items()}
  if table=='players':
   if not data.get('name'):raise ValueError('Player name required')
   data['age']=str(number(data.get('age'),'Age',1,120,True))
  elif table=='puzzles':
   if not data.get('title'):raise ValueError('Puzzle title required')
   if data.get('category') not in CATEGORIES or data.get('difficulty') not in DIFFICULTIES:raise ValueError('Choose a valid category and difficulty')
  else:
   if data.get('player_id') not in [r['player_id'] for r in self.all('players')]:raise ValueError('Select an existing player')
   if data.get('puzzle_id') not in [r['puzzle_id'] for r in self.all('puzzles')]:raise ValueError('Select an existing puzzle')
   data['played_on']=date_value(data.get('played_on',''))
   data['score']=str(number(data.get('score'),'Score',0,100))
   data['time_seconds']=str(number(data.get('time_seconds'),'Time in seconds',0.01))
   if data.get('completed') not in ('Yes','No'):raise ValueError('Completed must be Yes or No')
  key=identifier or table[0].upper()+'-'+uuid4().hex[:10].upper()
  row={pk:key,**data}
  if set(row)!={pk}|set([k for k in {'players':['name','age'],'puzzles':['title','category','difficulty'],'results':['player_id','puzzle_id','played_on','score','time_seconds','completed']}[table]]):raise ValueError('Invalid record fields')
  if identifier:rows=[row if r[pk]==identifier else r for r in rows]
  else:rows.append(row)
  self.store.save(table,rows);return key
 def delete(self,table,identifier):
  pk={'players':'player_id','puzzles':'puzzle_id','results':'result_id'}[table]
  rows=self.all(table)
  if not any(row[pk]==identifier for row in rows):raise ValueError('Select a record first')
  if table in ('players','puzzles') and any(r[pk]==identifier for r in self.all('results')):raise ValueError('Delete related results first')
  self.store.save(table,[r for r in rows if r[pk]!=identifier])
 def search(self,table,query=''):
  return [r for r in self.all(table) if query.strip().casefold() in ' '.join(r.values()).casefold()]
