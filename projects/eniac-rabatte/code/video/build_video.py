import sys, subprocess, os, io
from PIL import Image
from pptx import Presentation
D=os.path.dirname(os.path.abspath(__file__)); FPS=30; PX=192
pres=Presentation(os.path.join(D,'..','Eniac_CEO_Praesentation_v59.pptx'))
# Haltezeiten in Sekunden (bei GIF-Folien: Stand nach Ende der Animation)
HALT={1:3.5,2:5,3:4.5,4:5.5,5:1.2,6:7,7:1.2,8:6,9:4,10:1.2,11:6,12:1.2,13:3,14:6,15:1.2,16:4,17:6.5,18:4.5,19:5.5,20:7,21:2,22:3.5,23:6,24:3.5}
def gif_info(nr):
    sl=pres.slides[nr-1]
    for sh in sl.shapes:
        if sh.shape_type==13 and sh.image.ext=='gif':
            r=[round(v/914400*PX) for v in (sh.left,sh.top,sh.width,sh.height)]
            return Image.open(io.BytesIO(sh.image.blob)), r
    return None, None
import json
STATES=json.load(open(os.path.join(D,'states.json')))
NUMBOX=(1740,995,1830,1052)   # Bereich der Foliennummer, kommt aus der Originalfolie
def frames(nr):
    """liefert (Bild, Dauer in s) für eine Folie"""
    bg=Image.open(os.path.join(D,f's-{nr:02d}.png')).convert('RGB')
    if str(nr) in STATES:
        orig_num=bg.crop(NUMBOX); st=[]
        for p in STATES[str(nr)]:
            im=Image.open(os.path.join(D,f'st-{p:02d}.png')).convert('RGB')
            if nr not in (1,24): im.paste(orig_num,NUMBOX[:2])
            st.append(im)
        yield st[0], (1.5 if nr==1 else 0.35)
        for k in range(1,len(st)):
            for j in range(1,15):                       # Überblendung 0,47 s
                yield Image.blend(st[k-1],st[k],j/14), 1/FPS
            yield st[k], (HALT[nr] if k==len(st)-1 else 0.45)
        return
    g,r=gif_info(nr)
    if g is None: yield bg, HALT[nr]; return
    n=g.n_frames
    for k in range(n):
        g.seek(k); dur=g.info.get('duration',30)/1000
        if k==n-1: dur=HALT[nr]
        f=g.convert('RGB').resize((r[2],r[3]),Image.LANCZOS)
        im=bg.copy(); im.paste(f,(r[0],r[1])); yield im, dur
def render(nr,out):
    tmp=out+'.part.mp4'
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r',str(FPS),'-i','-',
        '-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p',tmp],stdin=subprocess.PIPE)
    t=0.0; shown=0
    for im,dur in frames(nr):
        t+=dur; target=round(t*FPS)
        b=im.tobytes()
        while shown<target: p.stdin.write(b); shown+=1
    p.stdin.close(); rc=p.wait()
    if rc==0: os.replace(tmp,out)
    return rc
if __name__=='__main__':
    if sys.argv[1]=='vorschau':
        for nr,k in [(7,-1),(17,-1),(18,-1),(24,-1),(14,10)]:
            fr=list(frames(nr)); fr[k][0].save(os.path.join(D,f'vorschau_{nr}.jpg'),quality=88)
    else:
        lst=[]
        for nr in range(1,25):
            out=os.path.join(D,f'szene_{nr:02d}.mp4'); assert render(nr,out)==0, nr; lst.append(out)
        open(os.path.join(D,'liste.txt'),'w').write(''.join(f"file '{x}'\n" for x in lst))
        subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',os.path.join(D,'liste.txt'),'-c','copy',os.path.join(D,'Eniac_Praesentation_Video.mp4')],check=True)
        print('fertig')
