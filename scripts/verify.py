"""Run the finite checks and, optionally, the separate Lean certificate audit."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys, time

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--lean',action='store_true',help='also rebuild and audit the N=21 certificate')
parser.add_argument('--lake',default='lake',help='lake executable, pinned by lean/lean-toolchain')
args=parser.parse_args()
logs=ROOT/'verification'/'current';logs.mkdir(parents=True,exist_ok=True)
results=[]

def run(name,command,cwd=ROOT):
    start=time.monotonic()
    p=subprocess.run(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (logs/(name+'.txt')).write_bytes(p.stdout)
    results.append({'check':name,'exit_code':p.returncode,'seconds':round(time.monotonic()-start,3)})
    if p.returncode: raise SystemExit('Failed '+name+'; see verification/current/'+name+'.txt')

py=[sys.executable,'-X','utf8','-I']
run('counterexample',py+['verification/python/check_counterexample.py'])
run('lean-data',py+['verification/python/check_lean_data.py','lean/GrundyStrong'])
run('all-parameter-finite-checks',py+['verification/python/verify_revision.py'])
p=subprocess.run(py+['scripts/gen_layers.py'],cwd=ROOT,stdout=subprocess.PIPE,check=True)
generated=p.stdout.replace(b'\r\n',b'\n')
supplied=(ROOT/'lean/GrundyStrong/Layers.lean').read_bytes().replace(b'\r\n',b'\n')
assert generated==supplied,'Layer generator differs from the supplied certificate'
results.append({'check':'regenerate-layer-certificate','equal_after_line_ending_normalization':True})
if args.lean:
    run('lean-build',[args.lake,'build'],ROOT/'lean')
    run('lean-axioms',[args.lake,'env','lean','Check.lean'],ROOT/'lean')
    run('axiom-audit',py+['scripts/audit_axioms.py',str(logs/'lean-axioms.txt')])
    lean_scope='N=21 certificate rebuilt; 25-declaration axiom audit passed.'
else:
    lean_scope='Lean was not rebuilt by this invocation. Use --lean for a fresh build.'
data={'checks':results,'lean_scope':lean_scope,
      'scope':'Finite checks corroborate the two written universal proofs; they do not prove the universal statements by themselves.'}
(logs/'verification-summary.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps(data,indent=2))
