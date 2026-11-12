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
U=(.2236,.2236,-.9487)
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

# Stardrive: rounded, tapered organic engineering body, not a triangular block.
hull=[(-290,2,2,0,0),(-274,14,6,-1,0),(-248,25,12,-4,0),(-216,36,19,-9,0),(-175,45,28,-15,0),(-125,49,35,-23,0),(-76,46,40,-28,0),(-26,38,37,-31,0),(12,31,29,-32,0),(40,26,22,-31,0),(58,19,15,-30,0),(66,2,2,-30,0)]
loft(hull,48)
# Swept wing-like pylons, lower hull to nacelle supports.
for side in [-1,1]:
    p=[(side*25,-180,2),(side*34,-215,0),(side*175,-260,53),(side*169,-226,58),(side*25,-180,9),(side*34,-215,7),(side*175,-260,60),(side*169,-226,65)]
    solid(p,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(3,2,6,7),(1,5,6,2),(0,3,7,4)],(142,157,166))
    line([(side*51,-215,14),(side*163,-247,60)],'#637b8b',.8)
    line([(side*49,-201,13),(side*163,-233,63)],'#b2bfc4',.65)

# High forward-swept neck, merging the saucer into the engineering section.
neck=[(-136,17,8,7,0),(-98,23,11,18,0),(-58,30,13,33,0),(-15,37,13,49,0),(22,45,10,62,0),(42,32,5,65,0)]
loft(neck,32,(143,156,166))
for side in [-1,1]:
    for row in range(4):
        z=22+row*7
        for j in range(7):
            y=-88+j*9
            x=side*(24+(y+88)*.18)
            if z<30+(y+88)*.45:
                line([(x,y,z),(x,y+3,z+.8)],'#e9d3a1',.85)

# Matched nacelles, identical dimensions in model space; long cobalt warp grilles.
for side in [-1,1]:
    x=side*172
    rings=[(-345,1,1,63,x),(-332,8,7,64,x),(-314,14,11,65,x),(-280,17,13,66,x),(-230,18,14,67,x),(-180,18,15,68,x),(-130,18,15,69,x),(-85,17,14,70,x),(-55,15,12,70,x),(-36,10,9,70,x),(-29,1,1,70,x)]
    loft(rings,40,(144,161,173))
    # Broad blue field-coil faces follow the outer upper shoulder.
    def nacpoint(y,a):
        aa,bb=next((aa,bb) for aa,bb in zip(rings,rings[1:]) if aa[0]<=y<=bb[0])
        t=(y-aa[0])/(bb[0]-aa[0])
        rx=aa[1]+(bb[1]-aa[1])*t+.6
        rz=aa[2]+(bb[2]-aa[2])*t+.6
        z=aa[3]+(bb[3]-aa[3])*t
        return(x+rx*cos(a),y,z+rz*sin(a))
    for angle in [pi*.10,pi*.72]:
        for j in range(24):
            y=-303+j*9.4
            a0,a1=angle,angle+.54
            pts=[nacpoint(yy,a) for yy,a in [(y,a0),(y+8.2,a0),(y+8.2,a1),(y,a1)]]
            normal=(cos(angle+.15),0,sin(angle+.15))
            if dot(normal,V)>0:
                decal(pts,'#3faff6',24)
                line([pts[0],pts[1]],'#b7e5ff',.5,24)
    # Dark spine and inset maintenance seams.
    line([(x,-314,77),(x,-72,85)],'#526775',2)
    line([(x+5,-301,78),(x+5,-82,84)],'#c1cbd0',.65)
    for y in [-295,-257,-219,-181,-143,-105]:
        line([(x-11,y,77),(x+9,y,81)],'#647885',.65)
    # Red forward Bussard collectors have a warm shell and curved frontal face.
    centre=(x,-36,70)
    for j in range(5):
        r0=j/5; r1=(j+1)/5
        for i in range(32):
            a=2*pi*i/32;b=2*pi*(i+1)/32
            pts=[(x+11*r*cos(t),-31+5*r*r,70+9*r*sin(t)) for r,t in [(r0,a),(r1,a),(r1,b),(r0,b)]]
            face(pts,colour=['#ffdeb1','#ffb470','#f78054','#c34838','#742e2d'][j],normal=(0,1,0))
    line([(x-8,-30,73),(x-3,-29,77)],'#ffe3ba',1)

# Primary hull: a family of compressed ovals. Every panel is projected in 3-D.
CX,CY,CZ=0,105,72
def saucer(r,t,top=True):
    # Shallow upper decks; rolled edge and thicker lower central hull.
    ztop=72+17*(1-r*r)**1.8+6*max(0,1-r/.23)
    zbottom=65-18*(1-r*r)**1.7
    return (238*r*cos(t),105+174*r*sin(t),ztop if top else zbottom)
rad=[0,.12,.23,.34,.45,.56,.67,.77,.86,.93,.98,1]
for top in [False,True]:
    for j in range(len(rad)-1):
        r0,r1=rad[j:j+2]
        for i in range(112):
            a=2*pi*i/112;b=2*pi*(i+1)/112
            pts=[saucer(r,t,top) for r,t in [(r0,a),(r1,a),(r1,b),(r0,b)]]
            mid=(a+b)/2
            if top:norm=unit((.12*r1*cos(mid),.17*r1*sin(mid),1))
            else:norm=unit((.12*r1*cos(mid),.17*r1*sin(mid),-1))
            # Aztec plating is intentionally subtle, distributed by concentric decks.
            tint=((i//2+j*3)%7-3)*1.1
            face(pts,(161,175,183) if top else (105,126,141),normal=norm,tint=tint)
    # Phaser strips, panel seams and restrained concentric deck boundaries.
    if top:
        for r in [.23,.34,.56,.77,.93]:
            for i in range(112):
                a=2*pi*i/112;b=2*pi*(i+1)/112
                line([saucer(r,a),saucer(r,b)],'#7e939f',.38)
        for i in range(40):
            a=2*pi*i/40
            line([saucer(.25,a),saucer(.97,a)],'#8398a2',.35)
        for i in range(104):
            a=2*pi*i/104;b=a+2*pi/104
            if sin(a)>-.62:line([saucer(.86,a),saucer(.86,b)],'#3b4b54',2.6)
        # Paired rows of inset windows on upper saucer decks.
        for rr in [.49,.64,.735,.965]:
            count=round(rr*138)
            for i in range(count):
                a=2*pi*i/count
                if i%11 in [0,1]:continue
                p=saucer(rr,a)
                delta=.008 if rr>.7 else .01
                q=saucer(rr,a+delta)
                line([add(p,(0,0,.8)),add(q,(0,0,.8))],'#e3dcc4' if i%6 else '#425e72',1.05)

# Rolled saucer rim, visible forward surface with multi-deck windows.
for i in range(160):
    a=2*pi*i/160;b=2*pi*(i+1)/160
    norm=(cos((a+b)/2),sin((a+b)/2),0)
    if dot(norm,V)<0:continue
    pts=[saucer(1,a,True),saucer(1,b,True),saucer(1,b,False),saucer(1,a,False)]
    face(pts,(145,161,172),normal=norm)
    for z in [67.2,70.2]:
        p=(238*cos(a),105+174*sin(a),z)
        q=(238*cos(a+.014),105+174*sin(a+.014),z)
        if i%8!=0:line([p,q],'#f4e1ba' if i%5 else '#263e52',.85,1)
    line([(238*cos(a),105+174*sin(a),64.8),(238*cos(b),105+174*sin(b),64.8)],'#384e5b',.6)

# Dorsal command module and bridge: deliberately tiny against the saucer.
loft([(81,1,1,95,0),(86,9,3,97,0),(102,16,4,98,0),(117,14,4,98,0),(126,7,2,97,0),(128,1,1,97,0)],32,(180,191,193))
loft([(98,1,1,102,0),(101,6,3,103,0),(109,7,4,103,0),(117,4,2,103,0),(120,1,1,102,0)],24,(192,202,202))
line([(-6,119,100),(5,119,100)],'#293c4a',1.4)
# Aft impulse engines and main shuttlebay.
for side in [-1,1]:
    pts=[(side*59,-38,83),(side*82,-29,82),(side*83,-26,79),(side*59,-34,80)]
    decal(pts,'#7b312b',1)
    line([(side*62,-36,83),(side*79,-29,82)],'#ed815a',1.5,1)

# Hull windows and longitudinal plating lines.
for side in [-1,1]:
    for row in [0,1,2]:
        for j in range(20):
            y=-245+j*13
            # Interpolate the real hull radius at this station.
            seg=next(((a,b) for a,b in zip(hull,hull[1:]) if a[0]<=y<=b[0]),None)
            if not seg:continue
            a,b=seg;t=(y-a[0])/(b[0]-a[0])
            rx=a[1]+(b[1]-a[1])*t;rz=a[2]+(b[2]-a[2])*t;zc=a[3]+(b[3]-a[3])*t
            angle=-.72+row*.38
            p=(side*rx*cos(angle),y,zc+rz*sin(angle))
            if side==1:line([p,add(p,(0,4,0))],'#e6d7b6' if j%4 else '#304c62',.85,8)
    line([(side*13,-268,3),(side*25,-232,5),(side*41,-181,8),(side*44,-126,10),(side*39,-75,6)],'#617b8b',.7)

# Eye-shaped navigational deflector, nested curved rings at the bow.
# Front plane is tilted upwards, making the dish readable from this viewpoint.
for j in range(10,0,-1):
    rr=j/10
    pts=[]
    for i in range(64):
        a=2*pi*i/64
        xx=30*rr*cos(a)
        zz=16*rr*sin(a)*(1-.2*abs(cos(a)))
        pts.append((xx,70+zz*.35+4*(1-rr),-31+zz))
    colour=['#a9efff','#82d9f9','#59bceb','#338ecb','#1f6f9f','#245675','#bca16d','#766744','#d0bb86','#405461'][j-1]
    decal(pts,colour,16)
line([(-9,75,-29),(9,75,-29)],'#bceeff',.65,17)
# Navigation lights: small hard highlights instead of a broad neon glow.
for p,c in [((237,105,72),'#ef796f'),((-237,105,72),'#8ed9ac'),((0,279,71),'#e9f7ff'),((0,-282,7),'#f8d3b5')]:
    x,y=proj(p);faces.append((dot(p,V)+2,f'<circle cx="{n(x)}" cy="{n(y)}" r="1.2" fill="{c}"/>'))

# Registry laid onto the projected upper saucer surface, kept small and authentic.
def surface_text(text,x,y,z,size,spacing=1):
    # Local x/y basis mapped into screen space; font top rises towards vessel aft.
    px,py=proj((x,y,z))
    a,b=R[0],U[0];c,d=R[1],U[1]
    markup=f'<text transform="matrix({a} {b} {c} {d} {n(px)} {n(py)})" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="700" letter-spacing="{spacing}" fill="#273c4c">{escape(text)}</text>'
    faces.append((dot((x,y,z),V)+2,markup))
surface_text('NCC-1701-D',0,213,79,12,1.4)
surface_text('U.S.S. ENTERPRISE',0,196,82,5.5,.7)

ship=''.join(m for depth,m in sorted(faces,key=lambda f:f[0]))
# Share the paint definitions instead of repeating stroke/fill on every surface.
paints={}
def paint(m):
    colour=m.group(1)
    if colour not in paints:paints[colour]='h'+str(len(paints))
    return 'class="'+paints[colour]+'"'
ship=re.sub(r'fill="(#[a-f0-9]+)" stroke="\1" stroke-width="\.22" stroke-linejoin="round"',paint,ship)
styles=''.join('.'+cls+'{fill:'+c+';stroke:'+c+'}' for c,cls in paints.items())
ship='<style>'+styles+'</style><g stroke-width=".22" stroke-linejoin="round">'+ship+'</g>'

def txt(x,y,text,size=16,fill='#cc99cc',anchor=None,weight=None,spacing=None):
    a=f' x="{x}" y="{y}" fill="{fill}" font-size="{size}"'
    if anchor:a+=f' text-anchor="{anchor}"'
    if weight:a+=f' font-weight="{weight}"'
    if spacing:a+=f' letter-spacing="{spacing}"'
    return f'<text{a}>{escape(text)}</text>'
def rect(x,y,w,h,fill,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'
def start(w,h,title,desc):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc><rect width="{w}" height="{h}" fill="#000"/><g font-family="Arial,Helvetica,sans-serif">'
title='Arndt Bohrenkämper — personal LCARS terminal'
desc='An original three-quarter vector illustration of the Galaxy-class U.S.S. Enterprise NCC-1701-D: broad elliptical saucer, detailed engineering hull, twin blue warp nacelles, illuminated windows and a blue navigational deflector. Fictional Starfleet telemetry frames the personal exploration logbook.'

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

s=start(1000,790,title,desc)
s+='<path d="M20 114V60Q20 20 60 20H171V46H81Q78 46 78 63V114Z" fill="#ff9966"/>'
s+=rect(184,20,584,12,'#ff9966')+rect(778,20,202,12,'#cc99cc',6)
s+=txt(105,96,'ARNDT BOHRENKÄMPER',46,'#ffcc99',weight='700')
s+=txt(107,126,'PERSONAL TERMINAL  /  EXPLORATION & RESEARCH',18,'#cc99cc',spacing=1.4)
s+=txt(978,68,'LCARS',20,'#cc99cc',anchor='end',weight='700')+txt(978,92,'47 • 1701-D',15,'#ff9966',anchor='end')
for y,h,c,label in [(122,95,'#cc99cc','01'),(225,70,'#a38abd','02'),(303,141,'#ff9966','03'),(452,74,'#ffcc99','04'),(534,105,'#879ab9','05')]:
    s+=rect(20,y,58,h,c)+txt(70,y+h-11,label,14,'#15111a',anchor='end',weight='700')
s+=txt(105,166,'U.S.S. ENTERPRISE',29,'#cc99cc',weight='700')+txt(105,192,'NCC-1701-D  /  GALAXY CLASS',18,'#ffcc99',spacing=1)
s+=txt(978,142,'STARFLEET EXPLORATORY VESSEL',14,'#a6b4cc',anchor='end')
s+=txt(978,164,'VESSEL STATUS  /  NOMINAL',14,'#ff9966',anchor='end')
# Sparse stars stay subordinate to the hull.
random.seed(1701)
for i in range(48):
    x=random.randint(110,972);y=random.randint(195,575)
    s+=f'<circle cx="{x}" cy="{y}" r="{.7 if i%4 else 1.1}" fill="#506077" opacity=".65"/>'
s+='<path d="M112 201H172M112 201V229M978 201H918M978 201V229M112 582H172M112 582V554M978 582H918M978 582V554" fill="none" stroke="#465267" stroke-width="1"/>'
s+='<g transform="translate(531 422) scale(1.17)">'+ship+'</g>'
# Fine callout tracks stay outside the main silhouette.
s+='<g fill="none" stroke="#746582" stroke-width=".8"><path d="M188 285H254L293 321"/><path d="M924 249H843L811 280"/><path d="M180 550H309L377 507"/></g>'
s+=txt(118,276,'PRIMARY HULL',11,'#b3a0c6',spacing=1)+txt(922,240,'WARP FIELD COILS',11,'#b3a0c6',anchor='end',spacing=1)+txt(118,567,'NAVIGATIONAL DEFLECTOR',11,'#b3a0c6',spacing=.8)
s+=rect(105,613,875,7,'#cc99cc',3)
# Three subordinate technical views.
s+=txt(105,649,'01  LONG-RANGE SENSORS',16,'#ff9966',weight='700')
s+=chart(105,661,250,72)+txt(105,755,'SECTOR 001  /  SOL SYSTEM',13,'#a6b4cc')
s+=txt(398,649,'02  PROPULSION',16,'#cc99cc',weight='700')
s+=txt(398,682,'WARP FIELD',14,'#b6bdd0')+txt(655,682,'STABLE',14,'#99ccee',anchor='end')
for i in range(18):s+=rect(398+i*14.5,696,10.5,23,'#99bbee' if i<15 else '#273446',2)
s+=txt(398,755,'DUAL NACELLES  /  SYNCHRONISED',13,'#a6b4cc')
s+=txt(707,649,'03  SCIENCE OPERATIONS',16,'#ff9966',weight='700')
for y,l,v in [(681,'SENSORS','ONLINE'),(708,'NAVIGATION','ALIGNED'),(735,'MISSION','EXPLORATION')]:s+=txt(707,y,l,13,'#a6b4cc')+txt(978,y,v,13,'#ffcc99',anchor='end')
s+='<path d="M20 649V730Q20 772 62 772H78V649Z" fill="#cc99cc"/>'+rect(105,773,875,5,'#cc99cc',2)
s+='</g></svg>'
(ROOT/'assets/lcars-starship.svg').write_text(s)

s=start(420,650,title,desc)
s+='<path d="M12 97V39Q12 12 39 12H84V30H48Q34 30 34 44V97Z" fill="#ff9966"/>'+rect(96,12,312,7,'#cc99cc',3)
s+=txt(48,72,'ARNDT',36,'#ffcc99',weight='700')+txt(48,108,'BOHRENKÄMPER',36,'#ffcc99',weight='700')
s+=txt(48,136,'PERSONAL TERMINAL / LCARS 47',16,'#cc99cc',spacing=.6)
s+=rect(12,105,22,124,'#cc99cc')+rect(12,237,22,110,'#ff9966')+rect(12,355,22,70,'#879ab9')
s+=txt(48,177,'U.S.S. ENTERPRISE',25,'#cc99cc',weight='700')+txt(48,202,'NCC-1701-D / GALAXY CLASS',17,'#ffcc99')
s+='<g transform="translate(200 332) scale(.53)">'+ship+'</g>'
s+=rect(48,426,360,5,'#cc99cc',2)
s+=txt(48,462,'EXPLORATION SYSTEMS',18,'#ff9966',weight='700')
for y,l,v in [(495,'SENSORS','ONLINE'),(523,'WARP FIELD','STABLE'),(551,'NAVIGATION','ALIGNED')]:s+=txt(48,y,l,16,'#b6bdd0')+txt(406,y,v,16,'#ffcc99',anchor='end')
s+=chart(48,570,145,51)
s+=txt(222,590,'SECTOR 001',16,'#cc99cc')+txt(222,615,'SOL SYSTEM',15,'#99bbee')
s+='<path d="M12 433V610Q12 638 34 638V433Z" fill="#cc99cc"/>'+rect(48,634,360,4,'#cc99cc',2)
s+='</g></svg>'
(ROOT/'assets/lcars-starship-mobile.svg').write_text(s)
print(f'Generated {len(faces)} vector surfaces and details; desktop {len((ROOT/"assets/lcars-starship.svg").read_bytes()):,} bytes.')
