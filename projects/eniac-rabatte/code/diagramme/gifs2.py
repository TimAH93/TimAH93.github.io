import pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt, io, json, sys
from PIL import Image
exec(open('rund.txt').read())
BG="#0A0A0C"; FG="#EDEDF0"; MUTE="#8A8F99"; OR="#F28E2B"; RT="#E15759"
OUT='/tmp/claude-0/-home-claude/ae02de73-ec78-550b-bc51-12f30093d777/scratchpad/gs/img2/'
import os; os.makedirs(OUT,exist_ok=True)
DPI=1600/15   # 1600 px breit: Google Slides komprimiert dann nicht neu
de=lambda v,d=1: f"{v:,.{d}f}".replace(",","X").replace(".",",").replace("X",".")
ease=lambda t: 1-(1-max(0,min(1,t)))**3
eio=lambda t: (lambda x: 3*x*x-2*x*x*x)(max(0,min(1,t)))
def stil():
  sns.set_theme(style="ticks"); plt.style.use("dark_background")
  plt.rcParams.update({"font.family":"Inter","figure.facecolor":BG,"axes.facecolor":BG,"savefig.facecolor":BG,"axes.edgecolor":"#5A5F69","xtick.color":FG,"ytick.color":FG,"text.color":FG,"axes.labelcolor":MUTE,"font.size":14})
def grab(fig):
  buf=io.BytesIO(); fig.savefig(buf,dpi=DPI); plt.close(fig); buf.seek(0); return Image.open(buf).convert("RGB")
def save(frames,dur,name):
  dur=list(dur); dur[-1]=655000   # GIF-Maximum (~11 Min.), damit Google Slides nicht neu startet
  pal=frames[-1].convert("P",palette=Image.ADAPTIVE,colors=255)
  fr=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
  for f in fr: f.info.pop('loop',None)
  fr[0].save(OUT+name+'.gif',save_all=True,append_images=fr[1:],duration=dur,optimize=True)  # kein loop -> spielt einmal
  frames[0].save(OUT+name+'_start.png')   # Standbild für die Folie davor (Klick-Steuerung)
  frames[-1].save(OUT+name+'_ende.png')
  print(name, frames[0].size)

# Phasen: Balken wachsen alle gleichzeitig (N1), dann Zahlen einblenden (N2)
N1=34; N2=20
def phasen():
  seq=[(0,0)]+[(ease(i/N1),0) for i in range(1,N1+1)]+[(1,i/N2) for i in range(1,N2+1)]
  dur=[30]*len(seq); dur[0]=200; dur[N1]=250; dur[-1]=4000
  return seq,dur

k=pd.read_csv('/mnt/user-data/outputs/F4/products_kategorie_vorlaeufig.csv')
b=pd.read_csv('orderlines_cl.csv'); b['u']=b.unit_price*b.product_quantity; b['re']=(b.price-b.unit_price)*b.product_quantity
bk=b.merge(k[['sku','kategorie_vorl']],on='sku')

def hbar_gif(s,name,titel,xlab,farbe,labs,xmax):
  s=s.sort_values(); n=len(s); seq,dur=phasen(); frames=[]
  for p,a in seq:
    stil(); fig,ax=plt.subplots(figsize=(16.5,7.2))
    ax.barh(range(n),s.values*p,color=farbe,height=0.62)
    if a>0:
      for i,v in enumerate(s.values): ax.text(v+xmax*0.01,i,labs[s.index[i]],va="center",fontsize=14,color=FG,alpha=a)
    ax.set_yticks(range(n),s.index,fontsize=14); ax.set_xlim(0,xmax); ax.set_ylim(-0.6,n-0.4)
    ax.set_xlabel(xlab,fontsize=14); ax.tick_params(axis='x',colors=MUTE)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: de(v,1)))
    ax.set_title(titel,fontsize=24,loc="left",pad=20,fontweight="bold"); sns.despine(ax=ax)
    fig.tight_layout()
    if p>0: balken_abrunden(ax,10,"rechts")
    frames.append(grab(fig))
  save(frames,dur,name)

def g33():
  u=bk.groupby('kategorie_vorl').u.sum()/1e6; ua=u/u.sum()*100
  hbar_gif(u,"g33","Umsatz je Kategorie","Umsatz in Mio. €",OR,{c:f"{de(u[c],2)} Mio. €  ({de(ua[c])} %)" for c in u.index},u.max()*1.3)
def g36():
  r=bk.groupby('kategorie_vorl').re.sum()/1e6; ra=r/r.sum()*100
  hbar_gif(r,"g36","Rabatt in Euro je Kategorie","Rabatt in Mio. €",RT,{c:f"{de(r[c],2)} Mio. €  ({de(ra[c])} %)" for c in r.index},r.max()*1.3)
def g34():  # Ø Rabatt in % je Kategorie
  r=bk.groupby('kategorie_vorl').rabatt.mean()*100
  hbar_gif(r,"g34","Ø Rabatt je Kategorie","Ø Rabatt in %",RT,{c:f"{de(r[c])} %" for c in r.index},r.max()*1.25)

def g4344():
  g=[0,50,100,500,1000,float('inf')]; K=["unter 50 €","50–100 €","100–500 €","500–1.000 €","über 1.000 €"]
  b['pk']=pd.cut(b.price,g,labels=K); U=b.groupby('pk',observed=False).u.sum().reindex(K)/1e6; UA=U/U.sum()*100; RB=(b.groupby('pk',observed=False).rabatt.mean()*100).reindex(K)
  def fr(pu,au,pr,ar):
    stil(); fig,axs=plt.subplots(1,2,figsize=(15,6.4))
    for ax,vals,c,p,a,ttl,yl,labs,top in [(axs[0],U.values,OR,pu,au,"Umsatz je Preisklasse","Umsatz in Mio. €",[de(v)+" %" for v in UA.values],U.max()*1.18),(axs[1],RB.values,RT,pr,ar,"Ø Rabatt je Preisklasse","Ø Rabatt in %",[de(v)+" %" for v in RB.values],RB.max()*1.18)]:
      ax.bar(range(5),vals*p,color=c,width=0.66); ax.set_ylim(0,top); ax.set_xlim(-0.6,4.6)
      if a>0:
        for i,v in enumerate(vals): ax.text(i,v+top*0.015,labs[i],ha="center",fontsize=13,color=FG,alpha=a)
      ax.set_xticks(range(5),K,fontsize=12); ax.set_ylabel(yl,fontsize=14); ax.set_title(ttl,fontsize=18,pad=12,fontweight="bold")
      ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: de(v,0))); sns.despine(ax=ax)
    fig.tight_layout()
    for ax,p in zip(axs,(pu,pr)):
      if p>0.01: balken_abrunden(ax,10,"oben")
    return grab(fig)
  seq,dur=phasen()
  save([fr(p,a,0,0) for p,a in seq],dur,"g43")      # Klick 1: Umsatz
  save([fr(1,1,p,a) for p,a in seq],dur,"g44")      # Klick 2: Rabatt

def g25():
  ol=b.copy(); ol['m']=pd.to_datetime(ol.date).dt.to_period('M')
  g=ol.groupby('m').agg(u=('u','sum'),r=('rabatt','mean'))   # echter Umsatz (Preis nach Rabatt x Menge)
  mn={1:"Jan",2:"Feb",3:"Mär",4:"Apr",5:"Mai",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Okt",11:"Nov",12:"Dez"}
  lab=[f"{mn[p.month]} {str(p.year)[2:]}" for p in g.index]; U=g.u.values/1e6; R=g.r.values*100; xs=np.arange(len(U))
  def frame(bf,lf):
    stil(); fig,ax1=plt.subplots(figsize=(15,6.6))
    ax1.bar(xs,U*bf,color=OR,width=0.66); ax1.set_ylim(0,U.max()*1.12); ax1.set_xlim(-0.6,len(xs)-0.4)
    ax1.set_ylabel("Umsatz in Mio. €",color=OR,fontsize=15); ax1.tick_params(axis='y',colors=OR,labelsize=14)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: de(v)))
    ax1.set_xticks(xs,lab,fontsize=14)
    ax2=ax1.twinx(); ax2.set_ylim(0,35); ax2.set_ylabel("Ø Rabatt in %",color=RT,fontsize=15); ax2.tick_params(axis='y',colors=RT,labelsize=14)
    if lf>0:
      end=lf*(len(xs)-1); k=int(np.floor(end)); px=list(xs[:k+1]); py=list(R[:k+1])
      if k<len(xs)-1: t=end-k; px.append(k+t); py.append(R[k]+(R[k+1]-R[k])*t)
      ax2.plot(px,py,color=RT,lw=3.5,marker="o",ms=8,markevery=list(range(k+1)))
    for a in (ax1,ax2): a.spines['top'].set_visible(False)
    fig.tight_layout()
    if bf>0.02: balken_abrunden(ax1,8,"oben")
    return grab(fig)
  frames=[frame(0,0)]; dur=[200]
  for i in range(1,33): frames.append(frame(ease(i/32),0)); dur.append(30)
  dur[-1]=600
  for i in range(1,61): frames.append(frame(1,eio(i/60))); dur.append(30)
  dur[-1]=4000
  save(frames,dur,"g25")

def marke():
  br=pd.read_csv('brands.csv'); b2=b.copy(); b2['short']=b2.sku.str[:3]
  b2=b2.merge(br.rename(columns={'long':'marke'}),on='short',how='left')
  g=b2.groupby('marke').agg(u=('u','sum'),re=('re','sum'))
  g['ua']=g.u/g.u.sum()*100; g['ra']=g.re/g.re.sum()*100
  g=g.rename(index={'Pack':'Pack (Bundles und\nKonfigurationen)'})
  g=g.sort_values('u',ascending=False).head(8).iloc[::-1]; n=len(g); seq,dur=phasen(); frames=[]
  xmax=g[['ua','ra']].values.max()*1.22; h=0.36
  for p,a in seq:
    stil(); fig,ax=plt.subplots(figsize=(15,7.2))
    y=np.arange(n)
    ax.barh(y+h/2,g.ua*p,height=h,color=OR); ax.barh(y-h/2,g.ra*p,height=h,color=RT)
    if a>0:
      for i,(u_,r_) in enumerate(zip(g.ua,g.ra)):
        ax.text(u_+xmax*0.008,i+h/2,de(u_)+" %",va="center",fontsize=13,color=FG,alpha=a)
        ax.text(r_+xmax*0.008,i-h/2,de(r_)+" %",va="center",fontsize=13,color=FG,alpha=a)
    ax.set_yticks(y,g.index,fontsize=14); ax.set_xlim(0,xmax); ax.set_ylim(-0.6,n-0.4)
    ax.set_xlabel("Anteil in %",fontsize=14); ax.tick_params(axis='x',colors=MUTE)
    ax.set_title("Anteil am Umsatz und am Rabatt je Marke (Top 8)",fontsize=24,loc="left",pad=20,fontweight="bold"); sns.despine(ax=ax)
    fig.tight_layout()
    if p>0: balken_abrunden(ax,8,"rechts")
    frames.append(grab(fig))
  save(frames,dur,"g_marke")
  print(g.round(1))
for n in sys.argv[1:]: globals()[n]()
