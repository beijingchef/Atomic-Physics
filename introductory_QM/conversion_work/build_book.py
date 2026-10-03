from pathlib import Path
import json,re,collections
from math_normalize import normalize
work=Path(__file__).resolve().parent; out=work.parent/'english';out.mkdir(exist_ok=True)
rows=json.loads((work/'rows.json').read_text(encoding='utf8'));raw=json.loads((work/'tokens.json').read_text(encoding='utf8'))
translations={int(a):b for a,b in (l.split('\t',1) for l in (work/'translations.tsv').read_text(encoding='utf-8-sig').splitlines() if '\t' in l)}
translations[1388]=translations[1388].replace('Its matrix form is','The matrix form of [[REF:ZEqnNum188299]] is')
translations[1442]=translations[1442].replace('Increasing detuning increases the oscillation frequency','Increasing detuning increases the oscillation frequency of [[X1368]]')
translations[141]=translations[141].replace('Every result for [[X32]] is [[X33]]','All particles ([[X32]]) give [[X33]]').replace('gives [[X36]] equal to [[X37]] every time','gives [[X37]] for all particles ([[X36]])')
tokens={k:normalize(k,v) for k,v in raw.items()}
(work/'normalized-math.json').write_text(json.dumps({k:v for k,v in tokens.items() if v and not v.startswith(('!','[^'))},ensure_ascii=False,indent=2),encoding='utf8')
chapters=['01-vectors-and-quantum-states','02-operators','03-quantum-measurement','04-commutation-relations','05-time-evolution','06-transitions','07-continuous-observables','08-angular-momentum','09-coupling-angular-momenta','10-topics-in-atomic-physics','11-appendices','12-exercise-solutions']
refmap={};labels={};chap=0;display_ids=set();unresolved=set();ambiguous=[]
def keys(s):return re.findall(r'\[\[(X\d+)\]\]',s)
def is_display(r):
 s=translations.get(r['id'],r['text']);ks=keys(s)
 if not ks or any(tokens[k].startswith('!') for k in ks):return False
 remaining=re.sub(r'\[\[.*?\]\]','',s)
 return not re.search(r'[A-Za-z0-9\u4e00-\u9fff]',remaining)
for r in rows:
 if r['style']=='Heading1':chap+=1
 if r['id']<132 or r['context']=='note':continue
 bookmarks=[b for b in r.get('bookmarks',[]) if b.startswith('ZEqnNum')]
 if is_display(r) and r['context']!='table':
  label='eq-'+(bookmarks[0].lower() if bookmarks else f'ch{chap:02d}-p{r["id"]:04d}')
  labels[r['id']]=label;display_ids.add(r['id'])
  for b in bookmarks:refmap[b]=label
 elif bookmarks:ambiguous.append((r['id'],bookmarks,r['text']))
# Any bookmark attached to prose refers to the formula embedded there; promote that
# formula to a display at its original position and retain the surrounding prose.
for rid,bookmarks,s in ambiguous:
 ks=[k for k in keys(s) if not tokens[k].startswith('!')]
 if len(ks)==1 or rid==1942:
  label='eq-'+bookmarks[0].lower();labels[rid]=label
  for b in bookmarks:refmap[b]=label
 else:print('AMBIGUOUS BOOKMARK',rid,bookmarks,s)
refmap['ZEqnNum281']=refmap['ZEqnNum281628']
refmap['ZEqnNum9353']=refmap['ZEqnNum935342']
refmap['ZEqnNum417391']=labels[1092]
allrefs=set(re.findall(r'\[\[REF:([^]]+)\]\]',' '.join(r['text'] for r in rows)))
print('MISSING REFERENCES',sorted(allrefs-refmap.keys()))
def expand(s):
 def tok(m):
  v=tokens[m[1]]
  return v if v.startswith(('!','[^')) or not v else '$'+v+'$'
 s=re.sub(r'\[\[(X\d+)\]\]',tok,s)
 def ref(m):
  if m[1] not in refmap:unresolved.add(m[1]);return '[MISSING EQUATION '+m[1]+']'
  return '@'+refmap[m[1]]
 s=re.sub(r'\[\[REF:([^]]+)\]\]',ref,s)
 return s
notes={};nid=None
for r in rows:
 if r['style']=='NoteStart':nid=r['text'];notes[nid]=[]
 elif r['context']=='note' and r['text']:notes[nid].append(expand(translations.get(r['id'],r['text'])))
files={};current='index';files[current]=['# Preface {.unnumbered}',*[expand(translations[i]) for i in [129,130,131]],'## References {.unnumbered}',*[expand(translations[i]) for i in [125,126]]];ch=0;table=None;cell=None
for r in rows:
 rid=r['id'];style=r['style']
 if rid<132 or r['context']=='note':continue
 s=translations.get(rid,r['text'])
 if re.search('[\u4e00-\u9fff]',s):raise ValueError(('Untranslated',rid))
 if style=='Heading1':
  current=chapters[ch];ch+=1;files[current]=['# '+expand(s).replace('* ',r'\* ',1)];continue
 if style=='TableStart':table={};continue
 if style=='CellStart':cell=tuple(map(int,s.split(',')));table[cell]=[];continue
 if style=='TableEnd':
  nr=max(x[0] for x in table)+1;nc=max(x[1] for x in table)+1
  lines=[]
  for ri in range(nr):
   line='| '+' | '.join(' '.join(table.get((ri,ci),[])) for ci in range(nc))+' |';lines.append(line)
   if ri==0:lines.append('| '+' | '.join('---' for _ in range(nc))+' |')
  files[current].append('\n'.join(lines));table=None;continue
 if not s:continue
 if rid in [1203,1205]:
  dk='X1038' if rid==1203 else 'X1056'
  files[current].append('$$\n'+tokens[dk]+'\n$$ {#eq-measurement-paths-'+str(rid)+'}\n\nFigure '+('4.7. A selected sequence of measurement outcomes; other channels are blocked.' if rid==1203 else '4.8. All intermediate channels are open.'))
  for k in (['X1038','X1039','X1040'] if rid==1203 else ['X1056','X1057']):s=s.replace('[['+k+']]','')
  s=s.strip()
 if rid==2253:
  figures=['X2340','X2341','X2342','X2343','X2344','X2345']
  files[current].append('::: {layout-ncol=3}\n\n'+'\n\n'.join(tokens[k] for k in figures)+'\n\n:::')
  files[current].append('Figure 9.1. Vector illustrations of the triplet and singlet formed by coupling two spin-1/2 particles. Each individual vector has an uncertain direction, but the directions are correlated. Dashed lines show the range of possible directions. The vector-addition sketches are reproduced from Yang Fujia, *Atomic Physics*.')
  for k in figures:s=s.replace('[['+k+']]','')
  s=s.strip()
 if table is not None:table[cell].append(expand(s));continue
 if style.startswith('Heading'):
  level=int(style[-1]);files[current].append('#'*level+' '+expand(s).replace('* ',r'\* ',1));continue
 if rid in display_ids:
  ks=keys(s);math=r'\qquad '.join(tokens[k] for k in ks)
  files[current].append('$$\n'+math+'\n$$ {#'+labels[rid]+'}');continue
 if rid in labels:
  k='X1937' if rid==1942 else keys(s)[0];s=s.replace('[['+k+']]', '\n\n$$\n'+tokens[k]+'\n$$ {#'+labels[rid]+'}\n\n')
 s=expand(s)
 if r['list'] or style=='ListParagraph':s='- '+s
 # Figure captions keep the original source numbering, independently of equations.
 if style=='Caption' and s.startswith('Figure'):s='::: {.source-caption}\n'+s+'\n:::'
 files[current].append(s)
for name,parts in files.items():
 s='\n\n'.join(parts)+'\n'
 s=re.sub(r'(\*\*\d+\.\d+\*\*)\*',r'\1\\*',s)
 for n in sorted(set(re.findall(r'\[\^(f\d+)\]',s))):s+='\n[^'+n+']: '+' '.join(notes[n])+'\n'
 (out/(name+'.qmd')).write_text(s,encoding='utf8')
config='''project:
  type: book
  output-dir: _book

book:
  title: "Introduction to Quantum Mechanics"
  subtitle: "Lecture Notes"
  chapters:
    - index.qmd
'''+''.join('    - '+x+'.qmd\n' for x in chapters)+'''
lang: en
number-sections: true
toc: true
toc-depth: 3
crossref:
  chapters: true
format:
  html:
    theme: cosmo
    css: styles.css
    html-math-method:
      method: mathjax
      url: assets/mathjax/tex-svg.js
    code-fold: true
  pdf:
    documentclass: scrreprt
    keep-tex: true
    papersize: a4
    geometry:
      - margin=25mm
'''
(out/'_quarto.yml').write_text(config,encoding='utf8')
(out/'styles.css').write_text('main { line-height: 1.7; }\n.math.display { display:block; overflow-x:auto; padding:0.5rem 0; }\n.source-caption { font-size:0.9em; color:#52616b; margin:0.4rem 0 1.5rem; }\nimg { max-width:100%; height:auto; }\ntable { font-size:0.94em; }\n',encoding='utf8')
report={'chapters':12,'translated_paragraphs':len(translations),'math_tokens':sum(bool(v) and not v.startswith(('!','[^')) for v in tokens.values()),'display_equations':len(labels)+2,'equation_reference_targets':len(refmap),'unresolved_references':sorted(unresolved),'ambiguous_bookmarks':ambiguous}
(work/'build-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k!='ambiguous_bookmarks'},indent=2))
