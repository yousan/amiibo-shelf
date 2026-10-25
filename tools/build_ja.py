#!/usr/bin/env python3
# amiibo の日本語名を作る: python3 tools/build_ja.py <amiiboapi.json> <acnhapi villagers.json> <nookipedia.json> > ja.json
# - どうぶつの森の住民: ACNHAPI の name-JPja
# - どうぶつの森のその他のキャラ: Nookipedia の日本語名
# - それ以外: tools/ja_manual.py
# 見つからない名前は出力しない（アプリ側で英語名のまま表示する）。見つからなかった名前は stderr に出す
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ja_manual import BASE, SUFFIX

amiibo = json.load(open(sys.argv[1]))['amiibo']
villagers = {v['name']['name-USen']: v['name']['name-JPja'] for v in json.load(open(sys.argv[2])).values()}
nooki = {k: v for k, v in json.load(open(sys.argv[3])).items() if v}
AC_FIX = {'Timmy': 'まめきち', 'Tommy': 'つぶきち', 'Timmy & Tommy': 'まめきち&つぶきち', 'K. K. Slider': 'とたけけ',
          'OHare': 'サントス', 'Spork/Crackle': 'ポーク', 'DJ KK': 'DJ K.K.', 'Mario (Melody Car)': 'マリオ（メロディカー）'}

def base_ja(name, ac):
  if name in AC_FIX: return AC_FIX[name]
  if ac and name in villagers: return villagers[name]
  if ac and name in nooki: return nooki[name]
  return BASE.get(name) or villagers.get(name)

out, missing = {}, []
for a in amiibo:
  n, ac = a['name'], a['amiiboSeries'] == 'Animal Crossing'
  ja = base_ja(n, ac)
  if not ja and ' - ' in n:
    b, s = n.split(' - ', 1)
    bj, sj = base_ja(b, ac), SUFFIX.get(s)
    if bj and sj: ja = f'{bj}（{sj}）'
  if ja: out[a['head'] + a['tail']] = ja.replace(' & ', '&')
  else: missing.append(n)
print(f'{len(out)}/{len(amiibo)} 件に日本語名。無し: {sorted(set(missing))}', file=sys.stderr)
json.dump(out, sys.stdout, ensure_ascii=False, separators=(',', ':'), sort_keys=True)
