# Echte Einblende-Animationen (Verblassen) in die fertige PPTX schreiben
import zipfile, re, sys, shutil
src=sys.argv[1]; SPEC=__import__('json').loads(open(sys.argv[2]).read())
def shapes(xml):
    out=[]
    for m in re.finditer(r'<p:(sp|pic|cxnSp)>.*?</p:\1>',xml,re.S):
        b=m.group(0)
        if '<a:fld' in b: continue   # Foliennummer nie animieren
        i=int(re.search(r'<p:cNvPr id="(\d+)"',b).group(1))
        t=''.join(re.findall(r'<a:t>([^<]*)</a:t>',b)); descr=(re.search(r'descr="([^"]*)"',b) or [None,''])[1]
        off=re.search(r'<a:off x="(\d+)" y="(\d+)"',b); x,y=(int(off.group(1))/914400,int(off.group(2))/914400) if off else (0,0)
        out.append(dict(id=i,text=t,descr=descr,x=x,y=y,kind=m.group(1)))
    return out
def match(sh,sel):
    if sel.startswith('text='): return sh['text']==sel[5:]
    if sel.startswith('has='): return sel[4:] in sh['text']
    if sel.startswith('descr='): return sel[6:] in sh['descr']
    if sel=='legend': return sh['y']<0.5 and sh['x']>5.5
    return False
class Ids:
    def __init__(s): s.n=2
    def __call__(s): s.n+=1; return s.n
def effekt(nid,spid,node,delay,dur=500):
    return (f'<p:par><p:cTn id="{nid()}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" nodeType="{node}"><p:stCondLst><p:cond delay="{delay}"/></p:stCondLst><p:childTnLst>'
      f'<p:set><p:cBhvr><p:cTn id="{nid()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
      f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{nid()}" dur="{dur}"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect></p:childTnLst></p:cTn></p:par>')
def timing(groups,mode):
    nid=Ids(); seqs=''
    if mode=='auto':   # startet von selbst nach dem Folienwechsel, Gruppen nacheinander
        blocks=''; t=300
        for g,ids in enumerate(groups):
            eff=''.join(effekt(nid,spid,'afterEffect' if k==0 else 'withEffect',0) for k,spid in enumerate(ids))
            blocks+=f'<p:par><p:cTn id="{nid()}" fill="hold"><p:stCondLst><p:cond delay="{t}"/></p:stCondLst><p:childTnLst>{eff}</p:childTnLst></p:cTn></p:par>'
            t+=750
        seqs=f'<p:par><p:cTn id="{nid()}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>{blocks}</p:childTnLst></p:cTn></p:par>'
    elif mode=='clickauto':   # schwarzer Start: ein Klick, dann laufen alle Gruppen nacheinander von selbst
        inner=''; t=0
        for g,ids in enumerate(groups):
            eff=''.join(effekt(nid,spid,('clickEffect' if g==0 else 'afterEffect') if k==0 else 'withEffect',0) for k,spid in enumerate(ids))
            inner+=f'<p:par><p:cTn id="{nid()}" fill="hold"><p:stCondLst><p:cond delay="{t}"/></p:stCondLst><p:childTnLst>{eff}</p:childTnLst></p:cTn></p:par>'
            t+=750
        seqs=f'<p:par><p:cTn id="{nid()}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>{inner}</p:childTnLst></p:cTn></p:par>'
    else:              # ein Klick pro Gruppe
        for ids in groups:
            eff=''.join(effekt(nid,spid,'clickEffect' if k==0 else 'withEffect',0) for k,spid in enumerate(ids))
            seqs+=f'<p:par><p:cTn id="{nid()}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="{nid()}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>{eff}</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>'
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
            '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'+seqs+
            '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')
zin=zipfile.ZipFile(src); dst=src+'.tmp'; zout=zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED); log=[]
for it in zin.infolist():
    data=zin.read(it.filename)
    if re.match(r'ppt/slides/slide\d+\.xml$',it.filename):
        x=data.decode('utf8'); sh=shapes(x); alltext=' | '.join(s['text'] for s in sh)
        for sp in SPEC:
            if all(k in alltext for k in sp['has']) and not any(k in alltext for k in sp.get('not',[])) and '<p:timing>' not in x:
                groups=[[s['id'] for s in sh if any(match(s,sel) for sel in g)] for g in sp['groups']]
                groups=[g for g in groups if g]
                tm=timing(groups,sp['mode'])
                if '</p:transition>' in x: x=x.replace('</p:transition>','</p:transition>'+tm,1)
                elif '<p:transition' in x and '/>' in x.split('<p:transition',1)[1]: x=re.sub(r'(<p:transition[^>]*/>)',r'\1'+tm,x,1)
                else: x=x.replace('</p:clrMapOvr>','</p:clrMapOvr>'+tm,1)
                log.append((it.filename,sp['name'],[len(g) for g in groups])); break
        data=x.encode('utf8')
    zout.writestr(it,data)
zout.close(); shutil.move(dst,src)
for l in sorted(log,key=lambda t:int(re.search(r'\d+',t[0]).group())): print(l)
