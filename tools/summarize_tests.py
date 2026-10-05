"""Exibe a causa registrada pelos testes, mantendo a falha original do workflow."""
import json
import os
from pathlib import Path

root = Path(__file__).resolve().parents[1]
evidence = root / 'evidence'
names = {}
failures = []
result = None
report = evidence / 'tests.json'
if report.exists():
    for line in report.read_text(errors='replace').splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get('type') == 'testStart':
            item = event.get('test', {})
            names[item.get('id')] = item.get('name', 'Teste não identificado')
        elif event.get('type') == 'error':
            failures.append((event.get('testID'), event.get('error', ''),
                             event.get('stackTrace', '')))
        elif event.get('type') == 'done':
            result = event.get('success')

parts = ['## Resultado dos testes Flutter', '']
if failures:
    for test_id, message, stack in failures:
        parts += ['### ' + names.get(test_id, 'Falha de preparação ou execução'),
                  '', '```text', str(message)[:10000], str(stack)[:4000], '```', '']
elif result is True:
    parts += ['A suíte foi concluída com sucesso. Os registros completos estão no artifact.']
else:
    parts += ['O protocolo de testes não registrou conclusão bem-sucedida. Consulte a saída abaixo.', '']
    p = evidence / 'test.txt'
    if p.exists():
        parts += ['```text', '\n'.join(p.read_text(errors='replace').splitlines()[-90:]), '```']
    else:
        parts += ['A etapa não produziu test.txt. Confira a preparação do ambiente.']

text = '\n'.join(parts) + '\n'
evidence.mkdir(exist_ok=True)
(evidence / 'resumo-testes.md').write_text(text)
summary = os.getenv('GITHUB_STEP_SUMMARY')
if summary:
    with open(summary, 'a') as f:
        f.write(text)
print(text)
