exec(open('flamme.py').read().split('def bild')[0])
import io; from PIL import Image
ease=lambda t: 1-(1-t)**3
OUT='/tmp/claude-0/-home-claude/ae02de73-ec78-550b-bc51-12f30093d777/scratchpad/gs/img2/'
dd=d.iloc[::-1]; ff=farben[::-1]
NOV=list(cols).index('Nov 17')          # unten klein, Mac oben
cum=np.vstack([np.zeros(len(x)),np.cumsum(dd.values,axis=0)])
LY=[0.22+k*(2.78-0.22)/(len(dd)-1) for k in range(len(dd))]
n=len(dd); reihen=list(range(n))            # Wachsen: unterste Schicht zuerst, Mac zuletzt
def frame(al):
  stil(); fig,ax=plt.subplots(figsize=(16.5,7.2))
  basis=np.zeros(len(x))   # echtes Stapeln: jede Schicht sitzt auf der aktuellen Höhe der Schichten darunter
  for k in range(n):
    h=dd.values[k]*al[k]
    if al[k]>0: ax.fill_between(x,basis,basis+h,color=ff[k],linewidth=0.6,edgecolor=BG)
    basis=basis+h
  ax.set_xticks(x,cols,fontsize=14); ax.set_xlim(0,len(x)-1); ax.set_ylim(0,3.1)
  ax.set_ylabel("Umsatz in Mio. €",fontsize=18); ax.tick_params(axis="y",labelsize=17)
  ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"{v:.1f}".replace(".",",")))
  # Legende wächst mit der Spitze im November 17: ein Eintrag erscheint erst, wenn die Spitze seine Höhe erreicht
  import matplotlib.transforms as mt; from matplotlib.patches import Rectangle
  tr=mt.blended_transform_factory(ax.transAxes,ax.transData)
  spitze=sum(dd.values[k][NOV]*al[k] for k in range(n))
  for k in range(n):
    yk=LY[k]; a=max(0.0,min(1.0,(spitze-(yk-0.12))/0.12))
    if a<=0: continue
    ax.add_patch(Rectangle((1.025,yk-0.055),0.035,0.11,transform=tr,color=ff[k],alpha=a,clip_on=False,linewidth=0))
    ax.text(1.075,yk,dd.index[k],transform=tr,va="center",fontsize=19,color=FG,alpha=a,clip_on=False)
  sns.despine(ax=ax); fig.subplots_adjust(left=0.065,right=0.725,top=0.97,bottom=0.08)
  buf=io.BytesIO(); fig.savefig(buf,dpi=1600/16.5); plt.close(fig); buf.seek(0); return Image.open(buf).convert("RGB")
# Zeitachse: Schichten starten versetzt und überlappen sich, weiche Ein- und Ausfahrt
eio=lambda t: (lambda u: u*u*(3-2*u))(max(0.0,min(1.0,t)))
start=[0.25+0.17*k for k in range(n-1)]+[0.25+0.17*(n-1)+0.15]
dauer=[0.75]*(n-1)+[1.3]
T=max(a+b for a,b in zip(start,dauer))+0.05; dt=0.03
frames=[]; dur=[]
t=0.0
while t<=T+1e-9:
  al=[eio((t-start[k])/dauer[k]) for k in range(n)]
  frames.append(frame(al)); dur.append(int(dt*1000)); t+=dt
dur[-1]=655000
W,H=frames[0].size; m=Image.new("RGB",(W,H*3))
for i,f in enumerate([frames[0],frames[len(frames)//2],frames[-1]]): m.paste(f,(0,i*H))
pal=m.convert("P",palette=Image.ADAPTIVE,colors=255)
q=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
q[0].save(OUT+'a5_smooth.gif',save_all=True,append_images=q[1:],duration=dur,optimize=True)
frames[0].save(OUT+'a5_smooth_start.png'); frames[-1].save(OUT+'a5_smooth_ende.png')
print(len(frames),frames[0].size,sum(dur[:-1])/1000,'s')
