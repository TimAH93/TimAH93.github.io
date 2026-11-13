import sys; sys.argv=['x']
exec(open('gifs2.py').read())
exec(open('welten2.py').read().split('def save3')[1].join(['def save3','']) if False else '')
BL="#4FA3E0"; BLD="#2A5E86"; ORD="#8F5420"; RTD="#8C3A3B"
A=[24,61,11,48]; N=[76,39,18,52]; d=0.21; w=0.38
def frame(pa,aa,pn,an):
  stil(); fig,ax=plt.subplots(figsize=(16.5,7.2))
  for x in range(4):
    for off,v,c,p,a,lab,lc in [(-d,A[x],[BL,OR,RT,RT][x],pa,aa,"Apple",BG),(d,N[x],[BLD,ORD,RTD,RTD][x],pn,an,"Andere",FG)]:
      if p>0.005: ax.bar(x+off,v*p,color=c,width=w,edgecolor='none',linewidth=0)
      if a>0:
        ax.text(x+off,v+90*0.022,f"{v} %",ha="center",fontsize=30,fontweight="bold",color=FG,alpha=a)
        ax.text(x+off,1.6,lab,ha="center",va="bottom",fontsize=15,fontweight="bold",color=lc,alpha=a)
  ax.set_xticks(range(4),["Anteil an\nverkauften Stück","Anteil am\nUmsatz","Ø Rabatt","Anteil am\nRabattgeld"],fontsize=19)
  ax.tick_params(axis='x',length=0,pad=10); ax.set_ylim(0,90); ax.set_yticks([]); ax.set_xlim(-0.6,3.6); sns.despine(ax=ax,left=True)
  fig.tight_layout()
  if max(pa,pn)>0.02: balken_abrunden(ax,10,"oben")
  return grab(fig)
def save3(frames,dur,name):
  dur=list(dur); dur[-1]=655000
  W,H=frames[0].size; m=Image.new("RGB",(W,H*2)); m.paste(frames[0],(0,0)); m.paste(frames[-1],(0,H))
  pal=m.convert("P",palette=Image.ADAPTIVE,colors=255)
  q=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
  q[0].save(OUT+name+'.gif',save_all=True,append_images=q[1:],duration=dur,optimize=True)
  frames[0].save(OUT+name+'_start.png'); frames[-1].save(OUT+name+'_ende.png'); print(name,frames[0].size)
seq,dur=phasen()
save3([frame(p,a,0,0) for p,a in seq],dur,"g_paare1")
save3([frame(1,1,p,a) for p,a in seq],dur,"g_paare2")
