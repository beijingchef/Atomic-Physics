from pathlib import Path
import json,re,collections
p=Path('introductory_QM/conversion_work');r=json.loads((p/'rows.json').read_text(encoding='utf8'));t=json.loads((p/'tokens.json').read_text(encoding='utf8'));tr={int(a):b for a,b in (l.split('\t',1) for l in (p/'translations.tsv').read_text(encoding='utf-8-sig').splitlines() if '\t' in l)}
print('MISSING',[(x['id'],x['text']) for x in r if re.search('[\u4e00-\u9fff]',x['text']) and not x['style'].startswith('TOC') and x['id'] not in tr])
for x in r:
 if x['id'] in tr:
  a=collections.Counter(re.findall(r'\[\[.*?\]\]',x['text']));b=collections.Counter(re.findall(r'\[\[.*?\]\]',tr[x['id']]))
  if a!=b:print('TOKENS',x['id'],dict(a-b),dict(b-a))
print('HEADINGS',[(x['id'],x['text']) for x in r if x['style']=='Heading1'])
print('FRONT',r[:2],r[116:133]);print('NOTES',r[2677:])
for k,v in t.items():
 if '\\unicode' in v or re.search('[\u4e00-\u9fff]',v):print(k,re.sub(r'\\unicode\{([0-9a-fA-F]+)\}',lambda m:chr(int(m[1],16)),v))
print('IMAGES',[(k,v) for k,v in t.items() if v.startswith('!')])
