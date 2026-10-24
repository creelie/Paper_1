"""Create exactly one complete ZIP, gated on confirmed Zenodo publication."""
from pathlib import Path
import datetime, hashlib, json, zipfile

ROOT=Path(__file__).resolve().parents[1]
NAME='Paper_1_Annals_submission_v1.2.0.zip'
record=json.loads((ROOT/'provenance'/'zenodo-published-record.json').read_text(encoding='utf-8'))
assert record['state']=='done' and record['doi']=='10.5281/zenodo.23607502'
assert record['metadata']['version']=='1.2.0'
paper=ROOT/'Paper_1_Annals.pdf'
entry=next(f for f in record['files'] if f['key']==paper.name)
assert entry['checksum']=='md5:'+hashlib.md5(paper.read_bytes()).hexdigest()

skip_suffix={'.aux','.log','.out','.blg','.rpi','.fls','.fdb_latexmk','.pyc','.exe'}
def include(p):
    rel=p.relative_to(ROOT)
    return (p.is_file() and not any(x in {'.git','.lake','__pycache__'} for x in rel.parts)
        and p.suffix not in skip_suffix and p.suffix!='.zip'
        and p.name not in {'SHA256SUMS.txt','main.pdf',NAME+'.sha256'})

# Match the repository's LF checkout policy, so ZIP and Git checksums agree.
text_suffix={'.md','.json','.txt','.tex','.bib','.bbl','.lean','.py','.c','.cff','.patch'}
text_names={'LICENSE','.gitattributes','.gitignore','lean-toolchain'}
for p in ROOT.rglob('*'):
    if include(p) and (p.suffix in text_suffix or p.name in text_names):
        data=p.read_bytes()
        if b'\r\n' in data: p.write_bytes(data.replace(b'\r\n',b'\n'))

meta={'version':'1.2.0','doi':record['doi'],
      'zenodo_record':'https://zenodo.org/records/23607502',
      'zenodo_publication_confirmed_before_packaging':True,
      'zenodo_record_state':record['state'],
      'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'archived_pdf_checksum_matches':True,
      'repository':'https://github.com/creelie/Paper_1',
      'journal_target':'Annals of Mathematics',
      'journal_submitted':False,'journal_accepted':False}
(ROOT/'PACKAGE-METADATA.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8',newline='\n')
files=sorted((p for p in ROOT.rglob('*') if include(p)),key=lambda p:p.relative_to(ROOT).as_posix())
sums=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files)
manifest=ROOT/'SHA256SUMS.txt';manifest.write_text(sums,encoding='utf-8',newline='\n')
files.append(manifest)
output=ROOT/NAME
with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files: z.write(p,'Paper_1/'+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(output) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))==len(files)
    for line in sums.splitlines():
        digest,name=line.split('  ',1)
        assert hashlib.sha256(z.read('Paper_1/'+name)).hexdigest()==digest,name
digest=hashlib.sha256(output.read_bytes()).hexdigest()
(ROOT/(NAME+'.sha256')).write_text(digest+'  '+NAME+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'zip':str(output),'files':len(files),'bytes':output.stat().st_size,'sha256':digest,'doi':record['doi'],'published_before_packaging':True}))
