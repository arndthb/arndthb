"""Original orthographic vector artwork. No traced or embedded raster assets."""
from pathlib import Path
from math import sin, cos, pi, sqrt
from html import escape
import random
import re

ROOT=Path(__file__).resolve().parents[1]
faces=[]
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,k): return tuple(x*k for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a): return mul(a,1/(sqrt(dot(a,a)) or 1))
# Camera above the starboard bow. Engine symmetry remains in vessel space.
R=(.7071,-.7071,0)
U=(.35355,.35355,-.86603)
V=unit(cross(R,U))
LIGHT=unit((-.45,.25,1))
def proj(p): return (dot(p,R),dot(p,U))
def n(v): return f'{v:.1f}'.rstrip('0').rstrip('.')
def path(points,close=True):
    q=[proj(p) for p in points]
    return 'M'+' '.join(n(c) for c in q[0])+''.join('L'+' '.join(n(c) for c in p) for p in q[1:])+('Z' if close else '')
def face(points,base=(135,151,161),normal=None,tint=0,colour=None,stroke=None):
    if normal is not None and dot(normal,V)<-.01:return
    if colour is None:
        norm=unit(normal or cross(sub(points[1],points[0]),sub(points[2],points[0])))
        brightness=.44+.56*max(0,dot(norm,LIGHT))
        colour='#'+''.join(f'{min(255,max(0,round(c*brightness+tint))):02x}' for c in base)
    markup=f'<path d="{path(points)}" fill="{colour}"'
    if stroke:markup+=f' stroke="{stroke}" stroke-width=".24"'
    else:markup+=f' stroke="{colour}" stroke-width=".22" stroke-linejoin="round"'
    markup+='/>'
    faces.append((sum(dot(p,V) for p in points)/len(points),markup))
def line(points,colour,width=.6,depth=.3):
    faces.append((sum(dot(p,V) for p in points)/len(points)+depth,f'<path d="{path(points,False)}" fill="none" stroke="{colour}" stroke-width="{width}" stroke-linecap="round"/>'))
def decal(points,colour,depth=.4):
    faces.append((sum(dot(p,V) for p in points)/len(points)+depth,f'<path d="{path(points)}" fill="{colour}"/>'))
def solid(points,indices,base=(146,161,171)):
    for ix in indices:face([points[i] for i in ix],base)
def loft(rings,steps=48,base=(151,164,171),axis='y'):
    # (longitudinal y, half width, half height, centre z, centre x)
    rr=[]
    for y,rx,rz,z,x in rings:
        rr.append([(x+rx*cos(2*pi*i/steps),y,z+rz*sin(2*pi*i/steps)) for i in range(steps)])
    for j in range(len(rr)-1):
        for i in range(steps):
            k=(i+1)%steps
            pts=[rr[j][i],rr[j+1][i],rr[j+1][k],rr[j][k]]
            norm=unit(cross(sub(pts[1],pts[0]),sub(pts[3],pts[0])))
            # ring order runs from stern towards bow
            face(pts,base,normal=norm,tint=((i//3+j//2)%3-1)*1.7)

# Independent AR04 survey shuttle. No franchise spacecraft geometry or insignia.
def angular_loft(rings,base=(164,175,179),soft=False):
    section=[(1,.48),(.70,1),(-.70,1),(-1,.48),(-1,-.48),(-.70,-1),(.70,-1),(1,-.48)]
    if soft:
        section=[(1,.30),(.995,.50),(.95,.74),(.86,.91),(.66,1),(.30,1),(-.30,1),(-.66,1),(-.86,.91),(-.95,.74),(-.995,.50),(-1,.30),(-1,-.30),(-.98,-.60),(-.85,-.87),(-.65,-1),(.65,-1),(.85,-.87),(.98,-.60),(1,-.30)]
    rr=[[(x+rx*a,y,z+rz*b) for a,b in section] for y,rx,rz,z,x in rings]
    for j in range(len(rr)-1):
        for i in range(len(section)):
            k=(i+1)%len(section)
            pts=[rr[j][i],rr[j+1][i],rr[j+1][k],rr[j][k]]
            material=base
            if soft:
                height=(section[i][1]+section[k][1])/2
                material=(185,197,203) if height>.45 else ((141,162,176) if height>-.3 else (99,123,140))
            face(pts,material,normal=unit(cross(sub(pts[1],pts[0]),sub(pts[3],pts[0]))),tint=0 if soft else (j%3-1))
    face(list(reversed(rr[0])),base,normal=(0,-1,0))
    face(rr[-1],base,normal=(0,1,0))
    return rr

# Faceted lifting cabin, an asymmetrical roof profile and a low instrument nose.
body=[(-170,48,27,5,0),(-148,72,39,9,0),(-105,83,44,13,0),(-42,85,47,15,0),(28,80,47,16,0),(85,70,40,12,0),(126,57,30,2,0),(159,41,19,-8,0),(176,27,10,-12,0)]
def smooth_stations(rings):
    result=[]
    for i in range(len(rings)-1):
        p0=rings[max(0,i-1)];p1=rings[i];p2=rings[i+1];p3=rings[min(len(rings)-1,i+2)]
        for j in range(6):
            t=j/6
            values=[p1[0]+(p2[0]-p1[0])*t]
            for k in range(1,5):values.append(.5*(2*p1[k]+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t*t*t))
            result.append(tuple(values))
    return result+[rings[-1]]
body=smooth_stations(body)
angular_loft(body,soft=True)
def hull_at(y,a=1,b=1):
    aa,bb=next((aa,bb) for aa,bb in zip(body,body[1:]) if aa[0]<=y<=bb[0])
    t=(y-aa[0])/(bb[0]-aa[0])
    rx=aa[1]+(bb[1]-aa[1])*t;rz=aa[2]+(bb[2]-aa[2])*t;z=aa[3]+(bb[3]-aa[3])*t
    return(a*rx,y,z+b*rz)

# Short swept shoulders carry the propulsion pods. Thin leading edges make
# these actual wings rather than detached decorative cylinders.
for side in [-1,1]:
    pp=[(side*60,-126,-9),(side*74,-18,-12),(side*130,8,-6),(side*138,-151,-9),
        (side*60,-126,-2),(side*74,-18,-5),(side*130,8,1),(side*138,-151,-2)]
    solid(pp,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],(143,158,166))
    line([(side*80,-109,0),(side*120,-128,0)],'#bfd0d6',.8,3)
    line([(side*82,-54,-1),(side*119,-57,1)],'#536b7a',1,3)
    # Compact hexagonal engine fairings; no red franchise-style collector caps.
    x=side*130
    rings=[(-184,6,7,-9,x),(-166,18,16,-7,x),(-116,22,18,-5,x),(-48,22,18,-3,x),(19,18,15,-1,x),(63,12,11,0,x),(79,3,5,0,x)]
    angular_loft(rings,(144,164,176))
    def pod_at(y,a,b):
        aa,bb=next((aa,bb) for aa,bb in zip(rings,rings[1:]) if aa[0]<=y<=bb[0])
        t=(y-aa[0])/(bb[0]-aa[0]);rx=aa[1]+(bb[1]-aa[1])*t;rz=aa[2]+(bb[2]-aa[2])*t;z=aa[3]+(bb[3]-aa[3])*t
        return(x+a*rx,y,z+b*rz)
    # Recessed blue ion-channel tiles, separated by structural ribs.
    for j in range(18):
        y=-152+j*9
        channel=[pod_at(yy,a,b) for yy,a,b in [(y-.5,1.035,.41),(y+8.5,1.035,.41),(y+8.5,1.035,-.32),(y-.5,1.035,-.32)]]
        decal(channel,'#243f53',25)
        line([channel[0],channel[1]],'#a5c9d9',.7,27)
        pts=[pod_at(yy,a,b) for yy,a,b in [(y,1.025,.30),(y+6.8,1.025,.30),(y+6.8,1.025,-.20),(y,1.025,-.20)]]
        decal(pts,'url(#driveGlass)',30)
        line([pts[0],pts[1]],'#b8eeff',.55,32)
    for y in [-147,-110,-73,-36,1,37]:
        line([pod_at(y,-.66,1.025),pod_at(y,.66,1.025)],'#586f7e',.65,3)
    for j in range(8):
        y=-132+j*15
        line([pod_at(y,-.35,1.04),pod_at(y+6,-.35,1.04)],'#344b59',1.5,4)
    # Forward manoeuvring jets and amber approach lights.
    p=pod_at(63,.72,.55)
    line([p,add(p,(0,7,-2))],'#e6b36e',1.9,6)

# A small swept stabiliser and a roof-mounted environmental sensor mast.
fin=[(-3,-160,31),(-3,-148,91),(-3,-133,86),(-3,-100,56),(3,-160,31),(3,-148,91),(3,-133,86),(3,-100,56)]
solid(fin,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(0,3,7,4)],(167,183,192))
line([(3.3,-148,91),(3.3,-133,86)],'#d5e2e7',.9,5)
line([(3.2,-145,78),(3.2,-133,67)],'#de9f65',1.4,5)
line([(0,-53,64),(0,-53,80)],'#a6bac7',1.5,3)
line([(-7,-53,80),(7,-53,80)],'#9ec9d9',1.5,3)

# Roof plating follows the real hull stations. Alternating insets add scale.
for y in [-133,-111,-82,-55,-28,0]:
    line([hull_at(y,-.66,1.025),hull_at(y,.66,1.025)],'#718896',.55,4)
for a in [-.54,.54]:
    line([hull_at(y,a,1.025) for y in [-140,-110,-70,-30,9]],'#849aa5',.6,4)
for side in [-1,1]:
    line([hull_at(y,side*.665,1.016) for y in range(-140,131,9)],'#d2dfe3',.8,8)
    line([hull_at(y,side*.98,-.33) for y in range(-139,141,9)],'#283f50',1.2,8)
for side in [-1,1]:
    for j in range(4):
        y=-124+j*23
        points=[hull_at(yy,side*a,1.03) for yy,a in [(y,.12),(y+13,.12),(y+13,.39),(y,.39)]]
        decal(points,'#a7b8c1' if j%2 else '#92a8b5',8)
        line([points[0],points[1]],'#c0ced2',.6,6)

# A broad, three-pane cockpit on the sloping upper bow, with a visible frame.
glass=[(-51,35,65),(51,35,65),(39,131,34),(-39,131,34)]
# Three trapezoidal panes share the same physical plane.
for lo,hi in [(-.94,-.35),(-.29,.29),(.35,.94)]:
    surround=[(lo*51,35,65),(hi*51,35,65),(hi*39,131,34),(lo*39,131,34)]
    decal(surround,'#1c303d',60)
    pts=[(lo*51,39,64.2),(hi*51,39,64.2),(hi*39,126,36.6),(lo*39,126,36.6)]
    decal(pts,'url(#cockpitGlass)',62)
    # A crisp reflection gives the glazing depth without raster shine.
    decal([(lo*51,40,64.4),(hi*51,40,64.4),(hi*44,87,49.4),(lo*44,87,49.4)],'url(#glassReflection)',90)
    line([pts[0],pts[1]],'#c4dbe4',.75,66)
    line([pts[2],pts[3]],'#507588',.55,66)
for a,b in zip(glass,glass[1:]+glass[:1]):line([a,b],'#819eaf',1.8,66)
line([glass[0],glass[1]],'#e0e8e8',.7,68)

# Side glazing, access hatch and service panels on the visible starboard flank.
side_glass=[hull_at(y,1.025,b) for y,b in [(-30,.40),(44,.40),(44,.06),(-30,.06)]]
decal(side_glass,'url(#cockpitGlass)',32)
for y in [-10,17]:line([hull_at(y,1.04,.07),hull_at(y,1.04,.40)],'#b6ccd6',1,34)
door=[hull_at(y,1.025,b) for y,b in [(-120,.44),(-63,.44),(-63,-.49),(-120,-.49)]]
decal(door,'#718a9b',32)
for a,b in zip(door,door[1:]+door[:1]):line([a,b],'#ccd8dc',.7,34)
line([hull_at(-77,1.04,.10),hull_at(-77,1.04,-.04)],'#e3d1a7',1.3,36)
line([hull_at(-115,1.06,-.56),hull_at(-67,1.06,-.56)],'#b1c9d6',1.6,36)
for y in [-111,-102,-93,-84,-75]:
    line([hull_at(y,1.055,-.43),hull_at(y+3,1.055,-.43)],'#ddbb82',1,35)
for y in [-138,-48,48,91,135]:
    line([hull_at(y,1.02,.44),hull_at(y,1.02,-.43)],'#536b79',.55,8)
for j in range(6):
    y=-112+j*9
    line([hull_at(y,1.04,-.63),hull_at(y+4,1.04,-.63)],'#dbd6be',.9,10)

# Independent forward sensor assembly, recessed below the cockpit.
sensor=[(-25,176,-6),(25,176,-6),(22,178,-18),(-22,178,-18)]
decal(sensor,'#263c4e',15)
for x in [-17,-7,7,17]:line([(x,179,-8),(x,180,-15)],'#74cce3',1.8,17)
line([(-18,170,0),(18,170,0)],'#d2d9d2',.7,8)

# Instrument lenses, thrusters and restrained identification stencils.
for x in [-10,0,10]:
    p=(x,180,-11);xx,yy=proj(p)
    faces.append((dot(p,V)+21,f'<circle cx="{n(xx)}" cy="{n(yy)}" r="1.2" fill="#b4e8f4"/>'))
for y in [92,117,141]:
    p=hull_at(y,1.05,-.05)
    line([p,add(p,(0,2.5,0))],'#283b49',2.3,24)
    line([add(p,(.5,0,.8)),add(p,(.5,2.5,.8))],'#e1c391',.65,25)
def stencil(text,p,size,along=(1,0,0),down=(0,1,0),colour='#405669'):
    x,y=proj(p);a,b=proj(along);c,d=proj(down)
    label=f'<text transform="matrix({n(a)} {n(b)} {n(c)} {n(d)} {n(x)} {n(y)})" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="700" letter-spacing="1" fill="{colour}">{escape(text)}</text>'
    faces.append((dot(p,V)+45,label))
stencil('AR04',(0,-91,63),10)
stencil('AR04',hull_at(-96,1.06,.28),7,(0,-1,0),(0,0,-1),'#d4e1e5')

# Tiny emissive approach beacons. The animation affects only these points.
for p,c,delay in [((53,120,34),'#8ce1ce','0s'),((-53,120,34),'#e4a778','1.6s'),((136,58,11),'#94d9f5','.8s'),((-136,58,11),'#94d9f5','2.4s')]:
    x,y=proj(p)
    faces.append((dot(p,V)+24,f'<g class="status-beacon" style="animation-delay:{delay}"><circle cx="{n(x)}" cy="{n(y)}" r="2.4" fill="{c}" opacity=".2"/><circle cx="{n(x)}" cy="{n(y)}" r=".95" fill="{c}"/></g>'))


ship=''.join(m for depth,m in sorted(faces,key=lambda f:f[0]))
# Share the paint definitions instead of repeating stroke/fill on every surface.
paints={}
def paint(m):
    colour=m.group(1)
    if colour not in paints:paints[colour]='h'+str(len(paints))
    return 'class="'+paints[colour]+'"'
ship=re.sub(r'fill="(#[a-f0-9]+)" stroke="\1" stroke-width="\.22" stroke-linejoin="round"',paint,ship)
styles=''.join('.'+cls+'{fill:'+c+';stroke:'+c+'}' for c,cls in paints.items())
styles+='@keyframes statusPulse{0%,55%,100%{opacity:.32}65%,82%{opacity:1}}@keyframes starTwinkle{0%,100%{opacity:.35}50%{opacity:1}}.status-beacon{animation:statusPulse 3.8s ease-in-out infinite}.star-twinkle{animation:starTwinkle 7.2s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.status-beacon,.star-twinkle{animation:none;opacity:1}}'
defs='<defs><linearGradient id="cockpitGlass" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="#74aec6"/><stop offset=".33" stop-color="#305d78"/><stop offset="1" stop-color="#0b2032"/></linearGradient><linearGradient id="glassReflection" x1="0" y1="0" x2=".7" y2="1"><stop stop-color="#e0f1f8" stop-opacity=".65"/><stop offset=".4" stop-color="#a0c9dc" stop-opacity=".22"/><stop offset="1" stop-color="#71a1c4" stop-opacity="0"/></linearGradient><linearGradient id="driveGlass" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#abebff"/><stop offset=".35" stop-color="#4faee0"/><stop offset="1" stop-color="#1b5f9d"/></linearGradient></defs>'
ship=defs+'<style>'+styles+'</style><g stroke-width=".22" stroke-linejoin="round">'+ship+'</g>'

def txt(x,y,text,size=16,fill='#cc99cc',anchor=None,weight=None,spacing=None):
    a=f' x="{x}" y="{y}" fill="{fill}" font-size="{size}"'
    if anchor:a+=f' text-anchor="{anchor}"'
    if weight:a+=f' font-weight="{weight}"'
    if spacing:a+=f' letter-spacing="{spacing}"'
    return f'<text{a}>{escape(text)}</text>'
def rect(x,y,w,h,fill,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'
def start(w,h,title,desc):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc><rect width="{w}" height="{h}" fill="#000"/><g font-family="Arial,Helvetica,sans-serif">'
title='Arndt Bohrenkämper: personal LCARS terminal'
desc='An independently designed fictional survey shuttle in a detailed three-quarter view. A sculpted metallic cabin with rounded shoulders, reflective three-pane cockpit glazing, recessed blue drive channels, service hatches and a forward sensor array sit within a dark exploration console. A visible star field surrounds the craft. Small status lights pulse slowly across several systems, with a few stars twinkling. Reduced-motion preferences disable all animation.'

def chart(x,y,w,h):
    random.seed(47)
    s=f'<g stroke="#1a2735" stroke-width=".6" fill="none">'
    s+=f'<path d="M{x} {y+h*.55}H{x+w}M{x+w*.4} {y}V{y+h}"/>'
    for r in [h*.24,h*.44]:s+=f'<ellipse cx="{x+w*.4}" cy="{y+h*.55}" rx="{r*1.65}" ry="{r}"/>'
    s+='</g><g fill="#627d9a">'
    for i in range(27):
        xx=x+random.random()*w; yy=y+random.random()*h
        s+=f'<circle cx="{n(xx)}" cy="{n(yy)}" r="{.8 if i%3 else 1.4}"/>'
    s+='</g>'
    s+=f'<path d="M{x+15} {y+h-12}L{x+w*.4} {y+h*.55}L{x+w-16} {y+15}" fill="none" stroke="#6f6085" stroke-width="1" stroke-dasharray="3 6"/>'
    return s

def starfield(x,y,w,h,count,seed):
    rng=random.Random(seed);out=[]
    for i in range(count):
        xx=x+rng.random()*w;yy=y+rng.random()*h
        radius=1.35 if i%13==0 else (.9 if i%3==0 else .65)
        colour=['#b6c9df','#e2dfd0','#8eb9d2'][i%3]
        animated=i%9==0
        attrs=f' class="star-twinkle" style="animation-delay:-{n(rng.random()*7.2)}s"' if animated else f' opacity="{n(.5+rng.random()*.35)}"'
        out.append(f'<g{attrs}><circle cx="{n(xx)}" cy="{n(yy)}" r="{radius}" fill="{colour}"/>')
        if i%19==0:out.append(f'<path d="M{n(xx-2.5)} {n(yy)}h5M{n(xx)} {n(yy-2.5)}v5" fill="none" stroke="{colour}" stroke-width=".45"/>')
        out.append('</g>')
    return ''.join(out)

s=start(1000,790,title,desc)
s+='<path d="M20 114V60Q20 20 60 20H171V46H81Q78 46 78 63V114Z" fill="#ff9966"/>'
s+=rect(184,20,584,12,'#ff9966')+rect(778,20,202,12,'#cc99cc',6)
s+=txt(105,96,'ARNDT BOHRENKÄMPER',46,'#ffcc99',weight='700')
s+=txt(107,126,'PERSONAL TERMINAL  /  EXPLORATION & RESEARCH',18,'#cc99cc',spacing=1.4)
s+=txt(978,68,'LCARS',20,'#cc99cc',anchor='end',weight='700')+txt(978,92,'47 / AR04',15,'#ff9966',anchor='end')
for y,h,c,label in [(122,95,'#cc99cc','01'),(225,70,'#a38abd','02'),(303,141,'#ff9966','03'),(452,74,'#ffcc99','04'),(534,105,'#879ab9','05')]:
    s+=rect(20,y,58,h,c)+txt(70,y+h-11,label,14,'#15111a',anchor='end',weight='700')
s+=txt(105,166,'SURVEY SHUTTLE',29,'#cc99cc',weight='700')+txt(105,192,'AR04  /  INDEPENDENT RESEARCH CRAFT',18,'#ffcc99',spacing=1)
s+=txt(978,142,'INDEPENDENT EXPLORATION CRAFT',14,'#a6b4cc',anchor='end')
s+=txt(978,164,'VESSEL STATUS  /  NOMINAL',14,'#ff9966',anchor='end')
# Visible stars remain behind the craft, with only a few slowly twinkling.
s+=starfield(111,209,863,387,130,47)
s+='<path d="M112 201H172M112 201V229M978 201H918M978 201V229M112 582H172M112 582V554M978 582H918M978 582V554" fill="none" stroke="#465267" stroke-width="1"/>'
s+='<g transform="translate(530 407) scale(1.7)">'+ship+'</g>'
# Fine callout tracks stay outside the main silhouette.
s+='<g fill="none" stroke="#746582" stroke-width=".8"><path d="M188 285H254L293 321"/><path d="M924 249H843L811 280"/><path d="M180 550H309L377 507"/></g>'
s+=txt(118,276,'PRIMARY HULL',11,'#b3a0c6',spacing=1)+txt(922,240,'PROPULSION PODS',11,'#b3a0c6',anchor='end',spacing=1)+txt(118,567,'FORWARD SENSOR ARRAY',11,'#b3a0c6',spacing=.8)
s+=rect(105,613,875,7,'#cc99cc',3)
# Three subordinate technical views.
s+=txt(105,649,'01  LONG-RANGE SENSORS',16,'#ff9966',weight='700')
s+=chart(105,661,250,72)+txt(105,755,'SECTOR 001  /  SOL SYSTEM',13,'#a6b4cc')
s+=txt(398,649,'02  PROPULSION',16,'#cc99cc',weight='700')
s+=txt(398,682,'DRIVE FIELD',14,'#b6bdd0')+txt(655,682,'STABLE',14,'#99ccee',anchor='end')
for i in range(18):
    if i==14:s+='<g class="status-beacon" style="animation-delay:1.2s">'
    s+=rect(398+i*14.5,696,10.5,23,'#99bbee' if i<15 else '#273446',2)
    if i==14:s+='</g>'
s+=txt(398,755,'TWIN DRIVE PODS / SYNCHRONISED',13,'#a6b4cc')
s+=txt(707,649,'03  SCIENCE OPERATIONS',16,'#ff9966',weight='700')
for y,l,v in [(681,'SENSORS','ONLINE'),(708,'NAVIGATION','ALIGNED'),(735,'MISSION','EXPLORATION')]:s+=txt(707,y,l,13,'#a6b4cc')+txt(978,y,v,13,'#ffcc99',anchor='end')
s+='<g class="status-beacon" style="animation-delay:.7s"><circle cx="850" cy="677" r="2.6" fill="#99ccee"/></g>'
s+='<g class="status-beacon" style="animation-delay:2s"><circle cx="850" cy="704" r="2.6" fill="#ffcc99"/></g>'
s+='<path d="M20 649V730Q20 772 62 772H78V649Z" fill="#cc99cc"/>'+rect(105,773,875,5,'#cc99cc',2)
s+='</g></svg>'
(ROOT/'assets/lcars-starship.svg').write_text(s)

s=start(420,650,title,desc)
s+='<path d="M12 97V39Q12 12 39 12H84V30H48Q34 30 34 44V97Z" fill="#ff9966"/>'+rect(96,12,312,7,'#cc99cc',3)
s+=txt(48,72,'ARNDT',36,'#ffcc99',weight='700')+txt(48,108,'BOHRENKÄMPER',36,'#ffcc99',weight='700')
s+=txt(48,136,'PERSONAL TERMINAL / LCARS 47',16,'#cc99cc',spacing=.6)
s+=rect(12,105,22,124,'#cc99cc')+rect(12,237,22,110,'#ff9966')+rect(12,355,22,70,'#879ab9')
s+=txt(48,177,'SURVEY SHUTTLE',25,'#cc99cc',weight='700')+txt(48,202,'AR04 / RESEARCH CRAFT',17,'#ffcc99')
s+=starfield(48,212,357,208,65,104)
s+='<g transform="translate(205 325) scale(.8)">'+ship+'</g>'
s+=rect(48,426,360,5,'#cc99cc',2)
s+=txt(48,462,'EXPLORATION SYSTEMS',18,'#ff9966',weight='700')
for y,l,v in [(495,'SENSORS','ONLINE'),(523,'DRIVE FIELD','STABLE'),(551,'NAVIGATION','ALIGNED')]:s+=txt(48,y,l,16,'#b6bdd0')+txt(406,y,v,16,'#ffcc99',anchor='end')
s+='<g class="status-beacon" style="animation-delay:.7s"><circle cx="240" cy="491" r="2.6" fill="#99ccee"/></g>'
s+='<g class="status-beacon" style="animation-delay:1.2s"><circle cx="240" cy="519" r="2.6" fill="#99ccee"/></g>'
s+='<g class="status-beacon" style="animation-delay:2s"><circle cx="240" cy="547" r="2.6" fill="#ffcc99"/></g>'
s+=chart(48,570,145,51)
s+=txt(222,590,'SECTOR 001',16,'#cc99cc')+txt(222,615,'SOL SYSTEM',15,'#99bbee')
s+='<path d="M12 433V610Q12 638 34 638V433Z" fill="#cc99cc"/>'+rect(48,634,360,4,'#cc99cc',2)
s+='</g></svg>'
(ROOT/'assets/lcars-starship-mobile.svg').write_text(s)
print(f'Generated {len(faces)} vector surfaces and details; desktop {len((ROOT/"assets/lcars-starship.svg").read_bytes()):,} bytes.')
