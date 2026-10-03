from pathlib import Path
import re,tempfile
src=Path(r'C:\Program Files (x86)\MathType\Translators')
def expand(name):
 s=(src/name).read_text(encoding='cp1252')
 return re.sub(r'^include "([^"]+)";',lambda m:expand(m[1]),s,flags=re.M)
s=expand('AMS LaTeX.tdl')
s=re.sub(r'^defchar\s*=.*?;',lambda m:r'defchar = "\unicode{<CharHex>}";',s,flags=re.M)
s=s.replace('"AMSLaTeX",','"Quarto AMSLaTeX",',1)
p=Path(tempfile.gettempdir())/'qm-book-translators'/'Quarto.tdl';p.write_text(s,encoding='cp1252')
