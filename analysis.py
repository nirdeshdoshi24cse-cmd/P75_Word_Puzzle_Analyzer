"""Pandas / NumPy analysis: attempts (not distinct people) are counted."""
import pandas as pd
import numpy as np

def dataset(records):
 r=records.all('results');cols=['result_id','player_id','puzzle_id','played_on','score','time_seconds','completed','name','title','category','difficulty']
 if not r:return pd.DataFrame(columns=cols)
 df=pd.DataFrame(r)
 df['score']=pd.to_numeric(df['score'],errors='raise');df['time_seconds']=pd.to_numeric(df['time_seconds'],errors='raise')
 if not np.isfinite(df[['score','time_seconds']].to_numpy()).all() or (df['time_seconds']<=0).any() or (df['score']<0).any() or (df['score']>100).any():raise ValueError('Invalid numeric data in saved results')
 df['played_on']=pd.to_datetime(df['played_on'],format='%Y-%m-%d',errors='raise')
 p=pd.DataFrame(records.all('players'),columns=['player_id','name']);q=pd.DataFrame(records.all('puzzles'),columns=['puzzle_id','title','category','difficulty'])
 df=df.merge(p,on='player_id',validate='many_to_one').merge(q,on='puzzle_id',validate='many_to_one')
 if len(df)!=len(r):raise ValueError('Saved results reference missing records')
 return df

def subset(df,query='',category='All',player='All',start='',end=''):
 d=df.copy()
 if category!='All':d=d[d.category==category]
 if player!='All':d=d[d.player_id==player]
 if start:
  x=pd.to_datetime(start,format='%Y-%m-%d',errors='raise');d=d[d.played_on>=x]
 if end:
  x=pd.to_datetime(end,format='%Y-%m-%d',errors='raise');d=d[d.played_on<=x]
 if start and end and start>end:raise ValueError('From date must be on or before To date')
 if query:
  mask=d[['name','title','category','difficulty','completed']].astype(str).apply(lambda s:s.str.contains(query,case=False,regex=False)).any(axis=1)
  d=d[mask]
 return d

def summary(df):
 if df.empty:return {'attempts':0,'average_score':0,'average_time_seconds':0,'completion_rate_pct':0}
 return {'attempts':len(df),'average_score':round(float(df.score.mean()),2),'average_time_seconds':round(float(df.time_seconds.mean()),2),'completion_rate_pct':round(float(df.completed.eq('Yes').mean()*100),2)}

def group_summary(df,column):
 if df.empty:return pd.DataFrame(columns=[column,'attempts','avg_score','avg_time_seconds','completion_pct'])
 g=df.groupby(column,as_index=False).agg(attempts=('score','size'),avg_score=('score','mean'),avg_time_seconds=('time_seconds','mean'),completion_pct=('completed',lambda x:100*x.eq('Yes').mean()))
 return g.round(2).sort_values('avg_time_seconds',ascending=False)

def patterns(df):
 if df.empty:return 'No matching attempts.'
 categories=group_summary(df,'category');players=group_summary(df,'name')
 hard=categories.iloc[0];best=players.sort_values('avg_score',ascending=False).iloc[0]
 return (f"Longest average completion time: {hard['category']} ({hard['avg_time_seconds']:.1f} seconds).\n"
         f"Highest average player score: {best['name']} ({best['avg_score']:.1f}/100).\n"
         'Longer times can indicate challenge, but also reflect player experience, puzzle difficulty and sample size.\n'
         'Completion rate is based on the Completed field, not time limits.')
