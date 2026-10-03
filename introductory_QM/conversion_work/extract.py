from pathlib import Path
import zipfile,xml.etree.ElementTree as E,re,json
base=Path('introductory_QM');work=base/'conversion_work';out=base/'english';src=base/'量子力学简介4.9e.docx'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';M='http://schemas.openxmlformats.org/officeDocument/2006/math';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
ns={'w':W,'m':M}; rows=[];tokens={}; media={}; notes={}
equations=json.loads((work/'equations.json').read_text(encoding='utf-8'))
def tag(x):return x.tag.split('}')[-1]
def math(x):
 t=tag(x);cs=list(x)
 def c(n):return ''.join(math(a) for a in cs if tag(a)==n)
 def prop(group,n,default):
  y=x.find('m:'+group+'/m:'+n,ns)
  return y.get('{'+M+'}val',default) if y is not None else default
 if t.endswith('Pr'):return ''
 if t=='t':return x.text or ''
 if t=='f':return r'\frac{'+c('num')+'}{'+c('den')+'}'
 if t=='sSup':return '{'+c('e')+'}^{'+c('sup')+'}'
 if t=='sSub':return '{'+c('e')+'}_{'+c('sub')+'}'
 if t=='sSubSup':return '{'+c('e')+'}_{'+c('sub')+'}^{'+c('sup')+'}'
 if t=='sPre':return '{}_{'+c('sub')+'}^{'+c('sup')+'}'+c('e')
 if t=='rad':return r'\sqrt'+('['+c('deg')+']' if c('deg') else '')+'{'+c('e')+'}'
 if t=='d':
  a=prop('dPr','begChr','(');b=prop('dPr','endChr',')');sep=prop('dPr','sepChr','|')
  conv={'{':r'\{','}':r'\}','‖':r'\Vert','⟨':r'\langle','⟩':r'\rangle','〈':r'\langle','〉':r'\rangle','':'.'}
  return r'\left'+conv.get(a,a)+' '+sep.join(math(y) for y in cs if tag(y)=='e')+r'\right'+conv.get(b,b)+' '
 if t=='nary':
  ch=prop('naryPr','chr','∫');return ch+('_{'+c('sub')+'}' if c('sub') else '')+('^{'+c('sup')+'}' if c('sup') else '')+' '+c('e')
 if t=='acc':
  ch=prop('accPr','chr','̂');cmd={'̂':'hat','⃗':'vec','̇':'dot','̈':'ddot','̅':'overline','̃':'tilde'}.get(ch,'hat');return '\\'+cmd+'{'+c('e')+'}'
 if t=='bar':return r'\overline{'+c('e')+'}'
 if t=='eqArr':return r'\begin{aligned}'+r'\\'.join(math(y) for y in cs if tag(y)=='e')+r'\end{aligned}'
 if t=='m':return r'\begin{matrix}'+r'\\'.join(math(y) for y in cs if tag(y)=='mr')+r'\end{matrix}'
 if t=='mr':return '&'.join(math(y) for y in cs if tag(y)=='e')
 if t=='limLow':return c('e')+'_{'+c('lim')+'}'
 if t=='limUpp':return c('e')+'^{'+c('lim')+'}'
 return ''.join(math(y) for y in cs)
def token(s):
 key='X'+str(len(tokens)+1);tokens[key]=s;return '[['+key+']]'
with zipfile.ZipFile(src) as z:
 rel={x.get('Id'):x.get('Target') for x in E.fromstring(z.read('word/_rels/document.xml.rels'))}
 root=E.fromstring(z.read('word/document.xml'))
 def image(x):
  if tag(x)=='object':
   ole=next((a for a in x.iter() if tag(a)=='OLEObject'),None)
   if ole is not None:
    path='word/'+rel[ole.get('{'+R+'}id')]
    if path in equations:return token(equations[path])
  found=[]
  for a in x.iter():
   rid=a.get('{'+R+'}embed') or (a.get('{'+R+'}id') if tag(a)=='imagedata' else None)
   if not rid:continue
   target=rel[rid];name=Path(target).name
   width=height=None
   for shape in x.iter():
    if tag(shape)=='shape':
     st=shape.get('style','');mw=re.search(r'width:([\d.]+)pt',st);mh=re.search(r'height:([\d.]+)pt',st)
     if mw:width=float(mw[1])*4/3
     if mh:height=float(mh[1])*4/3
    if tag(shape)=='extent' and shape.get('cx'):
     width=int(shape.get('cx'))/9525;height=int(shape.get('cy'))/9525
   vector=Path(name).suffix in ['.wmf','.emf'];dest=out/'assets'/name
   if not dest.exists():dest.write_bytes(z.read('word/'+target))
   if vector:
    width=width or 200;height=height or 30
    rec=media.setdefault(name,{'width':0,'height':0});rec['width']=max(rec['width'],width);rec['height']=max(rec['height'],height)
    name=Path(name).stem+'.png'
   label='Equation' if tag(x)=='object' else 'Figure'
   attr=''
   if width:attr='{width='+str(round(width))+'px'+(' .equation-image' if label=='Equation' else '')+'}'
   found.append(token('!['+label+'](assets/'+name+')'+attr))
  return ''.join(found)
 def content(x):
  t=tag(x)
  if t in ['pPr','rPr','del']:return ''
  if t=='instrText':
   m=re.search(r'\bREF\s+(ZEqnNum\w+)',x.text or '')
   return '[[REF:'+m[1]+']]' if m else ''
  if t=='oMath':return token('$'+math(x)+'$')
  if t=='t':return x.text or ''
  if t in ['drawing','pict','object']:return image(x)
  if t=='tab':return ' '
  if t=='br':return ' '
  if t in ['footnoteReference','endnoteReference']:return '[^'+t[0]+x.get('{'+W+'}id')+']'
  if t=='AlternateContent':
   children=list(x);return content(children[0]) if children else ''
  return ''.join(content(a) for a in x)
 def paragraph(p,context='body'):
  st=p.find('w:pPr/w:pStyle',ns);style=st.get('{'+W+'}val','') if st is not None else ''
  s=content(p).strip();num=p.find('w:pPr/w:numPr',ns)
  rows.append({'id':len(rows),'style':style,'text':s,'context':context,'list':num is not None,'bookmarks':[a.get('{'+W+'}name') for a in p.findall('w:bookmarkStart',ns)],'fields':[a.text for a in p.findall('.//w:instrText',ns)]})
 for b in root.find('w:body',ns):
  if tag(b)=='p':paragraph(b)
  elif tag(b)=='tbl':
   rows.append({'id':len(rows),'style':'TableStart','text':'','context':'table','list':False})
   for ri,tr in enumerate(b.findall('w:tr',ns)):
    for ci,tc in enumerate(tr.findall('w:tc',ns)):
     rows.append({'id':len(rows),'style':'CellStart','text':f'{ri},{ci}','context':'table','list':False})
     for p in tc.findall('w:p',ns):paragraph(p,'table')
   rows.append({'id':len(rows),'style':'TableEnd','text':'','context':'table','list':False})
 for part in ['footnotes','endnotes']:
  path='word/'+part+'.xml'
  if path in z.namelist():
   rp='word/_rels/'+part+'.xml.rels'
   rel={x.get('Id'):x.get('Target') for x in E.fromstring(z.read(rp))} if rp in z.namelist() else {}
   for note in E.fromstring(z.read(path)):
    nid=note.get('{'+W+'}id')
    if int(nid)>0:
     rows.append({'id':len(rows),'style':'NoteStart','text':part[0]+nid,'context':'note','list':False})
     for p in note.findall('w:p',ns):paragraph(p,'note')
for r in rows:
 if re.search(r'[\u4e00-\u9fff]',r['text']) and not r['style'].startswith('TOC'):print(f"{r['id']} [{r['style']}] {r['text']}")
(work/'rows.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'tokens.json').write_text(json.dumps(tokens,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'media.json').write_text(json.dumps(media,indent=2),encoding='utf-8')
print('TOTAL',len(rows),'TOKENS',len(tokens),'VECTOR',len(media))


