"""Populate empty files with reproducible fictional players and attempt data."""
from datetime import date
from records import Records

def seed(records=None):
 r=records or Records()
 if any(r.all(t) for t in ('players','puzzles','results')):return False
 players=[('Aarav',19),('Meera',20),('Kabir',21),('Riya',19)]
 pids=[r.put('players',{'name':name,'age':age}) for name,age in players]
 puzzle_rows=[('Daily Grid','Crossword','Hard'),('Hidden Words','Word Search','Easy'),('Letter Shuffle','Anagram','Medium'),('Secret Quote','Cryptogram','Hard')]
 qids=[r.put('puzzles',{'title':title,'category':category,'difficulty':diff}) for title,category,diff in puzzle_rows]
 # Same category attempted by each player; scores out of 100, times in seconds.
 base=[(77,560),(88,230),(81,340),(64,710)]
 for i,pid in enumerate(pids):
  for j,qid in enumerate(qids):
   score=max(0,min(100,base[j][0]+[6,-3,1,-5][i]));seconds=base[j][1]+[20,60,-25,45][i]
   r.put('results',{'player_id':pid,'puzzle_id':qid,'played_on':f'2026-09-{10+i*2+j:02d}','score':score,'time_seconds':seconds,'completed':'No' if (i+j)%7==0 else 'Yes'})
 return True

if __name__=='__main__':print('Demo records created' if seed() else 'Existing records retained; no changes made')
