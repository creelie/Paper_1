"""Build the submission PDF and vector figures; never creates an archive."""
from pathlib import Path
import argparse, shutil, subprocess

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--tex-bin', type=Path, help='directory containing pdflatex and bibtex')
args = parser.parse_args()

def executable(name):
    if args.tex_bin:
        found = args.tex_bin/(name+'.exe' if (args.tex_bin/(name+'.exe')).exists() else name)
        if not found.exists(): raise SystemExit(f'Missing executable: {found}')
        return str(found)
    found=shutil.which(name)
    if not found: raise SystemExit(f'{name} is required; install a TeX distribution with aomart.')
    return found

tex,bib=executable('pdflatex'),executable('bibtex')
logs=ROOT/'verification'/'current'; logs.mkdir(parents=True,exist_ok=True)

def run(command,cwd,log):
    p=subprocess.run(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (logs/log).write_bytes(p.stdout)
    if p.returncode:
        raise SystemExit(f'Build failed; see verification/current/{log}')

man=ROOT/'manuscript'
for stem in ['half-graph','octahedron','product']:
    run([tex,'-interaction=nonstopmode','-halt-on-error',stem+'.tex'],
        man/'figures',stem+'-build.txt')
run([tex,'-interaction=nonstopmode','-halt-on-error','main.tex'],man,'tex-pass-1.txt')
run([bib,'main'],man,'bibtex.txt')
for i in [2,3]:
    run([tex,'-interaction=nonstopmode','-halt-on-error','main.tex'],man,f'tex-pass-{i}.txt')
log=(man/'main.log').read_text(encoding='utf-8',errors='replace')
bad=[s for s in ['Overfull \\hbox','Overfull \\vbox','There were undefined references','There were undefined citations','Rerun to get cross-references right'] if s in log]
if bad: raise SystemExit('Resolve TeX diagnostics before delivery: '+', '.join(bad))
dest=ROOT/'Paper_1_Annals.pdf'
shutil.copy2(man/'main.pdf',dest)
print('Built '+str(dest))
