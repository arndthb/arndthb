from pathlib import Path
from html import escape
import re

ROOT=Path(__file__).resolve().parents[1]/'assets'
ORANGE='#ff9966'; LAVENDER='#cc99cc'; GOLD='#ffcc99'; BLUE='#99bbee'; INK='#000000'; WHITE='#eee8e5'
# Helvetica/Arial advance widths in em units. Conservative wrapping leaves room
# for fallback-font differences without relying on external fonts or foreignObject.
WIDTHS={**dict.fromkeys('ilI.,:;!|',.278),**dict.fromkeys('frt()',.333),**dict.fromkeys(' ',.278),**dict.fromkeys('mw',.778),**dict.fromkeys('MW',.89),**dict.fromkeys('ABCDEFGHKNOPQRSTUVXYZ',.69),**dict.fromkeys('J',.5),**dict.fromkeys('abcdeghknopqsuvxyz0123456789',.556),**dict.fromkeys('L',.556),**dict.fromkeys('j',.222),**dict.fromkeys('—',1.0),**dict.fromkeys('–',.556),**dict.fromkeys('’\'',.222)}
def measure(s,size): return sum(WIDTHS.get(c,.6) for c in s)*size
def wrap(s,size,width):
    result=[]; current=''
    for word in s.split():
        trial=(current+' '+word).strip()
        if current and measure(trial,size)>width-12: result.append(current); current=word
        else: current=trial
    if current:result.append(current)
    return result

SECTIONS=[
 {'title':'PERSONAL LOG','deck':'IDENTITY / BACKGROUND','colour':ORANGE,'meta':['SUBJECT: ARNDT BOHRENKÄMPER','CURIOUS · OPERATIONAL · STILL LEARNING'],
 'entries':[
 ('p',"Personal log. I've spent a fair amount of time exploring the wonderful universe of computers."),
 ('p','Some people collect stamps; I collect questions about how technology works — and spare cables.'),
 ('p',"My route hasn't followed a standard flight plan: entrepreneurship, leadership and IT consulting."),
 ('p','The best discoveries often begin with a simple question: Why does it work like that?'),
 ('p','Current interests: artificial intelligence, cybersecurity, Linux and connected systems.')]},
 {'title':'MISSION LOG','deck':'AQVIONIS / SECURITY RESEARCH','colour':LAVENDER,'meta':['CLASSIFICATION: EXPERIMENTAL RESEARCH','STATUS: IN PROGRESS'],
 'entries':[
 ('feature','AQVIONIS'),
 ('p','Mission objective: explore AI-assisted detection of suspicious behaviour in infrastructure.'),
 ('p','Connect observations across systems and time to reconstruct attack paths and aid investigation.'),
 ('row','SEC-01','AI-assisted threat hunting and anomaly detection'),
 ('row','OBS-02','Infrastructure, MCP and AI-agent observability'),
 ('row','GRAPH-03','Threat graphs and attack-path visualisation'),
 ('row','SIM-04','Counterfactual simulations'),
 ('row','MEM-05','Long-term threat memory'),
 ('row','HUM-06','Human–AI collaboration in security operations'),
 ('note',"SCIENCE OFFICER'S NOTE",'Research in progress — not a production-ready security product.')]},
 {'title':'SCIENCE LOG','deck':'AREAS OF EXPLORATION','colour':BLUE,'meta':['DIRECTIVE: EXPLORE · EXPERIMENT · UNDERSTAND'],
 'entries':[
 ('row','COMPUTER CORE','Linux · Containers · Kubernetes · Automation · Networking'),
 ('row','AI LABORATORY','AI agents · Local language models · Machine learning · AI security'),
 ('row','SECURITY ARRAY','Threat hunting · Observability · Attack graphs · Security research'),
 ('row','PHILOSOPHY DECK','Intelligence · Consciousness · The origins and possibilities of life'),
 ('p',"The ship's computer is excellent at answering questions."),
 ('p','I find the unanswered ones even more interesting.')]},
 {'title':'OFF-DUTY LOG','deck':'BEYOND THE KEYBOARD','colour':ORANGE,'meta':['LOCATION: BETWEEN THE HOLODECK','AND THE COMPUTER LAB'],
 'entries':[
 ('row','STAR TREK',"Exploration, science and imagining a better tomorrow."),
 ('row','RETRO GAMING','Classic point-and-click adventures; the stranger the inventory, the better.'),
 ('row','COMPUTERS','Hardware, operating systems and occasionally unnecessary experiments.'),
 ('row','MARTIAL ARTS','Shotokan Karate and Okinawan Kobudō (Jinbukan tradition).'),
 ('p','Different disciplines, familiar lessons: patience, practice and attention to detail.')]},
 {'title':"CAPTAIN’S LOG",'deck':'GUIDING PRINCIPLES','colour':LAVENDER,'meta':['STANDING ORDERS: NEVER STOP EXPLORING'],
 'entries':[
 ('p','Stay curious. Learn the fundamentals. Question assumptions. Improve what you can.'),
 ('p',"Admit what you don't know. Then find out."),
 ('p','The universe is far too interesting to stop asking questions.')]}
]

def build(mobile=False):
    w=420 if mobile else 1000
    x=48 if mobile else 105; right=w-(18 if mobile else 20); cw=right-x
    size=18 if mobile else 22; line=27 if mobile else 32
    out=[]
    def rect(a,b,c,d,col,rx=0):out.append(f'<rect x="{a}" y="{b}" width="{c}" height="{d}"'+(f' rx="{rx}"' if rx else '')+f' fill="{col}"/>')
    def path(d,col):out.append(f'<path d="{d}" fill="{col}"/>')
    def text(s,a,b,sz=18,col=WHITE,weight=None,anchor=None):
        out.append(f'<text x="{a}" y="{b}" font-size="{sz}" fill="{col}"'+(f' font-weight="{weight}"' if weight else '')+(f' text-anchor="{anchor}"' if anchor else '')+f'>{escape(s)}</text>')
    def lines(s,y,sz=size,col=WHITE,weight=None):
        for l in wrap(s,sz,cw): text(l,x,y,sz,col,weight);y+=line
        return y
    # The heading shares the hero's elbow and the log sections' left rail.
    if mobile:
        rect(12,0,22,20,LAVENDER);rect(48,0,354,8,LAVENDER)
        text('PERSONAL LOGBOOK',x,48,25,GOLD,'bold')
        text('ARNDT BOHRENKÄMPER',x,79,20,WHITE,'bold')
        text('TO BOLDLY GO WHERE NO ONE',x,111,14,LAVENDER)
        text('HAS GONE BEFORE',x,131,14,LAVENDER)
        y=165
    else:
        rect(20,0,58,24,LAVENDER);rect(105,0,875,10,LAVENDER)
        text('PERSONAL LOGBOOK',x,58,34,GOLD,'bold')
        text('ARNDT BOHRENKÄMPER',right,58,25,WHITE,'bold','end')
        text('TO BOLDLY GO WHERE NO ONE HAS GONE BEFORE',x,93,18,LAVENDER)
        text('LCARS 47 / LOG ACCESS',right,93,16,LAVENDER,None,'end')
        y=130
    for i,sec in enumerate(SECTIONS,1):
        top=y;c=sec['colour']; railx=12 if mobile else 20;railw=22 if mobile else 58
        # Flat band with a continuous elbow; body is pure black, not a card.
        if mobile:
            path(f'M{railx} {y+39}V{y+25}Q{railx} {y} {railx+25} {y}H{right}V{y+7}H{railx+34}Q{railx+22} {y+7} {railx+22} {y+25}V{y+39}Z',c)
            text(f'{i:02}',x,y+32,15,c,'bold')
            text(sec['title'],x+35,y+32,24,WHITE,'bold')
            y+=59
            y=lines(sec['deck'],y,15,c,'bold')
            y+=1
        else:
            path(f'M20 {y+70}V{y+42}Q20 {y} 62 {y}H980V{y+10}H101Q78 {y+10} 78 {y+34}V{y+70}Z',c)
            text(f'{i:02}',49,y+54,24,INK,'bold','middle')
            text(sec['title'],x,y+52,31,WHITE,'bold')
            text(sec['deck'],right,y+52,17,c,None,'end')
            y+=89
        for m in sec['meta']:
            # A paired location is kept semantically complete, just reflowed.
            y=lines(m,y,14 if mobile else 16,c)
        y+=10 if mobile else 12
        for entry in sec['entries']:
            kind=entry[0]
            if kind=='feature':
                text(entry[1],x,y+(7 if mobile else 14),37 if mobile else 48,c,'bold'); y+=57 if mobile else 70
            elif kind=='p':
                y=lines(entry[1],y);y+=11 if mobile else 12
            elif kind=='row':
                text(entry[1],x,y,14 if mobile else 16,c,'bold');y+=24 if mobile else 26
                y=lines(entry[2],y);y+=11 if mobile else 12
            elif kind=='note':
                rect(x,y-4,cw,1,c);y+=25
                text(entry[1],x,y,13 if mobile else 16,c,'bold');y+=25
                y=lines(entry[2],y,17 if mobile else 21,GOLD);y+=8
        bottom=y+5
        # Segment the left column, as on a TNG terminal, leaving black breaks.
        first=top+(47 if mobile else 78);height=bottom-first
        if height>80:
            split=round(height*.64)
            rect(railx,first,railw,split,c)
            rect(railx,first+split+6,railw,height-split-6,LAVENDER if c!=LAVENDER else ORANGE)
        else:rect(railx,first,railw,height,c)
        if not mobile:
            text(f'47-{i:03}',49,bottom-14,11,INK,None,'middle')
        rect(x,bottom-4,cw,4,c)
        y=bottom+(38 if mobile else 36)
    if mobile:
        rect(12,y,22,67,LAVENDER);rect(48,y,354,8,LAVENDER)
        text('END OF PERSONAL LOG',x,y+34,15,LAVENDER,'bold')
        text('LIVE LONG AND PROSPER',x,y+60,20,GOLD,'bold');h=y+85
    else:
        path(f'M20 {y}H78V{y+15}Q78 {y+37} 101 {y+37}H980V{y+49}H62Q20 {y+49} 20 {y+7}Z',LAVENDER)
        text('END OF PERSONAL LOG',x,y+21,17,LAVENDER,'bold')
        text('LIVE LONG AND PROSPER',right,y+21,24,GOLD,'bold','end');h=y+69
    desc='Complete personal logbook of Arndt Bohrenkämper: personal background; AQVIONIS experimental AI-assisted security research; computing, AI, security and philosophy; Star Trek, retro gaming and martial arts; curiosity and lifelong learning. Readable '+('mobile' if mobile else 'desktop')+' layout with orange and lavender LCARS rails on black.'
    header=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="log-title log-description">\n<title id="log-title">Arndt Bohrenkämper — personal LCARS logbook</title>\n<desc id="log-description">{escape(desc)}</desc>\n<rect width="{w}" height="{h}" fill="#000000"/>\n<g font-family="Arial, Helvetica, sans-serif">\n'
    result=header+'\n'.join(out)+'\n</g>\n</svg>\n'
    target=ROOT/('lcars-logbook-mobile.svg' if mobile else 'lcars-logbook.svg')
    target.write_text(result)
    print(target.name,w,h,len(result.encode()))

def link(mobile=False):
    w=420 if mobile else 1000;h=128 if mobile else 84
    x=48 if mobile else 105;rx=12 if mobile else 20;rw=22 if mobile else 58
    right=w-(18 if mobile else 20)
    title='Open AQVIONIS mission file on GitHub — research access required'
    body=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="link-title link-description">\n<title id="link-title">{title}</title>\n<desc id="link-description">Access the private AQVIONIS research repository. Repository access is required. Experimental AI-assisted security research.</desc>\n<rect width="{w}" height="{h}" fill="#000000"/>\n<rect x="{rx}" y="0" width="{rw}" height="{h-18}" fill="{ORANGE}"/>\n<path d="M{x} 0H{right-26}Q{right} 0 {right} 26V{h-18}H{x}Z" fill="{ORANGE}"/>\n<g font-family="Arial, Helvetica, sans-serif" fill="#000000" font-weight="bold">\n'
    if mobile:
        body+=f'<text x="{x+15}" y="29" font-size="15">OPEN MISSION FILE</text>\n<text x="{x+15}" y="60" font-size="25">AQVIONIS</text>\n<text x="{x+15}" y="93" font-size="14">PRIVATE RESEARCH REPOSITORY</text>\n<path d="M{right-49} 40h26m-11-11 11 11-11 11" fill="none" stroke="#000000" stroke-width="3"/>\n'
    else:
        body+=f'<text x="{x+22}" y="43" font-size="24">OPEN MISSION FILE / AQVIONIS</text>\n<text x="{right-68}" y="41" font-size="15" text-anchor="end">PRIVATE RESEARCH REPOSITORY</text>\n<path d="M{right-48} 33h26m-11-11 11 11-11 11" fill="none" stroke="#000000" stroke-width="3"/>\n'
    body+='</g>\n</svg>\n'
    (ROOT/('lcars-aqvionis-link-mobile.svg' if mobile else 'lcars-aqvionis-link.svg')).write_text(body)

if __name__=='__main__':
    for m in (False,True):build(m);link(m)
