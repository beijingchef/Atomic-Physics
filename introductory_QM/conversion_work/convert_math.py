import ctypes as C,sys,zipfile,io,struct,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'vendor'));import olefile
D=C.WinDLL(r'C:\Program Files (x86)\MathType\System\64\MT6.dll')
D.MTAPIConnect.argtypes=[C.c_short,C.c_short];D.MTXFormSetTranslator.argtypes=[C.c_ushort,C.c_char_p]
D.MTXFormEqn.argtypes=[C.c_short,C.c_short,C.c_void_p,C.c_int,C.c_short,C.c_short,C.c_void_p,C.c_int,C.c_char_p,C.c_void_p]
assert D.MTAPIConnect(1,10)==0
out={};errors={};start=time.time()
try:
 with zipfile.ZipFile('introductory_QM/量子力学简介4.9e.docx') as z:
  files=[n for n in z.namelist() if n.startswith('word/embeddings/')]
  for i,p in enumerate(files):
   try:
    with olefile.OleFileIO(io.BytesIO(z.read(p))) as o:data=o.openstream('Equation Native').read()
    hdr=struct.unpack_from('<H',data)[0];size=struct.unpack_from('<I',data,8)[0];eq=data[hdr:hdr+size]
    D.MTXFormReset();assert D.MTXFormSetTranslator(0,b'LaTeX.tdl')==0
    buf=C.create_string_buffer(262144);dims=C.create_string_buffer(64)
    res=D.MTXFormEqn(-3,4,eq,len(eq),-3,7,buf,len(buf),b'',dims)
    if res:raise ValueError(res)
    tex=buf.value.decode('utf-8',errors='replace').strip()
    out[p]=tex
   except Exception as e:errors[p]=str(e)
   if i%200==0:print(i,len(files),round(time.time()-start,1),flush=True)
finally:D.MTAPIDisconnect()
Path('introductory_QM/conversion_work/equations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
Path('introductory_QM/conversion_work/equation-errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2),encoding='utf-8')
print('CONVERTED',len(out),'ERRORS',errors,flush=True)
