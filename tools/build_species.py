#!/usr/bin/env python3
# どうぶつの森 amiibo の「どうぶつの種類」を作る（ポケ森の絞り込みと同じ分け方。住民以外は「スペシャル」）
#   python3 tools/build_species.py <amiiboapi.json> <acnhapi villagers.json> tools/nookipedia-species.json > species.json
import json, sys
SP = {'alligator':'ワニ','anteater':'アリクイ','bear':'クマ','cub':'コグマ','bear cub':'コグマ','bird':'トリ','bull':'ウシ','cow':'ウシ','cat':'ネコ',
      'chicken':'ニワトリ','deer':'シカ','dog':'イヌ','duck':'アヒル','eagle':'ワシ','elephant':'ゾウ','frog':'カエル','goat':'ヤギ','gorilla':'ゴリラ',
      'hamster':'ハムスター','hippo':'カバ','horse':'ウマ','kangaroo':'カンガルー','koala':'コアラ','lion':'ライオン','monkey':'サル','mouse':'ネズミ',
      'octopus':'タコ','ostrich':'ダチョウ','penguin':'ペンギン','pig':'ブタ','rabbit':'ウサギ','rhino':'サイ','rhinoceros':'サイ','sheep':'ヒツジ',
      'squirrel':'リス','tiger':'トラ','wolf':'オオカミ'}
FIX = {'K. K. Slider':'K.K. Slider','OHare':"O'Hare",'Spork/Crackle':'Spork','Timmy & Tommy':'Timmy'}
amiibo = json.load(open(sys.argv[1]))['amiibo']
vill = {v['name']['name-USen']: v['species'] for v in json.load(open(sys.argv[2])).values()}
nooki = json.load(open(sys.argv[3]))
out, missing = {}, []
for a in amiibo:
  if a['amiiboSeries'] != 'Animal Crossing': continue
  n = a['name'] if a['name'] in vill else a['name'].split(' - ')[0]
  n = FIX.get(n, n)
  if n in vill: out[a['head'] + a['tail']] = SP[vill[n].lower()]
  elif n in nooki:
    kind, sp = nooki[n]
    out[a['head'] + a['tail']] = SP.get((sp or '').lower(), 'スペシャル') if kind == 'Villager' else 'スペシャル'
  else: missing.append(a['name'])
print(f'{len(out)} 件。無し: {missing}', file=sys.stderr)
json.dump(out, sys.stdout, ensure_ascii=False, separators=(',', ':'), sort_keys=True)
