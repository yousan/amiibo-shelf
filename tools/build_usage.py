#!/usr/bin/env python3
# amiibo ごとの「Switch のゲームでの使いみち」を作る
#   curl -s 'https://amiiboapi.org/api/amiibo/?showusage' > usage-src.json
#   python3 tools/build_usage.py usage-src.json > usage.json
# 出力: {"g":[ゲーム名...], "u":[使いみち...], "m":{amiiboID:[[ゲーム番号,[使いみち番号...]],...]}}
# Switch と Switch 2 Edition は同じゲームとしてまとめる。あつまれ どうぶつの森を先頭に
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from usage_ja import GAMES, USES

ACNH = 'あつまれ どうぶつの森'
amiibo = json.load(open(sys.argv[1]))['amiibo']
games, uses, out, miss = [], [], {}, set()
def idx(lst, v):
  if v not in lst: lst.append(v)
  return lst.index(v)
for a in amiibo:
  per = {}
  for g in a.get('gamesSwitch', []) + a.get('gamesSwitch2', []):
    base = re.split(r' – Nintendo Switch 2 Edition', g['gameName'])[0]
    name = GAMES.get(base, base)
    if base not in GAMES: miss.add(base)
    for u in g['amiiboUsage']:
      for part in u['Usage'].split(' / '):
        ja = USES.get(part.strip())
        if not ja: miss.add(part.strip()); ja = part.strip()
        per.setdefault(name, [])
        if ja not in per[name]: per[name].append(ja)
  if per:
    order = sorted(per, key=lambda n: (n != ACNH, n))
    out[a['head'] + a['tail']] = [[idx(games, n), [idx(uses, u) for u in per[n]]] for n in order]
print(f'{len(out)} 件。訳なし: {sorted(miss)}', file=sys.stderr)
json.dump({'g': games, 'u': uses, 'm': out}, sys.stdout, ensure_ascii=False, separators=(',', ':'))
