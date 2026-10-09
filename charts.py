"""Charts for Tkinter or exporting figures."""
from matplotlib.figure import Figure
from analysis import group_summary

def category_chart(df):
 d=group_summary(df,'category')
 if d.empty:raise ValueError('No results to chart')
 fig=Figure(figsize=(8.5,5),dpi=110,layout='constrained');ax=fig.add_subplot()
 ax.bar(d.category,d.avg_time_seconds,color='#4f86c6')
 ax.set(title='Average Puzzle Completion Time by Category',ylabel='Average time (seconds)',xlabel='Puzzle category');ax.tick_params(axis='x',rotation=20);ax.grid(axis='y',alpha=.25)
 return fig

def player_chart(df):
 d=group_summary(df,'name')
 if d.empty:raise ValueError('No results to chart')
 fig=Figure(figsize=(8.5,5),dpi=110,layout='constrained');ax=fig.add_subplot()
 ax.bar(d.name,d.avg_score,color='#219b81');ax.set(title='Average Score by Player',ylabel='Average score / 100',xlabel='Player',ylim=(0,105));ax.tick_params(axis='x',rotation=15);ax.grid(axis='y',alpha=.25)
 return fig
