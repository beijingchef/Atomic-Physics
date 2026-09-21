from pathlib import Path
from math import sin, cos, radians
from html import escape

out=Path('images/dipole-radiation.svg'); out.parent.mkdir(exist_ok=True)
theta,phi=radians(40),radians(20)
def project(v):
    x,y,z=v
    return (-.8660254038*x+.5*y,.25*x+.4330127019*y-.8660254038*z)
er=(sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta))
et=(cos(theta)*cos(phi),cos(theta)*sin(phi),-sin(theta))
ep=(-sin(phi),cos(phi),0)
cross=(et[1]*ep[2]-et[2]*ep[1],et[2]*ep[0]-et[0]*ep[2],et[0]*ep[1]-et[1]*ep[0])
assert max(abs(a-b) for a,b in zip(cross,er))<1e-12
O=(560,385)
def pos(v,s=1,o=O):
    x,y=project(v); return (o[0]+s*x,o[1]+s*y)
P=pos(er,430)
Q=pos((er[0],er[1],0),430)
parts=['''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="545" viewBox="0 0 1000 545" role="img" aria-labelledby="title desc">
<title id="title">Electric dipole and the spherical basis</title>
<desc id="desc">A dipole on the z axis, spherical angles theta and phi, and field point at position vector r. The field point shows the right-handed radial, polar, and azimuthal unit vectors.</desc>
<defs>''']
colors={'axis':'#657585','radial':'#14745b','electric':'#bb3838','magnetic':'#285ca8','dark':'#263746'}
for key,color in colors.items():
    parts.append(f'<marker id="{key}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{color}"/></marker>')
parts.append('</defs><style>text {font-family: "DejaVu Sans", Arial, sans-serif; fill:#263746; font-size:19px} .small {font-size:17px} .label {font-family: "DejaVu Serif", Georgia, serif;font-style:italic;font-size:25px} .vector {font-weight:700} .heading {font-size:23px;font-weight:600}</style><rect width="1000" height="545" fill="white"/>\n<text x="38" y="42" class="heading">Dipole and spherical coordinate unit vectors</text>')
def line(a,b,key='axis',width=2,arrow=False,dash=False):
    parts.append(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="{colors[key]}" stroke-width="{width}"'+(f' marker-end="url(#{key})"' if arrow else '')+(' stroke-dasharray="6 5"' if dash else '')+'/>')
def text(x,y,s,cls='label',color=None):
    parts.append(f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}"'+(f' style="fill:{color}"' if color else '')+f'>{escape(s)}</text>')
def curve(points):
    parts.append('<polyline points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+'" fill="none" stroke="#657585" stroke-width="1.8"/>')
for v,s,label,dx,dy in [((1,0,0),270,'x',-25,10),((0,1,0),310,'y',10,10),((0,0,1),310,'z',-22,-6)]:
    end=pos(v,s);line(O,end,arrow=True);text(end[0]+dx,end[1]+dy,label)
line(O,Q,dash=True);line(Q,P,dash=True)
line(Q,pos((er[0],0,0),430),dash=True)
line(Q,pos((0,er[1],0),430),dash=True)
curve([pos((sin(t)*cos(phi),sin(t)*sin(phi),cos(t)),104) for t in [theta*i/40 for i in range(41)]])
curve([pos((cos(f),sin(f),0),110) for f in [phi*i/40 for i in range(41)]])
text(523,307,'θ');text(458,430,'φ')
line(O,P,'dark',2.8,True);text(445,310,'r','label')
text(O[0]-24,O[1]+22,'O')
# The dipole orientation is shown without assigning instantaneous charge signs.
line((560,350),(560,420),'dark',5)
parts.append('<circle cx="560" cy="350" r="7" fill="white" stroke="#263746" stroke-width="2"/><circle cx="560" cy="420" r="7" fill="white" stroke="#263746" stroke-width="2"/>')
text(680,330,'Dipole axis','small');line((672,335),(570,357),'axis',1)
parts.append('<text x="680" y="366" class="label"><tspan class="vector">p</tspan><tspan>(t) = p(t) </tspan><tspan class="vector">ẑ</tspan></text>')
for vec,key,label,scale,dx,dy in [(er,'radial','r̂',82.5,-30,-12),(et,'electric','θ̂',82.5,-30,25),(ep,'magnetic','φ̂',82.5,12,6)]:
    end=pos(vec,scale,P);line(P,end,key,4,True);text(end[0]+dx,end[1]+dy,label,'label vector',color=colors[key])
parts.append(f'<circle cx="{P[0]:.2f}" cy="{P[1]:.2f}" r="5" fill="#263746"/>')
text(P[0]+18,P[1]-20,'r','label vector')
parts.append('</svg>')
out.write_text('\n'.join(parts),encoding='utf-8')
print(out)


