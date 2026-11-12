"""Build a cutaway cabin from the shared shuttle mesh, in vessel coordinates."""
from pathlib import Path
import json, math
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'docs/shuttle.json'; model=json.loads(p.read_text())
faces=[]; lines=[]
def clip(points):
    out=[]
    for a,b in zip(points,points[1:]+points[:1]):
        if a[2]<=0:out.append(a)
        if (a[2]<=0)!=(b[2]<=0):
            t=-a[2]/(b[2]-a[2]);out.append([a[i]+t*(b[i]-a[i]) for i in range(3)])
    return out
for f in model['faces']:
    pod=all(abs(v[0])>89 for v in f['p'])
    pts=f['p'] if pod else clip(f['p'])
    if len(pts)>=3:faces.append({**f,'p':pts})
for l in model['lines']:
    if all(v[2]<=0 or abs(v[0])>89 for v in l['p']):lines.append(l)
def poly(points,c,n=None):
    if n is None:
        a,b,d=points[:3];u=[b[i]-a[i] for i in range(3)];v=[d[i]-a[i] for i in range(3)]
        n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];m=math.hypot(*n) or 1;n=[x/m for x in n]
    faces.append({'p':points,'c':c,'n':n,'kind':'interior'})
def box(x,y,z,w,d,h,c):
    pts=[[x-w/2,y-d/2,z],[x+w/2,y-d/2,z],[x+w/2,y+d/2,z],[x-w/2,y+d/2,z],[x-w/2,y-d/2,z+h],[x+w/2,y-d/2,z+h],[x+w/2,y+d/2,z+h],[x-w/2,y+d/2,z+h]]
    for ix,n in [([0,3,2,1],[0,0,-1]),([4,5,6,7],[0,0,1]),([0,1,5,4],[0,-1,0]),([1,2,6,5],[1,0,0]),([2,3,7,6],[0,1,0]),([3,0,4,7],[-1,0,0])]:poly([pts[i] for i in ix],c,n)
def track(points,c='#b7a2c8',w=.7):lines.append({'p':points,'c':c,'w':w,'bias':.3})
# Broad non-slip deck, tapered at the instrument nose. Low side sills retain the silhouette.
for y in range(-135,145,10):
    def width(yy):return 63 if yy<0 else 63-yy*.16
    def height(yy):return -2 if yy<90 else -2-(yy-90)*.2
    for i in range(8):
        a=-1+i/4;b=a+.25
        poly([[a*width(y),y,height(y)],[b*width(y),y,height(y)],[b*width(y+10),y+10,height(y+10)],[a*width(y+10),y+10,height(y+10)]],'#42535c',[0,0,1])
for x in [-65,65]:
    box(x,-67,0,5,130,13,'#b4bbb8')
    track([[x,-128,13.2],[x,-5,13.2]],'#f3ba82',1.3)
for y in range(-120,71,18):track([[-55,y,-1.6],[55,y,-1.6]],'#586970',.4)
for x in [-13,13]:track([[x,-125,-1.3],[x,50,-1.3]],'#a9b8ba',.65)
# Pilots face forward, towards the instrument nose (+Y).
for x in [-28,28]:
    box(x,27,-1,10,12,8,'#242f38')
    box(x,30,7,25,25,6,'#86739d')
    box(x,18,10,25,6,27,'#71658b')
    box(x,18,36,18,6,6,'#9a8bab')
    for side in [-1,1]:box(x+side*13,29,14,3,23,4,'#bec3bf')
    track([[x-9,18.1,23],[x+9,18.1,23]],'#ad9dbd',.7)
# Angled LCARS flight consoles: dark work surfaces with amber/lavender strips.
for x in [-28,28]:
    box(x,77,0,47,28,13,'#a7b3b3')
    surface=[[x-23,63,13.4],[x+23,63,13.4],[x+23,91,24],[x-23,91,24]]
    for j in range(7):
        y0=63+j*4;y1=y0+4
        z0=13.4+(y0-63)*10.6/28;z1=13.4+(y1-63)*10.6/28
        poly([[x-23,y0,z0],[x+23,y0,z0],[x+23,y1,z1],[x-23,y1,z1]],'#111b25',[0,-.35,.94])
    def tile(a,b,w,d,c):
        z=lambda yy:13.7+(yy-63)*10.6/28
        poly([[a,b,z(b)],[a+w,b,z(b)],[a+w,b+d,z(b+d)],[a,b+d,z(b+d)]],c,[0,-.35,.94])
    tile(x-20,66,7,20,'#eea172');tile(x-11,82,28,4,'#c4a0d1')
    for i in range(4):
        tile(x-10+i*7,68,5,3,'#88bed7');tile(x-10+i*7,74,5,3,'#d3a5c8')
    tile(x+15,66,4,12,'#efc891')
box(0,65,0,6,32,12,'#c1c6be')
# Rear cabin: bench, supply lockers, compact work station and central hatch.
box(-49,-67,0,23,62,7,'#a6b1b2');box(-49,-67,7,24,59,5,'#8c789e')
box(-60,-67,12,5,63,17,'#716184')
for y in [-86,-67,-48]:track([[-58,y,12.2],[-39,y,12.2]],'#c7b1d0',.8)
box(48,-88,0,26,47,25,'#8d9eaa')
for y in [-103,-88,-73]:
    box(48,y,25,22,12,1,'#b8c4c3');track([[44,y,26.3],[52,y,26.3]],'#edb583',1)
box(46,-29,0,28,35,15,'#a8b4b6');box(46,-29,15,29,36,2,'#172632')
for i in range(4):box(40+i*4,-25,17,2,14,.6,['#f1b07e','#c4a0d1','#99ccee','#c4a0d1'][i])
# Aft bulkhead and the closed double hatch; sectioned at shoulder height.
box(-43,-132,0,39,5,29,'#a6b2b5');box(43,-132,0,39,5,29,'#a6b2b5')
box(-11,-133,0,21,4,28,'#657889');box(11,-133,0,21,4,28,'#657889')
track([[0,-130.8,0],[0,-130.8,28]],'#c0cfcd',.9)
for x in [-20,20]:track([[x,-130.5,3],[x,-130.5,26]],'#e8b080',1)
box(30,-128,15,5,2,9,'#d6ab84')
model['interior']={'faces':faces,'lines':lines,'labels':[],'beacons':[]}
def compact(value):
    if isinstance(value,float):return round(value,3)
    if isinstance(value,list):return [compact(v) for v in value]
    if isinstance(value,dict):return {k:compact(v) for k,v in value.items()}
    return value
p.write_text(json.dumps(compact(model),separators=(',',':')))
print('Interior:',len(faces),'surfaces,',len(lines),'detail lines')
