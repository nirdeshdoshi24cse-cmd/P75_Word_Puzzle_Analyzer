"""Run this desktop app: python main.py"""
import tkinter as tk
from tkinter import ttk,messagebox,filedialog
from datetime import date
from records import Records,CATEGORIES,DIFFICULTIES
from analysis import dataset,subset,summary,group_summary,patterns
from charts import category_chart,player_chart

FIELDS={'players':['name','age'],'puzzles':['title','category','difficulty'],'results':['player_id','puzzle_id','played_on','score','time_seconds','completed']}
PK={'players':'player_id','puzzles':'puzzle_id','results':'result_id'}

class App:
 def __init__(self,root):
  self.root=root;self.records=Records();self.selected={x:None for x in FIELDS};self.vars={};self.trees={}
  root.title('P75 Word Puzzle Performance Analyzer - Nirdesh Doshi');root.geometry('1180x740')
  ttk.Label(root,text='WORD PUZZLE PERFORMANCE ANALYZER',font=('Arial',21,'bold')).pack(anchor='w',padx=15,pady=10)
  ttk.Label(root,text='IU2441230468  |  DOSHI NIRDESH JIGESHKUMAR  |  P75').pack(anchor='w',padx=15)
  self.tabs=ttk.Notebook(root);self.tabs.pack(fill='both',expand=True,padx=12,pady=10)
  for table in FIELDS:self.build_tab(table)
  self.build_analysis();self.refresh()
 def build_tab(self,table):
  tab=ttk.Frame(self.tabs);self.tabs.add(tab,text=table.title());form=ttk.LabelFrame(tab,text='Record details');form.pack(fill='x',padx=8,pady=7)
  self.vars[table]={};self.inputs=getattr(self,'inputs',{});self.inputs[table]={}
  for i,field in enumerate(FIELDS[table]):
   cell=ttk.Frame(form);cell.grid(row=i//3,column=i%3,padx=9,pady=6,sticky='ew');form.columnconfigure(i%3,weight=1)
   ttk.Label(cell,text=field.replace('_',' ').title()).pack(anchor='w');v=tk.StringVar();self.vars[table][field]=v
   if field in ('category','difficulty','completed','player_id','puzzle_id'):
    w=ttk.Combobox(cell,textvariable=v,state='readonly',width=29)
    if field=='category':w['values']=CATEGORIES
    if field=='difficulty':w['values']=DIFFICULTIES
    if field=='completed':w['values']=['Yes','No']
   else:w=ttk.Entry(cell,textvariable=v,width=32)
   w.pack(fill='x');self.inputs[table][field]=w
  if table=='results':
   self.vars[table]['played_on'].set(date.today().isoformat());self.vars[table]['completed'].set('Yes')
  actions=ttk.Frame(tab);actions.pack(fill='x',padx=8)
  for label,method in [('Add',lambda t=table:self.save(t)),('Update selected',lambda t=table:self.save(t,True)),('Delete selected',lambda t=table:self.delete(t)),('Clear form',lambda t=table:self.clear(t))]:ttk.Button(actions,text=label,command=method).pack(side='left',padx=3)
  searchbox=ttk.Frame(tab);searchbox.pack(fill='x',padx=8,pady=8)
  ttk.Label(searchbox,text='Search all record fields:').pack(side='left');query=tk.StringVar();self.vars[table]['_search']=query
  ttk.Entry(searchbox,textvariable=query,width=35).pack(side='left',padx=7);ttk.Button(searchbox,text='Search/Refresh',command=self.refresh).pack(side='left')
  box=ttk.Frame(tab);box.pack(fill='both',expand=True,padx=8,pady=4)
  cols=[PK[table]]+FIELDS[table];tree=ttk.Treeview(box,columns=cols,show='headings')
  for col in cols:tree.heading(col,text=col.replace('_',' ').title());tree.column(col,width=160,stretch=False)
  ys=ttk.Scrollbar(box,orient='vertical',command=tree.yview);xs=ttk.Scrollbar(box,orient='horizontal',command=tree.xview)
  tree.configure(yscrollcommand=ys.set,xscrollcommand=xs.set);tree.grid(row=0,column=0,sticky='nsew');ys.grid(row=0,column=1,sticky='ns');xs.grid(row=1,column=0,sticky='ew');box.columnconfigure(0,weight=1);box.rowconfigure(0,weight=1)
  tree.bind('<<TreeviewSelect>>',lambda e,t=table:self.select(t));self.trees[table]=tree
 def build_analysis(self):
  tab=ttk.Frame(self.tabs);self.tabs.add(tab,text='Analysis & Charts');bar=ttk.LabelFrame(tab,text='Search & Filter');bar.pack(fill='x',padx=10,pady=10)
  self.filter={key:tk.StringVar() for key in ['query','category','player','start','end']};self.filter['category'].set('All');self.filter['player'].set('All')
  for i,(key,title) in enumerate([('query','Search'),('category','Category'),('player','Player'),('start','From YYYY-MM-DD'),('end','To YYYY-MM-DD')]):
   ttk.Label(bar,text=title).grid(row=0,column=i,padx=7,sticky='w')
   if key in ('category','player'):
    widget=ttk.Combobox(bar,textvariable=self.filter[key],state='readonly',width=23);self.inputs[key+'_filter']=widget
   else:widget=ttk.Entry(bar,textvariable=self.filter[key],width=22)
   widget.grid(row=1,column=i,padx=6,pady=8)
  actions=ttk.Frame(tab);actions.pack(fill='x',padx=10,pady=5)
  for title,fn in [('Analyze',self.analyze),('Category time chart',lambda:self.plot('category')),('Player score chart',lambda:self.plot('player')),('Export PNG charts',self.export)]:ttk.Button(actions,text=title,command=fn).pack(side='left',padx=4)
  self.text=tk.Text(tab,font=('Consolas',10),wrap='none');self.text.pack(fill='both',expand=True,padx=10,pady=8)
 def current(self):
  return subset(dataset(self.records),self.filter['query'].get(),self.filter['category'].get(),self.filter['player'].get(),self.filter['start'].get(),self.filter['end'].get())
 def refresh(self):
  try:
   players=self.records.all('players');puzzles=self.records.all('puzzles')
   self.player_labels={f"{x['name']} | {x['player_id']}":x['player_id'] for x in players}
   self.puzzle_labels={f"{x['title']} | {x['puzzle_id']}":x['puzzle_id'] for x in puzzles}
   for field,labels in [('player_id',self.player_labels),('puzzle_id',self.puzzle_labels)]:
    widget=self.inputs['results'][field];widget['values']=list(labels)
    if self.vars['results'][field].get() not in labels:self.vars['results'][field].set(next(iter(labels),' ' ).strip())
   self.inputs['category_filter']['values']=['All']+list(CATEGORIES)
   self.inputs['player_filter']['values']=['All']+[x['player_id'] for x in players]
   for table,tree in self.trees.items():
    tree.delete(*tree.get_children());fields=[PK[table]]+FIELDS[table]
    for r in self.records.search(table,self.vars[table]['_search'].get()):tree.insert('', 'end',iid=r[PK[table]],values=[r[k] for k in fields])
  except (ValueError,OSError) as e:messagebox.showerror('Data error',str(e))
 def select(self,table):
  tree=self.trees[table];ids=tree.selection()
  if not ids:return
  self.selected[table]=ids[0];values=dict(zip([PK[table]]+FIELDS[table],tree.item(ids[0],'values')))
  for k,v in self.vars[table].items():
   if k.startswith('_'):continue
   raw=values[k]
   if k=='player_id':raw=next((a for a,b in self.player_labels.items() if b==raw),'')
   if k=='puzzle_id':raw=next((a for a,b in self.puzzle_labels.items() if b==raw),'')
   v.set(raw)
 def clear(self,table):
  self.selected[table]=None
  for k,v in self.vars[table].items():
   if not k.startswith('_'):v.set('')
  if table=='results':self.vars[table]['played_on'].set(date.today().isoformat());self.vars[table]['completed'].set('Yes')
 def save(self,table,update=False):
  try:
   ident=self.selected[table] if update else None
   if update and not ident:raise ValueError('Select a row first')
   data={k:v.get() for k,v in self.vars[table].items() if not k.startswith('_')}
   if table=='results':
    data['player_id']=self.player_labels.get(data['player_id'],'');data['puzzle_id']=self.puzzle_labels.get(data['puzzle_id'],'')
   self.records.put(table,data,ident);self.clear(table);self.refresh()
  except (ValueError,OSError) as e:messagebox.showerror('Validation',str(e))
 def delete(self,table):
  try:
   ident=self.selected[table]
   if not ident:raise ValueError('Select a row first')
   if messagebox.askyesno('Confirm','Permanently delete this record?'):
    self.records.delete(table,ident);self.clear(table);self.refresh()
  except (ValueError,OSError) as e:messagebox.showerror('Cannot delete',str(e))
 def analyze(self):
  try:
   d=self.current();s=summary(d)
   out=('SUMMARY\n'+ '\n'.join(f'{k}: {v}' for k,v in s.items())+'\n\nCATEGORY COMPARISON\n'+group_summary(d,'category').to_string(index=False)+'\n\nPLAYER COMPARISON\n'+group_summary(d,'name').to_string(index=False)+'\n\nOBSERVED PATTERNS\n'+patterns(d))
   self.text.delete('1.0','end');self.text.insert('1.0',out)
  except (ValueError,OSError) as e:messagebox.showerror('Analysis',str(e))
 def plot(self,kind):
  try:
   from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
   fig=category_chart(self.current()) if kind=='category' else player_chart(self.current())
   win=tk.Toplevel(self.root);win.title('Word Puzzle Performance - Visual Report');win.geometry('980x620')
   canvas=FigureCanvasTkAgg(fig,master=win);canvas.draw();NavigationToolbar2Tk(canvas,win);canvas.get_tk_widget().pack(fill='both',expand=True);win.canvas=canvas
  except (ValueError,OSError) as e:messagebox.showerror('Chart',str(e))
 def export(self):
  try:
   path=filedialog.askdirectory(title='Choose output folder')
   if path:
    category_chart(self.current()).savefig(path+'/category_average_time.png',dpi=160)
    player_chart(self.current()).savefig(path+'/player_average_score.png',dpi=160)
    messagebox.showinfo('Exported','Two PNG charts saved.')
  except (ValueError,OSError) as e:messagebox.showerror('Export',str(e))

if __name__=='__main__':
 root=tk.Tk();App(root);root.mainloop()
