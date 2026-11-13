import sys; sys.argv=['x']
exec(open('gifs2.py').read())
r=bk.groupby('kategorie_vorl').rabatt.mean()*100; e=bk.groupby('kategorie_vorl').re.sum()/1e6; ea=e/e.sum()*100
o=e.sort_values().index; r=r[o]; e=e[o]; n=len(o); y=np.arange(n)
stil(); fig,(a1,a2)=plt.subplots(1,2,figsize=(16.5,7.2),sharey=True,gridspec_kw={'wspace':0.08})
a1.barh(y,r.values,color=RT,height=0.62); a2.barh(y,e.values,color=RT,height=0.62)
for i,v in enumerate(r.values): a1.text(v+r.max()*0.015,i,de(v)+" %",va="center",fontsize=14,color=FG)
for i,c in enumerate(o): a2.text(e[c]+e.max()*0.015,i,f"{de(e[c],2)} Mio. €  ({de(ea[c],0) if ea[c]>=0.5 else '<1'} %)",va="center",fontsize=14,color=FG)
a1.set_yticks(y,o,fontsize=15); a1.set_xlim(0,r.max()*1.3); a2.set_xlim(0,e.max()*1.55); a1.set_ylim(-0.6,n-0.4)
for a,t in [(a1,"Ø Rabatt in Prozent"),(a2,"Rabatt in Euro")]:
  a.set_xticks([]); sns.despine(ax=a,bottom=True); a.tick_params(axis='y',length=0); a.set_title(t,fontsize=19,loc="left",pad=12,fontweight="bold")
a2.spines['left'].set_visible(False)
fig.subplots_adjust(left=0.2,right=0.985,top=0.9,bottom=0.03); balken_abrunden(a1,8,"rechts"); balken_abrunden(a2,8,"rechts")
fig.savefig('/tmp/claude-0/-home-claude/ae02de73-ec78-550b-bc51-12f30093d777/scratchpad/gs/img2/a4_kombi.png',dpi=1600/15)
print(pd.DataFrame({'r':r.round(1),'e':e.round(2),'ea':ea[o].round(0)}))
