import sys; sys.argv=['x']
exec(open('gifs2.py').read())
BL="#4FA3E0"; GR="#5A5F69"
d=pd.read_pickle('marken_d_miguel.pkl')   # Miguels Zuordnung (Pareto-Zelle)
d2=pd.read_pickle('marken_d_miguel_rabatt.pkl')   # Miguels Zuordnung (Rabatt-Zelle)
g=d.groupby('marke').agg(u=('u','sum'),re=('re','sum'),st=('product_quantity','sum'))
g['ua']=g.u/g.u.sum()*100; g['sa']=g.st/g.st.sum()*100; g['quote']=g.re/(g.u+g.re)*100
U=g.sort_values('u',ascending=False).head(10); S=g.sort_values('st',ascending=False).head(10)
def pareto():
  seq,dur=phasen(); frames=[]
  for p,a in seq:
    stil(); fig,axs=plt.subplots(1,2,figsize=(15,7.2))
    for ax,t,col,farben,ttl,xl in [(axs[0],U,'ua',[OR]*8+[GR]*2,"Umsatz: 8 Marken bringen 80 %","Anteil am Umsatz in %"),(axs[1],S,'sa',[BL]*10,"Stückzahl: 34 Marken bringen 80 %","Anteil an verkauften Stück in %")]:
      t=t.iloc[::-1]; f=farben[::-1]; n=len(t); xmax=t[col].max()*1.25
      ax.barh(range(n),t[col]*p,color=f,height=0.62)
      if a>0:
        for i,v in enumerate(t[col]): ax.text(v+xmax*0.015,i,de(v)+" %",va="center",fontsize=13,color=FG,alpha=a)
      ax.set_yticks(range(n),t.index,fontsize=13); ax.set_xlim(0,xmax); ax.set_ylim(-0.6,n-0.4)
      ax.set_xlabel(xl,fontsize=13); ax.tick_params(axis='x',colors=MUTE)
      ax.set_title(ttl,fontsize=18,loc="left",pad=14,fontweight="bold"); sns.despine(ax=ax)
    fig.tight_layout(w_pad=3)
    if p>0:
      for ax in axs: balken_abrunden(ax,8,"rechts")
    frames.append(grab(fig))
  save(frames,dur,"g_pareto")
def rabattgeld():
  g2=d2.groupby('marke').agg(u=('u','sum'),re=('re','sum')); g2['quote']=g2.re/(g2.u+g2.re)*100
  r=g2.sort_values('u',ascending=False).head(10)   # wie bei Miguel: die Top 10 Umsatzmarken
  hbar_gif((r.re/1e6),"g_rabattmarke","Rabatt in Euro: Top 10 Umsatzmarken","Rabatt in Mio. €",RT,
    {c:f"{de(r.re[c]/1e6,2)} Mio. €  ·  {de(r.quote[c])} % Rabatt" for c in r.index},r.re.max()/1e6*1.45)
print(U[['ua']].round(1).T); print(g.sort_values('re',ascending=False).head(10)[['re','quote']].round(2))

def vergleich():  # Option 3: Umsatz gegen Stückzahl je Marke, Miguels Reihenfolge (Top 10 Umsatz)
  t=U.iloc[::-1]; n=len(t); h=0.38; xmax=t.ua.max()*1.15; seq,dur=phasen(); frames=[]
  for p,a in seq:
    stil(); fig,ax=plt.subplots(figsize=(18.6,7.2)); y=np.arange(n)
    ax.barh(y+h/2,t.ua*p,height=h,color=OR); ax.barh(y-h/2,t.sa*p,height=h,color=BL)
    if a>0:
      for i,(u_,s_) in enumerate(zip(t.ua,t.sa)):
        ax.text(u_+xmax*0.008,i+h/2,de(u_)+" %",va="center",fontsize=16,color=FG,alpha=a)
        ax.text(s_+xmax*0.008,i-h/2,de(s_)+" %",va="center",fontsize=16,color=FG,alpha=a)
    ax.set_yticks(y,t.index,fontsize=18); ax.set_xlim(0,xmax); ax.set_ylim(-0.6,n-0.4)
    ax.set_xlabel("Anteil in %",fontsize=16); ax.tick_params(axis='x',colors=MUTE); sns.despine(ax=ax)
    ax.set_title("Umsatz gegen verkaufte Stück je Marke (Top 10 nach Umsatz)",fontsize=26,loc="left",pad=18,fontweight="bold")
    fig.tight_layout()
    if p>0: balken_abrunden(ax,7,"rechts")
    frames.append(grab(fig))
  save(frames,dur,"g_vergleich")
  print(t[['ua','sa']].round(1))

vergleich()
