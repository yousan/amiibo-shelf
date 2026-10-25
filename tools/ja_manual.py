# どうぶつの森以外の日本語名（英語名 → 日本語名）。どうぶつの森の住民・キャラは ACNHAPI と Nookipedia から取る（build_ja.py）
BASE = {
 # マリオ
 'Mario':'マリオ','Luigi':'ルイージ','Peach':'ピーチ','Yoshi':'ヨッシー','Toad':'キノピオ','Bowser':'クッパ','Bowser Jr.':'クッパJr.',
 'Rosalina':'ロゼッタ','Rosalina and Lumas':'ロゼッタ&チコ','Rosalina & Luma':'ロゼッタ&チコ','Mario and Luma':'マリオ&チコ',
 'Wario':'ワリオ','Waluigi':'ワルイージ','Daisy':'デイジー','Donkey Kong':'ドンキーコング','Diddy Kong':'ディディーコング',
 'Boo':'テレサ','Goomba':'クリボー','Koopa Troopa':'ノコノコ','Birdo':'キャサリン','Metal Mario':'メタルマリオ','Pink Gold Peach':'ピンクゴールドピーチ',
 'Baby Mario':'ベビィマリオ','Baby Luigi':'ベビィルイージ','Elephant Mario':'ゾウマリオ','Captain Toad & Talking Flower':'キノピオ隊長&おしゃべりフラワー',
 'Poplin & Prince Florian':'ポプリン&フロリアン王子','Dr. Mario':'ドクターマリオ','Piranha Plant':'パックンフラワー','Golden':'ゴールド',
 '8-Bit Mario Classic Color':'マリオ【クラシックカラー】','8-Bit Mario Modern Color':'マリオ【モダンカラー】',
 'Donkey Kong & Pauline':'ドンキーコング&ポリーン','Super Mario Cereal':'スーパーマリオ シリアル',
 'Green Yarn Yoshi':'毛糸のヨッシー（みどり）','Pink Yarn Yoshi':'毛糸のヨッシー（ピンク）','Light Blue Yarn Yoshi':'毛糸のヨッシー（みずいろ）',
 'Mega Yarn Yoshi':'デカ毛糸のヨッシー','Poochy':'ポチ',
 'Hammer Slam Bowser':'ハンマースラム・クッパ','Turbo Charge Donkey Kong':'ターボチャージ・ドンキーコング',
 # ゼルダ
 'Link':'リンク','Zelda':'ゼルダ','Ganondorf':'ガノンドロフ','Sheik':'シーク','Young Link':'こどもリンク','Toon Link':'トゥーンリンク',
 'Toon Link - The Wind Waker':'トゥーンリンク【風のタクト】','Toon Zelda - The Wind Waker':'ゼルダ【風のタクト】',
 'Zelda and Loftwing':'ゼルダ&ロフトバード【スカイウォードソード】','Link - Archer':'リンク(弓)【ブレス オブ ザ ワイルド】','Link - Rider':'リンク(騎乗)【ブレス オブ ザ ワイルド】',
 'Guardian':'ガーディアン【ブレス オブ ザ ワイルド】','Bokoblin':'ボコブリン【ブレス オブ ザ ワイルド】','Daruk':'ダルケル【ブレス オブ ザ ワイルド】',
 'Urbosa':'ウルボザ【ブレス オブ ザ ワイルド】','Mipha':'ミファー【ブレス オブ ザ ワイルド】','Revali':'リーバル【ブレス オブ ザ ワイルド】',
 'Midna & Wolf Link':'ウルフリンク【トワイライトプリンセス】','8-Bit Link':'リンク【ゼルダの伝説】',
 'Link - Ocarina of Time':'リンク【時のオカリナ】','Link - Majora\'s Mask':'リンク【ムジュラの仮面】','Link - Twilight Princess':'リンク【トワイライトプリンセス】',
 'Link - Skyward Sword':'リンク【スカイウォードソード】','Link - Link\'s Awakening':'リンク【夢をみる島】',
 'Link - Tears of the Kingdom':'リンク【ティアーズ オブ ザ キングダム】','Zelda - Tears of the Kingdom':'ゼルダ【ティアーズ オブ ザ キングダム】',
 'Ganondorf - Tears of the Kingdom':'ガノンドロフ【ティアーズ オブ ザ キングダム】','Riju':'ルージュ【ティアーズ オブ ザ キングダム】',
 'Sidon':'シド【ティアーズ オブ ザ キングダム】','Tulin':'チューリ【ティアーズ オブ ザ キングダム】','Yunobo':'ユン坊【ティアーズ オブ ザ キングダム】',
 "Mineru's Construct":'ミネルゴーレム【ティアーズ オブ ザ キングダム】',
 # スプラトゥーン
 'Inkling Girl':'ガール','Inkling Boy':'ボーイ','Inkling Squid':'イカ','Callie':'アオリ','Marie':'ホタル','Pearl':'ヒメ','Marina':'イイダ',
 'Octoling Girl':'タコガール','Octoling Boy':'タコボーイ','Octoling Octopus':'タコ','Inkling - Yellow':'インクリング【イエロー】','Octoling - Blue':'オクトリング【ブルー】',
 'Smallfry':'コジャケ','Shiver':'フウカ','Frye':'ウツホ','Big Man':'マンタロー','Inkling':'インクリング',
 # スマブラ（ファイター名）
 'Fox':'フォックス','Samus':'サムス','Wii Fit Trainer':'Wii Fit トレーナー','Villager':'むらびと','Pikachu':'ピカチュウ','Kirby':'カービィ','Marth':'マルス',
 'Little Mac':'リトル・マック','Pit':'ピット','Lucario':'ルカリオ','Captain Falcon':'キャプテン・ファルコン','Ike':'アイク','Falco':'ファルコ',
 'Zero Suit Samus':'ゼロスーツサムス','Olimar':'ピクミン&オリマー','Palutena':'パルテナ','Dark Pit':'ブラックピット','Mii Brawler':'Mii 格闘タイプ',
 'Mii Swordfighter':'Mii 剣術タイプ','Mii Gunner':'Mii 射撃タイプ','Charizard':'リザードン','Greninja':'ゲッコウガ','Jigglypuff':'プリン','Meta Knight':'メタナイト',
 'King Dedede':'デデデ','Lucina':'ルキナ','Robin':'ルフレ','Shulk':'シュルク','Ness':'ネス','Mr. Game & Watch':'Mr.ゲーム&ウォッチ','R.O.B. - Famicom':'ロボット（ファミコンカラー）',
 'R.O.B. - NES':'ロボット（NESカラー）','Duck Hunt':'ダックハント','Sonic':'ソニック','Mega Man':'ロックマン','Pac-Man':'パックマン','Mewtwo':'ミュウツー','Lucas':'リュカ',
 'Roy':'ロイ','Ryu':'リュウ','Cloud':'クラウド','Corrin':'カムイ','Bayonetta':'ベヨネッタ','King K. Rool':'キングクルール','Isabelle':'しずえ','Wolf':'ウルフ',
 'Ridley':'リドリー','Dark Samus':'ダークサムス','Ice Climbers':'アイスクライマー','Ivysaur':'フシギソウ','Squirtle':'ゼニガメ','Pichu':'ピチュー','Incineroar':'ガオガエン',
 'Pokemon Trainer':'ポケモントレーナー','Chrom':'クロム','Ken':'ケン','Snake':'スネーク','Simon':'シモン','Richter':'リヒター','Joker':'ジョーカー','Hero':'勇者',
 'Banjo & Kazooie':'バンジョー&カズーイ','Terry Bogard':'テリー','Byleth':'ベレト','Min Min':'ミェンミェン','Steve':'スティーブ','Alex':'アレックス',
 'Sephiroth':'セフィロス','Pyra':'ホムラ','Mythra':'ヒカリ','Kazuya':'カズヤ','Sora':'ソラ','Mega Man - Gold Edition':'ロックマン【ゴールドVer.】',
 # カービィ
 'Waddle Dee':'ワドルディ','Kirby (& Warp Star)':'カービィ（&ワープスター）','Meta Knight (& Shadow Star)':'メタナイト（&シャドースター）',
 'King Dedede (& Tank Star)':'デデデ大王（&タンクスター）','Bandana Waddle Dee (& Winged Star)':'バンダナワドルディ（&ウイングスター）',
 'Chef Kawasaki (& Hop Star)':'コックカワサキ（&ホップスター）',
 # メトロイド
 'Samus Aran':'サムス・アラン','Metroid':'メトロイド','Samus - Metroid Dread':'サムス【メトロイド ドレッド】','E.M.M.I.':'E.M.M.I.【メトロイド ドレッド】',
 'Samus & Vi-O-La':'サムス&ヴァイオラ【メトロイドプライム4】','Sylux':'サイラックス【メトロイドプライム4】',
 # ファイアーエムブレム・その他任天堂
 'Alm':'アルム','Celica':'セリカ','Tiki':'チキ','Qbby':'キュービィ','Chibi Robo':'ちびロボ','Pikmin':'ピクミン','Detective Pikachu':'名探偵ピカチュウ',
 'Shadow Mewtwo':'ダークミュウツー','Noah':'ノア','Mio':'ミオ',
 # サードパーティ
 'Shovel Knight':'ショベルナイト','Shovel Knight - Gold Edition':'ショベルナイト【ゴールドVer.】','Plague Knight':'プレイグナイト','Specter Knight':'スペクターナイト','King Knight':'キングナイト',
 'Solaire of Astora':'太陽の戦士ソラール','Loot Goblin':'宝物ゴブリン','Diana':'ディアナ','Grace Ashcroft':'グレース・アッシュクロフト','Leon S. Kennedy':'レオン・S・ケネディ',
 # モンスターハンター
 'Razewing Ratha':'破滅レウス','Ena':'エナ','Tsukino':'ツキノ','Ratha':'レウス','Ratha V':'レウスV','Rudy':'ルディ','Nabiru':'ナビルー',
 'One-Eyed Rathalos and Rider - Male':'隻眼のリオレウス&ライダー（男の子）','One-Eyed Rathalos and Rider - Female':'隻眼のリオレウス&ライダー（女の子）',
 'Rathian and Cheval':'リオレイア&シュヴァル','Barioth and Ayuria':'ベリオロス&アユリア','Qurupeco and Dan':'クルペッコ&ダン先輩',
 'Magnamalo':'マガイマガド','Palico':'オトモアイルー','Palamute':'オトモガルク','Malzeno':'メル・ゼナ',
 # ストリートファイター6
 'Luke':'ルーク','Jamie':'ジェイミー','Manon':'マノン','Kimberly':'キンバリー','Marisa':'マリーザ','Lily':'リリー','JP':'JP','Juri':'ジュリ','Dee Jay':'ディージェイ',
 'Cammy':'キャミィ','E. Honda':'エドモンド本田','Blanka':'ブランカ','Guile':'ガイル','Chun-Li':'春麗','Zangief':'ザンギエフ','Dhalsim':'ダルシム','Rashid':'ラシード',
 'A.K.I':'A.K.I.','Ed':'エド','Akuma':'豪鬼','M. Bison':'ベガ','Terry':'テリー','Mai':'舞','Elena':'エレナ','Sagat':'サガット','C. Viper':'C.ヴァイパー','Ingrid':'イングリッド',
 # 遊☆戯☆王
 'Yuga Ohdo':'王道遊我','Tatsuhisa “Luke” Kamijō':'上城龍久（ルーク）','Nail Saionji':'西園寺ネイル','Gakuto Sōgetsu':'蒼月学人',
 'Roa Kirishima':'霧島ロア','Romin Kirishima':'霧島ロミン','Asana Mutsuba':'睦橋あさな',
 # パワプロ
 'Pawapuro':'パワプロくん','Yabe':'矢部くん','Hayakawa':'早川あおい','Ikari':'猪狩守','Daijobu':'ダイジョーブ博士',
}
# 「名前 - 付記」の付記
SUFFIX = {
 'Baseball':'野球','Soccer':'サッカー','Tennis':'テニス','Golf':'ゴルフ','Horse Racing':'乗馬',
 'Power Up Band':'パワーアップバンド','My Mario Wooden Blocks':'マイマリオ 木製ブロック','Wedding':'ウェディングスタイル','Cat':'ネコ',
 'Gold Edition':'ゴールドVer.','Silver Edition':'シルバーVer.','Player 2':'2Pファイター','Alterna':'オルタナ','Side Order':'サイド・オーダー',
 'Splatoon Raiders':'レイダース','Purple':'パープル','Neon Green':'ネオングリーン','Neon Pink':'ネオンピンク','Lime Green':'ライムグリーン',
 'Orange':'オレンジ','Neon Purple':'ネオンパープル',
 # どうぶつの森
 'Winter':'冬服','Winter Outfit':'冬服','Summer Outfit':'夏服','Dress':'ドレス','Kimono':'着物','Sweater':'セーター','Character Parfait':'キャラパフェ',
 'Amiibo Festival':'amiiboフェスティバル','Without Hat':'帽子なし','Uniform':'制服','Jacket':'ジャケット','Coat':'コート','Full Apron':'エプロン',
 'Suit':'スーツ','Shirt':'シャツ','Loud Jacket':'派手なジャケット','Raincoat':'レインコート','Island':'島','Black Skirt And Bow':'黒いスカート',
 'Pikopuri':'ピコプリ',
}
