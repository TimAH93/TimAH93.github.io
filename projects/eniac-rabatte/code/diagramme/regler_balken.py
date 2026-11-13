import sys; sys.argv=['x']
exec(open('gifs2.py').read())
from matplotlib.patches import FancyBboxPatch
CY="#00E5FF"; TRACK="#2E3139"; ORD="#8A5A2B"
LA=10.523341; LR=7.118987; QA=11.148; QR=18.016
z=[11,10,9,8,7,6]; xs=np.arange(len(z))
frei=lambda a: 0 if a>=11 else max(0,LA*(QA-a)/100); rest=lambda a: QR+frei(a)/LR*100
def frame(a):
  stil(); fig=plt.figure(figsize=(15,6.6))
  # Regler oben
  axs=fig.add_axes([0.06,0.80,0.88,0.17]); axs.set_xlim(-0.6,len(z)-0.4); axs.set_ylim(0,1); axs.axis('off')
  pos=lambda v: (11-v)        # gleiche x-Positionen wie die Balken
  axs.add_patch(FancyBboxPatch((0,0.42),5,0.12,boxstyle="round,pad=0,rounding_size=0.06",color=TRACK))
  axs.add_patch(FancyBboxPatch((0,0.42),max(0.001,pos(a)),0.12,boxstyle="round,pad=0,rounding_size=0.06",color=CY))
  axs.plot([pos(a)],[0.48],marker='o',ms=26,color=FG,zorder=5); axs.plot([pos(a)],[0.48],marker='o',ms=13,color=CY,zorder=6)
  axs.text(pos(a),0.88,f"Apple-Rabatt {de(a)} %",ha="center",fontsize=17,fontweight="bold",color=FG)
  # Balken darunter
  ax=fig.add_axes([0.06,0.12,0.88,0.62])
  hs=[]
  for i,v in enumerate(z):
    t=max(0,min(1,(v+1-a)))          # Balken wächst, während der Regler von v+1 auf v fährt
    h=frei(v)*t if v<11 else 0
    hs.append(h)
  fc=[ORD if v>7 else OR for v in z]
  ax.bar(xs,hs,color=fc,width=0.6,edgecolor='none',linewidth=0)
  for x,h,v in zip(xs,hs,z):
    if h>0.005 and h>=frei(v)-1e-6: ax.text(x,h+0.015,f"+{de(frei(v),2)} Mio. €",ha="center",fontsize=15,fontweight="bold",color=FG if v<=7 else MUTE)
  ax.set_xticks(xs,[f"Apple {v} %" for v in z],fontsize=15); ax.tick_params(axis='x',length=0,pad=8)
  ax.set_ylim(0,0.72); ax.set_yticks([]); sns.despine(ax=ax,left=True); ax.set_xlim(-0.6,len(z)-0.4)
  ax2=ax.twinx(); ax2.set_ylim(-22,30); ax2.axis('off')
  px=[x for x,v in zip(xs,z) if v>=a]+([pos(a)] if a<11 and a not in z else [])
  py=[QR+frei(v)/LR*100 for v in z if v>=a]+([rest(a)] if a<11 and a not in z else [])
  ax2.plot(px,py,color=RT,lw=3.5); ax2.plot([x for x,v in zip(xs,z) if v>=a],[rest(v) for v in z if v>=a],'o',color=RT,ms=9)
  for x,v in zip(xs,z):
    if v>=a: ax2.text(x,rest(v)+1.5,f"Zubehör {de(rest(v))} %",ha="center",fontsize=12,color=RT,fontweight="bold")
  if hs[0]==0: pass
  return grab(fig)
frames=[]; dur=[]
def fahr(a0,a1,n):
  for i in range(1,n+1): frames.append(frame(a0+(a1-a0)*eio(i/n))); dur.append(30)
frames.append(frame(11.0)); dur.append(400)
fahr(11.0,7.0,80); dur[-1]=1000
fahr(7.0,6.0,25)
save(frames,dur,"g_regler_balken")
