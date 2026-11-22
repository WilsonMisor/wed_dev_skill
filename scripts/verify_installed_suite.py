"""Verify manifest-owned installed files against generated distributions."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone

BLUEPRINT=Path(__file__).resolve().parents[1]

def digest(raw):return hashlib.sha256(raw).hexdigest()

def inventory(blueprint,preos,gstack):
    skills=[];agents=[];seen=set()
    for label,root in [('blueprint',blueprint),('preos',preos),('gstack',gstack)]:
        manifest=json.loads((root/'CODEX-DISTRIBUTION.json').read_text(encoding='utf-8'))
        for skill in manifest['skills']:
            source_name=skill['name'];name='gstack-'+source_name if label=='gstack' and not source_name.startswith('gstack') else source_name
            if not re.fullmatch('[a-z][a-z0-9-]*',name) or name in seen:raise ValueError('unsafe or duplicate suite skill name')
            seen.add(name)
            source=(root/skill['source_path']).resolve()
            if not source.is_relative_to(root.resolve()) or not (source/'SKILL.md').is_file():raise ValueError('invalid distribution skill source')
            skills.append({'name':name,'source_name':source_name,'owner':label,'source':source})
        if label=='blueprint':
            for agent in manifest.get('agents',[]):
                source=(root/agent['source_path']).resolve()
                if not source.is_relative_to(root.resolve()) or not source.is_file():raise ValueError('invalid agent source')
                agents.append(source)
    return skills,agents

def verify(blueprint,preos,gstack,codex_home,skill_root=None):
    skill_root=(skill_root or codex_home/'skills').resolve();skills,agents=inventory(blueprint,preos,gstack);files=[]
    for entry in skills:
        target=(skill_root/entry['name']).resolve()
        if not target.is_relative_to(skill_root):raise ValueError('installed target escapes skill root')
        for source in entry['source'].rglob('*'):
            if not source.is_file():continue
            relative=source.relative_to(entry['source'])
            if '__pycache__' in relative.parts or source.suffix in {'.pyc','.pyo'}:continue
            expected=source.read_bytes()
            if relative.as_posix()=='SKILL.md' and entry['owner']=='gstack':
                text=expected.decode('utf-8');text=re.sub(r'(?m)^name:\s*[^\r\n]+','name: '+entry['name'],text,count=1)
                expected=text.encode('utf-8')
            destination=target/relative
            if not destination.is_file() or destination.read_bytes()!=expected:
                raise ValueError('installed distribution is missing or stale: '+str(destination))
            files.append({'path':entry['name']+'/'+relative.as_posix(),'sha256':digest(expected)})
    for source in agents:
        target=codex_home/'agents'/source.name
        if not target.is_file() or target.read_bytes()!=source.read_bytes():raise ValueError('installed agent metadata drift: '+source.name)
        files.append({'path':'agents/'+source.name,'sha256':digest(source.read_bytes())})
    components=[]
    for label,root in [('blueprint',blueprint),('preos',preos),('gstack',gstack)]:
        commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
        components.append({'repository':label,'commit':commit,'distribution_manifest_sha256':digest((root/'CODEX-DISTRIBUTION.json').read_bytes())})
    return {'schema_version':'pasv2-installed-suite-v2','verified_at':datetime.now(timezone.utc).isoformat(),
            'codex_home':str(codex_home),'skill_root':str(skill_root),'skills':[r['name'] for r in skills],
            'skill_count':len(skills),'agent_count':len(agents),'file_count':len(files),'files':files,'components':components,
            'model2_activation':'installed_not_default','production_authorized':False}

def write_receipt(result,blueprint,preos,gstack,codex_home):
    path=codex_home/'framework-installations/wilson-production-framework.json';path.parent.mkdir(parents=True,exist_ok=True)
    receipt={}
    if path.exists():
        previous=path.with_name(path.stem+'.previous-'+digest(path.read_bytes())[:16]+path.suffix)
        if not previous.exists():previous.write_bytes(path.read_bytes())
        receipt=json.loads(path.read_text(encoding='utf-8-sig'))
    skills,agents=inventory(blueprint,preos,gstack)
    repository={'blueprint':'WilsonMisor/wed_dev_skill','preos':'WilsonMisor/PREOS','gstack':'WilsonMisor/gstack'}
    receipt.update(schema_version=receipt.get('schema_version','1.0'),suite='wilson-production-framework',installed_at_utc=result['verified_at'],
        skills=[{'name':r['name'],'repository':repository[r['owner']],'source_path':'codex-distribution/skills/'+r['source_name'],'destination':str(Path(result['skill_root'])/r['name'])} for r in skills],
        agents=[{'name':p.stem,'destination':str(codex_home/'agents'/p.name)} for p in agents],repositories=result['components'])
    # Old materialization hashes describe the archived installation, not this one.
    receipt['distribution_materializations']=[]
    receipt['suite_verification']=result
    receipt.setdefault('receipt_extensions',{})['pasv2_installed_file_verification']='v2'
    path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    return path

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--blueprint',type=Path,default=BLUEPRINT);p.add_argument('--preos',type=Path,default=BLUEPRINT.parent/'PREOS');p.add_argument('--gstack',type=Path,default=BLUEPRINT.parent/'gstack')
    p.add_argument('--codex-home',type=Path,default=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex'))));p.add_argument('--skill-root',type=Path);p.add_argument('--write-receipt',action='store_true');a=p.parse_args()
    result=verify(a.blueprint,a.preos,a.gstack,a.codex_home,a.skill_root)
    if a.write_receipt:
        write_receipt(result,a.blueprint,a.preos,a.gstack,a.codex_home)
    print(json.dumps({k:v for k,v in result.items() if k not in {'files','skills'}},indent=2))
