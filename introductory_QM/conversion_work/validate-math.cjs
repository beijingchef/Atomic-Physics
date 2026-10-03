const fs=require('fs'),path=require('path');
const root=path.join(process.env.TEMP,'qm-math-validation','node_modules','mathjax-full');
const {mathjax}=require(root+'/js/mathjax.js');const {TeX}=require(root+'/js/input/tex.js');const {SVG}=require(root+'/js/output/svg.js');const {liteAdaptor}=require(root+'/js/adaptors/liteAdaptor.js');const {RegisterHTMLHandler}=require(root+'/js/handlers/html.js');const {AllPackages}=require(root+'/js/input/tex/AllPackages.js');
const adaptor=liteAdaptor();RegisterHTMLHandler(adaptor);
let errors=[];let current='';
const input=new TeX({packages:AllPackages,formatError:(jax,err)=>{errors.push({id:current,message:err.message});return jax.formatError(err);}});
const doc=mathjax.document('',{InputJax:input,OutputJax:new SVG({fontCache:'none'})});
const math=JSON.parse(fs.readFileSync('introductory_QM/conversion_work/normalized-math.json','utf8'));
for(const [id,tex] of Object.entries(math)){current=id;try{doc.convert(tex,{display:true});}catch(e){errors.push({id,message:e.message});}}
fs.writeFileSync('introductory_QM/conversion_work/math-errors.json',JSON.stringify(errors,null,2));console.log(JSON.stringify({count:Object.keys(math).length,errors:errors.length,details:errors.slice(0,80)},null,2));
