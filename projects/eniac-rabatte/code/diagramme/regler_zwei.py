import sys; sys.argv=['x']
exec(open('gifs2.py').read())
ORD="#8A5A2B"
LA=10.523341; LR=7.118987; QA=11.148; QR=18.016   # Marke Apple gegen alle anderen Marken
st=[10,9,8,7,6]; xs=np.arange(len(st))
frei=lambda a: LA*(QA-a)/100; zub=lambda a: QR+frei(a)/LR*100
def frame(pb,pl,pa=1):
  stil(); fig,ax=plt.subplots(figsize=(15,6.8))
  hs=[frei(a)*pb for a in st]
  if pb>0.005: ax.bar(xs,hs,color=OR,width=0.58,edgecolor='none',linewidth=0)   # alle Balken gleichfarbig
  if pb>=0.999 and pa>0:
    for x,a in zip(xs,st): ax.text(x,frei(a)+0.015,f"+{de(frei(a),2)} Mio. €",ha="center",fontsize=17,fontweight="bold",color=FG,alpha=pa)
  ax.set_xticks(xs,[f"Apple {a} %" for a in st],fontsize=18); ax.tick_params(axis='x',length=0,pad=8)
  ax.set_ylim(0,0.78); ax.set_yticks([]); ax.set_xlim(-0.6,len(st)-0.4); sns.despine(ax=ax,left=True)
  ax2=ax.twinx(); ax2.set_ylim(-8,30); ax2.axis('off')
  if pl>0:
    end=pl*(len(xs)-1); k=int(np.floor(end)); Y=[zub(a) for a in st]
    px=list(xs[:k+1]); py=Y[:k+1]
    if k<len(xs)-1: t=end-k; px.append(k+t); py.append(Y[k]+(Y[k+1]-Y[k])*t)
    ax2.plot(px,py,color=RT,lw=3.5); ax2.plot(xs[:k+1],Y[:k+1],'o',color=RT,ms=10)
    for i in range(k+1): ax2.text(xs[i],Y[i]+1.4,f"{de(Y[i])} %",ha="center",fontsize=16,fontweight="bold",color=RT)
  fig.tight_layout()
  if pb>0.02: balken_abrunden(ax,8,"oben")
  return grab(fig)
def save3(frames,dur,name):
  dur=list(dur); dur[-1]=655000
  W,H=frames[0].size; m=Image.new("RGB",(W,H*2)); m.paste(frames[0],(0,0)); m.paste(frames[-1],(0,H))
  pal=m.convert("P",palette=Image.ADAPTIVE,colors=255)
  q=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
  q[0].save(OUT+name+'.gif',save_all=True,append_images=q[1:],duration=dur,optimize=True)
  frames[0].save(OUT+name+'_start.png'); frames[-1].save(OUT+name+'_ende.png'); print(name,frames[0].size)
# Klick 1: Linie (Rabatt auf andere Marken) zeichnet sich, Klick 2: Balken (Umsatz) wachsen
f1=[frame(0,0)]; d1=[200]
for i in range(1,51): f1.append(frame(0,eio(i/50))); d1.append(30)
save3(f1,d1,"g_regler_linie")
f2=[frame(0,1)]; d2=[200]
for i in range(1,35): f2.append(frame(ease(i/34),1,0)); d2.append(30)
for i in range(1,16): f2.append(frame(1,1,i/15)); d2.append(30)
save3(f2,d2,"g_regler_balken")
