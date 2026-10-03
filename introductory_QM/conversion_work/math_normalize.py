"""Normalize MathType/OMML LaTeX and translate embedded annotations."""
import re,unicodedata
OVERRIDES={
'X45':'[^f2]',
'X1038':r'\boxed{\hat A}\xrightarrow{\lvert a\prime\rangle}\boxed{\hat B}\xrightarrow{\lvert b\prime\rangle}\boxed{\hat A}\xrightarrow{\lvert a\prime\prime\rangle}',
'X1039':'',
'X1040':'',
'X1056':r'\boxed{\hat A}\xrightarrow{\lvert a\prime\rangle}\boxed{\hat B}\xrightarrow{\text{all channels open}}\boxed{\hat A}\xrightarrow{\lvert a\prime\prime\rangle}',
'X1057':'',
'X201':r'\lvert\psi\rangle=\begin{pmatrix}\langle 1\vert\psi\rangle\\\langle 2\vert\psi\rangle\\\vdots\\\langle N\vert\psi\rangle\end{pmatrix}',
'X122':r'\lvert\text{vector name}\rangle',
'X123':r'\begin{aligned}\text{Commutativity:}\quad &\lvert\psi_\alpha\rangle+\lvert\psi_\beta\rangle=\lvert\psi_\beta\rangle+\lvert\psi_\alpha\rangle\\\text{Complex scalars:}\quad &c\lvert\psi\rangle=\lvert\psi\rangle c\\\text{Distributivity:}\quad &(c_1+c_2)\lvert\psi\rangle=c_1\lvert\psi\rangle+c_2\lvert\psi\rangle\\&c(\lvert\psi_\alpha\rangle+\lvert\psi_\beta\rangle)=c\lvert\psi_\alpha\rangle+c\lvert\psi_\beta\rangle\end{aligned}',
'X135':r'\begin{pmatrix}a_1\\a_2\\a_3\\\vdots\\a_n\end{pmatrix},\quad a_i\in\mathbb C;\qquad\lvert\mathrm{null}\rangle=\begin{pmatrix}0\\0\\0\\\vdots\\0\end{pmatrix}',
'X417':r'\lvert a_i\rangle=\begin{pmatrix}\langle a_1\vert a_i\rangle\\\vdots\\\langle a_i\vert a_i\rangle\\\vdots\\\langle a_N\vert a_i\rangle\end{pmatrix}=\begin{pmatrix}0\\\vdots\\1\\\vdots\\0\end{pmatrix}\quad\text{(1 in row }i\text{)}',
'X732':r'\lvert a_i\rangle=\sum_j\lvert a_j\rangle\langle a_j\vert a_i\rangle=\sum_j\lvert a_j\rangle\delta_{ij}=\begin{pmatrix}0\\\vdots\\1\\\vdots\\0\end{pmatrix}\quad\text{(1 in row }i\text{)}',
'X746':r'\lvert a_i\rangle\langle a_j\rvert=\bigl(\delta_{ki}\delta_{lj}\bigr)_{kl}\quad\text{(1 in row }i\text{, column }j\text{; 0 elsewhere)}',
'X764':r'\sigma_x',
'X719':r'\langle\mathbf S\rangle=\langle\hat S_x\rangle\mathbf i+\langle\hat S_y\rangle\mathbf j+\langle\hat S_z\rangle\mathbf k',
'X1781':r'V(x)=\begin{cases}0,&0<x<L,\\\infty,&x\leq0\text{ or }x\geq L.\end{cases}',
'X1818':r'\left[-\frac{\hbar^2}{2m}\frac{\partial^2}{\partial x^2}+V(x)\right]\psi(x)=E\psi(x),\qquad V(x)=\begin{cases}0,&\lvert x\rvert<L/2,\\ V_0,&\lvert x\rvert\geq L/2.\end{cases}',
'X2478':r'i\hbar',
'X2734':r'\lvert R\rangle,\lvert L\rangle,\hat\sigma_x',
'X2735':r'\hat\sigma_y',
}
WORDS={
'向量加法交换律':'Commutativity','向量可乘以一个复数':'Complex scalar multiplication','乘法满足分配律':'Distributivity',
'左矢空间':'Bra space','右矢空间':'Ket space','笛卡尔空间':'Cartesian space','向量空间':'Vector space','点乘':'Dot product','内积':'Inner product','垂直':'Perpendicular','正交':'Orthogonal','坐标系单位矢量':'Coordinate unit vectors','基矢':'Basis vectors','坐标系':'Coordinate system','完备基':'Complete basis','基':'basis','矢量的坐标形式':'Coordinates','向量在基上的展开式':'Basis expansion',
'测前态':'Initial state','测后态':'Final state','测得值':'Result','发生几率':'Probability','测量':'Measure ',
'必为虚数':' is purely imaginary','必为实数':' is real','为虚数':' is purely imaginary','为实数':' is real','时间演化':'time evolution','位置表象表达式':'Position representation','位置表象':'position representation','算符名称':'Observable','狄拉克符号':'Dirac notation',
'轨道角动量x分量':'Orbital x component','轨道角动量y分量':'Orbital y component','轨道角动量z分量':'Orbital z component','轨道角动量平方':'Squared orbital angular momentum','一维动量的平方':'Squared 1D momentum','三维动量的平方':'Squared 3D momentum','一维动量':'1D momentum','三维动量':'3D momentum','位置':'Position','势能':'potential energy','动能':'kinetic energy','能量':'Energy','新':'new','老':'old','若':'If ','则':'then ','当':'for ','个':' terms'
}
UNICODE={'ℏ':r'\hbar ','σ':r'\sigma ','ψ':r'\psi ','φ':r'\phi ','ϕ':r'\varphi ','α':r'\alpha ','β':r'\beta ','γ':r'\gamma ','δ':r'\delta ','θ':r'\theta ','ϑ':r'\vartheta ','λ':r'\lambda ','μ':r'\mu ','ν':r'\nu ','π':r'\pi ','ρ':r'\rho ','τ':r'\tau ','ω':r'\omega ','Δ':r'\Delta ','Ω':r'\Omega ','Σ':r'\Sigma ','Γ':r'\Gamma ','Φ':r'\Phi ','Ψ':r'\Psi ','ε':r'\epsilon ','ϵ':r'\varepsilon ','η':r'\eta ','ξ':r'\xi ','ζ':r'\zeta ','χ':r'\chi ','∫':r'\int ','∑':r'\sum ','∏':r'\prod ','∞':r'\infty ','∂':r'\partial ','∇':r'\nabla ','√':r'\sqrt ','×':r'\times ','⋅':r'\cdot ','∙':r'\cdot ','·':r'\cdot ','…':r'\ldots ','⋯':r'\cdots ','⋮':r'\vdots ','≡':r'\equiv ','≠':r'\ne ','≤':r'\le ','≥':r'\ge ','≈':r'\approx ','±':r'\pm ','∓':r'\mp ','→':r'\to ','↔':r'\leftrightarrow ','∝':r'\propto ','∈':r'\in ','⊗':r'\otimes ','∗':'*','−':'-','（':'(', '）':')','，':',','；':';','：':':','。':'.','、':',','‖':r'\Vert ','⟨':r'\langle ','⟩':r'\rangle ','〈':r'\langle ','〉':r'\rangle '}
def normalize(k,s):
 if k in OVERRIDES:return OVERRIDES[k]
 if s.startswith('!'):return s.replace('![Equation]','![]').replace('![Figure]','![]').replace(' .equation-image','')
 s=s.strip()
 if s.startswith('\\['):s=s[2:-2]
 elif s.startswith('$'):s=s.strip('$')
 s=re.sub(r'\\unicode\{([A-Fa-f0-9]+)\}',lambda m:chr(int(m[1],16)),s)
 for a,b in sorted(WORDS.items(),key=lambda x:-len(x[0])):s=s.replace(a,r'\text{'+b+'}')
 for a,b in UNICODE.items():s=s.replace(a,b)
 # Mathematical Unicode letters emitted by OMML become explicit LaTeX styles.
 def styled(m):
  c=m[0];n=unicodedata.name(c,'');v=unicodedata.normalize('NFKD',c)
  if 'BOLD' in n:return r'\mathbf{'+v+'}'
  if 'DOUBLE-STRUCK' in n:return r'\mathbb{'+v+'}'
  if 'SCRIPT' in n:return r'\mathcal{'+v+'}'
  return v
 s=re.sub('[\U0001d400-\U0001d7ff]',styled,s)
 s=re.sub(r'\s+',' ',s).strip().replace(r'\hfill','')
 s=s.replace(r'\kern-\nulldelimiterspace',r'\kern-1.2pt ')
 s=re.sub(r'(?<!\\)%',r'\\%',s)
 # MathType uses single-cell arrays for ordinary bra/ket contents. Remove those wrappers only.
 pat=r'\\begin\{array\}\{\*\{20\}\{c\}\}((?:(?!\\begin|\\end|&|\\\\).)*)\\end\{array\}'
 for _ in range(5):
  newer=re.sub(pat,lambda m:m[1].strip(),s)
  if newer==s:break
  s=newer
 # Translate alignment tabs outside array/aligned environments to spacing;
 # MathType exports such tabs for tab stops, including in gathered equations.
 parts=re.split(r'(\\begin\{[^}]+\}|\\end\{[^}]+\}|(?<!\\)&)',s);stack=[];out=[]
 for part in parts:
  if part.startswith('\\begin{'):stack.append(part[7:-1])
  elif part.startswith('\\end{'):
   if stack:stack.pop()
  elif part=='&' and (not stack or stack[-1] not in ['array','matrix','pmatrix','bmatrix','aligned','cases','alignedat']):part=r'\qquad '
  out.append(part)
 s=''.join(out)
 s=re.sub(r'(?:\\qquad\s*)+(?=\\\\|$)', '',s)
 # Consistent portable vertical bars (also safe in Markdown pipe tables).
 s=s.replace('|',r'\vert ')
 if re.search('[\u4e00-\u9fff]',s):raise ValueError((k,s))
 return s.strip()
