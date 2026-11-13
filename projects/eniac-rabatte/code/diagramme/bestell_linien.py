import sys; sys.argv=['x']
exec(open('gifs2.py').read())
BL="#4FA3E0"
o=pd.read_csv('orders_cl.csv'); o['m']=pd.to_datetime(o.created_date).dt.to_period('M')
ol=b.copy(); ol['m']=pd.to_datetime(ol.date).dt.to_period('M')
g=ol.groupby('m').agg(u=('u','sum'),r=('rabatt','mean')); g['n']=o.groupby('m').size()
mn={1:"Jan",2:"Feb",3:"Mär",4:"Apr",5:"Mai",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Okt",11:"Nov",12:"Dez"}
lab=[f"{mn[p.month]} {str(p.year)[2:]}" for p in g.index]; U=g.u.values/1e6; R=g.r.values*100; N=g.n.values/1000; xs=np.arange(len(U))
def teil(Y,f):
  end=f*(len(xs)-1); k=int(np.floor(end)); px=list(xs[:k+1]); py=list(Y[:k+1])
  if k<len(xs)-1: t=end-k; px.append(k+t); py.append(Y[k]+(Y[k+1]-Y[k])*t)
  return px,py,k
def frame(bf,nf,rf):
  stil(); fig,(ax1,axr)=plt.subplots(2,1,figsize=(15,6.6),sharex=True,gridspec_kw={'height_ratios':[6,0.55],'hspace':0.04})
  ax1.bar(xs,U*bf,color=OR,width=0.62); ax1.set_ylim(0,U.max()*1.12); ax1.set_xlim(-0.6,len(xs)-0.4)
  ax1.set_ylabel("Umsatz in Mio. €",color=OR,fontsize=15); ax1.tick_params(axis='y',colors=OR,labelsize=13)
  ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: de(v)))
  axr.set_ylim(0,1); axr.set_yticks([])
  for sp in ['top','right','left','bottom']: axr.spines[sp].set_visible(False)
  axr.set_xticks(xs,lab,fontsize=13); axr.tick_params(axis='x',length=0)
  axr.text(-0.95,0.5,"Ø Rabatt",ha="right",va="center",fontsize=13,color=RT)
  if rf>0:
    for i,(x,r) in enumerate(zip(xs,R)):
      a=max(0,min(1,(rf*(len(xs)-1)-i)+1))
      if a>0: axr.text(x,0.5,de(r,0)+" %",ha="center",va="center",fontsize=13,color=RT,fontweight="bold",alpha=a)
  ax2=ax1.twinx(); ax2.set_ylim(0,35); ax2.axis('off')   # Rabatt ohne eigene Achse, Werte stehen unten
  ax3=ax1.twinx(); ax3.set_ylim(0,N.max()*1.12)
  ax3.set_ylabel("Bestellungen in Tsd.",color=BL,fontsize=15); ax3.tick_params(axis='y',colors=BL,labelsize=13)
  if nf>0:
    px,py,k=teil(N,nf); ax3.plot(px,py,color=BL,lw=3.5,marker="o",ms=7,markevery=list(range(k+1)))
  if rf>0:
    px,py,k=teil(R,rf); ax2.plot(px,py,color=RT,lw=3.5,marker="o",ms=7,markevery=list(range(k+1)))
  for a in (ax1,ax3): a.spines['top'].set_visible(False)
  fig.subplots_adjust(left=0.07,right=0.92,top=0.97,bottom=0.08)
  if bf>0.02: balken_abrunden(ax1,7,"oben")
  return grab(fig)
frames=[frame(0,0,0)]; dur=[200]
for i in range(1,31): frames.append(frame(ease(i/30),0,0)); dur.append(30)
dur[-1]=500
for i in range(1,51): frames.append(frame(1,eio(i/50),0)); dur.append(30)
dur[-1]=600
for i in range(1,51): frames.append(frame(1,1,eio(i/50))); dur.append(30)
save(frames,dur,"g25_linien")
