#!/usr/bin/env python3
"""Validate this documentation package offline (not app behavior or remote URLs)."""
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/restore-legacy-ios-apps'


def validate(root=ROOT):
    errors = []
    skill = root / 'skills/restore-legacy-ios-apps'
    required = ['SKILL.md', 'agents/openai.yaml', 'assets/investigation-record.md',
                'references/source-evidence.json', 'references/sources.md',
                'assets/engineering-report-prompt.md', 'references/reporting.md']
    for name in required:
        if not (skill / name).is_file():
            errors.append('Missing: ' + name)
    if errors:
        return errors
    text = (skill / 'SKILL.md').read_text()
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not match:
        errors.append('Missing skill frontmatter')
    else:
        fields = dict(line.split(': ', 1) for line in match[1].splitlines() if ': ' in line)
        if fields.get('name') != skill.name or not fields.get('description'):
            errors.append('Incorrect name or missing description')
    for path in root.rglob('*'):
        if '.git' in path.relative_to(root).parts or path.suffix not in ('.md', '.json', '.yaml'):
            continue
        text = path.read_text()
        if re.search(r'/Users/|/home/[^/]+/|BEGIN (?:RSA |OPENSSH )?PRIVATE KEY', text):
            errors.append('Private path/key marker: ' + str(path.relative_to(root)))
        if re.search(r'\bTODO\b|\[INSERT\b', text):
            errors.append('Unresolved scaffold: ' + str(path.relative_to(root)))
        if path.suffix != '.md':
            continue
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if urlsplit(target.strip('<>')).scheme or target.startswith('#'):
                continue
            target = unquote(target.split('#')[0].strip('<>'))
            resolved = (path.parent / target).resolve()
            if root.resolve() not in resolved.parents or not resolved.exists():
                errors.append('Broken/escaping link: ' + target + ' in ' + str(path.relative_to(root)))
    readme = (root / 'README.md').read_text()
    embedded = re.search(r'<!-- report-prompt:start -->\n```text\n(.*?)```\n<!-- report-prompt:end -->', readme, re.S)
    if not embedded or embedded[1] != (skill / 'assets/engineering-report-prompt.md').read_text():
        errors.append('README report prompt differs from canonical prompt')
    if not (root / 'reports/README.md').is_file():
        errors.append('Missing engineering report index')
    evidence = json.loads((skill / 'references/source-evidence.json').read_text())
    for repo in evidence['repositories']:
        if not re.fullmatch(r'[0-9a-f]{40}', repo['commit']):
            errors.append('Invalid source commit: ' + repo['app'])
        for item in repo['files']:
            if not re.fullmatch(r'[0-9a-f]{64}', item['sha256']):
                errors.append('Invalid SHA-256: ' + item['path'])
            if item['url'] != repo['repository'] + '/blob/' + repo['commit'] + '/' + item['path']:
                errors.append('Unpinned source URL: ' + item['path'])
    return errors


if __name__ == '__main__':
    problems = validate()
    if problems:
        print('\n'.join(problems))
        raise SystemExit(1)
    print('PASS: required files, frontmatter basics, local links, privacy markers, pinned evidence structure')
