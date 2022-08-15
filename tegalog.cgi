#! /usr/bin/env perl

# ↑★注★↑上記は『書き換えずに』そのままアップロードしてみて下さい。（それで動けばそのままお使い頂けます。）もし Internal Server Error になる場合は、上記の1行を「 #! /usr/bin/perl 」または「 #! /usr/local/bin/perl 」など、お使いのサーバで求められている正しい記述(Perlパス)に修正して下さい。

# ================================================================== #
#  てがろぐ - Fumy Otegaru Memo Logger Ver 3.7.0      [tegalog.cgi]  #
# ================================================================== #
#  Copyright (C) Fumihiro Nishimura.(Nishishi) 2017-2022.            #
#                                                                    #
#  このCGIは、マイクロブログ的なお手軽一言掲示板CGIです。ユーザ認証  #
#  機能で複数人での共用も可能。自動バックアップ機能搭載。備忘録や、  #
#  メモ帳・日記・日報・更新案内・連絡掲示板・チャットツールなどとし  #
#  てのほか、自分専用Twitterなどのようにもご活用頂けます。           #
#                                                                    #
#  このCGIは、個人・法人を問わず、どなたでも自由にご使用頂けます。   #
#  商用利用も可能ですが、このCGIそのものを有償販売してはいけません。 #
#                                                                    #
#  このCGIの著作権は、西村文宏(にしし)にあります。                   #
#  どんな場合でも、著作権表示を削除・改変してはなりません。          #
#  使用する目的でのカスタマイズ(ソース改変)は、既存の著作権表記を改  #
#  変しない限りは自由に施して構いません。ただし、改変したものを不特  #
#  定多数に再配布することは禁じます。                                #
#                                                                    #
#  https://www.nishishi.com/                           [2022/06/09]  #
# ================================================================== #

# ======================== #
# ▼ ユーザ設定（基本） ▼ #	※ファイル名やフォルダ名を標準のままで使うなら、何も書き換える必要はありません。(詳しくは配布サイトの解説 https://www.nishishi.com/cgi/tegalog/setup/#highsettings をご参照下さい)
# ======================== #

# データファイル名
my $bmsdata = 'tegalog.xml';

# 設定ファイル名
my $setfile = 'tegalog.ini';

# パスワード・セッションID保存ファイル名 (※外部から読まれないように拡張子を.cgiにしています。他の拡張子に変更しても構いませんが、その際はこのファイルの中身が誰からも読まれない形で設置して下さい。)
my $passfile = 'psif.cgi';

# 自動バックアップファイル保存先ディレクトリ名 (※ディレクトリは自動では作成されないので、自動バックアップ機能を使いたいなら、事前に手動で作成して下さい。)
my $autobackupto = 'backup';

# 画像アップロード先ディレクトリ名 (※ディレクトリは自動では作成されないので、画像アップロード機能を使いたいなら、事前に手動で作成して下さい。)
my $imagefolder = 'images';

# ============================== #
# ▼ ユーザ設定（オプション） ▼ #	※特に必要がなければ、何も書き換える必要はありません。
# ============================== #

# ブラウザを終了してもログイン状態を維持する ※1:YES(＝セッション有効期限まではログインしたまま) / 0:NO(＝ブラウザを終了すると自動ログアウト)
my $keepsession = 1;

# セーフモード：HTMLソースを直接記述可能な設定項目に書かれた内容について(0:何もしない/1:scriptタグ系の記述は無効にする/9:あらゆるHTMLタグを無効にする) ※9は試験実装(β版)
my $safemode = 1;

# パスワード未設定のユーザのログインを拒否 (0:しない / 1:する / 2:全ユーザのパスワードが未設定の状態では管理画面以外の表示を拒否する )
my $nopassuser = 0;

# スキン内でのInclude(SSI)機能使用時に、上位ディレクトリの参照やフルパスでの記述を許可 (0:しない / 1:する / 9:SSI機能は無効にする )
my $safessi = 1;

# ログイン画面下部に表示させるメッセージ (※複数人で共用する場合の案内や、複数個設置する際の識別のために、ログインフォームの下部に何かメッセージを表示できます。HTMLを書くとそのまま出力されます。)
my $MsgForLoginScreen = '';

# ==================== #
# ▼ 書き換え非推奨 ▼ #	※問題(不具合)がある場合など、どうしても必要な場合には書き換えられます。
# ==================== #

# 文字コード ※UTF-8以外の文字コードでの動作は想定していません。変更しないことをお勧め致します。
my $charcode = 'UTF-8';

# スキンファイル名(外側／内側)
my $skincover  = 'skin-cover.html';
my $skininside = 'skin-onelog.html';

# CGI名の取得方法 ※ログインや画面遷移がうまくいかない場合には、この値を変更して下さい。(0:プロトコルから/1:ディレクトリから/2:ファイルだけ/9:決め打ち) ※標準は2
my $howtogetpath = 2;

# 必要に応じて読み込まれる外部ライブラリのURL群など (※注：LightboxのURLは管理画面の[設定]→[システム設定]で変更できます。)
my %libdat = (
	urljqueryjs => 'https://code.jquery.com/jquery-1.12.4.min.js',										# jQuery本体のデフォルトURL
	urllightboxjs => 'https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.0/js/lightbox.min.js',		# Lightbox本体のデフォルトURL
	urllightboxcss => 'https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.0/css/lightbox.min.css',	# Lightbox用CSSのデフォルトURL
	twitterwidgetjs => 'https://platform.twitter.com/widgets.js',	# Tweet埋め込み用公式ウィジェットのURL
	ogimagedefault => 'https://www.nishishi.com/cgi/tegalog/default-tegalog-ogimage.jpg'	# OGP共通画像の未指定時用画像URL
);

#use lib '.';	# サーバにインストールされていないモジュールを自力で置いた場合は、この行の先頭にある「#」を削除すれば読み込めます。

use CGI;					# 動作にはCGIモジュールが必須
$CGI::POST_MAX = 31457280;	# 仕様上の受信量：最大30MB(= 1024 * 1024 * 30)

# ============================================================== #
# 【カスタマイズされる方へ】                                     #
# CGIソースを修正してカスタマイズできる項目は上記だけです。      #
# それ以外の設定は、管理画面の「設定」メニューから設定できます。 #
# ============================================================== #

# -------------------- #
# これ以降はメイン処理 #
# -------------------- #
my $versionnum = '3.7.0';
my $reqfumycts = 2007002;	# 2.7.2 Required

use warnings;
use strict;

eval {
	require Time::Local;	# 動作にはTime::Localモジュール(Time/Local.pm)が必須
	require './fumycts.pl';	# 動作には同じディレクトリに fumycts.pl が必須
};
if($@) { &errormsg('動作に必須のモジュール(Time::Local)またはファイル(fumycts.pl)が読み込めませんでした。ウェブサーバに必須モジュールがインストールされているかどうか、または、必須ファイルが漏れなく置いてあるかどうかを確認して下さい。特にバージョンアップ後にこの画面が出た場合は、必須ファイル(fumycts.pl)も同時に最新版へ更新したかどうかも確認して下さい。<br><br>' . $@); }
eval {
	$reqfumycts = &fcts::checkVer($reqfumycts);
};
if($@ || ($reqfumycts < 0 )) { &errormsg('動作に必須のファイル「 fumycts.pl 」が古いバージョンのままになっている可能性があります。tegalog.cgiファイルと同じ場所に、fumycts.plファイルの最新版をアップロードできているか確認して下さい。<br>' . $@); }

my $cgi = new CGI;
my $cginame;	# 注:(原則)この変数を直接参照しない。代わりに &getCgiPath()を呼ぶ。
if(		$howtogetpath == 0 ) { $cginame = $cgi->url(); }
elsif(	$howtogetpath == 1 ) { $cginame = $cgi->url(-absolute, 1); }
elsif(	$howtogetpath == 2 ) { $cginame = $cgi->url(-relative, 1); }
else						 { $cginame = 'tegalog.cgi'; }
if( $cginame eq '' ) { $cginame = $0; }	# URLにCGI名がない場合は$0から得る。

my %flagDebug = (
	NoAuthentication	=> 0,	# デバッグ用認証省略	1:ON / 0:OFF
	ShowDebugStrings	=> 0	# デバッグ用情報の表示	1:ON / 0:OFF
);
my %flagDemo = (
	RefuseToChangePassword	=> 0,	# パスワードの変更を拒否(※パスワードを先に設定しておかないと最初のパスワードも作れなくなるので注意) 1:ON / 0:OFF
	RefuseToChangeSettings	=> 0,	# 設定の変更やユーザ情報の変更を拒否(※必要な設定を先にしておくこと。) 1:ON / 0:OFF
	LoginMessage			=> 0,	# デモ実行用のログインメッセージ 1:ON / 0:OFF
	AddRelNofollow			=> 0	# 投稿中の外部リンクすべてに「rel="nofollow"」属性を付加(設定と重複していたら二重に挿入されるので注意) 1:ON / 0:OFF
);
my $rentalflag = 0;		# レンタル版フラグ

# パラメータ取得
my %cp = (
	page	=> $cgi->param('page') || 1,
	mode	=> $cgi->param('mode') || 'view',		# view / edit / write / admin / export / getbackup / passcheck / licence / imageup / rss / gallery
	order	=> $cgi->param('order') || 'straight',	# straight / reverse
	search	=> $cgi->param('q') || '',
	datelim	=> $cgi->param('date') || '',
	hasgtag	=> $cgi->param('tag') || '',
	cat		=> $cgi->param('cat') || '',		# categoryではなくcat
	postid	=> $cgi->param('postid') || 0,
	userid	=> $cgi->param('userid') || '',
	skindir => $cgi->url_param('skin') || ''	# クエリから読む
);

# 恒常付加パラメータ
my @constantParams = ();

# スキン保持用 (動作の途中で書き換わることがある)
my $skinfilecover  = $skincover;
my $skinfileinside = $skininside;

# --- for DEBUG ---
# $cp{'mode'} = 'admin';
# $cp{'postid'} = 22;

# 各種データ保持用変数群 (※以下の各項目は管理画面の「設定」ページから設定可能／ここで値を変更しても設定ファイルに記録された設定の方が優先されます。)
my %setdat = (
	userids => '',							# ユーザIDリスト
	entryperpage => 30,						# 1ページあたりのエントリ数
	separatepoint => 2,						# 日付境界バー(ログ境界)の表示(0:なし、1:年別、2:月別、3:日別)
	separateoption => 1,					# 日付別表示時のログ境界(0:通常時と同じ、1:下位レベルにする)
	separateyear => 'Y年',					# 日付表記:年
	separatemonth => 'G月',					# 日付表記:月
	separatedate => 'N日',					# 日付表記:日
	separatebarreverse => 1,				# 境界バーに逆順表示リンクを挿入(0:しない、1:する)
	separatebaroutput => 1,					# 境界バーにHTML出力リンクを挿入(0:しない、1:する)
	eppoverride => 1,						# 1ページあたりのエントリ数をスキン側が強制指定できるように(0:しない、1:する)

	situationvariation => 0,				# 状況に応じた見出しのバリエーション(0:文章/1:ラベル/2:列挙)
	situationcount => 1,					# 該当件数を表示(1:する、0:しない)
	situationpage => 1,						# ページ番号を表示(1:する、0:しない)
	situationalwayspage => 0,				# 表示条件が限定されていない場合でも2ページ目以降はページ番号を表示(0:しない、1:する)
	situationcountlabel1 => '［',			# 該当件数のラベル:前
	situationcountlabel2 => '件］',			# 該当件数のラベル:後
	situationpagelabel1 => '（',			# ページ番号のラベル:前
	situationpagelabel2 => 'ページ目）',	# ページ番号のラベル:後

	onepostpagesituation => 1,				# 投稿単独表示ページでは、SITUATIONに記事Noを表示(0:しない、1:する)
	onepostpageutilitybox => 1,				# 投稿単独表示ページに、ユーティリティ枠を表示(0:しない、1:する)
	utilitystate => 1,						# ユーティリティリンク：状況別リンクを表示(0:しない、1:する)
	utilityrandom => 1,						# ユーティリティリンク：ランダム継続リンクを表示(0:しない、1:する)
	utilitycat => 2,						# ユーティリティリンク：カテゴリリンクを表示(0:しない、1:カテゴリがある場合のみリンクを列挙、2：カテゴリなしでもリンクする)
	utilitydates => 1,						# ユーティリティリンク：日付別リンクを表示(0:しない、1:する)
	utilitydateymd => 1,					# ユーティリティリンク：同一年月日リンクを表示(0:しない、1:する)
	utilitydateym => 1,						# ユーティリティリンク：同一年月リンクを表示(0:しない、1:する)
	utilitydatey => 1,						# ユーティリティリンク：同一年リンクを表示(0:しない、1:する)
	utilitydatemd => 1,						# ユーティリティリンク：全年同一月日リンクを表示(0:しない、1:する)
	utilitydated => 1,						# ユーティリティリンク：全年前月同一日リンクを表示(0:しない、1:する)
	utilityedit => 1,						# ユーティリティリンク：編集用リンクを表示(0:しない、1:する)
	unknownusername => '？',				# 表示名の設定されていない(まはた削除済み)ユーザの表示名
	unknownusericon => 0,					# 表示名の設定されていない(まはた削除済み)ユーザのアイコン(0:デフォルト、1:URL指定)
	unknownusericonurl => '',				# →そのURL

	fixedpostids => '',						# 先頭固定No.群
	fixedpostsign => '(先頭固定)',			# 先頭固定時のサイン
	fixedpostdate => 1,						# 先頭固定時の日付(1:本来の投稿日時、2:現在の投稿日時、3:固定表示を示すラベル、0:何も表示しない)
	fixedseparatepoint => 1,				# 先頭固定投稿が表示される場合に日付境界バーを表示(1:する、0:しない)
	fixedseparatelabel => '先頭固定',		# 先頭固定投稿用の日付境界バーに表示する文字列

	rearappearcat => 1,						# 下げた投稿をカテゴリ限定表示時に表示(1:する、0:しない)
	rearappeartag => 1,						# 下げた投稿をハッシュタグ限定表示時に表示(1:する、0:しない)
	rearappeardate => 1,					# 下げた投稿を日付指定表示時に表示(1:する、0:しない)
	rearappearsearch => 1,					# 下げた投稿を全文検索時に表示(1:する、0:しない)

	caladdweekrow => 1,						# カレンダーに曜日行を表示(1:する、0:しない)
	calsun => '日',							# 日曜日の表示
	calmon => '月',							# 月曜日の表示
	caltue => '火',							# 火曜日の表示
	calwed => '水',							# 水曜日の表示
	calthu => '木',							# 木曜日の表示
	calfri => '金',							# 金曜日の表示
	calsat => '土',							# 土曜日の表示

	rssoutput => 1,							# RSSフィードを出力(1:する、0:しない)
	rssskin => 1,							# RSSフィード用スキンの選択(0:内蔵抜粋、1:内蔵全体、2:自作)
	rssskindir => 'rss',					# RSSフィード用の自作スキンディレクトリ名
	rssentries => 25,						# RSSフィードに含める投稿数

	xmlsitemapoutput => 1,					# SITEMAP XMLを出力(1:する、0:しない)

	sitemappageoutput => 1,					# サイトマップページを出力(1:する、0:しない)
	sitemappageentries => 60,				# サイトマップページで1ページに表示する投稿数
	sitemappagedatebar => 0,				# サイトマップページに日付境界バーを表示(0:しない/1:する)
	sitemappageyname => 'サイトマップ',		# サイトマップページ機能の名称
	sitemappageskindir => 'skin-sitemap',	# サイトマップページ機能用のスキン名
	sitemappagefixed => 0,					# サイトマップページに先頭固定設定を反映(0:しない/1:する)
	sitemapsituation => 1,					# ギャラリーで該当件数とページ番号を表示(1:する/0:しない)

	galleryoutput => 1,						# ギャラリー機能を(1:使う、0:使わない)
	galleryname => 'ギャラリー',			# ギャラリー機能の名称
	galleryskindir => 'skin-gallery',		# ギャラリー機能用のスキン名
	gallerydatebar => 0,					# ギャラリー表示時に日付境界バーを表示(0:しない/1:する)
	gallerysituation => 1,					# ギャラリーで該当件数とページ番号を表示(1:する/0:しない)
	galleryentries => 24,					# ギャラリーで1ページに表示する投稿数

	pagelinkuse => 1,						# ページ移動リンクを表示(1:する、0:しない)
	pagelinknext => '次の',					# ページ移動リンク：文言「次の」
	pagelinkprev => '前の',					# ページ移動リンク：文言「前の」
	pagelinknum => 1,						# ページ移動リンク：1ページに表示される件数を表示(1:する、0:しない)
	pagelinkunit => '件',					# ページ移動リンク：文言「件」
	pagelinkarrownext => '»',				# ページ移動リンク：右矢印「»」(先へ)
	pagelinkarrowprev => '«',				# ページ移動リンク：左矢印「«」(戻る)
	pagelinkuseindv => 1,					# 投稿単独表示時：ページ移動リンクを表示(0:しない、1:する)
	pagelinknextindv1 => 'No.',				# 投稿単独表示時：ページ移動リンク：新しい方向リンクの前置文言（No.）
	pagelinknextindv2 => ' »',				# 投稿単独表示時：ページ移動リンク：新しい方向リンクの後置文言（ »）
	pagelinknextindvn => 1,					# 投稿単独表示時：ページ移動リンク：新しい方向リンクに投稿番号を挿入(1:する、0:しない)
	pagelinkprevindv1 => '« No.',			# 投稿単独表示時：ページ移動リンク：古い方向リンクの前置文言（« No.）
	pagelinkprevindv2 => '',				# 投稿単独表示時：ページ移動リンク：古い方向リンクの後置文言
	pagelinkprevindvn => 1,					# 投稿単独表示時：ページ移動リンク：古い方向リンクに投稿番号を挿入(1:する、0:しない)
	pagelinkseparator => '/',				# 前後ページ移動リンク間のセパレータ：「/」

	pagenumfigure => 0,						# ページ番号リンクの桁を(1:揃える、0:揃えない)
	pagenumomission => 0,					# 多いページ番号リンクを省略(0:しない、1:する)
	pagenumomitmark => '…',				# 多いページ番号リンクを省略する際の記号
	pagenumbracket1 => '',					# ページ番号リンクの左括弧
	pagenumbracket2 => '',					# ページ番号リンクの右括弧
	pagenumseparator => '',					# ページ番号リンク間の記号
	pagelinktop => '初期表示に戻る',		# ページ移動リンク：文言「最初に戻る」

	allowdecorate => 1,						# コメント本文内の装飾記法を許可(1:する/0:しない)
	postidlinkize => 1,						# コメント本文内で指定Noへのリンク記法を許可(1:する/0:しない)
	postidlinkgtgt => 1,					# コメント本文内で >>123 形式のリンク記法を許可(1:する/0:しない)
	urlautolink => 1,						# コメント本文内のURLを自動でリンクに(1:する/0:しない)
	urllinktarget => 0,						# URLのリンク先をどこに開くか(0:同一タブ/1:新規タブ/2:フレーム解除)
	urlnofollow => 0,						# URLを自動でリンクにする際に rel="nofollow" を付加(1:する/0:しない)
	urlnoprotocol => 0,						# URLの表示時にはプロトコル名を省略(0:しない/1:する)
	longurlcutter => 40,					# 長いURLを何文字で切り詰めるか
	urlexpandimg => 1,						# URLの直前に [IMG] ラベルがあれば画像として掲載(1:する/0:しない)
	embedonlysamedomain => 0,				# 画像埋め込みのドメイン制限(0:なし/1:同一ドメイン下に限定)
	urlimagelazy => 1,						# 埋め込み外部画像にLazyLoad用の属性を付加(1:する/0:しない)
	urlimageaddclass => 0,					# 埋め込み外部画像に追加class属性を(0:加えない/1:加える)
	urlimageclass => '',					# 埋め込み外部画像に加えるclass属性値
	urlimagelightbox => 1,					# 外部画像リンクにLightbox用の属性を付加(1:する/0:しない)
	urlimagelightboxatt => 'data-lightbox="tegalog"',	# Lightbox用の属性
	urlimagelightboxcap => 'data-title',	# Lightboxのキャプション用の属性名
	urlexpandyoutube => 1,					# URLの直前に [YouTube] ラベルがあれば動画として埋め込み(1:する/0:しない)
	urlexpandspotify => 1,					# URLの直前に [Spotify] ラベルがあれば音楽として埋め込み(1:する/0:しない)
	urlexpandtweet => 1,					# URLの直前に [Tweet] ラベルがあればツイートとして埋め込み(1:する/0:しない)
	urlexpandtwtheme => 0,					# 埋め込まれるツイートのカラーテーマ(0:Light/1:Dark)
	allowlinebreak => 1,					# 改行をそのまま改行として表示(1:する/0:しない)
	keepserialspaces => 1,					# 半角空白文字の連続をそのまま表示(1:する/0:しない)
	hashtagsort => 1,						# ハッシュタグ一覧の掲載順序			(0:出現順 / 1:出現数の多い順(同位なら出現順) / 2:出現数の少ない順(同位なら出現順) / 3:出現数の多い順(同位なら文字コード順) / 4:出現数の少ない順(同位なら文字コード順)
	hashtaglinkize => 1,					# 本文表示時にハッシュタグをリンク化(1:する/0:しない)
	hashtagcut => 25,						# 長すぎるハッシュタグの表示を切り詰める文字数
	hashtagnokakko => 0,					# ハッシュタグリンクの表示時に角括弧を省略(1:する/0:しない)
	catseparator => ',',					# カテゴリ名の区切り文字
	nocatshow => 0,							# カテゴリなし投稿では、カテゴリを(0:表示しない/1:指定の代替文字を表示)
	nocatlabel => 'なし',					# カテゴリなし投稿用の指定代替文字(ラベル)
	searchlabel => '検索',					# 検索ボタンのラベル
	searchholder => '',						# 検索窓のプレースホルダ
	searchoption => 1,						# 状況に応じて検索オプションを表示(1:する/0:しない)
	cslabeluser => '投稿者名：',			# 複合検索OPTラベル:投稿者名
	cslabeldate => '投稿年月：',			# 複合検索OPTラベル:投稿年月
	cslabeltag => '＃タグ：',				# 複合検索OPTラベル:＃タグ
	cslabelcat => 'カテゴリ：',				# 複合検索OPTラベル:カテゴリ
	cslabelorder => '出力順序：',			# 複合検索OPTラベル:出力順序
	catidinsearch => 1,						# 全文検索にカテゴリIDをヒット(1:させる/0:させない)
	latestlistup => 3,						# 新着リストに掲載する個数
	latestlistparts => 'HBDTU',				# 新着リストに掲載する情報(Header,Date,Time,Username,Id,Number,Length,B=br)
	latesttitlecut => 15,					# 新着リストに掲載するタイトルの最大文字数
	usericonsize => 1,						# ユーザアイコンサイズを指定(1:する/0:しない=原寸)
	usericonsizew => 32,					# ユーザアイコンサイズwidth
	usericonsizeh => 32,					# ユーザアイコンサイズheight
	usericonsource => 0,					# ユーザアイコンサイズ指定方法(0:HTML/1:CSS)
	showstraightheader => '新しい順',		# 正順の場合の表示文字列
	showreverseheader => '時系列順' ,		# 逆順の場合の表示文字列
	msgnolist => '表示できる投稿が1件も見つかりませんでした。',	# 表示データが1件もない場合のメッセージ(通常)
	msgnopost => '指定された番号の投稿は存在しません。まだ作成されていないか、または削除されました。',	# 表示データが1件もない場合のメッセージ(単独投稿指定時)
	msgnodata => 'まだ1件も投稿されていません。',	# そもそも1件も投稿されていない場合のメッセージ
	newsignhours => 72,						# 直近投稿を示す[New!]サインを表示しておく制限時間(数値／単位:時)
	newsignhtml => 'New!',					# 直近投稿を示す[New!]サインの文字列
	postareakey => 'p',						# 投稿入力欄へのショートカットキー
	searchinputkey => 'k',					# 検索窓へのショートカットキー
	datelistShowYear => 1,					# 投稿日付リスト：年単独の階層を(1:加える/0:加えない)
	datelistShowZero => 1,					# 投稿日付リスト：月が1桁の場合に先頭に0を(1:加える/0:加えない)

	readherebtnuse => 1,					# 指定範囲を隠す装飾機能を使用(1:する/0:しない)
	readmorebtnuse => 1,					# 続きを読むボタン機能を使用(1:する/0:しない)
	readmoreonsearch => 0,					# 続きを読むボタン機能を全文検索時にも使用(1:する/0:しない)
	readmorecloseuse => 1,					# 畳むボタン機能を使用(1:する/0:しない)
	readmorebtnlabel => '続きを読む',		# 続きを読むボタンのラベル文字列
	readmorecloselabel => '畳む',			# 畳むボタンのラベル文字列
	readmorestyle => 0,						# 展開する範囲の表示方法(0:inline/1:inline-block/2:block)

	imageshowallow => 1,					# 画像表示を(1:許可/0:不許可) ※内部投稿画像に限った設定(URLの画像化は別)
	imageupallow => 1,						# 画像投稿を(1:許可/0:不許可)
	imageupmultiple => 1,					# 複数枚の画像を同時UP可能に(1:する/0:しない)
	imageupsamename => 0,					# 元のファイル名をできるだけ維持(0:しない/1:する)
	imagefullpath => 0,						# 画像のパスを絶対URLで挿入する (0:相対パスで挿入)
	imageuprequirelevel => 1,				# 画像投稿に必要な権限の最低レベル(1～9)
	imageallowext => 'png|jpg|gif|jpeg|svg|webp',	# 投稿可能な画像の拡張子リスト(半角縦棒「|」区切り。大文字小文字不問)
	imagemaxlimits => 0,					# 投稿画像容量に上限を(1:設ける/0:設けない)
	imagemaxbytes => 5242880,				# 画像1枚あたりの最大アップロード可能サイズ(単位:Bytes／標準:5242880＝5MB) ※設定値はBytes単位だが、制限容量は1024Bytes単位でしかチェックしない。
	imagefilelimit => 10000,				# 保存可能な画像の最大枚数(標準:10000)
	imagestoragelimit => 314572800,			# 保存可能な最大容量(単位:Bytes／標準:314572800＝300MB)
	imageperpage => 15,						# 画像リスト1ページあたりに表示する画像個数
	imagelimitflag => 0,					# 画像上限到達フラグ(1:ON/0:OFF)
	imagelazy => 1,							# 掲載画像にLazyLoad用の属性を付加(1:する/0:しない)
	imagetolink => 1,						# 掲載画像を原寸画像にリンク(1:する/0:しない)
	imageaddclass => 0,						# 掲載画像に追加class属性を(0:加えない/1:加える)
	imageclass => '',						# 掲載画像に加えるclass属性値
	imagelightbox => 1,						# 画像リンクにLightbox用の属性を付加(1:する/0:しない)
	imagelightboxatt => 'data-lightbox="tegalog"',	# Lightbox用の属性
	imagelightboxcap => 'data-title',		# Lightboxのキャプション用の属性名
	imagewhatt => 1,						# 可能ならimg要素にwidth属性とheight属性を付加(1:する/0:しない)
	imagewhmax => 0,						# 縦横サイズの最大値を指定(1:する/0:しない)
	imagemaxwidth => '',					# 横幅最大px
	imagemaxheight => '',					# 高さ最大px
	imageoutdir => 1,						# 任意のディレクトリにある画像の表示を許可(1:する/0:しない)
	imageouturl => 1,						# 外部サーバにある画像のURLを指定を許可(1:する/0:しない)

	isuselightbox => 1,						# 画像拡大スクリプトにLightboxを(1:使う/2:他を指定する)
	imageexpandingjs => '',					# 画像拡大スクリプト用JavaScript URL
	imageexpandingcss => '',				# 画像拡大スクリプト用CSS URL

	alwaysshowquickpost => 1,				# QUICKPOSTを常時表示するかどうか(0:しない/1:する)
	postphloginname => 1,					# 入力欄のプレースホルダにログイン中のユーザ名を表示(1:する/0:しない)
	postplaceholder => 'さん、いまなにしてる？',	# 入力欄のプレースホルダ文字列
	postareaexpander => 1,					# 入力欄の高さを[Ctrl]+[↓]キーで拡張(1:する/0:しない)
	postcharcounter => 1,					# 入力文字列のカウンタを表示(1:する/0:しない)
	postchangeidlink => 1,					# 他のIDに切り替えるリンクを表示(1:する/0:しない)
	postchangeidlabel => '他のIDに切り替える',		# 他のIDに切り替えるリンクのラベル
	postbuttonlabel => '投稿する',			# 投稿ボタンのラベル
	postbuttonshortcut => 1,				# 投稿ボタンを[Ctrl]+[Enter]で(1:押せる/0:押せない)
	textareasizenormal => 12,				# 投稿入力欄の高さ(管理画面)
	textareasizequick => 4.3,				# 投稿入力欄の高さ(QUICKPOST)
	postautofocus => 1,						# 投稿入力欄の自動フォーカス
	usedefaultcssforquickpost => 1,			# QUICKPOSTの表示時に装飾としてデフォルトの内蔵CSSを(1:使う/0:使わない)		※未実装

	showLinkBtnStyle => 0,					# リンクボタンの表示形態(2:不使用/1:常時表示/0:二段階表示)
	linkbuttonlabel => 'リンク',			# リンクボタンのラベル
	showLinkBtnUrl => 1,	linkBtnUrlLabel => '任意URLリンク',		# リンクボタン[任意URL]の表示とラベル
	showLinkBtnNum => 1,	linkBtnNumLabel => '指定No.リンク',		# リンクボタン[指定No.]の表示とラベル
	showLinkBtnImg => 0,	linkBtnImgLabel => '画像埋込リンク',	# リンクボタン[画像埋込]の表示とラベル		※デフォルトでは非表示
	showLinkBtnTwe => 1,	linkBtnTweLabel => 'ツイート埋込',		# リンクボタン[ツイート埋込]の表示とラベル
	showLinkBtnYtb => 1,	linkBtnYtbLabel => 'YouTube埋込',		# リンクボタン[YouTube埋込]の表示とラベル
	showLinkBtnSpt => 1,	linkBtnSptLabel => 'Spotify埋込',		# リンクボタン[Spotify埋込]の表示とラベル

	showDecoBtnStyle => 0,					# 装飾ボタンの表示形態(2:不使用/1:常時表示/0:二段階表示)
	decobuttonlabel => '装飾',				# 装飾ボタンのラベル
	showDecoBtnBonA => 1,	showDecoBtnBonQ => 1,	decoBtnLabelB => 'Ｂ',		# 装飾ボタン[B]の表示(編集画面,QUICKPOST) 1:表示/0:非表示
	showDecoBtnConA => 1,	showDecoBtnConQ => 1,	decoBtnLabelC => '色',		# 装飾ボタン[C]の表示(編集画面,QUICKPOST)
	showDecoBtnDonA => 1,	showDecoBtnDonQ => 1,	decoBtnLabelD => '消',		# 装飾ボタン[D]の表示(編集画面,QUICKPOST)
	showDecoBtnEonA => 1,	showDecoBtnEonQ => 1,	decoBtnLabelE => '強',		# 装飾ボタン[E]の表示(編集画面,QUICKPOST)
	showDecoBtnFonA => 0,	showDecoBtnFonQ => 0,	decoBtnLabelF => '○',		# 装飾ボタン[F]の表示(編集画面,QUICKPOST)	※デフォルトでは非表示
	showDecoBtnHonA => 1,	showDecoBtnHonQ => 1,	decoBtnLabelH => '隠す',	# 装飾ボタン[H]の表示(編集画面,QUICKPOST)	※指定範囲を隠す
	showDecoBtnIonA => 1,	showDecoBtnIonQ => 1,	decoBtnLabelI => 'Ｉ',		# 装飾ボタン[I]の表示(編集画面,QUICKPOST)
	showDecoBtnMonA => 1,	showDecoBtnMonQ => 1,	decoBtnLabelM => '背',		# 装飾ボタン[M]の表示(編集画面,QUICKPOST)
	showDecoBtnQonA => 1,	showDecoBtnQonQ => 1,	decoBtnLabelQ => '”',		# 装飾ボタン[Q]の表示(編集画面,QUICKPOST)
	showDecoBtnRonA => 1,	showDecoBtnRonQ => 1,	decoBtnLabelR => 'ル',		# 装飾ボタン[R]の表示(編集画面,QUICKPOST)
	showDecoBtnSonA => 1,	showDecoBtnSonQ => 1,	decoBtnLabelS => '小',		# 装飾ボタン[S]の表示(編集画面,QUICKPOST)
	showDecoBtnTonA => 1,	showDecoBtnTonQ => 1,	decoBtnLabelT => '極',		# 装飾ボタン[T]の表示(編集画面,QUICKPOST)
	showDecoBtnUonA => 1,	showDecoBtnUonQ => 1,	decoBtnLabelU => 'Ｕ',		# 装飾ボタン[U]の表示(編集画面,QUICKPOST)

	showImageUpBtn => 1,					# 画像アップロードボタンの表示(1:二段階表示/2:常時表示/0:非表示)
	imagebuttonlabel => '画像',				# 画像アップロードボタンのラベル
	imagedefaultplace => 3,					# 本文と同時に画像を投稿した場合の画像配置(0:本文前、1:本文前＋改行、2:本文後、3:改行＋本文後)
	showImageBtnNewUp => 1,					# 画像ボタン[アップロード]の表示（ラベルはない）
	showImageBtnExist => 1,	imageBtnExistLabel => '任意画像の挿入',		# 画像ボタン[任意画像の挿入]の表示とラベル

	showFuncBtnStyle => 0,					# 機能ボタンの表示形態(2:不使用/1:常時表示/0:二段階表示)
	funcbuttonlabel => '機能',				# 機能ボタンのラベル
	showFuncBtnSpeech => 1,					# 機能ボタン[読み上げ]の表示
	showFuncBtnStaytop => 1,				# 機能チェック[先頭に固定]の表示
	showFuncBtnDraft => 1,					# 機能チェック[下書き]の表示
	showFuncBtnRear => 1,					# 機能チェック[下げる]の表示

	showFreeDateBtn => 0,					# 投稿日付の自由入力ボタンの表示(1:表示/0:非表示)
	datebuttonlabel => '日時',				# 日付ボタンのラベル
	allowillegaldate => 0,					# 存在しない日時を許容するかどうか(1:許容してそのまま使う/0:許容せず強制修正する)

	showHashtagBtnStyle => 0,				# ハッシュタグ挿入ボタンの表示形態(2:不使用/1:常時表示/0:二段階表示)
	hashbuttonlabel => '＃',				# ハッシュタグ挿入ボタンのラベル
	hashtagBtnListupMax => 20,				# ハッシュタグ挿入ボタン用のリストアップ最大個数
	showHashBtnHash => 0,					# 「#」記号だけを単独で入力する項目を先頭に追加(0:しない/1:する)

	showCategoryBtnStyle => 0,				# カテゴリ選択ボタンの表示形態(2:不使用/1:常時表示/0:二段階表示)
	categorybuttonlabel => '区分',			# カテゴリ選択ボタンのラベル
	allowblankdeco => 0,					# 範囲選択していなくても文字装飾系記法を挿入(0:しない/1:する)

	ogpoutput => 1,							# OGP＋Twitter Cardを出力(1:する/0:しない)	*
	ogdescription => 0,						# og:description(0～1:出力パターン)	*
	oglocale => 'ja_JP',					# og:locale
	ogsitename => '',						# og:site_name
	ogtype => 0,							# og:type(0～2:出力パターン)	*
	ogimagecommonurl => '',					# og:image(共通画像のURL)
	ogimageuse1st => 1,						# 投稿に内部画像が含まれる場合に1つ目の画像URLを指定(1:する/0:しない)	*
	twittercard => 0,						# twitter:card(0:小画像/1:大画像)	*
	twittersite => '',						# twitter:site
	twittercreator => '',					# twitter:creator
	insertalttext => 1,						# 画像出力の省略時に「(画像省略)」と出力(1:する/0:しない)

	freetitlemain => 'てがろぐ',			# フリー主タイトル
	freetitlesub => '- Fumy Otegaru Memo Logger -',	# フリー副タイトル
	freedescription => 'お手軽一言掲示板（この辺の文章は「管理画面」の「設定」内にある「フリースペース」タブから編集できます。）',	# フリー概要文
	freehomename => 'ウェブサイトのHOMEへ戻る',	# フリーリンクラベル
	freehomeurl => '/',						# フリーリンクURL
	freehomeatt => 0,						# フリーリンクtarget属性値(0:なし/1:_blank/2:_top)
	freesptitle => 'フリースペース：',		# フリースペースタイトル
	freespace => '',						# フリースペース用HTML
	allowbrinfreespace => 1,				# フリースペース内に入力された改行をそのまま改行として表示するか(1:BRタグに変換して改行/0:改行は省く)

	postperpageforsyslist => 100,			# 投稿リストアップ画面での1ページあたりに表示する投稿個数

	afterpost => 0,							# 投稿直後の表示(1:ステータス画面を表示/0:HOMEに戻る)
	shiftservtime => 0,						# サーバ時刻から指定時間ずらして現在時刻を解釈する(-23.5～23.5の範囲)
	howtogetfullpath => 0,					# フルパスの取得方法(0:自動/1:手動)
	fixedfullpath => '',					# 手動設定されたフルパス(CGIの絶対URL)
	howtogetdocroot => 0,					# ドキュメントルートの取得方法(0:環境変数/1:手動)
	fixeddocroot => '',						# 手動設定されたドキュメントルート
	outputlinkfullpath => 0,				# 本文中のリンクを絶対URLで出力(0:しない/1:する)
	outputlinkkeepskin => 1,				# 本文中のリンクでスキンを維持(1:する/0:しない)
	exportpermission => 0,					# エクスポート機能の利用制限(0:しない/1以上:する)
	autobackup => 1,						# 自動バックアップ処理(0:しない/1:する)
	backupfilehold => 30,					# 自動バックアップファイルの保持日数(2以上)
	conpanecolortheme => 0,					# 管理画面のカラーテーマ
	conpanedistinction => '',				# 管理画面のタイトル先頭に表示される識別名
	conpanegallerylink => 0,				# 管理画面の下部にギャラリーへ戻るリンクを表示(0:しない/1:する)
	conpaneretlinklabel => 'てがろぐHOMEへ戻る',	# てがろぐHOMEへ戻るリンクラベル
	conpanegallerylabel => 'ギャラリーへ戻る',		# ギャラリーページへ戻るリンクラベル
	syspagelinkomit => 1,					# 管理画面内でのページネーションで途中ページを(1:省く/0:省かない)
	sysdelbtnpos => 0,						# 管理画面内での削除ボタンの位置(0:左寄せ/1:右寄せ)
	funcrestreedit => 0,					# 機能制限:他者投稿の再編集を禁止(0:しない/1:する)
	datelimitreedit => 0,					# 機能制限:投稿から指定日数を超えたら再編集を禁止(0:しない/1:する)
	datelimitreeditdays => 31,				# その日数
	loadeditcssjs => 0,						# 編集画面でedit.cssやedit.jsを読み込(0:まない/1:む)
	envlistonerror => 0,					# エラー時に環境情報を省略(0:しない/1:する)
	sessiontimenum => 31,					# セッションの有効期限(日)　※標準設定：31日（0.1日～366日）
	coexistflag => 1,						# 複数CGI共存のためにCookieにSuffixを(1:加える/0:加えない)
	coexistsuffix => '',					# 複数CGI共存のためのCookie用Suffix文字列

	addnocatitem => 0,						# カテゴリツリー末尾に「なし」を追加(0:しない/1:する)
	addnocatlabel => 'なし',				# カテゴリツリー末尾に追加する「なし」項目のリンクラベル
	categorylist => '',						# カテゴリリスト (ここでは空文字にしておくこと必須)

	skindirectory => '',					# 本番適用するスキンディレクトリ名 (.や/記号を含めると無効)

	hashtagcount => '',						# ハッシュタグ一覧と集計結果(保持用)	(配列展開前の文字列)
	dateselecthtml => '',					# 日付限定プルダウンメニューのHTMLソース (保持用)
	datelisthtml => '',						# 日付リンクリストのHTMLソース (保持用)
	latestlisthtml => '',					# 新着リストのHTMLソース (保持用)
	rbni => 0,
	signhider => 0,
	aboutcgibox => 0,
	licencecode => ''
);

# 汎用定数など
use constant {
	NOIMAGEDEFAULTICON => 'data:image/gif;base64,R0lGODlhIAAgAIAAAP///wCmUSH5BAAAAAAALAAAAAAgACAAAAJ6hIOpy2sPmpwIHorVy7z7H0SOs3VXIoapykVrulZtqMlNfNv0zuA9avPxJrCgRFgDFkeZ2OnEav40pSPIdJ1lMSJIVAVzVaDd8a54SJeN5x8ayF6DxTILfC2n03z4uOsftdRn1kVXtQWHmDSkOIbUeASlaPH4QQnpWAAAOw==',
	MOVEPAGECONFIRM => q|onclick="return confirm('このまま移動すると設定は保存されずに破棄されますが、移動しますか？（一旦キャンセルして、リンク先は別タブに表示することをお勧め致します。）');"|,
	LOADINGLAZYATT => ' loading="lazy"',
	GALLERYSEARCH => '[PICT: -\[PICT: ',
	COPYRIGHTSINCE => '2017-2022'
};

# ユーザID種別
my @userlevels;
$userlevels[1][0] = 'ゲスト'; $userlevels[1][1] = '新規投稿のみができます。';
$userlevels[3][0] = '発言者'; $userlevels[3][1] = '新規投稿・再編集(自分の投稿のみ)・削除(自分の投稿のみ)ができます。';
$userlevels[5][0] = '寄稿者'; $userlevels[5][1] = '新規投稿・再編集(自分の投稿のみ)・削除(自分の投稿のみ)・ユーザ管理(自分のIDのみ)ができます。';
$userlevels[7][0] = '編集者'; $userlevels[7][1] = '新規投稿・再編集・削除・カテゴリ管理・バックアップ・エクスポート・ユーザ管理(自分のIDのみ)ができます。';
$userlevels[9][0] = '管理者'; $userlevels[9][1] = '新規投稿・再編集・削除・カテゴリ管理・バックアップ・エクスポート・ユーザ管理・設定などすべての操作ができます。';

# 作業用変数群
my @hashtaglist;		# ハッシュタグ格納用2次元配列 (常に入っているとは限らない)
my @loadedDATA;			# <DATA>読込用

# フラグ群
my %globalFlags = (
	tweetEmbedScript => 0	# ツイート埋め込みスクリプトを既に読んだかどうか
);

# 設定ファイルを読む
&loadsettings();

# データファイルを読む
my @xmldata = &fcts::XMLin($bmsdata,'log');

# セッション有効時間(秒)を設定
my $sessiontimeout = &fcts::calcsessionlimit( $setdat{'sessiontimenum'} );

# フルパスの設定
my $cgifullurl = $cgi->url(-full, 1);
if(( $setdat{'howtogetfullpath'} == 1 ) && ( $setdat{'fixedfullpath'} ne '' )) { $cgifullurl = &fcts::forsafety( $setdat{'fixedfullpath'} ); }
my $cgifulldir = &fcts::cutafterlastslash( $cgifullurl );

# Cookie Suffix設定
my $cookiename = 'fomlid';
if( $setdat{'coexistflag'} == 1 ) {
	# Suffixを加える場合
	if( $setdat{'coexistsuffix'} eq '' ) {
		# Suffix文字列がなければランダムな5文字を作る
		$setdat{'coexistsuffix'} = &fcts::getrandstr(5);
		# 設定ファイルへ保存する
		my @trywrites;
		push( @trywrites, "coexistsuffix=" . $setdat{'coexistsuffix'} );
		&savesettings( @trywrites );
	}
	else {
		# 英数字以外は強制削除
		$setdat{'coexistsuffix'} =~ s|[^a-zA-Z0-9]||g;
	}
	$cookiename .= $setdat{'coexistsuffix'};
}
my %aif = (
	name	=> 'て'.'が'.'ろ'.'ぐ',
	puburl  => 'h'.'t'.'t'.'p'.'s'.':'.'/'.'/'.'w'.'w'.'w'.'.'.'n'.'i'.'s'.'h'.'i'.'s'.'h'.'i'.'.'.'c'.'o'.'m'.'/'.'c'.'g'.'i'.'/'.'t'.'e'.'g'.'a'.'l'.'o'.'g'.'/'
);
my %firstdat = (
	users => 'admin<>9<>名無し<>自動作成された初期ID<><>',	# ユーザ
	categories => 'info<>情報<>カテゴリ例1<>-<>0<>10<><><,>memo<>メモ<>カテゴリ例2<>-<>0<>20<><><,>diary<>日記<>カテゴリ例3<>-<>0<>30<><><,>'	# カテゴリ
);

{
	no warnings 'once';

	# ユーザ情報の分解 (2次元配列)
	@fcts::userdata = &fcts::tidyDat( ( $setdat{'userids'} || $firstdat{'users'} ) );	# ID情報がなければデフォルトのIDをセットして使う

	# カテゴリ情報の分解
	@fcts::catdata = &fcts::tidyDat( ( $setdat{'categorylist'} || $firstdat{'categories'} ) );	# カテゴリ情報が何もなければデフォルト値を設定（自らの意思で白紙化した場合は区切り文字が含まれるのでデフォルト値にはならない）

	# 共有変数をパッケージ側にもコピー
	%fcts::flagDebug = %flagDebug;
	$fcts::passfile = $passfile;
	$fcts::cgi = $cgi;
	$fcts::sessiontimeout = $sessiontimeout;
	$fcts::keepsession = $keepsession;
	$fcts::charcode = $charcode;
	$fcts::cookiename = $cookiename;
}

# 別スキンの反映(プレビューまたは簡易本番適用)
my $usebuiltinskin = '';
if( $cp{'skindir'} ne '' ) {
	# プレビューの場合
	if( $cp{'skindir'} =~ m/#(.+)#/ ) {
		# 内蔵スキンが指定されている場合
		$usebuiltinskin = 'builtinskin-' . $1;	# 内蔵スキン名を保存し
		$cp{'skindir'} = '';					# スキン名パラメータは白紙に戻す
	}
	else {
		my $newskin = &fcts::forsafety($cp{'skindir'});
		&overrideskins( $newskin );		# スキン上書き
		push( @constantParams, "skin=$newskin" );
	}
}
elsif( $setdat{'skindirectory'} ne '' ) {
	# 簡易本番適用の場合
	my $newskin = &fcts::forsafety($setdat{'skindirectory'});
	&overrideskins( $newskin );		# スキン上書き
}

# パラメータの異常チェック(必要ならエラー終了)
&checkparams();

# メイン：モード別処理
if(		$cp{'mode'} eq 'view' 		) { &modeView(); }
elsif(	$cp{'mode'} eq 'edit'		) { &modeEdit(); }
elsif(	$cp{'mode'} eq 'write'		) { &modeWrite(); }
elsif(	$cp{'mode'} eq 'admin'		) { &modeAdmin(); }
elsif(	$cp{'mode'} eq 'imageup'	) { &modeImageup(); }
elsif(	$cp{'mode'} eq 'licence'	) { &modeLicence(); }
elsif(	$cp{'mode'} eq 'export'		) { &modeExport(); }
elsif(	$cp{'mode'} eq 'rss'		) { &modeRss(); }
elsif(	$cp{'mode'} eq 'xmlsitemap'	) { &modeXmlSitemap(); }
elsif(	$cp{'mode'} eq 'sitemap'	) { &modeSitemap(); }
elsif(	$cp{'mode'} eq 'gallery'	) { &modeGallery(); }
elsif(	$cp{'mode'} eq 'random'		) { &modeRandom(); }
elsif(	$cp{'mode'} eq 'getbackup'	) { &modeGetbackupfile(); }
elsif(	$cp{'mode'} eq 'passcheck'	) { &modePasscheck(); }
else {	&showadminpage("UNDEFINED MODE",'','<p>モードパラメータの値が誤っています。</p><p>自力でURLを作った場合は、パラメータのスペル等を再確認して下さい。</p>','CAB'); }
exit;



# ------------------------
# パラメータの異常チェック
# ------------------------
sub checkparams
{
	# パラメータの異常チェック(修正不能分)
	if(( $cp{'datelim'} ne '' ) && ( $cp{'datelim'} !~ m|\A\d\d\d\d\z| ) && ( $cp{'datelim'} !~ m|\A\d\d\d\d/\d\d\z| ) && ( $cp{'datelim'} !~ m|\A\d\d\d\d/\d\d/\d\d\z| ) && ( $cp{'datelim'} !~ m|\A\d\d/\d\d\z| ) && ( $cp{'datelim'} !~ m|\A\d\d\z| )) { &illegalparam('日付指定の書式が不正です。<br>値を省略しない場合は、YYYY、YYYY/MM、YYYY/MM/DD、MM/DD、DD以外の書式は指定できません。<br>なお、年は4桁、月日はそれぞれ2桁で指定する必要があります。'); }
	if(( $cp{'order'} ne '' ) && ( $cp{'order'} ne 'reverse' ) && ( $cp{'order'} ne 'straight' )) { &illegalparam('順序の値が不正です。値には、straightかreverseしか指定できません。'); }
	if(( $cp{'userid'} ne '' ) && ( $cp{'userid'} =~ m/\W/ )) { &illegalparam('ユーザIDの値が不正です。値には、英数字しか指定できません。'); }
	if(( $cp{'postid'} ne '' ) && ( $cp{'postid'} =~ m/\D/ )) { &illegalparam('投稿IDの値が不正です。値には、数字しか指定できません。'); }
	if(( $cp{'page'} ne '' ) && ( $cp{'page'} =~ m/\D/ )) { &illegalparam('ページ番号の値が不正です。値には、数字しか指定できません。'); }

	# パラメータの異常を強制修正
	if( $cp{'page'} <= 0 ) { $cp{'page'} = 1; }			# ページ番号は1が下限
	if( $cp{'postid'}  <  0 ) { $cp{'postid'}  = 0; }	# POST IDは0が下限
	if( $setdat{'entryperpage'} < 1 ) { $setdat{'entryperpage'} = 100; }
}

sub illegalparam
{
	my $msg = shift @_ || '';
	&showadminpage('ILLEGAL PARAMETER','',"<p>$msg</p>",'B');
	exit;
}


# ===========================
# ★EXPORT MODE
# ===========================
sub modeExport
{
	# 制限チェック
	if( $setdat{'exportpermission'} > 0 ) {
		# 制限が掛かっていれば確認する
		my $permittedid = &fcts::checkpermission();		# ログイン中ユーザのID名が得られる
		if( !$permittedid ) {
			# ユーザIDを確認できない場合
			my $msg = '<p>現在の設定では、エクスポート機能はログインしているユーザにしか使用できないよう制限されています。</p>';
			&showadminpage("LOGIN REQUIRED",'',$msg,'CL');
			exit;
		}
		if( &fcts::getUserDetail($permittedid, 1) < $setdat{'exportpermission'} ) {
			# ユーザIDがあっても権限が足りない場合
			my $msg = '<p>ご使用のIDではエクスポート機能は利用できません。</p>';
			&showadminpage("NO PERMISSION",'',$msg,'CA');
			exit;
		}
	}

	# 限定条件の該当データだけを抜き出す
	my @applydata = &extractApplyData();

	# 限定条件の該当個数がゼロだったら
	if( $#applydata == -1 ) {
		my $msg = '<p>指定条件に該当する投稿が存在しないため、エクスポートできませんでした。</p><p>条件を指定し直してみて下さい。</p>';
		&showadminpage("NO DATA",'',$msg,'CA');
		exit;
	}

	# ファイル名のベースを生成
	my $dlFileName = '';
	my $datestr = $cp{'datelim'};	$datestr =~ s|/||;	# 日付指定文字列からスラッシュを削除
	if( $cp{'userid'} ne '' ) { $dlFileName .= $cp{'userid'}; }	# ユーザID追加
	if( $datestr ne '' ) { $dlFileName .= $datestr; }	# 日付追加
	if( $cp{'search'} ne '' ) { $dlFileName .= 'Search'; }	# 検索サイン追加
	if( $cp{'hasgtag'} ne '' ) { $dlFileName .= 'Tag'; }	# タグサイン追加
	if( $cp{'cat'} ne '' ) { $dlFileName .= 'Cat'; }		# カテゴリサイン追加
	if( $cp{'order'} eq 'reverse' ) { $dlFileName .= 'reverse'; }	# 逆順の場合だけ追加
	if( $cp{'postid'} > 0 ) { $dlFileName .= 'Post' . $cp{'postid'}; }	# PostID追加

	# ダミーヘッダ＋フッタを生成
	my $dmhead = qq|<html><head><meta charset="$charcode"><title>$dlFileName</title></head><body>\n|;
	my $dmfoot = "\n</body></html>\n";

	# ファイル拡張子
	my $dlFileExt = '.html';

	# プレーンテキスト指定の場合の特殊処理1
	if( $usebuiltinskin eq 'builtinskin-plaintext' ) {
		$dmhead = "■ほぼプレーンテキストでの出力\n\n";	# ダミーヘッダ
		$dmfoot = '';	# ダミーフッタなし
		$dlFileExt = '.txt';	# 拡張子

		# プレーンテキスト用の上書き設定
		$setdat{'separatepoint'} = 0;	# 日付境界バーは出力しない
		$setdat{'imagefullpath'} = 1;	# 画像は絶対URLで出力
		$setdat{'imagetolink'} = 0;		# 画像をリンクにしない
		$setdat{'urlimagelazy'} = 0;		# LazyLoad用属性を出力しない(外部画像用)
		$setdat{'imagelazy'} = 0;			# LazyLoad用属性を出力しない(内部画像用)
		$setdat{'urlimagelightbox'} = 0;	# 外部画像のLightbox用属性を出力しない
		$setdat{'readmorebtnuse'} = 0;			# 続きを読む機能を使わない
		$setdat{'readherebtnuse'} = 0;			# 指定範囲を隠す機能を使わない
		$setdat{'onepostpageutilitybox'} = 0;	# ユーティリティリンク枠を出力しない
		$setdat{'allowdecorate'} = 0;		# コメント本文内の装飾記法を許可しない
		$setdat{'postidlinkize'} = 0;		# コメント本文内で指定Noへのリンク記法を許可しない
		$setdat{'urlautolink'} = 0;			# コメント本文内のURLを自動でリンクにしない
# 		$setdat{'allowlinebreak'} = 0;			# 改行をそのまま改行として表示しない
		$setdat{'hashtaglinkize'} = 0;			# 本文表示時にハッシュタグをリンク化しない
	}

	# 出力ファイル名を生成
	if( $dlFileName eq '' ) {
		$dlFileName = 'export' . &fcts::getNowDateForFileName() . $dlFileExt;	# 条件指定がない場合は、現在の日付を使う。
	}
	else {
		$dlFileName .= $dlFileExt;
	}

	# 該当データを分解して表示用データを作成
	my @cliphtmls = &expandDataBySkin( 0, $usebuiltinskin, @applydata );

	# プレーンテキスト指定の場合の特殊処理2
	if( $usebuiltinskin eq 'builtinskin-plaintext' ) {
		foreach my $ol ( @cliphtmls ) {
			$ol =~ s|<br />|\n|g;
		}
	}

	# ヘッダoctet-streamを出力してから、データを出力
	print "Content-type: application/octet-stream\n";
	print "Content-Disposition: attachment; filename=$dlFileName\n\n\n";
	print $dmhead;
	print join("\n",@cliphtmls);
	print $dmfoot;
}


# ===========================
# ★RSS MODE
# ===========================
sub modeRss
{
	# RSSを出力するかどうか
	if( $setdat{'rssoutput'} == 0 ) {
		# RSSフィードを出力しない場合の画面
		&showadminpage('NO FEED EXIST','','<p>このCGIは、RSSフィードを出力しない設定で動作しています。</p><p>RSSフィードを出力するためには、管理画面から設定を変更して下さい。</p>','CA');
		exit;
	}

	# RSS用の上書き設定
	$setdat{'entryperpage'} = $setdat{'rssentries'};	# 出力数
	$setdat{'eppoverride'} = 1;		# 1ページあたりのエントリ数をスキン側が強制指定できるようにする
	$setdat{'separatepoint'} = 0;	# 日付境界バーは出力しない
	$setdat{'imagefullpath'} = 1;	# 画像は絶対URLで出力
	$setdat{'imagetolink'} = 0;		# 画像をリンクにしない
	$setdat{'urlimagelazy'} = 0;		# LazyLoad用属性を出力しない(外部画像用)
	$setdat{'imagelazy'} = 0;			# LazyLoad用属性を出力しない(内部画像用)
	$setdat{'urlimagelightbox'} = 0;	# 外部画像のLightbox用属性を出力しない
	$setdat{'readmorebtnuse'} = 0;			# 続きを読む機能を使わない
	$setdat{'readherebtnuse'} = 0;			# 指定範囲を隠す機能を使わない
	$setdat{'onepostpageutilitybox'} = 0;	# ユーティリティリンク枠を出力しない
	$setdat{'outputlinkfullpath'} = 1;		# 本文中のリンクを絶対URLで出力する
	$setdat{'outputlinkkeepskin'} = 0;		# 本文中のリンクで一時適用中のスキンを維持しない (RSSモードでskinパラメータを併用する場合のため)

	# 出力に使用するRSSスキンを選択（※スキンがパラメータで別途指定されていない場合のみ）
	my $rssskinname = '';
	if( $cp{'skindir'} eq '' ) {
		$rssskinname = 'builtinskin-rss';		# 適用スキンは内蔵の抜粋版
		if($setdat{'rssskin'} == 1) 	{
			$rssskinname = 'builtinskin-rssfull';	# 適用スキンを内蔵の完全版に変更
		}
		elsif($setdat{'rssskin'} == 2)	{
			# 独自rssサブフォルダを使う場合
			$setdat{'rssskindir'} = &fcts::safetydirnamecutter( $setdat{'rssskindir'} );	# 自作RSSスキン用ディレクトリの前処理(安全化)
			# 指定ディレクトリがあるかどうかを確認
			if(!( -d $setdat{'rssskindir'} )) {
				# 自作RSSスキンを使う設定になっているのに、rssサブディレクトリがなければ、エラーを表示する
				my $errdir = &fcts::forsafety( $setdat{'rssskindir'} );
				&errormsg("自作のRSSスキンを使う設定になっていますが、RSS用スキンの格納場所として指定されたディレクトリ「$errdir」が見つかりませんでした。設定を確認して下さい。CGI設置場所の直下にあるディレクトリのみ指定可能です。",'');
			}
			$rssskinname = '';							# 内蔵のスキンは使わない
			&overrideskins( $setdat{'rssskindir'} );	# スキンデータを自作版RSSスキンで上書き
		}
	}

	# 指定のRSS用スキンでVIEW MODEを実行
	&modeView($rssskinname);
}

# ===========================
# ★XML-SITEMAP MODE
# ===========================
sub modeXmlSitemap
{
	# XML-SITEMAPを出力するかどうか
	if( $setdat{'xmlsitemapoutput'} == 0 ) {
		# RSSフィードを出力しない場合の画面
		&showadminpage('NO SITEMAP XML','','<p>このCGIは、SITEMAP XMLを出力しない設定で動作しています。</p><p>SITEMAP XMLを出力するためには、管理画面から設定を変更して下さい。</p><p class="noticebox">※検索サイト向けの「SITEMAP XML」モードと、人間向けの<a href="?mode=sitemap">サイトマップページ</a>モードは、それぞれ別の存在ですのでご注意下さい。</p>','CA');
		exit;
	}

	# XML-SITEMAP用の上書き設定
	$setdat{'entryperpage'} = 49999;	# 最大出力数(1ファイルに5万件まで収録するが、てがろぐTOPのURLを別個に含めるので最大数は-1。)
	$setdat{'separatepoint'} = 0;		# 日付境界バーは出力しない
	$setdat{'onepostpageutilitybox'} = 0;	# ユーティリティリンク枠を出力しない

	# パラメータでpostidを指定されている場合は意味がない点を指摘して終了
	if( $cp{'postid'} > 0 ) {
		&showadminpage('MEANINGLESS PARAMETER','','<p>SITEMAP XMLを出力する際に、投稿番号を指定しても意味がありません。</p><p>URLのパラメータから「 postid= 」の指定を取り除いて下さい。</p>','CA');
		exit;
	}

	# 出力に使用するXML-SITEMAPスキン
	my $xmlsitemapskinname = 'builtinskin-xmlsitemap';

	# 指定のXML-SITEMAP用スキンでVIEW MODEを実行
	&modeView($xmlsitemapskinname);
}

# ===================================
# ★SITEMAP MODE (サイトマップページ)
# ===================================
sub modeSitemap
{
	# サイトマップページモードを使うかどうか
	if( $setdat{'sitemappageoutput'} == 0 ) {
		# サイトマップページを出力しない場合の画面
		&showadminpage('NO SITEMAP PAGE','','<p>このCGIは、サイトマップページモードを使わない設定で動作しています。</p><p>サイトマップページモードを表示するためには、管理画面から設定を変更して下さい。</p><p class="noticebox">※人間向けの「サイトマップページ」モードと、検索サイト向けの<a href="?mode=xmlsitemap">SITEMAP XML</a>モードは、それぞれ別の存在ですのでご注意下さい。</p>','CA');
		exit;
	}

	# サイトマップページ用の強制上書き設定
	$setdat{'entryperpage'} = $setdat{'sitemappageentries'};	# 出力数
	$setdat{'outputlinkkeepskin'} = 0;		# 本文中のリンクで一時適用中のスキンを維持しない (skinパラメータを併用する場合のため)

	# 日付境界バーの設定を上書き
	if( $setdat{'sitemappagedatebar'} == 0 ) {
		# 使わない場合
		$setdat{'separatepoint'} = 0;
	}

	# 先頭固定の設定を上書き
	if( $setdat{'sitemappagefixed'} == 0 ) {
		# 先頭固定を反映しない場合
		$setdat{'fixedpostids'} = '';	# 先頭固定の対象ID群を一時的に消す。
	}

	# サイトマップページ用のスキンを指定（※スキンがパラメータで別途指定されていない場合のみ：スキンが指定されているなら既にそれを読む準備は整っている）
	if( $cp{'skindir'} eq '' ) {
		my $sitemappageskin = '';
		$sitemappageskin = &fcts::safetydirnamecutter( $setdat{'sitemappageskindir'} );	# サイトマップページスキン用ディレクトリの前処理(安全化)
		if( $sitemappageskin eq '' ) {
			$sitemappageskin = 'skin-sitemap';		# 空白ならとりあえずデフォルト値を試す
		}

		# ディレクトリの存在確認(一応)
		if(!( -d $sitemappageskin )) {
			# サイトマップページ用スキンとして指定されたディレクトリがなければ
			&showadminpage('SKIN NOT FOUND','','<p>サイトマップページ用に使われるスキンの格納先ディレクトリ ' . &fcts::forsafety( $sitemappageskin ) . ' が見つかりません。</p><p>サイトマップページモードを使うためには、サイトマップページを生成するためのスキンが必要です。管理画面の設定を確認するか、またはデフォルトのサイトマップページ用スキンを公式サイト等から入手してアップロードして下さい。</p>','CA');
			exit;
		}

		# 指定のスキンでVIEW MODEを実行させる
		&overrideskins($sitemappageskin);		# サイトマップページ用スキンで上書き
		$setdat{'skindirectory'} = "$sitemappageskin";
	}

	# VIEWモードを実行(内蔵スキンではないので引数はナシ)
	&modeView();
}

# ===========================
# ★GALLERY MODE
# ===========================
sub modeGallery
{
	# ギャラリーモードを使うかどうか
	if( $setdat{'galleryoutput'} == 0 ) {
		# ギャラリーを出力しない場合の画面
		&showadminpage('NO GALLERY','','<p>このCGIは、ギャラリーモードを使わない設定で動作しています。</p><p>ギャラリーモードを表示するためには、管理画面から設定を変更して下さい。</p>','CA');
		exit;
	}

	# ギャラリー用の強制上書き設定
	$setdat{'entryperpage'} = $setdat{'galleryentries'};	# 出力数
	$setdat{'imagefullpath'} = 1;	# 画像は絶対URLで出力
	$setdat{'insertalttext'} = 0;	# 画像出力の省略時に「(画像省略)」とは出力しない
	$setdat{'outputlinkkeepskin'} = 0;		# 本文中のリンクで一時適用中のスキンを維持しない (skinパラメータを併用する場合のため)

	# 日付境界バーの設定を上書き
	if( $setdat{'gallerydatebar'} == 0 ) {
		# 使わない場合
		$setdat{'separatepoint'} = 0;
	}

	# ギャラリー用のスキンを指定（※スキンがパラメータで別途指定されていない場合のみ：スキンが指定されているなら既にそれを読む準備は整っている）
	if( $cp{'skindir'} eq '' ) {
		my $galleryskin = '';
		$galleryskin = &fcts::safetydirnamecutter( $setdat{'galleryskindir'} );	# ギャラリースキン用ディレクトリの前処理(安全化)
		if( $galleryskin eq '' ) {
			$galleryskin = 'skin-gallery';		# 空白ならとりあえずデフォルト値を試す
		}

		# ディレクトリの存在確認(一応)
		if(!( -d $galleryskin )) {
			# ギャラリー用スキンとして指定されたディレクトリがなければ
			&showadminpage('SKIN NOT FOUND','','<p>ギャラリー用に使われるスキンの格納先ディレクトリ ' . &fcts::forsafety( $galleryskin ) . ' が見つかりません。</p><p>ギャラリーモードを使うためには、ギャラリーページを生成するためのスキンが必要です。管理画面の設定を確認するか、またはデフォルトのギャラリー用スキンを公式サイト等から入手してアップロードして下さい。</p>','CA');
			exit;
		}

		# 指定のスキンでVIEW MODEを実行させる
		&overrideskins($galleryskin);		# ギャラリー用スキンで上書き
		$setdat{'skindirectory'} = "$galleryskin";
	}

	# VIEWモードを実行(内蔵スキンではないので引数はナシ)
	&modeView();
}

# ===========================
# ★RANDOM MODE
# ===========================
sub modeRandom
{
	# データが2件以上ある場合は、ランダムに投稿IDを決める
	if( $#xmldata > 0 ) {
		my $rnum = int(rand( $#xmldata + 1 ));				# 投稿データの中から1レコードをランダムに選ぶ
		my $rid  = &fcts::getcontent($xmldata[$rnum],'id');	# その投稿番号を得る
		$cp{'postid'} = $rid;		# 表示用にID番号パラメータを上書き
	}

	# VIEW MODEを実行 (データが1件以下の場合はランダムではない通常の表示)
	&modeView('');
}

# ===========================
# ★VIEW MODE
# ===========================
sub modeView
{
	my $builtinskin = shift @_ || '';	# 引数1：Built-inスキンを読むかどうか

	# 引数でBuilt-inスキンの指定がない場合で、グローバルに内蔵スキンの指定があればそれを使う
	if(( $builtinskin eq '' ) && ( $usebuiltinskin ne '' )) {
		$builtinskin = $usebuiltinskin;
	}

	# セキュリティ確認
	if( $nopassuser == 2 ) {
		# 全ユーザのパスワードが未設定の場合は、警告だけを表示
		if( &fcts::checkpass('') == 2 ) {
			&infoboxmsg('このCGIは、全ユーザのパスワードが未設定の状態では、何もページを表示しない設定になっています。(パスワードを設定しない低セキュリティ状態で使用が継続されてしまうのを防ぐため)<br><br>まずは、<a href="?mode=admin">管理画面</a>にログインして、パスワードを作成して下さい。','ただいま、あなたの設定を待っている状態です。下記の手順で操作して下さい。');
		}
	}

	# 使用スキンの保持用
	my $cvskin = '';

	# スキンの確認と読み込み
	if( $builtinskin eq '' ) {
		# スキンファイルの存在確認
		if(!( -f $skinfilecover )) { &errormsg('スキンファイル(外側)を読み込めませんでした。存在やファイル名を確認して下さい。',''); }
		if(!( -f $skinfileinside )) {  &errormsg('スキンファイル(内側)を読み込めませんでした。存在やファイル名を確認して下さい。',''); }

		# SKINファイルの読み込み(COVER)
		open(SKIN, $skinfilecover);			# ロック不要＆所在確認済み
		$cvskin = join("",<SKIN>);
		close SKIN;
	}
	else {
		# Built-inスキンの読み込み
		$cvskin = join("", &loadbuiltin($builtinskin . ":outer") );
	}

	my $cgipath = &getCgiPath();

	# 動作速度向上のためのフラグ群（COVER SKIN内に特定のキーワードがあるかどうかを事前に確認しておく。／動作速度向上と関係ない場合もあるが、ここで一括チェックする方が見やすいので。）
	my %isExist = (
		NAVI			=> ( $cvskin =~ m/\[\[NAVI/ ) || 0,				# ページ移動リンクがある場合（オプションも含めてチェックするので閉じ括弧を含めない）
		DATEBOX			=> ( $cvskin =~ m/\[\[DATEBOX/ ) || 0,			# 日付指定窓の掲載がある場合（同上）
		HASHTAGLIST		=> ( $cvskin =~ m/\[\[HASHTAG/ ) || 0,			# ハッシュタグリストの掲載がある場合（同上）
		CATEGORYTREE	=> ( $cvskin =~ m/\[\[CATEGORY:TREE/ ) || 0,	# カテゴリツリーの掲載がある場合（同上）
		CATEGORYPULL	=> ( $cvskin =~ m/\[\[CATEGORY:PULL/ ) || 0,	# カテゴリプルの掲載がある場合（同上）
		QUICKPOST		=> ( $cvskin =~ m/\[\[QUICKPOST\]\]/ ) || 0,	# クイック投稿フォームの掲載がある場合
		ONEPOSTnum		=> ( $cvskin =~ m/\[\[ONEPOST:\d+/ ) || 0,		# 特定番号の投稿の単独での掲載がある場合（同上）
		FREESPACE		=> ( $cvskin =~ m/\[\[FREESPACE/ ) || 0,		# フリースペースの掲載がある場合（同上）
		FREESPACEnum	=> ( $cvskin =~ m/\[\[FREESPACE:\d+/ ) || 0,	# 番号付きフリースペースの掲載がある場合（同上）
		OGP				=> ( $cvskin =~ m/\[\[OGP\]\]/ ) || 0,			# OGPの掲載がある場合
		CALENDAR		=> ( $cvskin =~ m/\[\[CALENDAR/ ) || 0,			# カレンダーの掲載がある場合
		LATESTLIST		=> ( $cvskin =~ m/\[\[LATESTLIST/ ) || 0		# 新着リストの掲載がある場合（同上）
	);
	# print STDERR $isExist{'NAVI'} . $isExist{'DATEBOX'} . $isExist{'HASHTAGLIST'} . $isExist{'QUICKPOST'} . $isExist{'FREESPACE'} . $isExist{'FREESPACEnum'};

	# -----------------------------
	# 1ページあたりの表示数を上書き
	if(( $setdat{'eppoverride'} == 1 ) && ( $cvskin =~ /\[\[TEGALOG:(\d+)\]\]/ )) {
		# スキンによる表示数の上書きが許可されている場合で、
		# かつ、スキン側に1ページ当たりの表示数が指定されている場合には、設定を上書き (安全のため上限は10000)
		# print STDERR $1;
		my $overridepagenum = int($1);
		if(( $overridepagenum >= 1 ) && ( $overridepagenum <= 10000 )) {
			$setdat{'entryperpage'} = $overridepagenum;
		}
	}

	# ----------------------------------
	# 限定条件の該当データだけを抜き出す
	my @applydata = &extractApplyData();
	my $totaldatnum = $#applydata + 1;	# 限定条件の該当個数

	# ページネーション計算
	my( $startid, $endid, $endpage );
	( $startid, $endid, $endpage, $cp{'page'} ) = &fcts::calcpagenation( $totaldatnum, $setdat{'entryperpage'}, $cp{'page'} );

	# ----------------------------
	# 表示するデータだけを抜き出す(※表示するデータがある場合だけ)
	my @showdata = ();
	if( $#applydata >= 0 ) {
		for( my $i = ($startid - 1) ; $i <= ($endid - 1) ; $i++ ){
			push( @showdata, $applydata[$i] );
		}
	}

	# -------------------------
	# どのOGP情報が必要かを判断
	my $needoneogp = 0;		# 1=個別OGP情報を要求する必要がある
	my $needcmnogp = 0; 	# 1=共通OGP情報を利用する
	if( $isExist{'OGP'} && ($setdat{'ogpoutput'} == 1) ) {
		# OGP出力場所があり、OGP出力機能がONで、
		if(    $cp{'postid'} > 0  ) { $needoneogp = 1; }	# 単独ページ表示時なら、個別情報を要求する
		elsif( $cp{'postid'} == 0 ) { $needcmnogp = 1; }	# 単独ページ以外の表示時なら、共通情報のみを使う
	}

	# ------------------------------------
	# 該当データを分解して表示用HTMLを作成
	my @cliphtmls = ();
	if( $#showdata >= 0 ) {
		# データが1件以上存在する場合のみ、内側スキンを解釈
		@cliphtmls = &expandDataBySkin( $needoneogp, $builtinskin, @showdata );
	}

	# ～～～ ▼スキンへの挿入処理(ここから) ～～～
		# ユーザが設定画面で入力した文字列 $setdat{XXX} について：
		# ●HTML不可の場合は、常に &fcts::forsafety を呼ぶ。(強制エスケープ)
		# ●セーフモードのLvに応じて変える場合は &tagcheckforsafe を呼ぶ。(選択エスケープ)

	# --------------------------
	# デモ実行用のメッセージ挿入
	if( $flagDemo{'LoginMessage'} > 0 ) {
		$cvskin =~ s/<!-- ■(\w+)■ -->/&loaddemomsg($1)/eg;
	}

	# -------------------------
	# 任意のファイルを挿入(SSI)		※パスに使えるのは英数字と / - . _ のみ。
	$cvskin =~ s/\[\[INCLUDE:([\w\/.-]+)\]\]/&serversideinclude($1)/eg;

	# ------------------------
	# 表示限定メッセージを作る
	my $situationmsg = &tegalogsystemsafety( &makeLimitMsg( $totaldatnum, $cp{'page'} ) );	# 表示用限定文字列
	my $situationcls = &fcts::trim( &makeLimitClasses( $totaldatnum, $cp{'page'} ));		# class用状況文字列

	# 表示限定案内の挿入
	my $situationhtml = '<p class="situation">' . $situationmsg . '</p>';	# 表示用にHTML化する
	my $situationplain = &fcts::safetycuttag($situationmsg);		# HTMLタグを除外する
	my $situationtitle = '';
	if( $situationmsg ne '' ) { $situationtitle = $situationplain . ' -'; }	# TITLE用に(何か掲載がある場合のみ)末尾にハイフンを加える
	$cvskin =~ s/\[\[SITUATION:HTML\]\]/$situationhtml/g;
	$cvskin =~ s/\[\[SITUATION:TITLE\]\]/$situationtitle/g;
	$cvskin =~ s/\[\[SITUATION\]\]/$situationplain/g;
	$cvskin =~ s/\[\[SITUATION:CLASS\]\]/$situationcls/g;

	# --------------------------------
	# 前後ページ移動リンクを作成＆挿入
	if( $isExist{'NAVI'} ) {
		my $nextpagelink  = '';
		my $prevpagelink  = '';
		my $pagelinksep	  = '';
		my $pagelistlinks = '';
		my $backtotoplink = '';

		# 表示対象限定クエリを作る
		my @limquery = &makeLimitQuery();

		# 投稿単独表示時なら、前後の投稿へのリンクを加える（※表示する設定の場合のみ）
		if(( $cp{'postid'} > 0 ) && ( $setdat{'pagelinkuseindv'} == 1 )) {
			my ($previdnum,$nextidnum) = &findNeighbours( $cp{'postid'} );
			if( $previdnum > 0 ) {
				# 前の投稿があれば
				my $prevlink = &makeQueryString( "postid=$previdnum" );
				my $prevno = ($setdat{'pagelinkprevindvn'} == 1) ? $previdnum : '';		# 前の投稿Noを挿入する設定の場合だけ番号を入れる
				$prevpagelink = qq|<a href="$prevlink" class="prevlink">$setdat{'pagelinkprevindv1'}$prevno$setdat{'pagelinkprevindv2'}</a>|;
			}
			if( $nextidnum > 0 ) {
				# 次の投稿があれば
				my $nextlink = &makeQueryString( "postid=$nextidnum" );
				my $nextno = ($setdat{'pagelinknextindvn'} == 1) ? $nextidnum : '';		# 次の投稿Noを挿入する設定の場合だけ番号を入れる
				$nextpagelink = qq|<a href="$nextlink" class="nextlink">$setdat{'pagelinknextindv1'}$nextno$setdat{'pagelinknextindv2'}</a>|;
			}
		}

		# 前後ページへのリンクを表示する設定の場合は、リンク文字列を作る
		if( $setdat{'pagelinkuse'} == 1 ) {
			# 1ページあたりの表示件数用文字列を作る
			my $linknumandunit = '';
			if( $setdat{'pagelinknum'} == 1 ) { $linknumandunit = $setdat{'entryperpage'} . $setdat{'pagelinkunit'}; }

			# 表示開始が1番より大きければ→前のページが存在する
			if( $startid > 1 ) {
				# 前のページがあれば戻るリンクを加える
				my $prevlink = &makeQueryString( @limquery, ('page=' . ($cp{'page'} - 1)) );
				$prevpagelink = qq|<a href="$prevlink" class="prevlink">| . &tagcheckforsafe( $setdat{'pagelinkarrowprev'} . $setdat{'pagelinkprev'} . $linknumandunit ) . '</a>';
			}

			# 表示終了が全データ数より小さければ→次のページが存在する
			if( $endid < $totaldatnum ) {
				# まだ続きのページがあれば次へリンクを加える
				my $nextlink = &makeQueryString( @limquery, ('page=' . ($cp{'page'} + 1)) );
				$nextpagelink = qq|<a href="$nextlink" class="nextlink">| . &tagcheckforsafe( $setdat{'pagelinknext'} . $linknumandunit . $setdat{'pagelinkarrownext'} ) . '</a>';
			}
		}

		# 前後両方のリンクが出力されているなら間に区切り文字を加える
		if( ($prevpagelink ne '') && ($nextpagelink ne '') ) {
			$pagelinksep = ' <span class="linkseparator">' . &tagcheckforsafe( $setdat{'pagelinkseparator'} ) . '</span> ';
		}

		# ページ番号リストリンクを作る準備（ totaldatnum:総数 / setdat{'entryperpage'}:1ページの表示数 / cp{'page'}:今のページ )
		my $totalpage = int($totaldatnum / $setdat{'entryperpage'});
		if($totaldatnum % $setdat{'entryperpage'} > 0) { $totalpage++; }		# 総ページ数 totalpage
		my $pagenumbracket1 = &tagcheckforsafe( $setdat{'pagenumbracket1'} );	# P番号左側記号 pagenumbracket1
		my $pagenumbracket2 = &tagcheckforsafe( $setdat{'pagenumbracket2'} );	# P番号右側記号 pagenumbracket2
		my $pagenumseparator = &tagcheckforsafe( $setdat{'pagenumseparator'} );	# P番号境界記号 pagenumseparator
		my $pagefigures = ($setdat{'pagenumfigure'} == 1) ? length($totalpage) : 1;	# ページ番号リンクの桁を揃えるかどうかの設定に応じて、番号の表示精度を指定（※揃える場合は最大桁数を代入。揃えない場合は1を代入）
		my $pagenumomission = $setdat{'pagenumomission'} || 0;	# P番号の途中を省略(1:する/0:しない)
		my $nowpagenum = $cp{'page'};	# 現在P番号
		my $pagenumomitmark = $setdat{'pagenumomitmark'};	# 途中P省略記号
		my $classnameforpagenumlink = 'pagenumlink';	# ページ番号リンクに付加するclass名

		# ページ番号リストリンクを生成する
		$pagelistlinks = &fcts::outputPageListLinks(
			$totalpage, $nowpagenum, $pagenumbracket1, $pagenumbracket2, $pagenumseparator,	# 引数1:総ページ数 totalpage、引数2:現在P番号 nowpagenum、引数3:P番号左側記号 pagenumbracket1、引数4:P番号右側記号 pagenumbracket2、引数5:P番号境界記号 pagenumseparator
			$pagefigures, $pagenumomission, $pagenumomitmark, $classnameforpagenumlink,		# 引数6:番号の表示精度 pagefigures、引数7:P番号の途中を省略(1:する/0:しない) pagenumomission、引数8:途中P省略記号 pagenumomitmark、引数9:付加class名 classnameforpagenumlink
			&makeQueryString( &makeLimitQuery(), 'page=')									# 引数10以降:リンクに付加するパラメータベース (※makeLimitQueryを加えないと、表示対象の限定状況を維持できないので注意。)
		);

		# 表示対象が限定されている際には「全体表示に戻る」リンクを作る
		if( $cp{'postid'} > 0 || $cp{'userid'} ne '' || $cp{'cat'} ne '' || $cp{'hasgtag'} ne '' || $cp{'search'} ne '' || $cp{'datelim'} ne '' || $cp{'mode'} eq 'gallery' ) {
			my $homelink = &makeQueryString('');
			$backtotoplink .= qq|<a href="$homelink">| . &tagcheckforsafe( $setdat{'pagelinktop'} ) . "</a>\n";
		}

		# ページ移動リンクの挿入（COVERスキンに対して）
		$cvskin =~ s/\[\[NAVI:PAGELIST\]\]/$pagelistlinks/g;
		$cvskin =~ s/\[\[NAVI:PREVNEXT\]\]/$prevpagelink $pagelinksep $nextpagelink/g;
		$cvskin =~ s/\[\[NAVI:TOPPAGE\]\]/$backtotoplink/g;
		$cvskin =~ s/\[\[NAVI\]\]/$pagelistlinks $prevpagelink $pagelinksep $nextpagelink $backtotoplink/g;
	}

	# --------------------------------------
	# 画像拡大用スクリプト(Lightbox等)の挿入
	if( $setdat{'imageshowallow'} == 1 || $setdat{'urlexpandimg'} == 1 ) {
		# 画像の挿入表示が許可されている場合のみ
		my $existlbimage = 0;	
		# 画像拡大スクリプト用記述の存在チェック用正規表現を作る
		my $cfreg = &fcts::forsafetytag( $setdat{'imagelightboxatt'} ) . '|' . &fcts::forsafetytag( $setdat{'urlimagelightboxatt'} ) . '|' .
					&fcts::forsafety( $setdat{'imageclass'} ) . '|' . &fcts::forsafety( $setdat{'urlimageclass'} );
		# 画像拡大スクリプト用記述の存在を確認
		foreach my $oi ( @cliphtmls ) {
			if( $oi =~ m/$cfreg/ ) {
				$existlbimage = 1;
				last;
			}
		}
		if( $existlbimage == 1 ) {
			# Lightboxを参照する属性が存在する場合のみ
			$cvskin =~ s/\[\[JS:LIGHTBOX:JQ\]\]/&outputLightboxLoader(1,0)/e;		# jQuery＋Lightboxを読み込み
			$cvskin =~ s/\[\[JS:LIGHTBOX\]\]/&outputLightboxLoader(0,0)/e;		# Lightboxのみを読み込み
		}
		else {
			$cvskin =~ s/\[\[JS:LIGHTBOX.*\]\]/<!-- 画像拡大用スクリプトを必要としない状況なのでスクリプトは挿入されません。 -->/g;
		}
	}
	else {
		$cvskin =~ s/\[\[JS:LIGHTBOX.*\]\]/<!-- 画像表示を許可しない設定なので、画像拡大用スクリプトは挿入されません。 -->/g;
	}

	# --------------------------
	# フリースペースの挿入
	if( $isExist{'FREESPACE'} ) {
		# フリースペース内の自動挿入改行の処理
		if( $setdat{'allowbrinfreespace'} == 0 ) {
			# 入力された改行を、改行タグとして出力しない設定の場合は、改行タグを取り除く（※記録時に、改行コードは<br>に変換されている）
			$setdat{'freespace'} =~ s/<br>//g;
		}

		# 番号付きフリースペースの挿入
		if( $isExist{'FREESPACEnum'} ) {
			# 番号付きフリースペースの掲載がある場合のみ処理：
			my @eachfreespaces = split(/<>/,$setdat{'freespace'});
			$cvskin =~ s/\[\[FREESPACE:(\d+)\]\]/&tagcheckforsafe($eachfreespaces[$1])/eg;
		}

		# 番号なしフリースペースの挿入
		$setdat{'freespace'} =~ s/<>//g;		# 区切り文字を削除しておく。
		$cvskin =~ s/\[\[FREESPACE\]\]/&tagcheckforsafe($setdat{'freespace'})/eg;

		# フリースペース編集用URLの挿入
		my $fseurl = &makeQueryString( 'mode=admin', 'work=setting', 'page=3');
		$cvskin =~ s/\[\[FREESPACEEDIT:URL\]\]/$fseurl/g;
	}

	# フリー文言関連の挿入
	$cvskin =~ s/\[\[FREESPTITLE\]\]/&fcts::forsafety($setdat{'freesptitle'})/eg;
	$cvskin =~ s/\[\[FREE:TITLE:MAIN\]\]/&fcts::forsafety($setdat{'freetitlemain'})/eg;
	$cvskin =~ s/\[\[FREE:TITLE:SUB\]\]/&fcts::forsafety($setdat{'freetitlesub'})/eg;
	$cvskin =~ s/\[\[FREE:DESCRIPTION\]\]/&fcts::forsafety($setdat{'freedescription'})/eg;

	# フリーリンクの挿入
	my $flatt = '';
	if(		$setdat{'freehomeatt'} == 1 ) { $flatt = ' target="_blank"'; }
	elsif(	$setdat{'freehomeatt'} == 2 ) { $flatt = ' target="_top"'; }
	my $flhtml = '<a href="' . &fcts::forsafety($setdat{'freehomeurl'}) . '"' . $flatt . '>' . &fcts::forsafety($setdat{'freehomename'}) . '</a>';
	$cvskin =~ s/\[\[FREE:HOMELINK\]\]/$flhtml/g;

	# ------------------------
	# 特定番号の投稿だけを挿入
	if( $isExist{'ONEPOSTnum'} ) {
		$cvskin =~ s/\[\[ONEPOST:(\d+)\]\]/&insertOnePost($1)/eg;
	}

	# --------------------------
	# 日付指定窓の挿入
	if( $isExist{'DATEBOX'} ) {
		# 日付指定窓の掲載がある場合のみに処理：
		if( $setdat{'dateselecthtml'} eq '' || $setdat{'datelisthtml'} eq '' ) {
			# 日付限定プルダウンメニューのHTMLソース・日付リンクリストのHTMLソースのどちらかが空なら生成処理を先にする
			&datadatecounter();
		}

		# 日付検索フォームを作る
		my $dateselectform = &addSelectedForPulldownDateList( $setdat{'dateselecthtml'} );
		$dateselectform = qq|<form action="$cgipath" method="get" class="datelimitbox">$dateselectform</form>|;

		$cvskin =~ s/\[\[DATEBOX\]\]/$setdat{'datelisthtml'}\n$dateselectform/g;	# 両方
		$cvskin =~ s/\[\[DATEBOX:PULL\]\]/$dateselectform/g;			# 日付検索窓
		$cvskin =~ s/\[\[DATEBOX:LIST\]\]/$setdat{'datelisthtml'}/g;	# 日付リンクリスト
	}

	# ------------------------------
	# 新着リスト（最近の投稿）の挿入
	if( $isExist{'LATESTLIST'} ) {
		# 新着リストの掲載がある場合のみに処理：
		if( $setdat{'latestlisthtml'} eq '' ) {
			# 新着リストのHTMLソースが空なら生成処理を先にする
			&updatelatestlist( $setdat{'latestlistup'} , $setdat{'latestlistparts'} , $setdat{'latesttitlecut'} );
		}

		$cvskin =~ s/\[\[LATESTLIST\]\]/$setdat{'latestlisthtml'}/g;	# 新着リスト
	}

	# --------------------------
	# ハッシュタグリストの挿入	(※スキン仮適用中はskinパラメータが二重になるが、実害はないので放置。)
	if( $isExist{'HASHTAGLIST'} ) {
		# ハッシュタグリストの掲載がある場合のみに処理：
			# ▼製作メモ：
			# リスト用ソースは変数 $hashtagliststring に構築する。
			# プルダウン用ソースは、HTMLのみ版とJS版とで必要なソース構成が異なるため、変数 $hashtagpullstring1 + 2(a/b) + 3 + 4(a/b) で構成する。
			# リスト用ソースとプルダウン用ソースを同時に生成していくのでソースが見づらいが、どの変数名に代入しているのかを参考にすると処理を追いやすいハズ。
		my $hashtagliststring = '<ul class="hashtaglist">';
		my $hashtagpullstring1 = qq|<form action="$cgipath" method="get" class="hashtagpullbox">|;
		my $hashtagpullstring2a = '<select class="hashtagpull" name="tag">';
		my $hashtagpullstring2b = '<select class="hashtagpull" name="tag" onchange="submit();">';
		my $hashtagpullstring3 = '<option class="head" value="">(ハッシュタグを選択)</option>';
		my @hashtagdata = split(/<<<--->>>/,$setdat{'hashtagcount'});
		foreach my $onehash (@hashtagdata) {
			# ハッシュタグの名称とカウンタを分離
			my ($onehashname,$onehashcount) = split(/:::---:::/,$onehash);
			# リンク化して出力(制限文字数に応じて切り詰める)
			my $cuttedtagname = &fcts::forsafety( &fcts::mbSubstr($onehashname,$setdat{'hashtagcut'},'...'));
			$hashtagliststring  .= "\n<li class=\"count$onehashcount\">" . &makelinktagforhashtag( &fcts::forsafety($onehashname), 0 ) . $cuttedtagname . "</a><span class=\"num\">($onehashcount)</span></li>";
			my $nowTag = '';
			if( $cp{'hasgtag'} eq $onehashname ) {
				# 今表示中のハッシュタグなら選択しておく
				$nowTag = ' selected';
			}
			$hashtagpullstring3 .= "\n<option value=\"" . &fcts::forsafety($onehashname) . "\"$nowTag>$cuttedtagname ($onehashcount)</option>";
		}
		if( $#hashtagdata == -1 ) {
			# ハッシュタグが1つも記録されていなければ
			$hashtagliststring  .= qq|<li class="notexist">ハッシュタグは見つかりませんでした。(または、まだ集計されていません。)|;
			$hashtagpullstring3 .= qq|<option class="head">(なし)</option>|;
		}
		$hashtagliststring  .= "\n</ul>\n";
		$hashtagpullstring3 .= "\n</select>";
		my $hashtagpullstring4a .= q|<input type="submit" value="表示" class="hashtagpullsubmit"></form>|;
		my $hashtagpullstring4b .= q|</form>|;
		$cvskin =~ s/\[\[HASHTAG:LIST\]\]/$hashtagliststring/g;		# ハッシュタグ:リストを挿入
		$cvskin =~ s/\[\[HASHTAGLIST\]\]/$hashtagliststring/g;		# 古い書き方も許容する
		$cvskin =~ s/\[\[HASHTAG:PULL\]\]/$hashtagpullstring1$hashtagpullstring2a$hashtagpullstring3$hashtagpullstring4a/g;		# ハッシュタグ:プルダウンメニューを挿入
		$cvskin =~ s/\[\[HASHTAG:PULL:JS\]\]/$hashtagpullstring1$hashtagpullstring2b$hashtagpullstring3$hashtagpullstring4b/g;	# ハッシュタグ:プルダウンメニューJS版を挿入
	}

	# --------------------
	# カテゴリツリーの挿入
	if( $isExist{'CATEGORYTREE'} ) {
		if( $cvskin =~ m/\[\[CATEGORY:TREE\]\]/ ) {
			# デフォルト設定のツリーを出力するなら
			my $catTreeSource = &makeCategoryTree();			# 先にカテゴリツリーを生成しておく (同じツリーを何度も生成してしまわないように)
			$cvskin =~ s/\[\[CATEGORY:TREE\]\]/$catTreeSource/g;
		}
		# フラグ付きのカテゴリツリーを出力
		$cvskin =~ s/\[\[CATEGORY:TREE:(.+?)\]\]/&makeCategoryTree($1)/eg;
	}

	# カテゴリプルダウンメニューの挿入
	if( $isExist{'CATEGORYPULL'} ) {
		# ▼製作メモ：プルダウン用ソースは「HTMLのみ版」と「JS版」とで必要なソース構成が異なるため、変数 $catPullSource1 + 2(a/b) + 3 + 4(a/b) で構成する。
		my @cats = &fcts::getCategoryList(2);	# 「カテゴリID<>カテゴリ名<>該当数」の配列を得る
		my $catPullSource1 = qq|<form action="$cgipath" method="get" class="catpullbox">|;
		my $catPullSource2a = '<select class="catpull" name="cat">';
		my $catPullSource2b = '<select class="catpull" name="cat" onchange="submit();">';
		my $catPullSource3 = '<option class="head" value="">(カテゴリを選択)</option>';
		foreach my $oneCat ( @cats ) {
			# カテゴリ1件のデータを、ID・名称・該当数の3つに分解
			my @catDetails = split(/<>/,$oneCat);
			my $catName = &fcts::forsafety($catDetails[1]);
			my $nowCat = '';
			if( $cp{'cat'} eq $catDetails[0] ) {
				# 今表示中のカテゴリなら選択しておく
				$nowCat = ' selected';
			}
			$catPullSource3 .= qq|<option value="$catDetails[0]"$nowCat>$catName ($catDetails[2])</option>|;
		}
		$catPullSource3 .= "\n</select>";
		my $catPullSource4a .= q|<input type="submit" value="表示" class="catpullsubmit"></form>|;
		my $catPullSource4b .= q|</form>|;
		$cvskin =~ s/\[\[CATEGORY:PULL\]\]/$catPullSource1$catPullSource2a$catPullSource3$catPullSource4a/g;	# カテゴリ:プルダウンメニューを挿入
		$cvskin =~ s/\[\[CATEGORY:PULL:JS\]\]/$catPullSource1$catPullSource2b$catPullSource3$catPullSource4b/g;	# カテゴリ:プルダウンメニューJS版を挿入
	}

	# --------------------------
	# クイック投稿フォームの挿入
	if( $isExist{'QUICKPOST'} ) {
		# クイック投稿フォームの掲載がある場合のみに処理：
		my $quickpost;
		my $permittedid = &fcts::checkpermission(1);	# 読み取り専用モードで認証を確認
		if( !$permittedid && ($setdat{'alwaysshowquickpost'} == 0) ) {
			# ログインしておらず、QUICKPOSTの常時表示も設定されていない場合
			$quickpost = q|<style type="text/css">.Login-Required { display: none !important; } /* ログインされていません */</style>|;
		}
		else {
			# ログインしているか、常時表示が設定されている場合はフォームを表示
			$quickpost = &makepostform( '', '', '', '', '', '', 'QUICK' );
		}
		$cvskin =~ s/\[\[QUICKPOST\]\]/&fcts::uniquerand($quickpost)/eg;
	}

	# --------------------
	# 新規投稿リンクの挿入
	my $unp = &makeQueryString('mode=edit');
	$cvskin =~ s/\[\[NEWPOST:URL\]\]/$unp/g;
	$cvskin =~ s/\[\[NEWPOST:URL:FULL\]\]/$cgifullurl$unp/g;	# 絶対URL

	# 管理画面リンクの挿入
	my $uam = &makeQueryString('mode=admin');
	$cvskin =~ s/\[\[ADMIN:URL\]\]/$uam/g;
	$cvskin =~ s/\[\[ADMIN:URL:FULL\]\]/$cgifullurl$uam/g;	# 絶対URL

	# ランダムリンクの挿入
	my $rdl = &makeQueryString('mode=random');
	$cvskin =~ s/\[\[RANDOM:URL\]\]/$rdl/g;
	$cvskin =~ s/\[\[RANDOM:URL:FULL\]\]/$cgifullurl$rdl/g;	# 絶対URL

	# HOME(CGIが生成するTOPページ)へ戻るリンクの挿入
	$cvskin =~ s/\[\[HOME:URL\]\]/&getCgiPath()/eg;		# スキン維持(相対パス)
	$cvskin =~ s/\[\[HOME:URL:FULL\]\]/$cgifullurl/g;	# スキン無視(絶対URL)

	# RSSリンクの挿入 (一時適用スキンは無視する)
	my $urf = '?mode=rss';
	my $limitforurf = '&amp;' . join('&amp;', &makeLimitQuery(1));	# 現在の表示限定対象パラメータを &amp; で繋ぐ
	$cvskin =~ s/\[\[RSS:URL\]\]/$cginame$urf$limitforurf/g;			# 相対パスだが(後処理で)一時適用スキンが追加されないようにCGI名を加えておく
	$cvskin =~ s/\[\[RSS:URL:FULL\]\]/$cgifullurl$urf$limitforurf/g;	# 絶対URL
	$cvskin =~ s/\[\[RSS:URL:PURE\]\]/$cginame$urf/g;			# 表示限定なし：相対URL
	$cvskin =~ s/\[\[RSS:URL:PURE:FULL\]\]/$cgifullurl$urf/g;	# 表示限定なし：絶対URL

	# ギャラリーリンクの挿入 (一時適用スキンは無視する)
	my $glr = '?mode=gallery';
	$cvskin =~ s/\[\[GALLERY:URL\]\]/$cginame$glr/g;			# 相対パスだが(後処理で)一時適用スキンが追加されないようにCGI名を加えておく
	$cvskin =~ s/\[\[GALLERY:URL:FULL\]\]/$cgifullurl$glr/g;	# 絶対URL

	# サイトマップページリンクの挿入 (一時適用スキンは無視する)
	my $smp = '?mode=sitemap';
	$cvskin =~ s/\[\[SITEMAP:URL\]\]/$cginame$smp/g;			# 相対パスだが(後処理で)一時適用スキンが追加されないようにCGI名を加えておく
	$cvskin =~ s/\[\[SITEMAP:URL:FULL\]\]/$cgifullurl$smp/g;	# 絶対URL

	# --------------------------
	# バージョン情報の挿入
	my $pwrdbypre = '<!-- ' . $aif{'name'} . ' Version: -->';
	my $pwrdbypos = '';
	if(( $setdat{'signhider'} == 1 ) && ( &fcts::lcc($setdat{'licencecode'}) )) {
		$pwrdbypre = '<!-- ' . &fcts::showlccover($setdat{'licencecode'});
		$pwrdbypos = ' -->';
	}
	my $poweredby = qq|Powered by <a href="$aif{'puburl'}" target="_top">$aif{'name'}</a> Ver $versionnum|;
	if( $rentalflag == 1 ) { $poweredby .= ' (<a href="/">レンタル版</a>)' }
	$cvskin =~ s/\[\[VERSION\]\]/$pwrdbypre$poweredby$pwrdbypos/g;

	# --------------------------
	# 今の表示を逆順にするURLの挿入
	my $revurl = &managequerystring('order','reverse');
	$cvskin =~ s/\[\[REVERSE:URL\]\]/$revurl/g;

	# 今の表示を逆順にする名称の挿入
	if( $cp{'order'} eq 'reverse' ) {
		# 今が逆順なら正順を挿入
		$cvskin =~ s/\[\[REVERSE:NAME\]\]/&fcts::forsafety($setdat{'showstraightheader'})/eg;
	}
	else {
		# 今が正順なら逆順を挿入
		$cvskin =~ s/\[\[REVERSE:NAME\]\]/&fcts::forsafety($setdat{'showreverseheader'})/eg;
	}

	# --------------------------
	# カレンダーの挿入
	if( $isExist{'CALENDAR'} ) {
		# カレンダーの掲載がある場合のみに処理：
		my $firstdate = '';

		# dateパラメータで年月が指定されていれば、それをそのまま採用する
		if( $cp{'datelim'} =~ m|^(\d{4})/(\d{1,2})| ) {
			# 年と月の指定があれば
			if( $2 <= 12 ) {
				# 月が12以下の場合だけ採用
				$firstdate = "$1/$2";
			}
		}

		# (dateパラメータから得られなかった場合は)表示対象の先頭の日付を得る (表示データが1件以上存在する場合のみ)
		elsif( $#showdata >= 0 ) {

			my $n = 0;	# カレンダーに採用する日付のある投稿の(表示対象配列内での)位置

			# 先頭固定投稿がある場合はそれらを除外して考える(表示条件が限定されていない場合に限る)
			if(( $setdat{'fixedpostids'} ne '' ) && ( &islimited == 0 )) {
				# 表示条件が限定されておらず、先頭固定投稿があればリストアップする
				my @topnums = split(/,/,$setdat{'fixedpostids'});	# 先頭固定する投稿番号の配列を作る

				# 表示対象を1件ずつ調べて、先頭固定ではない最初の投稿が何番目($n)にあるのかを調べる
				for( $n = 0 ; $n <= $#showdata ; $n++ ) {
					# n番目の投稿番号を得る
					my $tryid = &fcts::forsafety( &fcts::getcontent($showdata[$n],'id') );
					# その投稿番号が先頭固定リストに含まれるかどうかを調べる
					my $matched = 0;
					foreach my $fixid ( @topnums ) {
						if( $fixid eq '' ) { next; }	# 不正な値があれば飛ばす(空文字列をif文で数値として比較するのを防ぐ)
						if( $fixid == $tryid ) {
							# 一致したらフラグを立ててループ終了
							$matched = 1;
							last;
						}
					}
					# 含まれていなかったら、それが先頭固定ではない最初の投稿(の位置)なのでループ終了
					if( $matched == 0 ) {
						last;
					}
				}
			}

			if( $n > $#showdata ) {
				# 全件が先頭固定だったら現在日時を採用する (＝空文字のまま何も代入しない)
			}
			else {
				# 指定番目にある投稿の日付を採用する
				$firstdate = &fcts::forsafety( &fcts::getcontent($showdata[$n],'date') );
			}
		}

		# 日付データが抜き出せなかった場合のために現在月日を得ておく
		my ($fmonth,$fyear) = (localtime(time))[4,5];
		$fyear += 1900;
		$fmonth += 1;

		# 日付データを抜き出せたらその月日をカレンダー表示用に使う
		if( $firstdate =~ m|^(\d{4})/(\d{1,2})/?| ) {
			$fyear = $1;
			$fmonth = $2;
		}

		# カレンダーを生成
		$cvskin =~ s/\[\[CALENDAR\]\]/&getCalendarBox($fyear,$fmonth,0)/eg;
		$cvskin =~ s/\[\[CALENDAR:(-?\d{1,4})\]\]/&getCalendarBox($fyear,$fmonth,$1)/eg;

		# カレンダー移動リンクを出力
		$cvskin =~ s/\[\[MOVEMONTH:(-?\d{1,4}):URL\]\]/&getOneMonthPageUrl($fyear,$fmonth,$1)/eg;
		$cvskin =~ s/\[\[MOVEMONTH:(-?\d{1,4}):URL:FULL\]\]/$cgifullurl . &getOneMonthPageUrl($fyear,$fmonth,$1)/eg;
	}

	# --------------------------
	# 文字コードの挿入
	$cvskin =~ s/\[\[CHARCODE\]\]/$charcode/g;

	# --------------------------
	# 各種情報の挿入
	$cvskin =~ s/\[\[INFO:TARGETPOSTS\]\]/$totaldatnum/g;	# 表示対象になっている投稿の数

	if( $cvskin =~ m/\[\[INFO:LASTUPDATE/ ) {
		# 最終投稿日時を取得する必要がある場合のみ取得
		my @fs = stat $bmsdata;
		my $lastup = &fcts::getdatetimestring( $fs[9] ); # 更新時刻

		# 時刻をずらす設定ならずらす
		if( $setdat{'shiftservtime'} != 0 ) {
			$lastup = &fcts::shifttime( $lastup, $setdat{'shiftservtime'} );
		}

		$cvskin =~ s/\[\[INFO:LASTUPDATE\]\]/$lastup/g;
		$cvskin =~ s/\[\[INFO:LASTUPDATE:(.+?)\]\]/&arrangeDateStr($1,$lastup)/eg;
	}

	# ページ番号の挿入
	$cvskin =~ s/\[\[INFO:PAGENUM\]\]/$cp{'page'}/g;

	# --------------------------
	# 検索窓の挿入
	my $searchboxhtml = qq|<form action="$cgipath" method="get" class="searchbox"><span class="searchinputs"><input type="text" value="| . &fcts::forsafety($cp{'search'}) . q|" name="q" class="queryinput" placeholder="| . &fcts::forsafety($setdat{'searchholder'}) . q|" accesskey="| . &fcts::forsafety($setdat{'searchinputkey'}) . q|"><input type="submit" value="| . &fcts::forsafety($setdat{'searchlabel'}) . q|" class="submitbutton"></span>|;
	# 検索オプションの作成
	if( $setdat{'searchoption'} != 0 ) {
		# オプション出力を拒否していない場合のみ
		my $searchoptions = '';
		if( $cp{'userid'} ne '' ) {
			$searchoptions .= qq|<label class="searchoption"><input type="checkbox" value="| . &fcts::forsafety($cp{'userid'}) . qq|" name="userid" checked>表示中のユーザに限定して検索</label><br>|;
		}
		if( $cp{'hasgtag'} ne '' ) {
			$searchoptions .= qq|<label class="searchoption"><input type="checkbox" value="| . &fcts::forsafety($cp{'hasgtag'}) . qq|" name="tag" checked>表示中のハッシュタグに限定して検索</label><br>|;
		}
		if( $cp{'cat'} ne '' ) {
			$searchoptions .= qq|<label class="searchoption"><input type="checkbox" value="| . &fcts::forsafety($cp{'cat'}) . qq|" name="cat" checked>表示中のカテゴリに限定して検索</label><br>|;
		}
		if( $cp{'datelim'} ne '' ) {
			$searchoptions .= qq|<label class="searchoption"><input type="checkbox" value="| . &fcts::forsafety($cp{'datelim'}) . qq|" name="date" checked>表示中の日付範囲に限定して検索</label><br>|;
		}
		if( $cp{'mode'} eq 'gallery' ) {
			my $galleryname = &fcts::forsafety($setdat{'galleryname'});
			if( $galleryname eq '' ) { $galleryname = 'ギャラリー'; }	# 名称が空文字だったら、とりあえずギャラリーと表記しておく。
			$searchoptions .= qq|<label class="searchoption"><input type="checkbox" value="gallery" name="mode" checked>$galleryname内に限定して検索</label><br>|;
		}
		if( $cp{'mode'} eq 'sitemap' ) {
			my $sitemappageyname = &fcts::forsafety($setdat{'sitemappageyname'});
			if( $sitemappageyname eq '' ) { $sitemappageyname = 'サイトマップ'; }	# 名称が空文字だったら、とりあえずギャラリーと表記しておく。
			$searchoptions .= qq|<label class="searchoption"><input type="checkbox" value="sitemap" name="mode" checked>検索結果を$sitemappageynameとして表示</label><br>|;
		}
		# 検索オプションがあれば挿入する
		if( $searchoptions ne '' ) {
			$searchboxhtml .= '<p class="searchtarget limitedsearch">' . $searchoptions . '</p>';
		}
	}
	$searchboxhtml .= '</form>';
	$cvskin =~ s/\[\[SEARCHBOX\]\]/$searchboxhtml/g;

	# --------------------------
	# 複合検索窓の挿入
	$cvskin =~ s/\[\[SEARCHBOX:COMPLEX\]\]/&complexsearchform()/eg;
	$cvskin =~ s/\[\[SEARCHBOX:COMPLEX:\]\]/$searchboxhtml/g;					# この場合は複合ではない単検索窓を挿入する
	$cvskin =~ s/\[\[SEARCHBOX:COMPLEX:(.+?)\]\]/&complexsearchform($1)/eg;

	# ----------------------
	# OGP＋Titter Cardを挿入
	if( $isExist{'OGP'} ) {
		# OGP出力場所がある場合のみ実行
		my $ogpmeta = '';	# 出力metaタグ格納用

		if( $#cliphtmls >= 0 ) {
			# 表示用データが1件以上ある場合のみ中身を解釈する

			# OGP画像 (まずは共通画像の採用判定のみを行う(※指定があればそれを使用。空欄ならデフォルト提供画像を使用))
			my $imageurlforogp = $libdat{'ogimagedefault'};
			if( $setdat{'ogimagecommonurl'} ne '' ) { $imageurlforogp = &fcts::forsafety($setdat{'ogimagecommonurl'}); }

			# 状況別項目を生成 (og:title , og:description , og:type , og:image)
			if( $needoneogp == 1 ) {
				# 個別用OGPを出力
				$ogpmeta = "<!-- ▼投稿単独用OGPを出力 -->\n";

				# title, description, image を抽出 (＋元データは出力しないよう消しておく) ※表示データ件数が0の際には下記のif文が実行されないよう注意する
				if( $cliphtmls[0] =~ s/<!-- OGPmetadata:\s(.+)\s:mO -->// ) {
					# さらに分解
					if( $1 =~ /Ot:\s(.*)\s:tOOd:\s(.*)\s:dOOi:\s(.*)\s:iO/ ) {
						$ogpmeta .= qq|<meta property="og:title" content="$1">\n|;			# og:title
						$ogpmeta .= qq|<meta property="og:description" content="$2">\n|;	# og:description
						if(( $3 ne '' ) && ( $setdat{'ogimageuse1st'} == 1 )) { $imageurlforogp = $3; }		# og:imageに抽出画像を使うよう指定 (画像が含まれていて、1枚目の画像をOGPに使う設定なら)
					}
				}

				if(( $setdat{'ogtype'} == 0 ) || ( $setdat{'ogtype'} == 1 )) { $ogpmeta .= q|<meta property="og:type" content="article">| . "\n"; }	# og:type = article
				else { $ogpmeta .= q|<meta property="og:type" content="website">| . "\n"; }	# og:type = website
			}
			elsif( $needcmnogp == 1 ) {
				# 全体用OGPを出力
				$ogpmeta = "<!-- ▼共通OGPを出力 -->\n";
				$ogpmeta .= q|<meta property="og:title" content="| . "$situationtitle " . &fcts::forsafety($setdat{'freetitlemain'}) . ' ' . &fcts::forsafety($setdat{'freetitlesub'}) . qq|">\n|;	# og:title = シチュエーション＋メイン題＋サブ題
				$ogpmeta .= q|<meta property="og:description" content="| . &fcts::forsafety($setdat{'freedescription'}) . qq|">\n|;		# og:description = フリー一行概要文

				if(( $setdat{'ogtype'} == 0 ) || ( $setdat{'ogtype'} == 2 )) { $ogpmeta .= q|<meta property="og:type" content="website">| . "\n"; }	# og:type = website
				else { $ogpmeta .= q|<meta property="og:type" content="article">| . "\n"; }	# og:type = article
			}

			# 共通項目を生成
			if(( $needoneogp == 1 ) || ( $needcmnogp == 1 )) {
				$ogpmeta .= q|<meta property="og:url" content="| . $cgi->url(-path_info=>1,-query=>1) . qq|">\n|;	# og:url
				$ogpmeta .= qq|<meta property="og:image" content="$imageurlforogp">\n|;		# og:image

				if( $setdat{'oglocale'} ne '' )   { $ogpmeta .= q|<meta property="og:locale" content="| . &fcts::forsafety($setdat{'oglocale'}) . qq|">\n|; }		# og:locale
				if( $setdat{'ogsitename'} ne '' ) { $ogpmeta .= q|<meta property="og:site_name" content="| . &fcts::forsafety($setdat{'ogsitename'}) . qq|">\n|; }	# og:site_name

				if( $setdat{'twittercard'} == 1 ) { $ogpmeta .= q|<meta name="twitter:card" content="summary_large_image">| . "\n"; }	# twitter:card
				else { $ogpmeta .= q|<meta name="twitter:card" content="summary">| . "\n"; }

				if( $setdat{'twittersite'} ne '' )    { $ogpmeta .= q|<meta name="twitter:site" content="| . &fcts::forsafety($setdat{'twittersite'}) . qq|">\n|; }			# twitter:site
				if( $setdat{'twittercreator'} ne '' ) { $ogpmeta .= q|<meta name="twitter:creator" content="| . &fcts::forsafety($setdat{'twittercreator'}) . qq|">\n|; }	# twitter:creator
			}

			# 生成物がなければ
			if( $ogpmeta eq '' ) { $ogpmeta = '<!-- OGP出力機能はOFFです。 -->'; }

		}
		else {
			$ogpmeta = '<!-- 表示できる投稿がない状況では、OGPは出力されません。 -->';
		}

		# 生成物を出力
		$cvskin =~ s/\[\[OGP\]\]/$ogpmeta/g;
	}

	# その他 細々した挿入機能群
	$cvskin =~ s/\[\[RANDOM:([0-9]{1,10})\]\]/&fcts::getrandnum($1,1)/eg;	# 指定範囲(10桁まで)でランダムな正の整数を得る

	# ----------------------------------
	# 別スキン適用時の自動調整処理
	if( $cp{'skindir'} ne '' ) {
		# プレビューの場合
		my $addfolder = &fcts::forsafety($cp{'skindir'});

		# ?記号で始まるリンクに、skinパラメータを付加する
		$cvskin =~ s/<a(.+?)href="\?(.*?)"(.*?)>/<a$1href="?skin=$addfolder&amp;$2"$3>/g;

		# もしskinパラメータが二重に存在したら1つに戻す
		$cvskin =~ s/skin=$addfolder&amp;skin=$addfolder/skin=$addfolder/g;

		# フォームにskinパラメータを付加する (※恒常付加パラメータは、postフォームなら維持できるが、getフォームだと失われるのでそれを防ぐため)
		$cvskin =~ s|</form>|<input type="hidden" name="skin" value="$addfolder"></form>|g;

		# 相対パスで指定されているCSSファイルの位置を自動調整
		if( $addfolder !~ m/\/$/ ) { $addfolder .= '/'; }
		$cvskin =~ s/<link(.+?)href="([^:]+?)"(.*?)>/<link$1href="$addfolder$2"$3>/g;		# href属性値にコロン記号が含まれる場合は調整しない。
	}
	elsif( $setdat{'skindirectory'} ne '' ) {
		# 簡易本番適用の場合
		my $addfolder = &fcts::forsafety($setdat{'skindirectory'});

		# 相対パスで指定されているCSSファイルの位置を自動調整
		if( $addfolder !~ m/\/$/ ) { $addfolder .= '/'; }
		$cvskin =~ s/<link(.+?)href="([^:]+?)"(.*?)>/<link$1href="$addfolder$2"$3>/g;		# href属性値にコロン記号が含まれる場合は調整しない。
	}

	# --------------------------
	# 投稿を挿入するため、カバースキンを前後に2分割（※仕様：投稿は1回しか挿入できない）※ここに到達するまでにすべての置き換えを済ませておく。
	my $coverfirst;  # COVER前半
	my $coversecond; # COVER後半
	if( $cvskin =~ /^([\W\w]*)\[\[TEGALOG:?\d*\]\]([\w\W]*)$/ ) {
		$coverfirst = $1;
		$coversecond = $2;
	}
	else {
		# カバースキンを分割できなかった場合
		&errormsg('外側スキンにキーワード [[TEGALOG]] が含まれていないため、ページを生成できません。正しいスキンが指定されているかどうかを確認して下さい。','<a href="?mode=admin">管理画面へ移動する</a>');
	}
	$coversecond = $coversecond . &cepb(($coverfirst,$coversecond));

	# 表示するデータが1件もなかったら（※cliphtmls配列には投稿データしか入っていないことが前提）
	if( $#cliphtmls < 0 ) {
		if( $cp{'postid'} > 0 ) {
			# システムメッセージ(Default:指定された番号の投稿は存在しません。まだ作成されていないか、または削除されました。)を出力
			push( @cliphtmls, '<div class="nodata nopost">' . $setdat{'msgnopost'} . '</div>' );
		}
		else {
			if( $#xmldata >= 0 ) {
				# 元データ自体は1件以上あるなら
				my $reconst = '';
				if( $cp{'hasgtag'} ne '' || $cp{'datelim'} ne '' ) {
					# ハッシュタグ限定・日付限定なら再構築リンクを出す。
					$reconst = '<p class="recountlink Login-Required"><small>［ <a href="' . &makeQueryString('mode=admin','work=recount') . '">再カウントしてキャッシュを更新</a> ］</small></p>';
				}
				# システムメッセージ(Default:表示できる投稿が1件も見つかりませんでした。)を出力
				push( @cliphtmls, '<div class="nodata nolist">' . $setdat{'msgnolist'} . '</div>' . $reconst );
			}
			else {
				# 元データが0件の場合、システムメッセージ(Default:まだ1件も投稿されていません。)を出力
				push( @cliphtmls, '<div class="nodata zeropost">' . $setdat{'msgnodata'} . '</div>' );
				if(!( -f $bmsdata )) {
					# データファイルがそもそも存在しなかった場合は (※ここは、たぶん実行されないハズ。ファイルの存在は事前にチェックされるので。)
					push( @cliphtmls, '<p class="nodata nofile">※データファイルが見つかりませんでした。データファイルがアップロードされているか、ファイル名が正しく設定されているかを確認して下さい。</p>' );
				}
			}
		}
	}

	# --------------
	# HTTPヘッダ出力
	# --------------
	if( $coverfirst =~ /^<\?xml/ ) {
		# スキンの先頭が「<?xml」で始まっていれば、XML用のヘッダを出力
		print $cgi->header( -type => "application/xml" , -charset => $charcode );
	}
	else {
		# それ以外ならHTML用のヘッダを出力
		print $cgi->header( -type => "text/html" , -charset => $charcode );
	}

	# 中身の表示
	print $coverfirst;
	print @cliphtmls;
	print $coversecond;
}

# -----------------------------------------------
# 指定年月から指定月ほど移動するページのURLを得る	引数1：年、引数2：月、引数3：移動月数
# -----------------------------------------------	返値：ページのURL
sub getOneMonthPageUrl
{
	my $year  = shift @_ || &errormsg('No Year on getOneMonthPageUrl');
	my $month = shift @_ || &errormsg('No Month on getOneMonthPageUrl');
	my $move  = shift @_ || 0;

	# 移動月数を反映
	if( $move + 0 ) {
		($year, $month) = &fcts::getnMonthLater($year,$month,$move);
		$month = &fcts::addzero($month);
	}

	# パラメータ付きURLを生成して返す
	return &makeQueryString("date=$year/$month");
}

# ------------------------------	※カレンダーのキャッシュがあるかどうかを調べて、あればそれを表示して終わる ……と思ったが、キャッシュしなくても充分速いので毎回生成する。
# 指定年月の箱形カレンダーを得る	引数1：年、引数2：月、引数3：移動月数
# ------------------------------	返値：カレンダー表示HTML
sub getCalendarBox
{
	my $year  = shift @_ || &errormsg('No Year on getCalendarBox');
	my $month = shift @_ || &errormsg('No Month on getCalendarBox');
	my $move  = shift @_ || 0;

	# 移動月数を反映
	if( $move + 0 ) {
		($year, $month) = &fcts::getnMonthLater($year,$month,$move);
		$month = &fcts::addzero($month);
	}

	# 当該月の中で、日データの存在を得る
	my @days = &existdaycounter($year,$month);

	# 日付リンク用配列の作成
	my @daylinks = ();
	for( my $i=1 ; $i<=31 ; $i++ ) {
		# 31日分ループ (31日より短い月でも不都合はないので31回回す)
		if( defined($days[$i]) ) {
			# 定義されていればフラグが立っていると解釈
			my $daynum = &fcts::addzero($i);	# 日を2桁にする
			# リンク用文字列を作る
			$daylinks[$i] = qq|?date=$year/$month/$daynum|;
		}
		else {
			$daylinks[$i] = '';
		}
	}

	# 曜日行を表示する設定なら、曜日配列も用意する
	my $weekrow = '';
	if( $setdat{'caladdweekrow'} == 1 ) {
		$weekrow .= '<' . &fcts::forsafety($setdat{'calsun'}) . '>';
		$weekrow .= '<' . &fcts::forsafety($setdat{'calmon'}) . '>';
		$weekrow .= '<' . &fcts::forsafety($setdat{'caltue'}) . '>';
		$weekrow .= '<' . &fcts::forsafety($setdat{'calwed'}) . '>';
		$weekrow .= '<' . &fcts::forsafety($setdat{'calthu'}) . '>';
		$weekrow .= '<' . &fcts::forsafety($setdat{'calfri'}) . '>';
		$weekrow .= '<' . &fcts::forsafety($setdat{'calsat'}) . '>';
	}

	# カレンダーを生成してHTMLを返す ※第3引数はリンク用配列へのリファレンス、第4引数は曜日群変数(曜日を表示しない場合は空)、第5引数はなし。
	return &fcts::makecalendarbox($year,$month,\@daylinks,$weekrow);
}

# ----------------------------
# 指定番号の投稿を挿入する準備	引数：Post ID、返値：当該PostIDの本文文字列(またはエラー文字列)
# ----------------------------	※開発メモ：関数expandDataBySkinと重複する処理が結構ある点をもうちょっと何とかできると望ましいのだが。
sub insertOnePost
{
	my $tid = shift @_ || 0;
	my $ret = '指定番号の投稿はありません。';

	if( $tid > 0 ) {
		my ($date,$user,$comment,$cats) = &getOnePost( $tid );
		if( length($comment) > 0 ) {
			# 本文が得られたら処理
			$comment = &fcts::forsafety($comment);	# まず安全化してから

			# 改行を再現
			if( $setdat{'allowlinebreak'} == 1 ) {
				$comment =~ s|&lt;br /&gt;|<br />|g;	# 改行を改行として表示
			}
			else {
				$comment =~ s|&lt;br /&gt;||g;			# 改行は削除
			}

			# 文字実体参照・数値文字参照のためにアンパサンドのエスケープを解除
			$comment =~ s|&amp;|&|g;

			# コメントに含まれる指定番号(投稿No)へのリンク処理（本文は安全化されているので文字実体参照を使って探す）※安全のため最長10桁まで。
			if( $setdat{'postidlinkize'} == 1 ) {
				# 絶対URLで出力する場合はフルパスを加えておく
				my $base = '';
				if( $setdat{'outputlinkfullpath'} == 1 ) { $base = $cgifullurl; }
				# リンク処理（一時適用中のスキンを維持しない場合は、クエリ文字列からスキン指定だけを除外して使う）
				$comment =~ s|\[&gt;([0-9]{1,10})\]|'<a href="' . $base . &cutSkinFromQueryIfOrder( &makeQueryString("postid=" . int($1)) ) . '" class="postidlink">' . $1 . '</a>'|eg;
				$comment =~ s|\[&gt;([0-9]{1,10}):(.+?)\]|'<a href="' . $base . &cutSkinFromQueryIfOrder( &makeQueryString("postid=" . int($1)) ) . '" class="postidlink">' . $2 . '</a>'|eg;
				# 「>>123」の記法も有効な場合
				if( $setdat{'postidlinkgtgt'} == 1 ) {
					# 既存のリンクラベルを再度(重複)リンク化しないように「&gt;&gt;」の直前に「">」が来ない場合に限ってリンクする。
					$comment =~ s|(?<!">)&gt;&gt;([0-9]{1,10})|'<a href="' . $base . &cutSkinFromQueryIfOrder( &makeQueryString("postid=" . int($1)) ) . '" class="postidlink">&gt;&gt;' . $1 . '</a>'|eg;
				}
			}

			# コメントに含まれるハッシュタグ関連処理
			if( $setdat{'hashtaglinkize'} == 1 ) {
				# リンク化する設定の場合のみ実行
				$comment = &extracthashtagsandlink( $comment );		# ここでの $comment は既に安全化されている点に注意
			}

			# コメントに含まれる内部画像の展開指示を解釈してHTML化する
			if( $setdat{'imageshowallow'} != 0 ) {
				$comment =~ s|\[PICT:(?:([^\[\]]+?):)?([-_.!~*\'()a-zA-Z0-9;\/?:@&=+\$,%#]+)\]|&showinsideimage($2,$1)|eg;	# 画像を表示用に変換
			}

			# コメントに含まれるURLをリンク化する
			if( $setdat{'urlautolink'} != 0 ) {
				$comment = &linkize( $comment );
			}

			# コメントに含まれる装飾指示を解釈する (※角括弧をエスケープする処理が入るので、コマンド解釈処理の中ではこれを一番最後にする。)
			if( $setdat{'allowdecorate'} != 0 ) {
				$comment = &comdecorate( $comment );
			}

			# 空白の連続を再現 (リンクを展開した後に処理しないと、URLの後に続く文字実体参照の空白をURLの末尾に加えてしまうので注意)
			if( $setdat{'keepserialspaces'} == 1 ) {
				$comment =~ s/   |\t/&nbsp; &nbsp;/g;	# 3つの連続する半角空白文字または1つのタブ記号は、文字実体参照→半角空白文字→文字実体参照の3文字に置き換える
				$comment =~ s/  /&nbsp; /g;				# 2つの連続する半角空白文字は、1つの文字実体参照と1つの半角空白文字に置き換える
			}

			# 最後に、てがろぐ記法をエスケープする (この関数の戻り先では、まだてがろぐ記法の解釈処理が続くため)
			$comment = &tegalogsystemsafety( $comment );

			$ret = $comment;
		}
	}

# &fcts::DEBUGOUT("---insertOnePost\n" . $ret);
	return $ret;
}

# ------------------------------
# ユーザ識別画像の表示HTMLを生成	引数1：アイコンURL、引数2：ユーザID
# ------------------------------
sub outputUserIcon
{
	my $imgsource = &fcts::forsafety( shift @_ );
	my $userid = &fcts::forsafety( shift @_ );

	# アイコンサイズ (※カスタマイズされる方へ：従来ここに書いていた width="32" height="32" のアイコンサイズは、管理画面の「設定」から設定できるようになりました。)
	my $iconsize = '';

	if( $setdat{'usericonsize'} != 0 ) {
		# アイコンサイズを出力するよう設定されている場合
		my $iconw = &fcts::forsafety($setdat{'usericonsizew'});
		my $iconh = &fcts::forsafety($setdat{'usericonsizeh'});
		if( $setdat{'usericonsource'} == 0 ) {
			# HTMLで出力する設定の場合
			$iconsize = qq|width="$iconw" height="$iconh"|;
		}
		else {
			# CSSで出力する設定の場合
			$iconsize = qq|style="width:| . $iconw . q|px; height:| . $iconh . q|px;"|;
		}
	}

	if( $imgsource eq '' ) {
		# アイコンが未指定なら、NO IMAGEアイコンを返す
		my $iconurl = NOIMAGEDEFAULTICON;
		if(( $setdat{'unknownusericon' } == 1 ) && ( $setdat{'unknownusericonurl'} ne '' )) {
			# NO IMAGE用の画像URLが指定されていれば（内蔵アイコンの代わりに）それを使う
			$iconurl = &fcts::forsafety($setdat{'unknownusericonurl'});
		}
		return '<img src="' . $iconurl . qq|" $iconsize class="usericon noimage" alt="NO IMAGE" />|;
	}
	else {
		# 指定の画像を表示
		return qq|<img src="$imgsource" $iconsize class="usericon freeimage" alt="Icon of $userid" />|;
	}
}

# ------------------------------------------
# 表示条件が限定されているかどうかのチェック	引数:なし
# ------------------------------------------	返値:0=何も限定されていない／1=限定されている
sub islimited
{
	if($cp{'postid'} > 0)		{ return 1; }
	if($cp{'datelim'} ne '')	{ return 1; }
	if($cp{'search'} ne '')		{ return 1; }
	if($cp{'hasgtag'} ne '')	{ return 1; }
	if($cp{'cat'} ne '')		{ return 1; }
	if($cp{'userid'} ne '')		{ return 1; }
	return 0;
}

# --------------------------------
# 限定条件の該当投稿を抜き出す
# --------------------------------
sub extractApplyData
{
	# 正順か逆順か
	if( $cp{'order'} eq 'reverse' ) {
		# 逆順ならデータの配列を逆転
		@xmldata = reverse(@xmldata);
	}

	# 特殊モード用の前処理
	my $orgSearch = $cp{'search'};	# 検索語があるかどうかの判定のために、特殊モード用の検索語を含めないオリジナル文字列を保存しておく。
	my $nowlimited = &islimited();	# 表示条件が限定されているかどうかのチェックを先に済ませておく。
	if( $cp{'mode'} eq 'gallery' ) {
		$cp{'search'} = GALLERYSEARCH . $cp{'search'};		# ギャラリーモードなら文字列「 [PICT: 」を探す（ただし角括弧がエスケープされている場合は除外する）
	}

	# 何も限定されていなければ
	if( &islimited == 0 ) {
		# 指定投稿の先頭固定が指定されていれば、移動させておく（※モードがVIEWかSITEMAPの場合のみ／RSS等では無視する）
		if(( $setdat{'fixedpostids'} ne '' ) && ( ($cp{'mode'} eq 'view') || ($cp{'mode'} eq 'sitemap') )) {
			&putpoststohead( $setdat{'fixedpostids'} );
		}
	}

	# (将来ToDo) 何も限定されておらず、下書き状態の投稿もない場合は、抜き出す処理が不要なので、ここで「return @xmldata;」することで高速に返すようにしたい。

	# 抜き出す必要がある場合はループ
	my @retdata;
	foreach my $oneclip (@xmldata) {

		# 分解
		my $id		= &fcts::forsafety( &fcts::getcontent($oneclip,'id') );
		my $date	= &fcts::forsafety( &fcts::getcontent($oneclip,'date') );
		my $user	= &fcts::forsafety( &fcts::getcontent($oneclip,'user') );
		my $cats	= &fcts::forsafety( &fcts::getcontent($oneclip,'cat') );		# カテゴリCSV
		my $flags	= &fcts::forsafety( &fcts::getcontent($oneclip,'flag') );		# フラグ群CSV
		my $comment	= &fcts::forsafety( &fcts::getcontent($oneclip,'comment') );	# 中身が既に安全化されていることに注意！（検索する際にそれを考慮する必要がある）

		# 表示対象の判定(各種フラグ)
		if( $flags =~ m/draft/ ) {
			# 下書きだったら
			if( $cp{'postid'} > 0 ) {
				# 個別表示の場合ならログイン状態を確認する
				my $permittedid = &fcts::checkpermission(1);	# 読み取り専用モードで認証を確認 (※ログインされていればユーザIDが得られる)
				if( !$permittedid || ( $permittedid ne $user ) ) {
					# ログインされていないか、もしくはユーザIDが投稿者のIDと不一致なら、表示対象にせず次を探す
					next;
				}
			}
			else {
				# 個別表示の場合でなければ、表示対象にせず次を探す
				next;
			}
		}
		if( $flags =~ m/rear/ ) {
			# 下げるだったら
			if( $cp{'postid'} > 0 ) {
				# 個別表示なら表示する(ので、ここでは何もせず処理を先へ通す)
			}
			if(
				( $nowlimited == 0 ) ||	# 何も表示条件が限定されていない場合は表示しない
				(( $setdat{'rearappearcat'} == 0 ) && ( $cp{'cat'} ne '' )) ||		# カテゴリ限定表示時に表示しない設定で、今がカテゴリ限定表示時なら、表示しない
				(( $setdat{'rearappeartag'} == 0 ) && ( $cp{'hasgtag'} ne '' )) ||	# ハッシュタグ限定表示時に表示しない設定で、今がハッシュタグ限定表示時なら、表示しない
				(( $setdat{'rearappeardate'} == 0 ) && ( $cp{'datelim'} ne '' )) ||	# 日付指定表示時に表示しない設定で、今が日付指定表示時なら、表示しない
				(( $setdat{'rearappearsearch'} == 0 ) && ( $orgSearch ne '' ))		# 全文検索時に表示しない設定で、今が全文検索時なら、表示しない
			) {
				# 表示しない条件に該当していたら、表示対象にせずに次を探す
				next;
			}
		}

		# 表示対象の判定
		if( $cp{'postid'} > 0 && $id != $cp{'postid'} ) {
			# 個別表示の場合でIDが違うなら次を探す
			next;
		}
		if( $cp{'userid'} ne '' && $user ne $cp{'userid'} ) {
			# ユーザ名指定の場合でユーザ名が違うなら次を探す
			next;
		}
		if( $cp{'hasgtag'} ne '' ) {
			# タグの場合
			my $temphs = $comment;
			$temphs =~ s/#\[+/#[/g;	# 角括弧が連続していると(たぶん正規表現が)エラーになる現象を回避するため連続する角括弧を1つにまとめておく。
			# タグが含まれているかどうかを確認（処理内容の見やすさのために冗長に記述してある）	# ★ハッシュタグ判定
			my $quoted_hashtag = &fcts::forsafety( quotemeta($cp{'hasgtag'}) );
			if(     $temphs =~ m/#\[$quoted_hashtag\]/i ) {	}		# (Through)見つかったら表示：角括弧に囲まれたハッシュタグ
			elsif ( ($quoted_hashtag =~ m/[^_a-zA-Z\~\`\!\@\#\$\%\^\&\*\(\)\-\+\=\[\]\{\}\|\;\:\\'\"\,\.\<\>\/\?\/\d\s]+/ )	&& ($temphs =~ m/#$quoted_hashtag[_a-zA-Z\~\`\!\@\#\$\%\^\&\*\(\)\-\+\=\[\]\{\}\|\;\:\\'\"\,\.\<\>\/\?\/\d\s]/ )) {	}	# (Through)見つかったら表示：直後にASCII文字が存在する括弧なし非ASCIIハッシュタグ	※\p{ASCII}が使えない環境のために。
			elsif ( ($quoted_hashtag =~ m/\w+/ )		&& ($temphs =~ m/#$quoted_hashtag[\W]/i )) {	}		# (Through)見つかったら表示：直後に英数字以外の文字列が存在する括弧なしASCIIハッシュタグ
			elsif ( $temphs =~ m/#$quoted_hashtag$/i ) {	}		# (Through)見つかったら表示：文末に存在する括弧なしハッシュタグ
			else {
				# 見つからなかったら次を探す
				next;
			}
		}
		if( $cp{'cat'} ne '' ) {
			# カテゴリの場合
			my $foundcat = 0;
			if( $cats ne '' ) {
				# カテゴリがある場合は分解して一致を調べる
				my @cat = split(/,/,$cats);		# カテゴリ分解
				foreach my $oc ( @cat ) {
					# パラメータ側のカテゴリをカンマ区切りで分割
					my @pcats = split(/,/,$cp{'cat'});
					# 一致するか探す
					foreach my $pcat ( @pcats ) {
						if( $pcat eq $oc ) {
							# 一致したらフラグを立ててループを終わる
							$foundcat = 1;
							last;
						}
					}
					if( $foundcat == 1 ) { last; }	# 一致していたら外側のループも終わる
				}
			}
			else {
				# カテゴリがない場合
				if( $cp{'cat'} eq '-' ) {
					# 検索カテゴリIDに「-」が指定されていれば(カテゴリなしの一覧を出すため)、フラグを立てる
					$foundcat = 1;
				}
			}
			if( $foundcat == 0 ) {
				# 見つからなかったら次を探す
				next;
			}
		}
		if( $cp{'search'} ne '' ) {
			# 検索の場合（コメント本文が検索対象）
			my $searchstring = $comment;

			if( $setdat{'catidinsearch'} == 1 ) {
				# 検索対象にカテゴリIDも含む場合は追加する
				$searchstring .= $cats;
			}

			# 検索を実行
			if( &fcts::wordsearch($searchstring,$cp{'search'}) == 0 ) {
				# 非該当なら次を探す
				next;
			}
		}
		if( $cp{'datelim'} ne '' ) {
			# 日付指定の場合
			my $datestring = $cp{'datelim'};
			if( $datestring =~ m/\A(\d\d\/\d\d)\z/ ) {
				# MM/DD形式の場合
				$datestring = '/' . $1;
			}
			elsif( $datestring =~ m/\A(\d\d)\z/ ) {
				# DD形式の場合
				$datestring = $1 . ' ';
			}
			# 検索
			my $quoted_datelim = quotemeta($datestring);
			if( $date !~ m/$quoted_datelim/ ) {
				# 違っていれば次を探す
				next;
			}
		}

		# 該当したデータは配列に加える
		push(@retdata,$oneclip);
	}

	# 特殊モード用の後処理
	if( $cp{'mode'} eq 'gallery' ) {
		$cp{'search'} =~ s/\[PICT: -\\\[PICT: //;
	}

	return @retdata;
}

# ------------------------------------------
# 該当投稿にスキンを適用して表示用HTMLにする	引数1：OGP用の情報抽出が必要かどうか(1:必要/0:不要), 引数2：Built-inスキンを使う場合の名称, 引数3：表示する投稿データ
# ------------------------------------------
sub expandDataBySkin
{
	my $needogp = shift @_ || 0;
	my $builtinskin = shift @_ || '';
	my @rethtml;

	# スキンの読み込み
	my $inskin = '';
	if( $builtinskin eq '' ) {
		# 内側SKINファイルの読み込み
		open(MSKIN, $skinfileinside);	# ロック不要＆所在確認済み
		$inskin = join("",<MSKIN>);
		close MSKIN;
	}
	else {
		# Built-inスキンの読み込み
		$inskin = join("", &loadbuiltin($builtinskin . ":inner") );
	}

	# 日付境界バーの挿入判定用
	my $pastdate = '';		# 前の日付保持用
	my $alreadytopfix = 0;	# 先頭固定回数保持用
	my $sepinsflag = 1;		# 境界挿入有無のチェック
	my $separatepoint = $setdat{'separatepoint'};	# 境界挿入設定を得る
	if( $separatepoint == 0 ) { $sepinsflag--; }	# 非挿入設定
	if( $cp{'postid'} > 0 )	{ $sepinsflag--; }		# ポストID指定なら挿入しない
# 	if( $cp{'userid'} ne '')	{ $sepinsflag--; }	# ユーザID指定なら挿入しない
	if( $cp{'hasgtag'} ne '')	{ $sepinsflag--; }	# ハッシュタグ指定なら挿入しない
	if( $cp{'cat'} ne '')		{ $sepinsflag--; }	# カテゴリ指定なら挿入しない
	if( $cp{'search'} ne '' )	{ $sepinsflag--; }	# 検索指定なら挿入しない

	# 日付指定表示時のログ境界挿入判定上書き（上書きするよう設定されている場合のみ）
	if(( $setdat{'separateoption'} == 1 ) && ( $separatepoint != 0 ) && ( $cp{'datelim'} ne '' )) {
		if(		$cp{'datelim'} =~ m|^\d\d\d\d$|			) { $separatepoint = 2; }	# 年別表示ならセパレータは月別
		elsif(	$cp{'datelim'} =~ m|^\d\d\d\d/\d\d$|	) { $separatepoint = 3; }	# 月別表示ならセパレータは日別
		elsif(	$cp{'datelim'} =~ m|^\d\d$|				) { $separatepoint = 2; }	# 長月表示(n年m月日記)ならセパレータは月別
		elsif(	$cp{'datelim'} =~ m|^\d\d/\d\d$|		) { $separatepoint = 1; }	# 長年表示(n年日記)ならセパレータは年別
		else { $sepinsflag--; }	# 日別表示ならセパレータはなし
	}

	# PostID指定(で表示が1件だけのとき)はユーティリティリンク追加フラグを立てる（※ただし、ユーティリティリンク枠を表示する設定の場合のみ）
	my $flagUtil = 0;
	if(( $cp{'postid'} > 0 ) && ( $#_ == 0 ) && ( $setdat{'onepostpageutilitybox'} == 1 )) {
		$flagUtil = 1;
	}

	# 続きを読む機能の使用判定
	my $isUseReadmoreFunc = 0;
	if( $setdat{'readmorebtnuse'} == 1 ) {
		# 条件1:「続きを読む」を使う設定になっている
		if(( $cp{'search'} eq '' ) || ( $setdat{'readmoreonsearch'} == 1 )) {
			# 条件2:検索状況ではない または 検索時でも有効に設定されている
			# なら、機能を使う
			$isUseReadmoreFunc = 1;
		}
	}

	my $loopcount = 0;
	foreach my $oneclip (@_) {
		my $mtemplate = $inskin;	# 内側スキンをコピー
		$loopcount++;

		# 分解
		my $id		= &fcts::forsafety( &fcts::getcontent($oneclip,'id') );
		my $date	= &fcts::forsafety( &fcts::getcontent($oneclip,'date') );
		my $user	= &fcts::forsafety( &fcts::getcontent($oneclip,'user') );
		my $cats	= &fcts::forsafety( &fcts::getcontent($oneclip,'cat') );		# カテゴリ(配列ではなくCSV)
		my $comment	= &fcts::forsafety( &fcts::getcontent($oneclip,'comment') );
		my $uname   = &fcts::forsafety( &fcts::getUserDetail($user,2) ) || &fcts::forsafety($setdat{'unknownusername'});

		my $flagtf	= &fcts::getcontent($oneclip,'topfixed');	# 先頭固定の場合だけに付加されるフラグ(＝ 1 or 空文字列 )

		# 時刻をずらす設定ならずらす
		if( $setdat{'shiftservtime'} != 0 ) {
			$date = &fcts::shifttime( $date, $setdat{'shiftservtime'} );
		}

		# 文字数をカウント(加工前の文字列を元にカウントする必要があるのでここで実行する)
		$mtemplate =~ s/\[\[LENGTH\]\]/&fcts::mbLength( &fcts::adjustForCharCount($comment) )/eg;

		# 改行を再現
		if( $setdat{'allowlinebreak'} == 1 ) {
			$comment =~ s|&lt;br /&gt;|<br />|g;	# 改行を改行として表示
		}
		else {
			$comment =~ s|&lt;br /&gt;||g;			# 改行は削除
		}

		# 文字実体参照・数値文字参照のためにアンパサンドのエスケープを解除する (※仕様変更v2.4.7:設定の余地を排して強制適用)
		$comment =~ s|&amp;|&|g;

		# 日付境界の判定（日付境界バー挿入フラグが立っている場合のみ）
		if( $sepinsflag == 1 ) {
			my $nowcheckdate = '';	# クエリ用日付
			my $datestrforbar = '';	# バー表示用日付
			if( $date =~ m|(\d\d\d\d)/(\d\d)/(\d\d)(.*)| ) {
				if( $separatepoint == 1 ) {
					# 年別
					$nowcheckdate = $1;
					$datestrforbar = &arrangeDateStr( $setdat{'separateyear'}, "$1/00/00 00:00:00" );
				}
				elsif( $separatepoint == 2 ) {
					# 月別
					$nowcheckdate = "$1/$2";
					$datestrforbar = &arrangeDateStr( $setdat{'separateyear'}, "$1/00/00 00:00:00" )
									.&arrangeDateStr( $setdat{'separatemonth'}, "$1/$2/00 00:00:00" );
				}
				elsif( $separatepoint == 3 ) {
					# 日別
					$nowcheckdate = "$1/$2/$3";
					$datestrforbar = &arrangeDateStr( $setdat{'separateyear'}, "$1/00/00 00:00:00" )
									.&arrangeDateStr( $setdat{'separatemonth'}, "$1/$2/00 00:00:00" )
									.&arrangeDateStr( $setdat{'separatedate'}, "$1/$2/$3 00:00:00" );
				}
			}
			if( $flagtf ne '' ) {
				# 先頭固定で
				if(( $setdat{'fixedseparatepoint'} == 1 ) && ( $alreadytopfix == 0 )) {
					# 先頭固定時に日付境界バーを挿入する設定の場合で、まだ1度も先頭固定用の境界バーを挿入していない場合は挿入
					push( @rethtml,'<p class="dateseparator fixedseparator">' . &fcts::forsafety($setdat{'fixedseparatelabel'}) . '</p>');
					$alreadytopfix++;
				}
			}
			elsif( $nowcheckdate ne $pastdate ) {
				# 前の日付と違っていれば日付境界バーを挿入
				push( @rethtml, &getDateSeparator($nowcheckdate, $datestrforbar) );
				$pastdate = $nowcheckdate;
			}
		}

		# 管理用リンクを作成
		my $parmalink	= &makeQueryString("postid=$id");				# 投稿IDのURL(恒常付加パラメータ付き)
		my $parmapure	= &cutSkinFromQuery($parmalink);			# 投稿IDのURLだけ
		my $editlink	= &makeQueryString('mode=edit',"postid=$id");	# 編集のURL(恒常付加パラメータ付き)
		my $deletelink	= &makeQueryString('mode=admin','work=trydels',"postid=$id");	# 削除のURL(恒常付加パラメータ付き)
		my $userlink	= &makeQueryString("userid=$user");				# 投稿者別のURL(恒常付加パラメータ付き)
		my $userpure	= &cutSkinFromQuery($userlink);					# 投稿者別のURLだけ

		# コメントに含まれる指定番号(投稿No)へのリンク処理（本文は安全化されているので文字実体参照を使って探す）※安全のため最長10桁まで。
		if( $setdat{'postidlinkize'} == 1 ) {
			# 絶対URLで出力する場合はフルパスを加えておく
			my $base = '';
			if( $setdat{'outputlinkfullpath'} == 1 ) { $base = $cgifullurl; }
			# リンク処理（一時適用中のスキンを維持しない場合は、クエリ文字列からスキン指定だけを除外して使う）
			$comment =~ s|\[&gt;([0-9]{1,10})\]|'<a href="' . $base . &cutSkinFromQueryIfOrder( &makeQueryString("postid=" . int($1)) ) . '" class="postidlink">' . $1 . '</a>'|eg;
			$comment =~ s|\[&gt;([0-9]{1,10}):(.+?)\]|'<a href="' . $base . &cutSkinFromQueryIfOrder( &makeQueryString("postid=" . int($1)) ) . '" class="postidlink">' . $2 . '</a>'|eg;
			# 「>>123」の記法も有効な場合
			if( $setdat{'postidlinkgtgt'} == 1 ) {
				# 既存のリンクラベルを再度(重複)リンク化しないように「&gt;&gt;」の直前に「">」が来ない場合に限ってリンクする。
				$comment =~ s|(?<!">)&gt;&gt;([0-9]{1,10})|'<a href="' . $base . &cutSkinFromQueryIfOrder( &makeQueryString("postid=" . int($1)) ) . '" class="postidlink">&gt;&gt;' . $1 . '</a>'|eg;
			}
		}

		# コメントに含まれるハッシュタグ関連処理
		if( $setdat{'hashtaglinkize'} == 1 ) {
			# リンク化する設定の場合のみ実行
			$comment = &extracthashtagsandlink( $comment );		# ここでの $comment は既に安全化されている点に注意
		}

		# コメントに含まれる内部画像の展開指示を解釈してHTML化する
		# ＋コメントに含まれる内部画像のURLだけを得る　＋個数もカウントする
		my @imageurls = ();		# ファイルパス保存用
		my @imagealts = ();		# 代替文字保存用
		my @imghtmls = ();		# 画像表示HTML保存用
		my $pictcount = 0;
		if( $setdat{'imageshowallow'} != 0 ) {
			$pictcount = (() = $comment =~ /\[PICT:([^\[\]]+?:)?[-_.!~*\'()a-zA-Z0-9;\/?:@&=+\$,%#]+\]/g);		# 画像挿入記法の出現個数を数える
			my $img = '';
			$comment =~ s|\[PICT:(?:([^\[\]]+?):)?([-_.!~*\'()a-zA-Z0-9;\/?:@&=+\$,%#]+)\]|&showinsideimage($2,$1) . &fcts::retempty(push( @imghtmls, &showinsideimage($2,$1) )) . &fcts::retempty(push(@imageurls,$2)) . &fcts::retempty(push(@imagealts,$1))|eg;	# 画像を表示用に変換すると同時に、生成HTMLソースを配列に入れ、ファイル名を配列に入れ、代替文字も配列に入れる。
		}
		# ▲上記正規表現のメモ [PICT:『α=角括弧以外の文字列が1文字以上あり半角コロン記号で終わっている部分』が0回または1回＋『β=URLに使える文字列が1文字以上』]
		# 　α部分は全体をキャプチャせず(?:～)、コロン以外の部分だけをキャプチャして、後方参照で利用している点に注意。
		# ※本当は正規表現の否定戻り読み記法を使って「ただしコロンの直前にhttps?が存在しない場合のみ」という条件を加えた \[PICT:(?:([^\[\]]+?(?<!https?)):)?([-_.!~*\'()a-zA-Z0-9;\/?:@&=+\$,%#]+)\] と書きたいのだが、Perl 5.30未満では Variable length lookbehind not implemented in regex エラーになるので断念。

		# 代替文字配列に「http(s)」が入っていたらURLに戻す （※製作メモ：この処理は、上記で正規表現の否定戻り読み記法が使えていれば不要なのだが。）
		my $countoa = 0;
		foreach my $oa ( @imagealts ) {
			if( $oa && ( $oa =~ m/^(https?)$/ )) {
				# alt属性値が存在していて、http(a)だけが入っていたら（※正規表現で抽出できなかった場合は中身が undefined になっているので、中身を確認しないままだと Use of uninitialized value $oa と言われる。）
				$imageurls[$countoa] = $1 . ':' . $imageurls[$countoa];		# 対応するURL文字列の頭にそれを加える
				$oa = '';	# 代替文字は消す
			}
			$countoa++;
		}

		# コメントに含まれるURLをリンク化する
		if( $setdat{'urlautolink'} != 0 ) {
			$comment = &linkize( $comment );
		}

		# コメントに含まれる装飾指示を解釈する (※角括弧をエスケープする処理が入るので、コマンド解釈処理の中ではこれを一番最後にする。)
		if( $setdat{'allowdecorate'} != 0 ) {
			$comment = &comdecorate( $comment );
		}

		# 空白の連続を再現  (リンクを展開した後に処理しないと、URLの後に続く文字実体参照の空白をURLの末尾に加えてしまうので注意)
		if( $setdat{'keepserialspaces'} == 1 ) {
			$comment =~ s/   |\t/&nbsp; &nbsp;/g;	# 3つの連続する半角空白文字または1つのタブ記号は、文字実体参照→半角空白文字→文字実体参照の3文字に置き換える
			$comment =~ s/  /&nbsp; /g;				# 2つの連続する半角空白文字は、1つの文字実体参照と1つの半角空白文字に置き換える
		}

		# 先頭固定表示のときの日時調整
		my $dsp = '';
		if(( $flagtf eq '1' ) && ( $setdat{'fixedpostdate'} != 1 )) {
			# 調整する場合(＝値が1以外のとき)のみ
			if( $setdat{'fixedpostdate'} == 2 ) {
				# 現在日時を使う
				$date = &fcts::getdatetimestring();
			}
			elsif( $setdat{'fixedpostdate'} == 3 ) {
				# 固定ラベルを使う
				$dsp = $setdat{'fixedpostsign'};
				$date = '';
				# 最初に見つかったDATE挿入1つだけを置換
				$mtemplate =~ s/\[\[DATE\]\]/$dsp$date/;
				$mtemplate =~ s/\[\[DATE:(.+?)\]\]/$dsp . &arrangeDateStr($1,$date)/e;
				# 以降は何も挿入しない
				$dsp = '';
			}
			elsif( $setdat{'fixedpostdate'} == 0 ) {
				# 何も出さない
				$date = '';
			}
			# 値が指定外だった場合は調整しない
		}


		$mtemplate =~ s/\[\[VOICEREADING\]\]/&outputSpeechScript( $id, $comment )/eg;	# 読み上げ機能

		# 内側スキンからHTMLを作成(1)
		$mtemplate =~ s/\[\[POSTID\]\]/$id/g;
		$mtemplate =~ s/\[\[PARMAURL\]\]/$parmalink/g;
		$mtemplate =~ s/\[\[PARMAURL:FULL\]\]/$cgifullurl$parmalink/g;
		$mtemplate =~ s/\[\[PARMAURL:PURE\]\]/$parmapure/g;
		$mtemplate =~ s/\[\[PARMAURL:PURE:FULL\]\]/$cgifullurl$parmapure/g;
		$mtemplate =~ s/\[\[EDITURL\]\]/$editlink/g;
		$mtemplate =~ s/\[\[DELETEURL\]\]/$deletelink/g;
		$mtemplate =~ s/\[\[USERURL\]\]/$userlink/g;
		$mtemplate =~ s/\[\[USERURL:FULL\]\]/$cgifullurl$userlink/g;
		$mtemplate =~ s/\[\[USERURL:PURE\]\]/$userpure/g;
		$mtemplate =~ s/\[\[USERURL:PURE:FULL\]\]/$cgifullurl$userpure/g;
		$mtemplate =~ s/\[\[DATE\]\]/$dsp$date/g;
		$mtemplate =~ s/\[\[DATE:(.+?)\]\]/$dsp . &arrangeDateStr($1,$date)/eg;
		$mtemplate =~ s/\[\[USERID\]\]/$user/g;
		$mtemplate =~ s/\[\[USERNAME\]\]/$uname/g;
		$mtemplate =~ s/\[\[USERICON\]\]/&outputUserIcon( &fcts::getUserDetail($user,4) , $user )/eg;
		$mtemplate =~ s|\[\[ONEPICT:([0-9]+)\]\]|&pinpointarray($1,'<span class="NoImageError">(対象画像がありません)</span>',@imghtmls)|eg;
		$mtemplate =~ s|\[\[GETALT:PICT:([0-9]+)\]\]|&fcts::forsafety( &pinpointarray($1,'',@imagealts) )|eg;
		$mtemplate =~ s|\[\[GETURL:PICT:([0-9]+)\]\]|&showinsideimageurl($1,$setdat{'imagefullpath'},@imageurls)|eg;
		$mtemplate =~ s/\[\[PICTCOUNT\]\]/$pictcount/g;
		$mtemplate =~ s/\[\[ATT:LIGHTBOX\]\]/$setdat{'imagelightboxatt'}/g;
		$mtemplate =~ s/\[\[RANDOM:([0-9]{1,10})\]\]/&fcts::getrandnum($1,1)/eg;	# 指定範囲(10桁まで)でランダムな正の整数を得る
		$mtemplate =~ s/\[\[LOOPCOUNT\]\]/$loopcount/g;								# ループカウンタ(1から順の整数)

		# 先頭固定表示かどうかによる分岐
		if( $flagtf eq '1' ) {
			# 先頭固定なら固定用に指定された文字列を(専用マークアップで)挿入
			my $fixsign = '<span class="fixed">' . $setdat{'fixedpostsign'} . '</span>';
			$mtemplate =~ s/\[\[NEW\]\]/$fixsign/g;
		}
		else {
			# そうでないならNEW判定結果を挿入
			$mtemplate =~ s/\[\[NEW\]\]/&addnewsign($date,$setdat{'newsignhours'});/eg;
		}

		$mtemplate =~ s/\[\[CATEGORYLINKS\]\]/&outputCategoryInfo( $cats, '<IT>' )/eg;
		$mtemplate =~ s/\[\[CATEGORYLINKS:(.+?)\]\]/&outputCategoryInfo( $cats, $1 )/eg;
		$mtemplate =~ s/\[\[CATEGORYNAMES\]\]/&outputCategoryInfo( $cats, 'IT' )/eg;
		$mtemplate =~ s/\[\[CATEGORYIDS\]\]/&outputCategoryIDs( $cats, ' ' , '' )/eg;					# 空白区切り
		$mtemplate =~ s/\[\[CATEGORYIDS:IFEMPTY:(.+?)\]\]/&outputCategoryIDs( $cats, ' ' , $1 )/eg;		# 空白区切り＋無指定時の代替文字列指定

		# コメントの内部に [[COMMENT～ の記述が存在する場合に、それを展開してしまわないようにする
		$comment =~ s/\[\[COMMENT/&#91;&#91;COMMENT/g;

		# ………………………………
		# ▼コメント本文の挿入処理：この処理は最後に。でないとコメント本文内に書かれたキーワードを解釈してしまう。
		# ………………………………
		# コメントの分解挿入がある場合(※ない場合には余計な分解処理を実行しないようにする)
		if( $mtemplate =~ m/\[\[COMMENT:/ ) {
			# 分解の必要があれば分解
			my @eachlines = split(/<br \/>/,$comment);

			# 指定行の内容だけを挿入する
			$mtemplate =~ s/\[\[COMMENT:LINE:(\d+)\]\]/&getLatterLines($1,1,@eachlines)/eg;

			# 指定行以下のすべてを挿入する
			$mtemplate =~ s/\[\[COMMENT:LINE:(\d+)\*\]\]/&getLatterLines($1,0,@eachlines)/eg;

			# 指定キーワードに合致する内容を挿入する
			$mtemplate =~ s/\[\[COMMENT:([A-Z]+):(\d+)\]\]/&getPartOfLines($1,$2,0,"No.$id",@eachlines)/eg;
			$mtemplate =~ s/\[\[COMMENT:([A-Z]+)\]\]/&getPartOfLines($1,0,0,"No.$id",@eachlines)/eg;
			$mtemplate =~ s/\[\[COMMENT:(TAGS):GALLERY\]\]/&rewriteHrefToGallery( &getPartOfLines($1,0,0,'',@eachlines) )/eg;
			$mtemplate =~ s/\[\[COMMENT:(TAGS):SITEMAP\]\]/&rewriteHrefToSitemappage( &getPartOfLines($1,0,0,'',@eachlines) )/eg;
		}

		# ………………………
		# ▼OGP出力準備処理:
		# ………………………
		if( $needogp > 0 ) {
			# OGP用の情報が必要な状況なら抽出する
			my $ogpdata = '<!-- OGPmetadata: ';

			# 本文を分解
			my @eachlines = split(/<br \/>/,$comment);

			# 前処理
			foreach my $one (@eachlines) {
				$one =~ s/<script.+?<\/script>//g;		# HTMLのscript要素を除外する(※システム側の処理によって改行が入ることがある)
				$one =~ s/\n//g;						# 改行コードを除外する(※コメント本文に改行コードは含まれないハズだが、システム側の処理によって改行が入ることがある)
			}

			# 抽出
			my $ogtitle = &tegalogsystemsafety( &getPartOfLines('TITLE',30,0,"No.$id",@eachlines) );
			my $ogdescription = &tegalogsystemsafety( &getPartOfLines('TEXT',180,0,"No.$id",@eachlines) );
			if( $setdat{'ogdescription'} == 1 ) { $ogdescription = $ogtitle; }	# og:descriptionの内容をog:titleと同じにする設定の場合

			# 抽出して整形
			$ogpdata .= 'Ot: ' . $ogtitle . ' :tO';
			$ogpdata .= 'Od: ' . $ogdescription . ' :dO';
			$ogpdata .= 'Oi: ' . &showinsideimageurl(1,1,@imageurls) . ' :iO';
			$ogpdata .= ' :mO -->';

			# できあがった文字列を出力配列の先頭に差し込む
			unshift(@rethtml,$ogpdata);
		}

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
		# 続きを読む処理 (※コメントを分解挿入する場合には実施しないので、この位置で実行する)
		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
		if( $isUseReadmoreFunc == 1 ) {

			# コメントに区切り文字が1個以上含まれる場合 (※必ず文字実体参照で記録されている)
			if( $comment =~ m/&lt;&gt;/ ) {

				# 要素名（将来的に選択可能にする？）
				my $readmorebuttontag = 'a';	# 続きを読むボタンを作る要素名
				my $readmorehidetag = 'span';	# 続きを読む範囲を隠すための要素名

				# 続きを読むリンクを加える処理
				my @separatedcomments = split(/&lt;&gt;/,$comment);
				$comment = '';
				my $spcomcount = 0;
				foreach my $sepcomment (@separatedcomments) {
					if( $comment eq '' ) {
						# 最初は無条件表示
						$comment = $sepcomment;
					}
					elsif( $sepcomment eq '' ) {
						# 中身がなければ無視
						next;
					}
					else {
						# 2番目以降は「続きを読む」仕様を加える（中身があれば）
						my $moreid = 'post' . $id . 'more' . $spcomcount;						# 続きを読む領域1つ1つに割り当てるユニークID
						my $morenum = ''; if( $spcomcount >= 2 ) { $morenum = $spcomcount; }	# 続きを読むが2個以上ある場合に限って番号を付加するため

						$comment .= &outputHiddenArea(
							'続きを読む' ,						# 引数1：種別名
							$moreid ,							# 引数2：隠す領域1つ1つに割り当てるユニークID
							$morenum ,							# 引数3：隠す番号
							$readmorebuttontag ,				# 引数4：隠すボタンを作る要素名
							$readmorehidetag ,					# 引数5：隠す範囲を出力する要素名
							$setdat{'readmorestyle'} ,			# 引数6：展開する範囲の表示方法(0:inline/1:inline-block/2:block)
							$setdat{'readmorebtnlabel'} ,		# 引数7：展開ボタンのラベル
							$setdat{'readmorecloselabel'} ,		# 引数8：畳むボタンのラベル
							$setdat{'readmorecloseuse'} ,		# 引数9：畳むボタンの出力が(1:必要/0:不要)
							$sepcomment							# 引数10:隠される本文(Separated Comment)
						);
					}
					$spcomcount++;
				}
			}
		}
		elsif( $setdat{'readmorebtnuse'} == 1 ) {
			# 続きを読む機能が有効だけども、処理対象外な場合は区切り文字を削除
			$comment =~ s/&lt;&gt;//g;
		}

		# コメント全文を挿入
		$mtemplate =~ s/\[\[COMMENT\]\]/$comment/g;

		# スキンを含めて生成を完了したHTMLに対して処理
		if( $flagDemo{'AddRelNofollow'} == 1 ) {
			# 外部リンク(httpから書かれたリンク)のみに属性値「rel="nofollow"」を加える
			$mtemplate =~ s/<([aA]\s.*)([hH][rR][eE][fF]=.*http.*)>/<$1rel="nofollow" $2>/g;
		}

		push( @rethtml, $mtemplate );

		# ユーティリティリンクを追加
		if( $flagUtil == 1) {
			push( @rethtml, &utilitylinksforonepost($id,$user,$uname,$cats,$date) );
		}

	}

	return @rethtml;
}

# --------------------------
# 所属カテゴリ情報を挿入する	引数1：所属カテゴリCSVデータ、引数2：コロン記号で分離されたフラグやオプション群
# --------------------------	返値：カテゴリ情報として出力するHTMLソース
sub outputCategoryInfo
{
	my $catcsv	= shift @_ || '';	# 所属カテゴリCSVデータ (カテゴリIDだけがカンマ区切りで並ぶ形式)
	my $options	= shift @_ || '';	# コロン記号で分離されたフラグやオプション群

	# ----------------
	# オプションを分離
	# ----------------
	my $optFull = 0;
	my $optPure = 0;
	my $optGallery = 0;
	my $optSitemap = 0;
	my $flags = '';

	my @opts = split(/:/,uc($options));		# オプションは全部大文字に変換して解釈する

	my $flagc = 0;
	foreach my $oneopt ( @opts ) {
		if( $oneopt eq 'FULL' ) { $optFull = 1; }							# フルパス
		elsif( $oneopt eq 'PURE' ) { $optPure = 1; }						# 適用スキン無効化
		elsif( $oneopt eq 'GALLERY' ) { $optGallery = 1; $optPure = 1; }	# ギャラリーモード適用（＋適用スキン無効化）
		elsif( $oneopt eq 'SITEMAP' ) { $optSitemap = 1; $optPure = 1; }	# サイトマップモード適用（＋適用スキン無効化）
		else { $flags = $oneopt; $flagc++; }
	}

	# フラグと解釈される文字列(＝フラグまたは想定外文字列)が2回以上出てきたらエラーメッセージを返す
	if( $flagc >= 2 ) {
		return '[[CATEGORYLINKSの記述に誤りがあります]]';
	}

	# フラグの指定がなかった場合→デフォルト指定
	if( $flags eq '' ) {
		$flags = '<IT>';	# アイコン＋テキスト
	}

	# -----------------------
	# カテゴリが1つもない場合
	# -----------------------
	if( $catcsv eq '' ) {
		# 指定の文字列を出力する設定の場合は出力する
		my $nocatlinka1 = '';	# リンク用マークアップ(前)
		my $nocatlinka2 = '';	# リンク用マークアップ(後)
		if( $setdat{'nocatshow'} == 1 ) {
			# リンクするかどうか
			if( $flags =~ /</ ) {
				# リンクする場合
				my $nocatlink = &makeQueryString("cat=-");		# カテゴリなし用
				if( $optPure == 1 ) {
					# スキン維持を無効化
					$nocatlink = &cutSkinFromQuery( $nocatlink );
				}
				if( $optFull == 1 ) {
					# フルパス化
					$nocatlink = $cgifullurl . $nocatlink;
				}
				# リンク用マークアップを生成
				$nocatlinka1 = qq|<a href="$nocatlink" class="categorylink cat-">|;
				$nocatlinka2 = '</a>';
			}
			return ('<span class="nocategory">' . $nocatlinka1 . &fcts::forsafety( $setdat{'nocatlabel'} ) . $nocatlinka2 . '</span>');
		}
	}

	# ------------------
	# カテゴリごとに処理
	# ------------------
	# カテゴリを配列に分解
	my @cats = split(/,/,$catcsv);

	my $ret = '';
	foreach my $cid ( @cats ) {

		my $catname	= &fcts::forsafety( &fcts::getCategoryDetail( $cid, 1 ));	# カテゴリ名を得る
		my $catid	= &fcts::forsafety( $cid );	# カテゴリIDを安全化(規格通りのIDなら不要だが)

		my $catret = '';
		foreach my $flag (split //, $flags) {
			# フラグがあるだけループ
			if(    $flag eq 'T' )	{ $catret .= qq|<span class="categoryname cat-$catid">$catname</span>|; }
			elsif( $flag eq 'D' )	{ $catret .= '<span class="categorydescription">' . &fcts::forsafety( &fcts::getCategoryDetail( $cid, 2 ) ) . '</span>'; }
			elsif( $flag eq 'I' )	{
				# カテゴリアイコンの出力
				my $caticonurl = &fcts::getCategoryDetail( $cid, 6 ) || '';
				if( $caticonurl ne '' ) {
					# アイコンURLがある場合のみ追加
					$catret .= '<span class="categoryicon"><img src="' . &fcts::forsafety($caticonurl) . '" alt="' . $catname . '" class="cat-' . $catid . '"></span>';
				}
			}
			elsif( $flag eq '<' )	{
				# カテゴリリンクの出力
				my $catlink = &makeQueryString("cat=$catid");	# カテゴリIDがある場合用
				if( $optPure == 1 ) {
					$catlink = &cutSkinFromQuery( $catlink );	# スキン維持を無効化
				}
				if( $optFull == 2 ) {
					$catlink = $cgifullurl . $catlink;			# フルパス化
				}
				if(    $optGallery == 1 ) { $catlink .= '&amp;mode=gallery'; }		# ギャラリーモード適用
				elsif( $optSitemap == 1 ) { $catlink .= '&amp;mode=sitemap'; }		# サイトマップモード適用

				$catret .= qq|<a href="$catlink" class="categorylink cat-$catid">|;
			}
			elsif( $flag eq '>' )	{ $catret .= '</a>'; }
			elsif( $flag eq '"' )	{ $catret .= '&quot;'; }
			elsif( $flag eq "'" )	{ $catret .= '&apos;'; }
			else { $catret .= $flag; }
		}

		# 既に別のカテゴリがあるなら区切り文字を加える (※区切り文字が指定されている場合のみ)
		if( $ret ne '' && $setdat{'catseparator'} ne '' ) {
			$ret .= qq|<span class="catseparator">| . &fcts::forsafety($setdat{'catseparator'}) . '</span>';	# 安全化して加える
		}

		# 生成したカテゴリ文字列を追加する
		$ret .= $catret;
	}

	return $ret;
}

# ----------------------
# 所属カテゴリを挿入する	引数1：所属カテゴリCSVデータ、引数2：区切り文字列、引数3：リンクに(2:する(フルパス)1:する(相対パス)/0:しない)、引数4：現在スキンの無効化(0:しない/1:する)
# ----------------------	返値：カテゴリ名とカテゴリIDを含むリンクのHTMLソース
sub outputCategorySet
{
	my $catcsv	= shift @_ || '';	# 所属カテゴリCSVデータ (カテゴリIDだけがカンマ区切りで並ぶ形式)
	my $sep		= shift @_ || '';	# 区切り文字列
	my $linkize = shift @_ || 0;	# リンク化
	my $pureize = shift @_ || 0;	# スキン無効化

	my $ret = '';

	# カテゴリを配列に分解
	my @cats = split(/,/,$catcsv);

	# カテゴリリンク群を生成
	foreach my $cid ( @cats ) {
		my $catname = &fcts::forsafety( &fcts::getCategoryDetail( $cid, 1 ));	# カテゴリ名を得る
		my $catid = &fcts::forsafety( $cid );	# カテゴリIDを安全化(規格通りのIDなら不要だが)
		my $catlink = &makeQueryString("cat=$catid");	# カテゴリIDがある場合用
		if( $pureize == 1 ) {
			# スキン維持を無効化
			$catlink = &cutSkinFromQuery( $catlink );
		}
		if( $linkize == 2 ) {
			# フルパス化
			$catlink = $cgifullurl . $catlink;
		}
		# 既に別のカテゴリがあるなら区切り文字を加える (※区切り文字が指定されている場合のみ)
		if( $ret ne '' && $sep ne '' ) {
			$ret .= qq|<span class="catseparator">| . &fcts::forsafety($sep) . '</span>';	# 安全化して加える
		}
		# カテゴリ名を追加
		if( $linkize >= 1 ) {
			# カテゴリリンクHTMLを生成して追加
			$ret .= qq|<a href="$catlink" class="categorylink cat-$catid">$catname</a>|;
		}
		else {
			# カテゴリ名だけを追加
			$ret .= qq|<span class="categoryname cat-$catid">$catname</span>|;
		}
	}

	# カテゴリが1つもなければ：
	if( $ret eq '' ) {
		# 指定の文字列を出力する設定の場合は出力する
		my $nocatlinka1 = '';	# リンク用マークアップ(前)
		my $nocatlinka2 = '';	# リンク用マークアップ(後)
		if( $setdat{'nocatshow'} == 1 ) {
			# リンクするかどうか
			if( $linkize >= 1 ) {
				# リンクする場合
				my $nocatlink = &makeQueryString("cat=-");		# カテゴリなし用
				if( $pureize == 1 ) {
					# スキン維持を無効化
					$nocatlink = &cutSkinFromQuery( $nocatlink );
				}
				if( $linkize == 2 ) {
					# フルパス化
					$nocatlink = $cgifullurl . $nocatlink;
				}
				# リンク用マークアップを生成
				$nocatlinka1 = qq|<a href="$nocatlink" class="categorylink cat-">|;
				$nocatlinka2 = '</a>';
			}
			$ret .= '<span class="nocategory">' . $nocatlinka1 . &fcts::forsafety( $setdat{'nocatlabel'} ) . $nocatlinka2 . '</span>';
		}
	}

	return $ret;
}

# -----------------------
# 所属カテゴリIDを列挙する	引数1：所属カテゴリCSVデータ、引数2：区切り文字列
# -----------------------
sub outputCategoryIDs
{
	my $catcsv	= shift @_ || '';	# 所属カテゴリCSVデータ (カテゴリIDだけがカンマ区切りで並ぶ形式)
	my $sep		= shift @_ || '';	# 区切り文字列
	my $altstr	= shift @_ || '';	# 無指定時の代替文字列

	if( $catcsv eq '' ) {
		# カテゴリCSVが空なら、代替文字列に置き換える
		$catcsv = $altstr;
	}

	$catcsv =~ s/,/$sep/g;	# カテゴリCSVの区切り文字「,」を指定区切り文字に置き換えるだけ

	return $catcsv;
}

# ------------------------------------------
# てがろぐローカルなシステム記号を安全化する
# ------------------------------------------
sub tegalogsystemsafety
{
	my $str = shift @_ || '';

	$str =~ s/\[\[/&#91;&#91;/g;
#	$str =~ s/\]\]/&#93;&#93;/g;	# [[SYSTEM]] のような記述をブロックするのが目的だが、 [B:あああ[U:いいい]] のようなケースで、問題ない「 ]] 」が登場する可能性があるので、閉じ括弧の連続は処理しない。

	return $str;
}

# -----------------------------------------
# 指定範囲を隠す部分(HTML/JavaScript)の出力		※「続きを読む」と「範囲を隠す」で共通
# -----------------------------------------
sub outputHiddenArea
{
	my $kind = shift @_ || '隠';						# 引数1：種別名
	my $moreid  = shift @_ || &fcts::getrandstr(7);		# 引数2：隠す領域1つ1つに割り当てるユニークID
	my $morenum = shift @_ || '';						# 引数3：隠す番号
	my $readmorebuttontag	= shift @_ || 'a';			# 引数4：隠すボタンを作る要素名
	my $readmorehidetag		= shift @_ || 'span';		# 引数5：隠す範囲を出力する要素名
	my $readmorestyle		= shift @_ || 0;			# 引数6：展開する範囲の表示方法(0:inline/1:inline-block/2:block)
	my $readmorelabelopen	= shift @_ || '展開';		# 引数7：展開ボタンのラベル
	my $readmorelabelclose	= shift @_ || '畳む';		# 引数8：畳むボタンのラベル
	my $needclosebutton		= shift @_ || 0;			# 引数9：畳むボタンの出力が(1:必要/0:不要)
	my $sepcomment = shift @_ || '';					# 引数10:隠される本文(Separated Comment)

	# ラベル名を安全化
	$readmorelabelopen  = &fcts::forsafety( $readmorelabelopen  );
	$readmorelabelclose = &fcts::forsafety( $readmorelabelclose );

	# 展開する範囲の表示方法(0:inline/1:inline-block/2:block)
	my $readmoreblock = 'inline';
	if(		$readmorestyle == 1 ) { $readmoreblock = 'inline-block'; }
	elsif(	$readmorestyle == 2 ) { $readmoreblock = 'block'; }

	# 内部に続きを読む用の記号が存在する場合には無効化する
	$sepcomment =~ s/&lt;&gt;/&#60;&#62;/g;

	my $ret = '';

	# 展開ボタンの出力(Button)
	$ret .= qq|<!-- $kind$morenum(B) --><$readmorebuttontag href="#readmore" id="button4$moreid" style="display:none;" class="readmorebutton readmoreopen" onclick="document.getElementById('$moreid').style.display = '$readmoreblock'; this.style.display = 'none'; return false;">$readmorelabelopen$morenum</$readmorebuttontag>|;

	# 本文の出力(Honbun)
	$ret .= qq|<!-- $kind$morenum(H) --><$readmorehidetag id="$moreid" class="readmorearea">| . $sepcomment;
	if( $needclosebutton != 0 ) {
		$ret .= qq|<$readmorebuttontag href="#readclose" class="readmorebutton readmoreclose" onclick="document.getElementById('$moreid').style.display = 'none'; document.getElementById('button4$moreid').style.display = 'inline-block'; return false;">$readmorelabelclose$morenum</$readmorebuttontag>|;
	}
	$ret .= qq|</$readmorehidetag>|;

	# スクリプトの出力(Script)
	$ret .= qq|<!-- $kind$morenum(S) --><script type="text/javascript">document.getElementById('$moreid').style.display = 'none'; document.getElementById('button4$moreid').style.display = 'inline-block';</script>|;

	return $ret;
}
# ------------------------------
# 音声読み上げ用スクリプトの出力	引数1：識別用のユニークな文字列、引数2：本文
# ------------------------------
sub outputSpeechScript
{
	my $unique = shift @_ || &fcts::getrandstr(5);	# 指定がなければランダム英数字5文字
	my $text = shift @_ || '';

	# HTMLタグや改行をすべて除外する
	$text =~ s/<.*?>//g;
	$text =~ s/[\r\n]//g;

	# 読み上げに不都合のある数値文字参照等を実体に戻すか消す
	$text =~ s/&#91;/[/g;	# 角括弧は戻す
	$text =~ s/&#93;/]/g;	# 角括弧は戻す
	$text =~ s/&#58;/:/g;	# ：は戻す
	$text =~ s/&#35;/#/g;	# ＃は戻す
	$text =~ s/&apos;/'/g;	# 'は戻す
	$text =~ s/&lt;|&gt;|&quot;|<|>|"//g;		# <>"は消す

	# 文字数が多い場合の確認ダイアログ
	my $check = '';
	if( length($text) >= 100 ) {
		$check = q|if(!window.confirm('読み上げ対象が100文字を超えていますが、本当に読み上げますか？（読み上げは途中で停止できません）')) { return; }|;
	}

	# スクリプトを出力 (※変数$textには半角アポストロフィがそのまま入る可能性がある点に注意！)
	my $ret = &fcts::tooneline( qq|
		<script>
		function comSpeech$unique() {
			$check
			const uttr = new SpeechSynthesisUtterance("$text");
			speechSynthesis.speak(uttr);
		}
		</script>
		<a href="#" onclick="comSpeech$unique(); return false;">読上</a>
	| );

	return $ret;
}

# -----------------------------------------------
# COMMENT：指定行だけor指定行より後のすべてを返す
# -----------------------------------------------
sub getLatterLines
{
	my $first = shift @_ || 0;	# 引数1：欲しい最初の対象行番号(0は1と等価)
	my $wants = shift @_ || 0;	# 引数2：1行だけを欲しい場合は1、対象行以降のすべてを欲しい場合は0
								# 引数3：行単位で分解済みのコメント配列
	my $ret = '';

	my $i = 1;
	foreach my $oneline ( @_ ) {
		if( $i >= $first ) {
			# 対象行かそれ以降なら
			$ret .= $oneline . '<br />';
			if( $wants == 1 ) {
				# 1行だけで良いならループを終わる
				last;
			}
		}
		$i++;
	}

	return $ret;
}

# --------------------------------------------------
# リンクのhref属性値をギャラリーモード用に書き換える	引数：HTMLソース
# --------------------------------------------------
sub rewriteHrefToGallery
{
	my $html = shift @_ || '';
	$html =~ s|href="(.+?)"|href="$1&amp;mode=gallery"|g;
	return $html;
}

# ----------------------------------------------------------
# リンクのhref属性値をサイトマップページモード用に書き換える	引数：HTMLソース
# ----------------------------------------------------------
sub rewriteHrefToSitemappage
{
	my $html = shift @_ || '';
	$html =~ s|href="(.+?)"|href="$1&amp;mode=sitemap"|g;
	return $html;
}

# -------------------------
# COMMENT：特定の条件で返す
# -------------------------
sub getPartOfLines
{
	my $want  = shift @_ || '';	# 引数1：キーワード( TITLE, BODY, TEXT )
	my $limit = shift @_ || 0;	# 引数2：文字数の制限数値「40」とか(＝40文字)
	my $rdec  = shift @_ || 0;	# 引数3：文字数を制限する際に、てがろぐ記法の数値文字参照をデコード(1:する/0:しない)
	my $altnt = shift @_ || 0;	# 引数4：TITLEが空の場合に挿入する文字列(alternate)
								# 引数5：行単位で分解済みのコメント配列
	my $ret = '';

	# TITLE：原則として1行目を返す。ただし装飾や画像(＝HTMLタグ)は除外する。
	if( $want eq 'TITLE' ) {
		$ret = &getLatterLines(1,1,@_);
		$ret =~ s/<blockquote.*?>.+<\/blockquote>//g;	# ツイート埋め込み全体を除外する
		$ret =~ s/<script.*?>.+<\/script>//g;			# JavaScript全体を除外する
		$ret =~ s/<.*?>//g;		# HTMLタグを除外する
		if( &fcts::trim($ret) eq '' ) {
			# 中身が空なら代替文字(たぶんPost ID)を挿入
			$ret = $altnt;
		}
	}
	# BODY：原則として2行目以降の全行を返す。ただし1行しかない投稿なら1行全部を返す。
	elsif( $want eq 'BODY' ) {
		if( $#_ == 0 ) {
			# 1行しかない場合は全部を返す
			$ret = $_[0];
		}
		else {
			# 複数行あるなら2行目以降を返す
			$ret = &getLatterLines(2,0,@_);
		}
	}
	# TEXT：全行を返す。(プレーンテキスト化して文字数を制限する用)
	elsif( $want eq 'TEXT' ) {
		$ret = join('<br>',@_);
	}
	# TAGS：ハッシュタグのみを返す
	elsif( $want eq 'TAGS' ) {
		my $targettemp = join('',@_);	# とりあえず1変数に統合
		my @htags = $targettemp =~ m|(<a href="\?tag=.+?" class="taglink" title=".+?">.+?</a>)|g;		# ハッシュタグ部分を抜き出して全部配列に入れる
		# 全部を表示
		foreach my $show ( @htags ) {
			$ret = join(' ',@htags );
		}
	}
	else {
		# 定義外のキーワードだった場合はエラー文字列を返す
		return '[COMMENT:スペルミス？]'
	}

	if( $limit > 0 ) {
		# 文字数制限があれば切り詰める(HTMLタグは抹消してから／画像だけは省略の事実を文字で加える)
		my $imgomit = '';
		if( $setdat{'insertalttext'} == 1 ) { $imgomit = '(画像省略)'; }
		$ret =~ s/<img .+?>/$imgomit/g;
		$ret =~ s/<.+?>//g;
		if( $rdec == 1 ) {
			# てがろぐ記法の数値文字参照をデコード
			$ret = &fcts::decreftegalog($ret);
			$ret =~ s/&nbsp;/ /g;	# 空白の文字実体参照もデコードしておく
		}
		$ret = &fcts::mbSubstr( $ret, $limit, '…' );	# 切り詰める
		if( $rdec == 1 ) {
			# てがろぐ記法を再エンコード(安全化)
			$ret = &fcts::encreftegalog($ret);
		}
	}

	return $ret;
}

# -----------------------------------
# 文字列内に含まれるURLをリンク化する	※引数の文字列は既に安全化されていることが前提
# -----------------------------------
sub linkize
{
	my $ts = shift @_ || '';

	# ▼画像リンク処理
	if( $setdat{'urlexpandimg'} != 0 ) {
		# 画像ラベル付きURLなら画像として掲載
		$ts =~ s|\[[Ii][Mm][Gg]:(\S*?)\](https?:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:@&=+\$,%#]+)|&embedimage($2,$1)|eg;
	}

	# ▼動画リンク処理
	if( $setdat{'urlexpandyoutube'} != 0 ) {
		# YouTubeラベル付きURLなら動画を埋め込む
		$ts =~ s|\[[Yy][Oo][Uu][Tt][Uu][Bb][Ee]\]https?:\/\/www\.youtube\.com\/watch\?[-_.!~*\'()a-zA-Z0-9;\/?:@&=+\$,%#]*?v=([-\w]+)[-_.!~*\'()a-zA-Z0-9;\/?:@&=+\$,%#]*|&embedyoutube($1)|eg;
		$ts =~ s|\[[Yy][Oo][Uu][Tt][Uu][Bb][Ee]\]https?:\/\/youtu\.be\/([-\w]+)[-_.!~*\'()a-zA-Z0-9;\/?:@&=+\$,%#]*|&embedyoutube($1)|eg;
	}

	# ▼音楽リンク処理
	if( $setdat{'urlexpandspotify'} != 0 ) {
		# Spotifyラベル付きURLなら音楽を埋め込む
		$ts =~ s|\[[Ss][Pp][Oo][Tt][Ii][Ff][Yy]\](https?:\/\/open\.spotify\.com\/embed/[-_.!~*\'()a-zA-Z0-9;\/?:@&=+\$,%#]+)|&embedspotify('-',$1)|eg;
		$ts =~ s|\[[Ss][Pp][Oo][Tt][Ii][Ff][Yy]\]https?:\/\/open\.spotify\.com\/([A-Za-z]+?)/([-_.!~*\'()a-zA-Z0-9;\/?:@&=+\$,%#]+)|&embedspotify($1,$2)|eg;
	}

	# ▼ツイートリンク処理
	if( $setdat{'urlexpandtweet'} != 0 ) {
		# Tweetラベル付きURLならツイートを埋め込む
		$ts =~ s|\[[Tt][Ww][Ee][Ee][Tt]\](https?:\/\/[\w\.]*twitter\.com\/[-_.!~*\'()a-zA-Z0-9;\/?:@&=+\$,%#]*)|&embedtweet($1)|eg;
	}

	# ▼テキストリンク処理
	if( $setdat{'urlautolink'} != 0 ) {
		# URL単独ならそのままリンク化 (正規表現1行で書ける！ 驚きだぜ！)
		$ts =~ s|((?<!=")https?:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:@&=+\$,%#]+)|&urlshorter($1,$setdat{'longurlcutter'})|eg;	# 否定戻り読み (?<!regex)を使用。

		# --------------------------------
		# ▼ラベルがあればラベルでリンク化	※リンクラベルには半角角括弧 [ , ] と#以外なら何でも可とする。
		# --------------------------------	※リンクラベルとして画像が指定されていれば、画像でリンクを作れる。

		# ▽ラベル内にaタグが存在する場合はaタグを排除してリンク化する処理を加える (→内部画像/外部画像を任意のリンク先にリンクできる)
		$ts =~ s/\[<a .+?>(.+?)<\/a>\](<a class="url".+?>)(.+?)(<\/a>)/$2$1$4/g;

		# ▽LBコマンド付きラベル：
		$ts =~ s/\[([^\[\]#]+?):LB\](<a class="url".+?)>(.+?)(<\/a>)/$2 $setdat{'urlimagelightboxatt'}>$1$4/g;
		# ▽ノーマルラベル
		$ts =~ s/\[([^\[\]#]+?)\](<a class="url".+?>)(.+?)(<\/a>)/$2$1$4/g;
	}

	return $ts;
}

# -------------------------------------------
# 文字列内に含まれる装飾指示をマークアップする	※引数の文字列は既に安全化されていることが前提
# -------------------------------------------	※角括弧をエスケープする処理が入るので、コマンド解釈処理の中ではこの関数を一番最後に実行すること。
sub comdecorate
{
	my $ts = shift @_ || '';

	if( $setdat{'allowdecorate'} != 0 ) {
		# 角括弧の個数回数だけループすることで、入れ子構造になっていても全数を対象できるようにする。(エスケープ用ループと、装飾用ループの、2回のループで使う)
		my $count = (() = $ts =~ /\[/g);

		# 角括弧とコロン記号のエスケープ記法処理
		$ts =~ s|\\\[|&#91;|g;		# \[ の記述を &#91; に置き換える。(＝ \ の存在は消える)
		$ts =~ s|\\\]|&#93;|g;		# \] の記述を &#93; に置き換える。(＝ \ の存在は消える)
		$ts =~ s|\\\:|&#58;|g;		# \: の記述を &#58; に置き換える。(＝ \ の存在は消える)

		# 装飾記法ではないコロン記号をエスケープする処理(5ステップ必要) ※偶然登場する可能性のなさそうな画数の多い漢字を一時的に使用。
		$ts =~ s|\[([A-Z]):([a-zA-Z0-9]+):|顗$1靍$2魵|g;	# 装飾の開始部分『 [英:英数: 』の文字を仮エスケープする1	※装飾記法の開始仕様を変更した際には、ここも併せて書き換える必要がある。
		$ts =~ s|\[([A-Z]):|鑈b靏$1隝e髜|g;					# 装飾の開始部分『 [英: 』の3文字を仮エスケープする2		※装飾記法の開始仕様を変更した際には、ここも併せて書き換える必要がある。
		$ts =~ s|:|&#58;|g;									# すべてのコロン記号を &#58; に置き換える
		$ts =~ s|鑈b靏([A-Z])隝e髜|[$1:|g;					# 仮エスケープを元に戻す2
		$ts =~ s|顗([A-Z])靍([a-zA-Z0-9]+)魵|[$1:$2:|g;		# 仮エスケープを元に戻す1

		# 装飾記法ではない角括弧の対応をエスケープするループ
		for( my $i = 0; $i < $count ; $i++ ) {
			$ts =~ s|\[([^:\[\]]*)\]|&#91;$1&#93;|g;		# 角括弧の内側にある文字列が、コロン記号:と角括弧[]の3文字を含まない文字列(＝0文字も含む)なら、角括弧をエスケープする。
		}

		# 装飾ループ
		for( my $i = 0; $i < $count ; $i++ ) {
			# 太字記述があれば(Bold)
			$ts =~ s|\[B:([^\[\]]+)\]|<b class="decorationB">$1</b>|g;
			# 色指定記述があれば(Color)
			$ts =~ s|\[C:([a-fA-F0-9]{6}):([^\[\]]+)\]|<span class="decorationC" style="color:#$1;">$2</span>|g;
			$ts =~ s|\[C:([a-z]+):([^\[\]]+)\]|<span class="decorationC" style="color:$1;">$2</span>|g;
			# 削除記述があれば(Delete)
			$ts =~ s|\[D:([^\[\]]+)\]|<del class="decorationD">$1</del>|g;
			# 強調記述があれば(Emphasis)
			$ts =~ s|\[E:([^\[\]]+)\]|<em class="decorationE">$1</em>|g;
			# 自由装飾指定記述があれば(Free)
			$ts =~ s|\[F:(\w+):([^\[\]]+)\]|<span class="decorationF deco-$1">$2</span>|g;
			# 斜体記述があれば(Italic)
			$ts =~ s|\[I:([^\[\]]+)\]|<i class="decorationI">$1</i>|g;
			# マーカー指定記述があれば(Marker)
			$ts =~ s|\[M:([a-fA-F0-9]{6}):([^\[\]]+)\]|<span class="decorationM" style="background-color:#$1;">$2</span>|g;
			$ts =~ s|\[M:([a-z]+):([^\[\]]+)\]|<span class="decorationM" style="background-color:$1;">$2</span>|g;
			# 引用記述があれば(Quote)
			$ts =~ s|\[Q:([^\[\]]+)\]|<q class="decorationQ" style="display:block;">$1</q>|g;
			# ルビ記述があれば(Ruby)
			$ts =~ s{\[R:([^\[\]]+?)(&#58;|:)([^\[\]]+?)\]}{<ruby class="decorationR">$1<rp>(</rp><rt>$3</rt><rp>)</rp></ruby>}g;	# 正規表現の区切り記号として s||| の代わりに s{}{} を使用。
			# 小記述があれば(Small)
			$ts =~ s|\[S:([^\[\]]+)\]|<small class="decorationS">$1</small>|g;
			# 極小記述があれば(Tiny)
			$ts =~ s|\[T:([^\[\]]+)\]|<small class="decorationT">$1</small>|g;
			# 下線記述があれば(Underline)
			$ts =~ s|\[U:([^\[\]]+)\]|<u class="decorationU">$1</u>|g;

			# 隠す記述があれば(Hide)
			if(( $setdat{'readherebtnuse'} != 0 ) && (( $cp{'search'} eq '' ) || ( $setdat{'readmoreonsearch'} == 1 )) ) {
				# 有効な場合＋使用可能な状況のみ
				$ts =~ s|\[H:([^\[\]]+)\]|&outputHiddenArea('範囲を隠す' ,'' ,'' ,'' ,'' ,$setdat{'readmorestyle'} ,$setdat{'readmorebtnlabel'} ,$setdat{'readmorecloselabel'} ,$setdat{'readmorecloseuse'} ,$1)|eg;
			}
			else {
				# 使えない状況なら全文を表示
				$ts =~ s|\[H:([^\[\]]+)\]|$1|g;
			}
		}
	}

	return $ts;
}

# -------------------
# DOCUMENT ROOTを得る	（環境変数または設定から）
# -------------------
sub getDocumentRoot
{
	# 環境変数から得るのか、設定固定値を使うのかを調べる
	if( $setdat{'howtogetdocroot'} == 1 ) {
		# 設定固定値を使う場合
		return $setdat{'fixeddocroot'};
	}
	else {
		# 環境変数から得る場合
		return &fcts::envDocumentRoot();
	}
}

# -----------------------------------------------------
# 文字列内に含まれる内部画像の展開指示をマークアップする	※引数1：ファイル名、引数2：代替文字
# -----------------------------------------------------
sub showinsideimage
{
	my $targetfile = &fcts::safetycutter( shift @_ ) || '';		# HTMLタグ関連記号は削除する
	my $alt = &fcts::forsafety( shift @_ ) || '';		# HTMLタグ関連記号はエスケープする

	# 引数の調整 ※製作メモ：呼び出し元の正規表現で否定戻り読み記法が使えればこの処理は不要だが、Perl 5.30未満では使えないのでここで処理する。
	if( $alt =~ m/^https?/ ) {
		# 代替文字が「http」または「https」ならURLを構成するコロンが区切り文字だと誤読された結果なので、第1引数側に結合して、第2引数は空にする。
		$targetfile = $alt . ':' . $targetfile;
		$alt = '';
	}
	$alt =~ s/(.+):$/$1/;	# 第2引数の末尾にあるコロン記号は取り除く

	my $tryfile = '';	# 最終的に src属性値として出力するファイル名(パス)
	my $servpath = '';	# 縦横サイズを取得するためのサーバパス(または相対パス)

	# --------------------------------------------------------------------------------------------------------------------------
	# 指定ファイル名をチェックして挿入用PATHを作る＋画像が内部サーバにあるなら縦横サイズを取得できるよう画像へのサーバパスを作る
	# --------------------------------------------------------------------------------------------------------------------------
	if( $targetfile eq '' ) {
		# ファイル名なしなら空文字列を返す
		return '';
	}
	elsif( $targetfile =~ m/^https?:\/\/.+/ ) {
		# …………………………………………
		# ▼httpまたはhttpsで始まるURLなら
		# …………………………………………
		if( $setdat{'imageouturl'} == 1 ) {
			# 許可されていれば
			$tryfile = $targetfile;

			# CGIの稼働URLと同じならサーバパス化する
			if( &fcts::checkSameDomain( $cgifullurl, $tryfile ) ) {
				# CGI稼働URLと同じドメインなら
				my $fullpath = &fcts::cutofftofullpath( $tryfile );		# 「/」で始まるフルパスの形を得る
				$servpath = &fcts::combineforservpath( &getDocumentRoot(), $fullpath );		# DOCUMENT ROOTと合体させてサーバパスを作る
			}

		}
		else {
			# 許可されていなければエラーを返す
			return q|<i style="| . &styleforembeddederror() . q|">現在の設定では、画像をURLで指定する記法の使用は許可されていません。</i>|;
		}
	}
	elsif( $targetfile =~ m/^\/+/ ) {
		# …………………………………………
		# ▼スラッシュで始まる絶対パスなら
		# …………………………………………
		if( $setdat{'imageoutdir'} == 1 ) {
			# 許可されていれば
			$tryfile = $targetfile;

			# DOCUMENT ROOTと合体させてサーバパスを作る
			$servpath = &fcts::combineforservpath( &getDocumentRoot(), $tryfile );
		}
		else {
			# 許可されていなければエラーを返す
			return q|<i style="| . &styleforembeddederror() . q|">現在の設定では、画像用ディレクトリの外にある画像の表示は許可されていません。</i>|;
		}
	}
	elsif( $targetfile =~ m/\.($setdat{'imageallowext'})$/i ) {
		# …………………………………………
		# ▼ファイル名があり、許可拡張子なら
		# …………………………………………
		if(( $targetfile =~ m/\.\.\// ) && ( $setdat{'imageoutdir'} == 0 )) {
			# 「../」が含まれていて、それが許可されていなければエラーを返す
			return q|<i style="| . &styleforembeddederror() . q|">現在の設定では、画像用ディレクトリの外を参照できる「../」の記述は許可されていません。</i>|;
		}
		# パスを作る
		$tryfile = "$imagefolder/$targetfile";

		# 存在確認
		if( -f $tryfile ) {
			# ファイルがあれば
			$servpath = $tryfile;
			# 絶対URLでの挿入が指定されていれば画像パスを上書き
			if( $setdat{'imagefullpath'} == 1 ) {
				$tryfile = $cgifulldir . "$tryfile";
			}
		}
		else {
			# なければエラー用HTMLを返す (文字列は安全化されていることが前提だが、念のために表示するファイル名は再度安全化。)
			return q|<i style="| . &styleforembeddederror() . q|">画像用ディレクトリ内に、ファイル | . &fcts::mbSubstr($targetfile,30,'…') . ' は見つかりませんでした。</i>';
		}
	}
	else {
		# ファイル名があるが、許可拡張子でなければエラー用HTMLを作る
		return q|<i style="| . &styleforembeddederror() . q|">この拡張子を画像として表示することは、現在の設定では許可されていません。</i>|;
	}

	# ----------------
	# 表示用HTMLを作る
	# ----------------
	# ▼(1)原寸画像へのリンクにするかどうか
	my $ilink1 = '';
	my $ilink2 = '';
	if( $setdat{'imagetolink'} != 0 ) {
		# リンクにするなら

		# ▼(2)Lightbox用の属性を付加するかどうか
		my $lightboxatt = '';
		if( $setdat{'imagelightbox'} != 0 ) {
			# 付加する場合は、空白1文字の後に指定文字列を加える（タグ括弧はエスケープ）
			$lightboxatt = ' ' . &fcts::forsafetytag( $setdat{'imagelightboxatt'} );

			# 代替文字がある場合で、キャプション用属性名の指定があれば
			if(( $alt ne '' ) && ( $setdat{'imagelightboxcap'} ne '' )) {
				# さらに加える（altは安全化済み。属性名は安全化して加える）
				$lightboxatt .= ' ' . &fcts::forsafety( $setdat{'imagelightboxcap'} ) . '="' . $alt . '"';
			}
		}

		# ▼(3)独自のclass属性値を付加するかどうか
		my $userclass = '';
		if( $setdat{'imageaddclass'} == 1 ) {
			# 付加するなら
			$userclass = ' ' . &fcts::forsafety( $setdat{'imageclass'} );
		}

		# リンクHTMLを作る
		$ilink1 = qq|<a class="imagelink$userclass" href="$tryfile"$lightboxatt>|;
		$ilink2 = '</a>';
	}

	# ▼LazyLoad用の属性を付加するかどうか
	my $lazyatt = '';
	if( $setdat{'imagelazy'} != 0 ) {
		# 付加するなら
		$lazyatt = LOADINGLAZYATT;
	}

	# ▼縦横サイズを付加するかどうか
	my $whatt = '';
	if( $setdat{'imagewhatt'} != 0 ) {
		# 付加するなら
		my ($iw,$ih) = &fcts::getImageWidthHeight($servpath);	# 縦横サイズを得る
		if( $iw > 0 && $ih > 0 ) {
			# 縦横サイズが得られたら
			# ▼最大値を制限するかどうか
			if( $setdat{'imagewhmax'} != 0 ) {
				# 制限するなら
				if(( $setdat{'imagemaxwidth'} && $setdat{'imagemaxwidth'} > 16 ) && ( $iw > $setdat{'imagemaxwidth'} )) {
					# 実横幅が横幅最大値を超えていた場合（最大値の指定があり、それが16以上の場合のみ実行）
					my $aspectHW = $ih / $iw;			# 縦横比を計算(=縦/横)
					$iw = $setdat{'imagemaxwidth'};		# 横幅を指定最大値にする
					$ih = $iw * $aspectHW;				# 高さを計算して指定
				}
				if(( $setdat{'imagemaxheight'} && $setdat{'imagemaxheight'} > 16 ) && ( $ih > $setdat{'imagemaxheight'} )) {
					# 実高さが高さ最大値を超えていた場合（最大値の指定があり、それが16以上の場合のみ実行）
					my $aspectWH = $iw / $ih;			# 縦横比を再計算(=横/縦)
					$ih = $setdat{'imagemaxheight'};	# 高さを指定最大値にする
					$iw = $ih * $aspectWH;				# 横幅を計算して指定
				}
				# 小さすぎる場合の対処（10pxを下回るようなら10pxにする／この場合は縦横比を考慮しない）
				if( $iw < 10 ) { $iw = 10; }
				if( $ih < 10 ) { $ih = 10; }
			}

			# 整数にする
			$iw = int($iw);
			$ih = int($ih);

			# 出力用の属性文字列を作る
			$whatt = qq| width="$iw" height="$ih"|;
		}
		# 縦横サイズが得られなかった場合は何もしない。
	}

	# 代替文字を決める
	if( $alt eq '' ) {
		$alt = $targetfile;
	}

	# 表示用HTMLを作って返す
	return qq|$ilink1<img class="embeddedimage"$whatt$lazyatt src="$tryfile" alt="$alt">$ilink2|;
}

# -----------------------------------------
# 文字列内に含まれる内部画像のURLだけを得る		引数1：何番目が必要か, 引数2：絶対URLが必要か(1:必要/0:不要), 引数3：イメージ配列
# -----------------------------------------
sub showinsideimageurl
{
	my $targetnum = shift @_ || 1;
	my $needfullpath = shift @_ || 0;
	my @imageurls = ();

	# イメージ配列全体を走査して、有効な画像リストを作成する
	foreach my $fn ( @_ ) {

		if( $fn eq '' ) {
			# ファイル名なしなら除外
			next;
		}
		elsif( $fn =~ m/^https?:\/\/.+/ ) {
			# URLだったら
			if( $setdat{'imageouturl'} == 1 ) {
				# URLによる画像表示が許可されていれば、そのまま追加
				push(@imageurls, $fn);
			}
			next;	# 許可されていなければ次へ
		}
		elsif( $fn =~ m/^\/.+/ ) {
			# 「/」で始まる絶対パスだったら
			if( $setdat{'imageoutdir'} == 1 ) {
				# 任意ディレクトリ画像の表示が許可されている場合
				if( $needfullpath == 1 ) {
					# 絶対URLでの挿入が指定されていれば（先頭の「/」を除外してフルパスと連結して追加
					my $ret = $cgifulldir . substr($fn,1);
					push(@imageurls, $ret);
				}
				else {
					# 絶対URLにしないならそのまま追加
					push(@imageurls, $fn);
				}
			}
			next;	# 許可されていなければ次へ
		}
		else {
			# その他のファイル名があるなら

			if(( $setdat{'imageoutdir'} == 0 ) && ( $fn =~ m/\.\.\// )) {
				# 任意ディレクトリ画像の表示が許可されていない場合で、「../」を含んでいるなら除外
				next;
			}

			# パスを作る
			my $ret = "$imagefolder/$fn";

			# 存在確認
			if( -f $ret ) {
				# ファイルがあれば

				# 絶対URLでの挿入が指定されていれば画像パスを上書き
				if( $needfullpath == 1 ) {
					$ret = $cgifulldir . "$ret";
				}

				push(@imageurls, $ret);		# ファイルがある場合にだけ追加
			}
			next;	# ファイルがなければ次へ
		}
	}

	return $imageurls[ $targetnum - 1 ] || '';	# 未定義にしないよう修正(v2.4.0+)
}

# --------------------------
# 配列内の指定番目だけを得る		引数1：何番目が必要か, 引数2：対象がない場合の返値、引数3：代替文字の配列
# --------------------------
sub pinpointarray
{
	my $targetnum = shift @_ || 1;
	my $ifnone = shift @_ || '';
	my @array = @_;

	my $arrnum = $#_ + 1;	# 配列の個数

	if( $targetnum > $arrnum || $targetnum <= 0 ) {
		# 指定番号が配列の総数を超えているか、または0以下だったら
		return $ifnone;
	}

	return $array[ $targetnum - 1 ] || '';
}

# ----------------------------------------
# 個別表示時用のユーティリティリンクを作成
# ----------------------------------------
sub utilitylinksforonepost
{
	my ($id,$user,$uname,$cats,$date) = @_;
	my $reversename = &fcts::forsafety($setdat{'showreverseheader'});

	my $ret = "<!-- ▼ユーティリティリンク枠：この表示内容は管理画面の[設定]で取捨選択できます。 -->\n" . '<div class="utilitylinks"><ul>';

	# --------------
	# 状況別リンク群
	# --------------
	if( $setdat{'utilityrandom'} == 1 ) {

		# ランダム継続リンク
		if( $cp{'mode'} eq 'random' ) {
			my $rdl = &makeQueryString('mode=random');
			$ret .= '<li class="urandom"><a href="' . $rdl . '">さらにランダムに表示する</a></li>';
		}

	}

	# ----------------
	# ユーザ別リンク群
	# ----------------
	if( $setdat{'utilitystate'} == 1 ) {

		# ユーザページリンク
		my $ulinks = &makeQueryString("userid=$user");
		my $ulinkr = &makeQueryString("userid=$user",'order=reverse');
		$ret .= qq|<li class="uuser"><a href="$ulinks">ユーザ「$uname」の投稿だけを見る</a> <span class="revlink">(※<a href="$ulinkr">$reversenameで見る</a>)</span></li>|;

	}

	# ------------------
	# カテゴリ別リンク群
	# ------------------
	if( $setdat{'utilitycat'} >= 1 ) {

		# カテゴリが1つ以上ある場合はリンクを列挙
		if( $cats ne '' ) {
			# サブリスト開始
			$ret .= '<li class="ucat"><span class="uchead">この投稿と同じカテゴリに属する投稿：</span><ul class="categorylinks">';

			# カテゴリを配列に分解
			my @cats = split(/,/,$cats);

			# カテゴリリンク群を生成
			foreach my $cid ( @cats ) {
				my $catname = &fcts::forsafety( &fcts::getCategoryDetail( $cid, 1 ));	# カテゴリ名を得る
				my $catid = &fcts::forsafety( $cid );	# カテゴリIDを安全化(規格通りのIDなら不要だが)
				my $catlink1 = &makeQueryString("cat=$catid");	# カテゴリリンクを生成
				my $catlink2 = &makeQueryString("cat=$catid",'order=reverse'); # 時系列版を生成
				# カテゴリリンクHTMLを生成して追加
				$ret .= qq|<li class="ucat"><a href="$catlink1" class="cat-$catid">カテゴリ「$catname」の投稿だけを見る</a> <span class="revlink">(※<a href="$catlink2">$reversenameで見る</a>)</span></li>|;
			}

			# サブリスト終了
			$ret .= '</ul></li>';
		}

		# カテゴリが1つもない場合で、それでもリンクを出力する設定なら出力
		elsif(( $cats eq '' ) && ( $setdat{'utilitycat'} == 2 )) {
			my $nocatlink1 = &makeQueryString("cat=-");
			my $nocatlink2 = &makeQueryString("cat=-",'order=reverse');
			my $nocatlabel = 'どのカテゴリにも属していない';
			if( $setdat{'addnocatitem'} == 1 ) {
				# カテゴリなし独自名称をツリーに加えている場合は、その名称を採用する
				$nocatlabel = 'カテゴリ「' . &fcts::forsafety($setdat{'addnocatlabel'}) . '」の';
			}
			$ret .= qq|<li class="ucat"><a href="$nocatlink1" class="cat-">$nocatlabel投稿だけを見る</a> <span class="revlink">(※<a href="$nocatlink2">$reversenameで見る</a>)</span></li>|;
		}
	}

	# --------------
	# 日付別リンク群
	# --------------
	if( $setdat{'utilitydates'} == 1 ) {
		if( $date =~ m|(\d\d\d\d)/(\d\d)/(\d\d).*| ) {
			# クエリを作成
			my $dlds = &makeQueryString("date=$1/$2/$3");	my $dldr = &makeQueryString("date=$1/$2/$3" ,"order=reverse");	# 同一年月日
			my $dlms = &makeQueryString("date=$1/$2");		my $dlmr = &makeQueryString("date=$1/$2" ,'order=reverse');		# 同一年月
			my $dlys = &makeQueryString("date=$1");			my $dlyr = &makeQueryString("date=$1" ,'order=reverse');		# 同一年
			my $dlns = &makeQueryString("date=$2/$3");		my $dlnr = &makeQueryString("date=$2/$3" ,'order=reverse');		# n年日記
			my $dlts = &makeQueryString("date=$3");			my $dltr = &makeQueryString("date=$3" ,'order=reverse');		# n年m月日記

			# 月日の桁を削減
			my $month = int($2);
			my $day   = int($3);

			# リンクを作成
			my $dret = '';
			$dret .= '<li class="date-ymd"><a href="'	. $dlds . '">' . "$1年$month月$day日" .	qq|の投稿だけを見る</a> <span class="revlink">(※<a href="$dldr">$reversenameで見る</a>)</span></li>|		if( $setdat{'utilitydateymd'} == 1 );
			$dret .= '<li class="date-ym"><a href="'	. $dlms . '">' . "$1年$month月" .		qq|の投稿だけを見る</a> <span class="revlink">(※<a href="$dlmr">$reversenameで見る</a>)</span></li>|		if( $setdat{'utilitydateym'} == 1 );
			$dret .= '<li class="date-y"><a href="'		. $dlys . '">' . "$1年" .				qq|の投稿だけを見る</a> <span class="revlink">(※<a href="$dlyr">$reversenameで見る</a>)</span></li>|		if( $setdat{'utilitydatey'} == 1 );
			$dret .= '<li class="date-md"><a href="'	. $dlns . '">' . "全年$month月$day日" .	qq|の投稿をまとめて見る</a> <span class="revlink">(※<a href="$dlnr">$reversenameで見る</a>)</span></li>|	if( $setdat{'utilitydatemd'} == 1 );
			$dret .= '<li class="date-d"><a href="'		. $dlts . '">' . "全年全月$day日" .		qq|の投稿をまとめて見る</a> <span class="revlink">(※<a href="$dltr">$reversenameで見る</a>)</span></li>|	if( $setdat{'utilitydated'} == 1 );

			# リンクを出力 (1項目以上ある場合だけ)
			if( $dret ne '' ) {
				$ret .= '<li class="udate"><span class="udhead">この投稿日時に関連する投稿：</span><ul class="datelinks">' . $dret . '</ul></li>';
			}
		}
	}

	# --------------
	# 再編集リンク
	# --------------
	if( $setdat{'utilityedit'} == 1 ) {
		my $elink = &makeQueryString("mode=edit","postid=$id");
		$ret .= qq|<li class="uedit"><a href="$elink">この投稿を再編集または削除する</a></li>|;
	}

	$ret .= '</ul></div>';

	return $ret;
}

# ---------------------
# URLを切り詰めリンク化		引数1：URL、引数2：切り詰める文字数(省略可)
# ---------------------
sub urlshorter
{
	my $url = shift @_ || '' ;
	my $len = shift @_ || 40;	# デフォルト文字数

	# 表示時にプロトコル名を省略するかどうか
	my $sho;
	if( $setdat{'urlnoprotocol'} == 1 ) {
		# 省略する
		my $npurl = $url;
		if( $npurl =~ m|https?://(.+)|i ) {
			$npurl = $1;
		}
		# 切り詰め
		$sho = &fcts::mbSubstr($npurl, $len, '...');	# 切り詰めていれば「...」を追加
	}
	else {
		# 省略しないなら
		$sho = &fcts::mbSubstr($url, $len, '...');	# 切り詰めていれば「...」を追加
	}

	# 表示用の安全化
	$url = &fcts::forsafety( $url );
	$sho = &fcts::forsafety( $sho );

	# nofollowの付加
	my $rnf = '';
	if( $setdat{'urlnofollow'} == 1 ) { $rnf = ' rel="nofollow"'; }

	# target属性の付加
	my $linktarget = '';
	if( $setdat{'urllinktarget'} == 1 ) { $linktarget = ' target="_blank"'; }	# 新規ウインドウ
	if( $setdat{'urllinktarget'} == 2 ) { $linktarget = ' target="_top"'; 	}	# フレーム解除

	return qq|<a class="url" href="$url"$linktarget title="$url"$rnf>$sho</a>|;
}

# ----------------------
# 画像の埋め込みリンク化		引数1：URL、引数2：オプション文字列、(引数3：外部リンクURL)
# ----------------------
sub embedimage
{
	my $url = shift @_ || '';
	my $opt = shift @_ || '';
	my $linkto = shift @_ || '';	# 未使用:第3引数は今のところ使っていないので常に空

	# Lightbox用の属性を付加するかどうか(※外部画像用の設定値で判断)
	my $lightboxatt = '';
	if( $setdat{'urlimagelightbox'} != 0 ) {
		# 付加する場合は、空白1文字の後に指定文字列を加える（タグ括弧はエスケープ）
		$lightboxatt = ' ' . &fcts::forsafetytag( $setdat{'urlimagelightboxatt'} );

		# 代替文字があってキャプション用属性値の指定もあれば
		if(( $opt ne '' ) && ( $setdat{'urlimagelightboxcap'} ne '' )) {
			# 安全化して追加
			$lightboxatt .= ' ' . &fcts::forsafety( $setdat{'urlimagelightboxcap'} ) . '="' . &fcts::forsafety( $opt ) . '"';
		}
	}

	# 独自のclass属性値を付加するかどうか
	my $userclass = '';
	if( $setdat{'urlimageaddclass'} == 1 ) {
		# 付加するなら
		$userclass = ' ' . &fcts::forsafety( $setdat{'urlimageclass'} );
	}

	# 同一ドメインに限定する場合の制限処理
	if( $setdat{'embedonlysamedomain'} != 0 ) {
		# 同一ドメインに限定する設定なら
		my $baseurl = $cgi->url(-base, 1);
		if( index($url, $baseurl) != 0 ) {
			# 同一ドメインではない場合は
			return qq|<a class="url urlimage" href="$url"><i style="| . &styleforembeddederror() . q|">URLを指定した外部画像の埋め込みは、現在の設定では同一ドメイン下の画像だけに制限されています。</i></a>|;
		}
	}

	# LazyLoad用の属性を付加するかどうか
	my $lazyatt = '';
	if( $setdat{'urlimagelazy'} != 0 ) {
		# 付加するなら
		$lazyatt = LOADINGLAZYATT;
	}

	# HTML化して返す
	if( $linkto eq '' ) {
		# 外部リンク先の指定がなければ、画像のセルフリンクとして掲載
		return qq|<a class="url urlimage selflink$userclass" href="$url"$lightboxatt><img src="$url" class="embeddedimage"$lazyatt alt="$opt"></a>|;
	}
	else {
		# 外部リンク先の指定があれば、そこへリンクする画像として掲載(※Lightboxは使わない)
		return qq|<a class="url urlimage outerlink$userclass" href="$linkto"><img src="$url" class="embeddedimage"$lazyatt alt="$opt"></a>|;
	}
}

# ------------------------------------
# 埋め込みエラー文字列用の共通スタイル
sub styleforembeddederror {
	return 'font-size:0.75em; color:#c00; background-color:#fee; display:inline-block; border:3px solid pink; border-radius:0.75em; max-width:200px; padding:0.25em; line-height:1.25; overflow-wrap:break-word;';
}

# ----------------
# 動画の埋め込み化		引数1：YouTube動画ID
# ----------------
sub embedyoutube
{
	my $ytid = shift @_ || '';

	# HTML化して返す (LazyLoad標準)
	return qq|<span class="embeddedmovie"><iframe class="embeddedmovie" width="560" height="315" src="https://www.youtube-nocookie.com/embed/$ytid" loading="lazy" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></span>|;
}

# ----------------
# 音楽の埋め込み化		引数1：種類、引数2：シェア用URL
# ----------------
sub embedspotify
{
	my $kind = shift @_ || '';
	my $eurl = shift @_ || '';

	my $urlforembed = '';

	if( $kind eq '-' ) {
		# 埋め込みコード用のURLならそのまま使う
		$urlforembed = $eurl;
	}
	else {
		# シェア用URLなら埋め込み用URLに変換する
		$urlforembed = 'https://open.spotify.com/embed/' . $kind . '/' . $eurl;
	}

	# HTML化して返す
	return qq|<span class="embeddedmusic"><iframe src="$urlforembed" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe></span>|;
}

# --------------------
# ツイートの埋め込み化		引数1：ツイート単独URL
# --------------------
sub embedtweet
{
	my $ytid = shift @_ || '';
	my $retjs = '';

	# スクリプトを既に読んでいるかどうかを確認
	if( $globalFlags{'tweetEmbedScript'} == 0 ) {
		# 読んでいなかったら読み込む
		$retjs = '<script async src="' . $libdat{'twitterwidgetjs'} . '" charset="utf-8"></script>';
		$globalFlags{'tweetEmbedScript'} = 1;
	}

	# テーマの指定があれば含める
	my $twtheme = '';
	if( $setdat{'urlexpandtwtheme'} == 1 ) {
		# Darkテーマ
		$twtheme = ' data-theme="dark"';
	}

	# ツイート埋め込み用のHTMLにして返す (Do not trackオプションは標準で含めておく)
	return qq|<blockquote class="twitter-tweet" data-dnt="true"$twtheme>（ツイート埋め込み処理中...）<a href="$ytid">Twitterで見る</a></blockquote>$retjs|;
}

# ------------------
# 日付境界バーを挿入	引数：クエリ用日付文字列、表示用日付文字列
# ------------------
sub getDateSeparator
{
	my $orgdate = shift @_ || '';
	my $showdate = shift @_ || '';

	# クエリ文字列を作成
	my @qs = ('date=' . $orgdate);

	my $lab;
	my $urlforread;
	my $urlforoutput;

	# ユーザ名限定だったらそれもクエリに追加 (表示文字列も作る)
	my $lm = '';
	if( $cp{'userid'} ne '' ) {
		push(@qs, ("userid=" . &fcts::forsafety($cp{'userid'}) ));
		my $limitedusername = &fcts::forsafety(&fcts::getUserDetail($cp{'userid'},2)) || &fcts::forsafety($setdat{'unknownusername'});
		$lm = '(' . $limitedusername . 'の投稿に限定)';
	}

	# 正順/逆順
	if( $cp{'order'} eq 'reverse' ) {
		# 逆順表示中ならリンクは正順
		$lab = &fcts::forsafety($setdat{'showstraightheader'});					# 正順の文字列
		$urlforread   = &makeQueryString(@qs);									# 読むリンクは正順
		$urlforoutput = &makeQueryString(@qs,'order=reverse','mode=export');	# 出力リンクは逆順
	}
	else {
		# 正順表示中ならリンクは逆順
		$lab = &fcts::forsafety($setdat{'showreverseheader'});	# 逆順の文字列
		$urlforread   = &makeQueryString(@qs,'order=reverse');	# 読むリンクは逆順
		$urlforoutput = &makeQueryString(@qs,'mode=export');	# 出力リンクは正順
	}

	# 絶対URLで出力する場合はフルパスを加えておく
	if( $setdat{'outputlinkfullpath'} == 1 ) {
		$urlforread   = $cgifullurl . $urlforread;
		$urlforoutput = $cgifullurl . $urlforoutput;
	}

	# この範囲だけを読むリンクを生成 (出力する設定の場合だけ)
	my $limlink = '';
	if( $setdat{'separatebarreverse'} != 0 ) {
		$limlink = '<a href="' . $urlforread . '">この範囲を' . $lab . 'で読む' . $lm . '</a>';
	}

	# この範囲をエクスポートするリンクを生成 (出力する設定の場合だけ)
	my $limexport = '';
	if( $setdat{'separatebaroutput'} != 0 ) {
		$limexport = '<a href="' . $urlforoutput . '">この範囲をファイルに出力する</a>';
	}

	# 境界文字列を作成
	my $ret = '<p class="dateseparator">' . $showdate . ' ' . $limlink . ' ' . $limexport . '</p>';

	return $ret;
}

# ------------------------------------
# 日付を分割して指定形式に整形して出力	引数：フラグs、日付文字列
# ------------------------------------
sub arrangeDateStr
{
	my $dflags = shift @_ || '';
	my $date   = shift @_ || '';
	my $ret = '';

	if( $date =~ m|(\d\d\d\d)/(\d\d)/(\d\d) (\d\d):(\d\d):(\d\d)| ) {
		# フラグからフッタ用リンク群を作成
		foreach my $flag (split //, $dflags) {
			# フラグがあるだけループ
			if(    $flag eq 'Y' )	{ $ret .= $1; }
			elsif( $flag eq 'y' )	{ $ret .= substr($1, -2); }	# 西暦(年)下2桁
			elsif( $flag eq 'R' )	{ $ret .= join('', &fcts::getImperialEraYear($1,int($2),int($3)) ); }	# 元号＋和年
			elsif( $flag eq 'r' )	{ $ret .= (&fcts::getImperialEraYear($1,int($2),int($3)) )[1]; }		# 和年のみ
			elsif( $flag eq 'M' )	{ $ret .= $2; }
			elsif( $flag eq 'G' )	{ $ret .= int($2); }
			elsif( $flag eq 'J' )	{ $ret .= &fcts::getmonthname($2,0); }	# 和暦(睦月～師走)
			elsif( $flag eq 'e' )	{ $ret .= &fcts::getmonthname($2,1); }	# 英名略(Jan～Dec)
			elsif( $flag eq 'E' )	{ $ret .= &fcts::getmonthname($2,2); }	# 英名長(January～December)
			elsif( $flag eq 'D' )	{ $ret .= $3; }
			elsif( $flag eq 'N' )	{ $ret .= int($3); }
			elsif( $flag eq 'h' )	{ $ret .= $4; }
			elsif( $flag eq 'm' )	{ $ret .= $5; }
			elsif( $flag eq 's' )	{ $ret .= $6; }
			elsif( $flag eq 'W' )	{ $ret .= &getweekday($1,$2,$3,$4,$5,$6,3); }
			elsif( $flag eq 'w' )	{ $ret .= &getweekday($1,$2,$3,$4,$5,$6,2); }
			elsif( $flag eq 'B' )	{ $ret .= &getweekday($1,$2,$3,$4,$5,$6,1); }
			elsif( $flag eq 'b' )	{ $ret .= &getweekday($1,$2,$3,$4,$5,$6,0); }
			elsif( $flag eq '<' )	{ $ret .= '&lt;'; }
			elsif( $flag eq '>' )	{ $ret .= '&gt;'; }
			elsif( $flag eq '"' )	{ $ret .= '&quot;'; }
			elsif( $flag eq "'" )	{ $ret .= '&apos;'; }
			else { $ret .= $flag; }
		}
	}

	return $ret;
}

sub getweekday
{
	my ( $year, $month, $day, $hour, $min, $sec, $kind ) = @_;
	my $epoch = eval{ &Time::Local::timelocal($sec, $min, $hour, $day, $month - 1, $year - 1900) };
	if( defined( $epoch ) ) {
		# epochが定義されていれば正しい日付なので曜日の取得処理を実行
		return &fcts::getweek( $kind,$epoch );
	}
	# epochが未定義なら存在しない日付なので曜日は「？」を返す
	return '？';
}

# -----------------------------------
# 表示限定(SITUATION)メッセージを作る	引数1：該当件数、引数2：現在ページ番号　／返値：表示用プレーンテキスト
# -----------------------------------
sub makeLimitMsg
{
	my $totaldatnum = shift @_;
	my $nowpagenum = shift @_;
	my $specialmode = '';
	my $limitmsg = '';

	# モード別
	if( $cp{'mode'} eq 'gallery' ) {
		# ギャラリーモードの場合
		$specialmode = &fcts::forsafety( $setdat{'galleryname'} ) . ' ';	# ギャラリー名称
		if( $setdat{'gallerysituation'} == 1 ) {
			$limitmsg = ' ';	# 空白で区切る
		}
	}
	elsif( $cp{'mode'} eq 'sitemap' ) {
		# サイトマップモードの場合
		$specialmode = &fcts::forsafety( $setdat{'sitemappageyname'} ) . ' ';	# サイトマップページ名称
		if( $setdat{'sitemapsituation'} == 1 ) {
			$limitmsg = ' ';	# 空白で区切る
		}
	}

	# 文言バリエーション(ベース)
	my $msg_USER_BEF = 'ユーザ「';			my $msg_USER_AFT = '」の投稿';
	my $msg_1CAT_BEF = 'カテゴリ「';		my $msg_1CAT_AFT = '」に属する投稿';
	my $msg_CATS_BEF = '「';				my $msg_CATS_AFT = '」';
	my $msg_CATS_HEAD = 'カテゴリ';
	my $part_CATS_NO = 'の';
	my $part_CATS_DOCHIRA = 'どちら';
	my $part_CATS_DORE = 'どれ';
	my $msg_CATS_FOOT = 'かに属する投稿';
	my $msg_NOCAT_BEF = 'カテゴリ「';		my $msg_NOCAT_AFT = '」の投稿';
	my $msg_HTAG_BEF = 'タグ「';			my $msg_HTAG_AFT = '」を含む投稿';
	my $msg_SEARCH_BEF = '検索語「';		my $msg_SEARCH_AFT = '」の検索結果';
	my $msg_DATE_AFT = 'の投稿';
	my $conj_DE = 'で、';
	my $conj_NIGENTEI = 'に限定した、';
	my $conj_NAKAGURO = '・';

	# 文言バリエーション切り替え
	if( $setdat{'situationvariation'} == 1 ) {
		# ラベルの場合
		$msg_USER_BEF = 'ユーザ「';			$msg_USER_AFT = '」';
		$msg_1CAT_BEF = 'カテゴリ「';		$msg_1CAT_AFT = '」';
		$msg_CATS_BEF = '「';				$msg_CATS_AFT = '」';
		$msg_CATS_HEAD = 'カテゴリ';
		$part_CATS_NO = '';
		$part_CATS_DOCHIRA = '';
		$part_CATS_DORE = '';
		$msg_CATS_FOOT = '';
		$msg_NOCAT_BEF = 'カテゴリ「';		$msg_NOCAT_AFT = '」';
		$msg_HTAG_BEF = 'タグ「';			$msg_HTAG_AFT = '」';
		$msg_SEARCH_BEF = '検索語「';		$msg_SEARCH_AFT = '」';
		$msg_DATE_AFT = '';
		$conj_DE = '、';
		$conj_NIGENTEI = '、';
	}
	elsif( $setdat{'situationvariation'} == 2 ) {
		# 列挙の場合
		$msg_USER_BEF = '';		$msg_USER_AFT = '';
		$msg_1CAT_BEF = '';		$msg_1CAT_AFT = '';
		$msg_CATS_BEF = '';		$msg_CATS_AFT = '';
		$msg_CATS_HEAD = '';
		$part_CATS_NO = '';
		$part_CATS_DOCHIRA = '';
		$part_CATS_DORE = '';
		$msg_CATS_FOOT = '';
		$msg_NOCAT_BEF = '';		$msg_NOCAT_AFT = '';
		$msg_HTAG_BEF = '';			$msg_HTAG_AFT = '';
		$msg_SEARCH_BEF = '';		$msg_SEARCH_AFT = '';
		$msg_DATE_AFT = '';
		$conj_DE = ' ';
		$conj_NIGENTEI = ' ';
		$conj_NAKAGURO = ' ';
	}

	# ユーザ名限定
	my $username;
	if( $cp{'userid'} ne '' ) {
		$username = &fcts::forsafety(&fcts::getUserDetail($cp{'userid'},2)) || &fcts::forsafety($setdat{'unknownusername'});
		$limitmsg .= '<span class="situation-username-cover">' . $msg_USER_BEF . '<span class="situation-username">' . $username . '</span>' . $msg_USER_AFT . '</span>';
	}

	# カテゴリ限定
	my $catname;
	if( $cp{'cat'} ne '' ) {
		if( $limitmsg ne '' ) { $limitmsg .= $conj_DE; }	# 連結「で、」
		if( $cp{'cat'} ne '-' ) {
			# カテゴリ名が指定されている場合
			if( $cp{'cat'} =~ m/\w,\w/ ) {
				# カンマ区切りで複数のカテゴリがある場合
				my @pcats = split(/,/,$cp{'cat'});	# カンマ区切りで分割
				my $catcount = 0;
				my $catnames = '';
				foreach my $pcat ( @pcats ) {
					$catname = &fcts::forsafety( &fcts::getCategoryDetail($pcat,1) ) || '？';		# 名称があればそれを表示、なければ「？」を表示
					$catname = $msg_CATS_BEF . '<span class="situation-catname">' . $catname . '</span>' . $msg_CATS_AFT;
					if( $catnames ne '' ) {
						# 1つ目のカテゴリ以外なら中黒を追加
						$catnames .= $conj_NAKAGURO;
					}
					$catnames .= $catname;
					$catcount++;
				}
				# カテゴリ数に応じて代名詞を変える
				my $pronoun = $part_CATS_DOCHIRA;						# どちら
				if( $catcount >= 3 ) { $pronoun = $part_CATS_DORE; }	# どれ
				$limitmsg .= '<span class="situation-catnames-cover">' . $msg_CATS_HEAD . $catnames . $part_CATS_NO . $pronoun . $msg_CATS_FOOT . '</span>';
			}
			else {
				# カテゴリ1つの場合
				$cp{'cat'} =~ s/,//g;	# もしカンマ記号があったら削除しておく
				$catname = &fcts::forsafety( &fcts::getCategoryDetail($cp{'cat'},1) ) || '？';		# 名称があればそれを表示、なければ「？」を表示
				$limitmsg .= '<span class="situation-onecatname-cover">' . $msg_1CAT_BEF . '<span class="situation-catname">' . $catname . '</span>' . $msg_1CAT_AFT . '</span>';
			}
		}
		else {
			# カテゴリなしが指定されている場合
			$limitmsg .= '<span class="situation-nocatname-cover">';
			if( $setdat{'addnocatitem'} == 1 ) {
				# カテゴリなし独自名称をツリーに加えている場合は、その名称を採用する
				$limitmsg .= $msg_NOCAT_BEF . '<span class="situation-catname">' . &fcts::forsafety($setdat{'addnocatlabel'}) . '</span>' . $msg_NOCAT_AFT;
			}
			else {
				$limitmsg .= 'どのカテゴリにも属していない投稿';
			}
			$limitmsg .= '</span>';
		}
	}

	# ハッシュタグ限定
	if( $cp{'hasgtag'} ne '' ) {
		if( $limitmsg ne '' ) { $limitmsg .= $conj_DE; }	# 連結「で、」
		$limitmsg .= '<span class="situation-tagname-cover">' . $msg_HTAG_BEF . '<span class="situation-tagname">' . &fcts::forsafety($cp{'hasgtag'}) . '</span>' . $msg_HTAG_AFT . '</span>';
	}

	# 検索限定
	if( $cp{'search'} ne '' ) {
		if( $limitmsg ne '' ) { $limitmsg .= $conj_NIGENTEI; }	# 連結「に限定した、」

		# 検索語の表示用調整
		my $searchstr = $cp{'search'};
		$searchstr =~ s/　/ /g;			# 全角空白を半角空白にする
		$searchstr =~ s/\s+/ /g;		# 空白系文字の連続を半角空白1つにする
		my @searchwords = split(/ /,$searchstr);		# 空白で分割
		foreach my $oneword (@searchwords) {
			# 特殊検索の内容を表示
			if( $oneword =~ m/^-(.+)/ ) {
				# 先頭がマイナスの場合
				$oneword = "〔除外:$1〕";
			}
			elsif( $oneword =~ m/(.+)\|(.+)/ ) {
				# 途中に縦棒がある場合
				$oneword = "〔$1 or $2〕";
			}
		}
		my $wordsforshow = join(' ', @searchwords);

		$limitmsg .= '<span class="situation-search-cover">' . $msg_SEARCH_BEF . '<span class="situation-search">' . &fcts::forsafety($wordsforshow) . '</span>' . $msg_SEARCH_AFT . '</span>';
	}

	# 日付指定限定
	if( $cp{'datelim'} ne '' ) {
		if( $limitmsg ne '' ) { $limitmsg .= $conj_NIGENTEI; }	# 連結「に限定した、」
		$limitmsg .= '<span class="situation-date-cover"><span class="situation-date">' . &fcts::cutzeroinjpdate( &fcts::datetojpstyle( &fcts::forsafety($cp{'datelim'}) ) ) . '</span>' . $msg_DATE_AFT . '</span>';
	}

	# ページ移動リンクに恒常系設定を付加
	if( $cp{'order'} eq 'reverse' ) {
		# 逆順の場合：
		my $revmsg = &fcts::forsafety($setdat{'showreverseheader'});
		if( $limitmsg ne '' ) {
			# 他の条件があればカッコ付きで表示する
			$revmsg = '(' . $revmsg . ')';
		}
		$limitmsg .= $revmsg;
	}

	# 限定メッセージがある場合に限って、該当表示件数を追加（表示する設定の場合のみ）
	if(( $limitmsg ne '' ) && ( $setdat{'situationcount'} == 1 )) {
		$limitmsg .= '<span class="situation-hits">' . &fcts::forsafety($setdat{'situationcountlabel1'}) . '<span class="num">' . $totaldatnum . '</span>' . &fcts::forsafety($setdat{'situationcountlabel2'}) . '</span>';	# デフォルトでは ［xx件］
	}

	# 2ページ目以降の場合は、さらにページ番号を追加（表示する設定の場合のみ）
	if( $nowpagenum > 1 ) {
		# 限定メッセージがない場合で常にページ番号を表示する設定になっているか、または、限定メッセージがある場合でページ番号を表示する設定になっていれば
		if( (( $limitmsg eq '' ) && ( $setdat{'situationalwayspage'} == 1 )) || (( $limitmsg ne '' ) && ( $setdat{'situationpage'} == 1 )) ) {
			$limitmsg .= '<span class="situation-page">' . &fcts::forsafety($setdat{'situationpagelabel1'}) . '<span class="num">' . $nowpagenum . '</span>' .  &fcts::forsafety($setdat{'situationpagelabel2'}) . '</span>';	# デフォルトでは （xxページ目）
		}
	}

	# 単独表示の場合
	if( $cp{'postid'} > 0 ) {

		# プレビューかどうかの判定をしておく
		my $preview = '';
		my $permittedid = &fcts::checkpermission(1);	# 読み取り専用モードで認証を確認 (※ログインされていればユーザIDが得られる)
		if( $permittedid ) {
			# ログインされていたら、当該データを読んで中身を得る（必要なのは「フラグ(下書きかどうか)」と「投稿者ID」だけだが）
			my ($date,$user,$comment,$cats,$flags) = &getOnePost( $cp{'postid'} );
			if( $flags =~ /draft/ ) {
				# 下書きだったら、投稿者IDとログイン中ユーザIDが等しいかどうかを確認
				if( $permittedid eq $user ) {
					# 等しかったらプレビュー表示
					$preview = ' (下書きのプレビュー)';
				}
			}
		}

		# ランダム表示の追記
		my $randomshow = '';
		if( $cp{'mode'} eq 'random' ) {
			$randomshow = ' (ランダム表示)';
		}

		# 投稿番号を表示する設定か、プレビュー表示時か、ランダム表示時ならPostIDを表示
		if(( $setdat{'onepostpagesituation'} == 1 ) || ( $preview ne '' ) || ( $cp{'mode'} eq 'random' )) {
			$limitmsg = '<span class="situation-postno">No.' . $cp{'postid'} . $preview . $randomshow . '</span>';		# 追加せず上書き
		}

	}

	return $specialmode . $limitmsg;
}

# -------------------------
# 表示限定class文字列を作る	引数1：該当件数、引数2：現在ページ番号　／返値：class用プレーンテキスト
# -------------------------
sub makeLimitClasses
{
	my $totaldatnum = shift @_ || 0;
	my $nowpagenum  = shift @_ || 1;
	my @classkeys = '';

	# 何も限定されていない場合
	if( &islimited() == 0 ) {
		# 限定されていなかったら
		if( $nowpagenum == 1 ) {
			# Topページなら
			push(@classkeys,('home','nofiltering'));
		}
		else {
			# Deepページなら
			push(@classkeys,'nofiltering');
		}
	}

	# ユーザ名限定
	my $username;
	if( $cp{'userid'} ne '' ) {
		push(@classkeys,('selected-user', ('user-'. &fcts::forsafety($cp{'userid'})) ));
	}

	# カテゴリ限定
	my $catname;
	if( $cp{'cat'} ne '' ) {
		push(@classkeys,'selected-cat');
		my @pcats = split(/,/,$cp{'cat'});	# カンマ区切りで分割
		foreach my $pcat ( @pcats ) {
			push(@classkeys,('cat-'. &fcts::forsafety( $pcat )) );
		}
	}

	# ハッシュタグ限定
	if( $cp{'hasgtag'} ne '' ) {
		push(@classkeys,('selected-tag', ('tag-'. &fcts::urlencode($cp{'hasgtag'})) ));
	}

	# 検索限定
	if( $cp{'search'} ne '' ) {
		push(@classkeys,('search-result'));
	}

	# 日付指定限定
	if( $cp{'datelim'} ne '' ) {
		my $datestr = &fcts::forsafety($cp{'datelim'});		# 指定されている日付表記の
		$datestr =~ s|/|-|g;								# /記号を -記号に置き換える
		push(@classkeys,('selected-date', ('date-'. $datestr ) ));
	}

	# 単独表示の場合
	if( $cp{'postid'} > 0 ) {
		push(@classkeys, 'onelog');
		push(@classkeys, ('log-' . &fcts::forsafety($cp{'postid'}) ));
	}

	# 表示データがあるかどうか＆ページ数を追加
	if( $totaldatnum > 0 ) {
		# 1件以上ある場合
		push(@classkeys, 'hit' );

		# ページ数を追加（単独投稿ではない場合のみ）
		if( $cp{'postid'} == 0 ) {
			if( $nowpagenum == 1 ) {
				# 1ページ目の場合
				push(@classkeys, 'toppage' );
			}
			else {
				# 2ページ目以降の場合
				push(@classkeys, 'deeppage' );
			}
		}
	}
	else {
		# ヒットなし
		push(@classkeys, 'nohit');
	}

	# 表示順を追加
	if( $cp{'order'} eq 'reverse' ) {
		# 逆順の場合
		push(@classkeys,('reversed'));
	}

	return join(' ', @classkeys);
}

# ------------------------
# 表示対象限定クエリを作る	引数:除外する限定項目(0=何も除外しない／1=「mode」を除外する)
# ------------------------
sub makeLimitQuery
{
	my $exclude = shift @_ || 0;
	my @lq;

	# 特殊モード
	if( $exclude == 0 ) {
		if( $cp{'mode'} eq 'gallery' ) {
			push(@lq, "mode=gallery");		# ギャラリーモードを維持するため
		}
		elsif( $cp{'mode'} eq 'sitemap' ) {
			push(@lq, "mode=sitemap");		# サイトマップページモードを維持するため
		}
	}

	# 投稿限定（※IDはユニークな番号なので、正しいデータで動作している限り、このコードが実行されることはない。＝同じIDの投稿が複数は存在しない。）
	if( $cp{'postid'} > 0 ) {
		push(@lq, ("postid=" . &fcts::forsafety($cp{'postid'}) ));
	}

	# ユーザ名限定
	if( $cp{'userid'} ne '' ) {
		push(@lq, ("userid=" . &fcts::forsafety($cp{'userid'}) ));
	}

	# カテゴリ名限定
	if( $cp{'cat'} ne '' ) {
		push(@lq, ("cat=" . &fcts::forsafety($cp{'cat'}) ));
	}

	# ハッシュタグ限定
	if( $cp{'hasgtag'} ne '' ) {
		my $htagencoded = &fcts::forsafety($cp{'hasgtag'});
		$htagencoded =~ s/(\W)/'%'.unpack('H2',$1)/eg;
		push(@lq, "tag=$htagencoded" );
	}

	# 検索限定
	if( $cp{'search'} ne '' ) {
		my $sqencoded = &fcts::forsafety($cp{'search'});
		$sqencoded =~ s/(\W)/'%'.unpack('H2',$1)/eg;
		push(@lq, "q=$sqencoded" );
	}

	# 日付指定限定
	if( $cp{'datelim'} ne '' ) {
		push(@lq, ("date=" . &fcts::forsafety($cp{'datelim'}) ));
	}

	# ページ移動リンクに恒常系設定を付加
	if( $cp{'order'} eq 'reverse' ) {
		# 逆順の場合：
		push(@lq, "order=reverse");
	}

	return @lq;
}

# ------------------
# クエリ文字列を作る	引数：クエリに追加する文字列の配列(※何もない場合でも空文字を1つは指定すること)
# ------------------	返値：クエリ文字列 (※何もない場合でも「?」が1つ返る)
sub makeQueryString
{
	my @queries = @_;
	my $ret = '';

	# 恒常付加パラメータの追加処理
	unshift(@queries, @constantParams);

	# 配列からクエリを生成
	foreach my $one (@queries) {
		# 1文字以上ある場合だけ追加
		if( $ret eq '' ) {
			# まだ何もなければ「?」から (※パラメータがない場合でも「?」は出力する必要がある)
			$ret .= '?' . $one;
		}
		else {
			# 既になにかあれば「&amp;」で連結
			if( $one ne '' ) {
				# 文字列がある場合のみ連結
				$ret .= '&amp;' . $one;
			}
		}
	}

	return $ret;
}

# クエリ文字列の中からスキンの指定だけを除外する
sub cutSkinFromQuery
{
	my $targetquery = shift @_ || '';
	$targetquery =~ s/skin=[\w\d\._-]+//g;		# スキン名に使える文字は、英数字＋3記号「._-」のみの前提。
	$targetquery =~ s/^\?&amp;/?/;				# 「?&amp;」という文字列が先頭にあれば「?」だけに修正する
	return $targetquery;
}

# クエリ文字列の中からスキンの指定だけを除外する（一時適用中のスキンを維持しないよう設定されている場合のみ）
sub cutSkinFromQueryIfOrder
{
	my $str = shift @_ || '';
	if( $setdat{'outputlinkkeepskin'} == 0 ) {
		# 一時適用中のスキンを維持しない場合
		return &cutSkinFromQuery($str);	# 上記の関数に渡して返す
	}
	# 一時適用中のスキンを維持するなら、何もせず返す
	return $str;
}


# -------------------------
# CGIプログラムの所在を返す		※恒常付加パラメータ付き	引数：さらに加えるパラメータ(先頭に?がある場合も可)
# -------------------------
sub getCgiPath
{
	my $plusquery = shift @_ || '';
	if( $plusquery =~ m/^\?(.+)/ ) {
		# 先頭が?記号ならそれ以降のみを使う
		$plusquery = $1;
	}

	return $cginame . &makeQueryString($plusquery);
}

# --------------------------------------
# 指定されたPostIDの投稿データだけを得る	引数：PostID
# --------------------------------------	返値：date, user, comment, cat, flags の配列	(※catはカンマ区切りCSVのままな点に注意)
sub getOnePost
{
	my $tid = shift @_ || &errormsg('getOnePost：PostIDの指定が必須');
	my ($date,$user,$comment,$cats,$flags) = '';

	# データを得て分解して既存情報を得る
	foreach my $oneclip (@xmldata) {
		my $id = &fcts::getcontent($oneclip,'id');
		# IDの一致を確認
		if( $tid != $id ) {
			# 違っていれば次を探す
			next;
		}
		else {
			# 一致したら他の情報を取得してループ終わり
			$date		= &fcts::getcontent($oneclip,'date');
			$user		= &fcts::getcontent($oneclip,'user');
			$cats		= &fcts::getcontent($oneclip,'cat');
			$flags		= &fcts::getcontent($oneclip,'flag');
			$comment	= &fcts::getcontent($oneclip,'comment');
			last;
		}
	}

	return ($date,$user,$comment,$cats,$flags);
}

# ----------------------------------------
# 指定されたPost番号の前後のPost番号を得る	引数：現在番号
# ----------------------------------------	返値：該当する投稿番号2つ「前→次」の配列（存在しない場合は 0 を返す） ※(0,0)が返る場合は、全1件以下しかデータがないか、または引数の番号が存在しない。
sub findNeighbours
{
	my $tryid = shift @_ || 0;

	my $bef = 0;	# 前の投稿番号
	my $aft = 0;	# 後の投稿番号

	# 全データをループ（新→旧の方向）
	my $pointflag = 0;
	foreach my $oneclip (@xmldata) {
		my $id = &fcts::getcontent($oneclip,'id');
		# フラグが立っていたら、そのIDを記録してループを終了
		if( $pointflag ) {
			$bef = $id;
			last;
		}
		# フラグが立っていない場合：IDの一致を確認
		if( $tryid != $id ) {
			# フラグが立っていなくて、IDが違っていれば一旦保持して次を探す
			$aft = $id;
			next;
		}
		else {
			# 一致したらフラグを立てて次を探す
			$pointflag = 1;
			next;
		}
	}

	if( $pointflag ) {
		# 該当があれば(フラグが立っていたら)変数を返す。
		return ($bef,$aft);
	}
	else {
		# 該当がなければ（※該当なしでも$aftには最後のidが入っているので、変数の中身は返さないようにする）
		return (0,0);
	}
}

# -------------------------------------
# SSI機能：指定されたファイルを挿入する		引数：ファイルパス
# -------------------------------------		返値：挿入されるデータ
sub serversideinclude
{
	my $filepath = shift @_ || '';
	my @data = ();

	# 無効判定
	if( $safessi == 9 ) {
		return '《INCLUDEは無効に設定されています。》';
	}

	# 禁止判定
	my $err = 0;
	if( $safessi != 1 ) {
		# 上位ディレクトリの参照やフルパスでの記述が禁止されている場合はそれらを判定
		if( index($filepath, '..') >= 0 ) {
			# 上位ディレクトリへの参照があった場合
			$err++;
		}
		elsif( index($filepath, '/') == 0 ) {
			# 先頭がスラッシュだった場合(＝フルパスでの記述)
			$err++;
		}
	}
	if( $err > 0 ) {
		# エラーがあれば
		return '《INCLUDEエラー》上位ディレクトリの参照やフルパスでの記述は、CGIの設定によって禁止されています。対象ファイルの置き場所を変更するか、またはCGIの設定を変更して下さい。';
	}

	# 対象ファイルの存在をチェックして読む
	if( open(SSIFILE, $filepath) ) {
		@data = <SSIFILE>;
		close SSIFILE;
	}
	else {
		return '《INCLUDEエラー》対象ファイルが読み込めませんでした。';
	}
	return join('',@data);
}

# --------------------
# デモ用ファイルの挿入
sub loaddemomsg
{
	my $tfc = shift @_ || '';
	my $tfn = 'demo-' . &fcts::forsafety($tfc) . '.html';
	my @data;

	if( open(DMF, $tfn) ) {
		@data = <DMF>;
		close DMF;
	}
	else {
		push(@data,'<!-- DEMO: NO FILE -->');
	}
	return join('',@data);
}

# ===========================
# ★EDIT MODE
# ===========================
sub modeEdit
{
	my $id = $cp{'postid'} || '';	# 注:ゼロではなく空文字をデフォルトにする (※これ、何のためだっけ？)

	# Cookieに事前入力文字列があれば、格納しておく (※ここでは読むだけで消さない。消すのは投稿処理が完了できてから。)	#$cgi->param('prewrite') || '';
	my $prewrite = $cgi->cookie(-name=>'logsnpt') || '';

	# 直接指定された文字列があるなら格納する (※メモ:最終的なフォームへの出力時点で安全化される)
	$prewrite .= shift @_ || '';

	# ------------
	# ログイン確認
	# ------------
	my $permittedid = &fcts::checkpermission();
	if( !$permittedid ) {
		# 権限を確認できない場合：パスワードチェック
		&passfront( &makeQueryString('mode=edit',"postid=$id") );
		exit;
	}

	# ユーザ名を得る
	my $loginname = &fcts::forsafety( &fcts::getUserDetail($permittedid,2) || '名前未設定');
	# 権限値を得る
	my $plv = &fcts::getUserDetail($permittedid,1) || 0;

	my $permitforedit = 1;

	# -----------------
	# 新規or編集 UI作成
	# -----------------
	my ( $date, $user, $comment, $cats, $flags, $username, $editperson ) = ('','','','','','');
	my $isNew;
	if(( $id eq '' ) || ( $id == 0 )) {		# 空文字 or 番号0 なら新規作成
		# ………………
		# 新規作成なら
		# ………………
		$isNew = 'NEW';
		if( $prewrite ne '' ) {
			# 事前入力文字列があれば入れる
			$prewrite =~ s/<br>/\r\n/g;		# 改行を展開
			$comment = $prewrite;
			$editperson .= qq|<p><strong class="important">注意：まだ投稿は完了していません。</strong>上記の内容を投稿しても良いなら「投稿する」ボタンを押して下さい。</p>|;
		}
		$id = '';	# 0の場合も空文字に修正しておく(v2.4.0+)
	}
	elsif( $id < 0 ) {
		# 0未満ならエラー
		&errormsg('投稿番号の指定が不正です。マイナスの番号は指定できません。');	# パラメータの事前チェックがあるので、この行は実行されないハズ。
	}
	else {
		# ………………………
		# 既存投稿の編集なら
		# ………………………
		&accesslevelcheck(3,$plv);	# 権限Lv.3未満なら編集権がない

		# データを得て分解して既存情報を得る
		($date,$user,$comment,$cats,$flags) = &getOnePost( $id );
		if( length($comment) == 0 ) { &showadminpage('NOT FOUND','','<p>投稿番号の指定が誤っています。指定された番号の投稿データはありませんでした。</p>','BA'); exit; }
		$username   = &fcts::forsafety( &fcts::getUserDetail($user,2) || '名前未設定');

		# 編集番号
		$isNew = &fcts::forsafety( "No.$id" );

		# 投稿から指定日数を超えたら再編集を禁止する設定の場合
		if( $setdat{'datelimitreedit'} == 1 ) {
			# 指定日数を超えているかどうかを確認
			my $pastday = $setdat{'datelimitreeditdays'} * 60 * 60 * 24;	# 日指定の数値を秒に変換する
			my $compare = &fcts::comparedatestr( &fcts::getdatetimestring(), $date );	# 現在時刻から投稿時刻を引く
			if(( $compare ne 'NA' ) && ( $compare > $pastday )) {
				# 存在しない日時ではなく、引き算の結果(秒)が指定日数(秒)を超えていたら編集拒否
				$editperson .= '※<b>現在の設定では</b>、投稿日時から ' . &fcts::forsafety($setdat{'datelimitreeditdays'}) . '日を超えている投稿は再編集できません。（この設定は、管理者のみが変更できます。）<br>※この投稿を<strong class="important">削除したい場合</strong>は、<a href="' . &makeQueryString('mode=admin','work=manage') . '">投稿の削除/編集</a>から選べば削除できます。（あなたに削除権限がある場合のみ。）';
				$permitforedit = 0;
			}
		}
	}

	# --------------------------
	# 元投稿者とログイン者の比較
	# --------------------------
	if( $permitforedit ) {
		if(( $permittedid eq $user ) || ( $id eq '' )) {
			# 元投稿者とログイン者が一致しているか、新規作成時だったら
			$editperson .= qq|<p class="loginNameGuide">※ただいま、$loginnameさん($permittedid)としてログインしています。</p>|;
		}
		else {
			# 別人の場合
			$editperson .= qq|<p class="loginNameGuide">※これは、<strong>$usernameさん($user)の投稿</strong>です。<br>|;
			if( $plv >= 7 ) {
				# 強制編集権限あり
				if( $setdat{'funcrestreedit'} == 1 ) {
					# (権限のあるIDでも)再編集が禁止されている場合
					$editperson .= '※現在の設定では、投稿者本人しか再編集できません。再編集するには投稿に使われたIDで<a href="' . &makeQueryString('mode=admin','work=logout') . '">ログインし直す</a>か、または設定を変更して下さい。<br>※この投稿を<strong class="important">削除したい場合</strong>は、<a href="' . &makeQueryString('mode=admin','work=manage') . '">投稿の削除/編集</a>から選べば削除できます。';
					$permitforedit = 0;
				}
				else {
					$editperson .= qq|※このまま編集すると、$loginnameさん($permittedid)の投稿に名義が変更されます。|;
				}
			}
			else {
				# 編集権限なし
				$editperson .= qq|※ただいま、$loginnameさん($permittedid)としてログインしているため、この投稿に対する編集権限がありません。|;
				$permitforedit = 0;
			}
			$editperson .= '</p>';
		}
	}

	# ------------------------------------
	# 編集権限があれば、編集フォームの作成
	# ------------------------------------
	my $msg;
	if( $permitforedit > 0 ) {
		$msg = &makepostform( $id, $user, $date, $comment, $cats, $flags, '' ) . $editperson;
		# UNIQUERANDを短いSYSに置き換える
		$msg =~ s/UNIQUERAND/SYS/g;
		# 削除ボタンの配置調整
		my $delbtnpos = '';
		if( $setdat{'sysdelbtnpos'} == 1 ) {
			# 右寄せ指定ならCSSを追加
			$delbtnpos = ' style="text-align:right;"';
		}
		# 新規作成でなければ、削除フォームも表示
		if( $id ne '' ) {
			my $cgipath = &getCgiPath();
			$msg .= qq|
			<form action="$cgipath" method="post"$delbtnpos>
				<input type="hidden" value="admin" name="mode">
				<input type="hidden" value="trydels" name="work">
				<input type="hidden" value="$id" name="postid">
				<input type="submit" value="この投稿を削除" class="btnlink deleteButton">
			</form>
			|;
		}
	}
	else {
		$msg = $editperson;
	}

	# ------------------------------------
	# edit.css と edit.js があれば読み込む
	# ------------------------------------
	my $editcss = '';
	my $editjs = '';
	if( $setdat{'loadeditcssjs'} == 1 ) {
		# 読み込む設定の場合だけ
		if( -f 'edit.css' ) {
			# edit.cssがあれば読み込む
			$editcss = '<link type="text/css" rel="stylesheet" href="edit.css">';
		}
		if( -f 'edit.js' ) {
			# edit.jsがあれば読み込む
			$editjs = '<script type="text/javascript" src="edit.js"></script>';
		}
	}

	# 編集フォーム用のCSS：
	my $cssform = q|
		/* ▼投稿画面 */
		.postform { margin:0 0 2em 0; padding:0; /* for Mobile */ }
		.postform p { margin:0; }
		textarea.tegalogpost { border:2px green solid; border-radius:0.67em; background-color:white; padding:0.5em; font-size:1rem; box-sizing:border-box; width:100%; height:8.6em; overflow-wrap:break-word; overflow:auto; margin-bottom:0.25em; }
		textarea.tegalogpost:placeholder-shown { color:#aaa; }
		textarea.tegalogpost:-ms-input-placeholder { color:#aaa; }
		.postbutton { background:green; color:white; font-size:1rem; border-radius:1em; padding:0.25em 0.75em; font-weight:bold; border:1px solid green; }
		.postbutton:hover { background-color:#00cc00; }
		.flagguide { display:inline-block; background-color:#888; color:white; line-height:1; padding:3px 0.34em; border-radius:3px; cursor:pointer; font-size:0.9em; margin-right:0.2em; float:left; }
		#draftsign { background-color:#55c; }
		@media all and (min-width:600px) {
			.postform { background-color:#eee; margin:0.5em 0 1em 0; padding:1em; }
		}
		@media all and (max-width:599px) {
			h1 { font-size:0.75em; padding:0.25em 0; }
			.adminhome a { font-size:0.4em; top:0.5px; }
			.postform { margin-bottom:1.25em; }
			.postform p { font-size:0.8em; }
			.postform ul { font-size:0.9em; }
			.postform p input { vertical-align: -2px; }
			.flagguide { float:right; margin:0 0 0 0.1em; }
			#main { margin:0.1em 0.75em 1em 0.75em; }
			.loginNameGuide { font-size:0.85em; margin:1em 0; line-height:1.2; }
		}
		/* ▼編集or新規 */
		.line-postid { list-style-type:none; margin:0; padding:0; }
		.line-postid li { display:inline-block; }
		.line-postid .trydelete { color:#aaa; }
		.line-postid :checked + label + label { color:black; }
		/* ▼システムボタン(削除ボタン) */
		.deleteButton { background-color:crimson; color:white; border-color:darkred; }
		.deleteButton:hover { background-color:#fda; color:crimson; border-color:crimson; }
		/* ▼装飾ボタン群 */
		.decoBtns { display:inline-block; margin-top:0.5em; }
		.decoBtns input { min-width:32px; min-height:28px; margin:1px; background-color:#eee; border:1px solid #aaa; cursor:pointer; border-radius:3px; font-size:14px; vertical-align:middle; }
		.decoBtns input:hover { background-color:#e5f1fb; border-color:#0078d7; }
		/* 太字  :B */ .decoBtnB { font-weight:bold; }
		/* 取消線:D */ .decoBtnD { text-decoration:line-through; text-decoration-color:red; text-decoration-style:double; }
		/* 強調  :E */ .decoBtnE { font-weight:bold; color:blue; }
		/* 斜体  :I */ .decoBtnI { font-style:italic; }
		/* 引用  :Q */ .decoBtnQ {  }
		/* 小さめ:S */ .decoBtnS {  }
		/* 極小  :T */ .decoBtnT { font-size:11px !important; }
		/* 下線  :U */ .decoBtnU { text-decoration:underline; text-decoration-color:red; }
		/* 文字色:C */ .decoBtnC { color:red; }
		/* 背景色:M */ .decoBtnM { color:blue; }
		@media all and (min-width:600px) {
			.decoBtns { margin-top:0; }
		}
		.catChecks { font-size:0.9em; padding-top: 0.5em; }
		.catChecks label { display:inline-block; cursor:pointer; margin:0 0.75em 0 0; }
		.catChecks label:hover { text-decoration:underline; }
		.catChecks input { min-width:0; min-height:0; margin-right:0.2em;  }
		/* ▼Themes */
		.themeKHA .postform { background-color:#f4f2eb; } .themeKHA .postbutton { background-color:#aaaa43; border-color:#e6d540; } .themeKHA .postbutton:hover { background-color:#858527; } .themeKHA textarea.tegalogpost { border-color:#e6d540; }
		.themeFGR .postform { background-color:#ecffd9; } .themeFGR textarea.tegalogpost { border-color:#62c400; }
		.themeSKR .postform { background-color:#feede6; } .themeSKR .postbutton { background-color:#f7a4b9; border-color:#f58ee8; } .themeSKR .postbutton:hover { background-color:#f2698e; } .themeSKR textarea.tegalogpost { border-color:#f7a4b9; }
		.themeBDU .postform { background-color:#d1dcf3; } .themeBDU .postbutton { background-color:#2e55af; border-color:#0e1a39; } .themeBDU .postbutton:hover { background-color:#877fac; } .themeBDU textarea.tegalogpost { border-color:#877fac; }
		.themeMKN .postform { background-color:#f7e1c0; } .themeMKN .postbutton { background-color:#ef6b04; border-color:#ef6b04; } .themeMKN .postbutton:hover { background-color:#fea239; } .themeMKN textarea.tegalogpost { border-color:#fea239; }
		.themeKRM .postform { background-color:#dddddd; } .themeKRM .postbutton { background-color:#000000; border-color:#000000; } .themeKRM .postbutton:hover { background-color:#555555; } .themeKRM textarea.tegalogpost { border-color:#555555; }
	|;
	my $css = '<style type="text/css">' . $cssform . "</style>" . $editcss . $editjs;

	&showadminpage("Edit $isNew Post",'',$msg,'CA',$css);
}


# ===========================
# ★WRITE MODE
# ===========================
sub modeWrite
{
	my $neworedit = '編集';		# 結果報告表示用

	# 不正送信の確認
	&fcts::postsecuritycheck('mode=write');

	# ------------------
	# データ受信内容確認
	# ------------------
	my $newid = $cgi->param('postid') || '';
	my $newdate = $cgi->param('datetime') || '';
	my $newcomment = $cgi->param('comment') || '';
	my @newcats = $cgi->param('category');		# ※ここではmulti_paramを使いたいのだが、古い環境では使えないので、今のところは保留。
	my @newflags = $cgi->param('flag');			# ※同上

	# Functions:
	my $fixed = $cgi->param('fixed') || 0;

	# フラグ群
	my $draftflag = 0;	# 下書きフラグ
	my $rearflag = 0;	# 下げるフラグ
	foreach my $oneflag (@newflags) {
		if( $oneflag eq 'draft' ) {
			# 下書きならフラグを立てる
			$draftflag = 1;
		}
		elsif( $oneflag eq 'rear' ) {
			# 下げるならフラグを立てる
			$rearflag = 1;
		}
	}

	# 指定日付を無視して現在日時を記録する (※仕様変更：新規の場合に問答無用で現在日時を登録する仕様は廃止。1.4.1)
	if( 
		$newdate eq ''		# 日付情報がない場合
		||
		(($newid eq '') && ($setdat{'showFreeDateBtn'} == 0))	# 新規投稿で、かつ、日付の自由入力ボタンが非表示の場合 (※JavaScriptがOFFだと旧投稿の日付が入っている場合があるため)
		||
		(
			($setdat{'allowillegaldate'} == 0)		# 存在しない日付を許容しない設定の場合で、
			&&
			(&fcts::datevalidation($newdate) == 0)	# 存在しない日時が指定されている場合(※存在する場合に1が返ってくる)
		)
	) {
		$newdate = &fcts::getdatetimestring();		# 現在日時を使う
	}

	# ----------------------
	# ログイン確認・権限取得
	# ----------------------
	my $permittedid = &fcts::checkpermission();		# ログイン中ユーザのID名が得られる
	if( !$permittedid ) {
		# ユーザIDを確認できない場合はログイン画面へ送る

		# 改行を変換しておく
		$newcomment =~ s/\r\n/<br>/g;
		$newcomment =~ s/\n/<br>/g;

		# ログインフォームへ送る前に、書きかけの内容をCookieに入れておく。
		if( length($newcomment) > 0 ) {
			# 1文字以上あれば(セッションはブラウザを終了するまで)
			my $spcookie = $cgi->cookie(-name =>'logsnpt', -value => $newcomment , -expires => "+1d" );
			# 出力
			print "Set-Cookie: $spcookie\n";
		}

		# ログインフォームへ送る
		&passfront( &makeQueryString('mode=edit') );	# パラメータではなくCookieで渡すように仕様変更。改行やハッシュタグが入らないため。 ,"prewrite=$newcomment"
		exit;
	}
	my $plv = &fcts::getUserDetail($permittedid, 1);	# ログイン中ユーザの権限値

	# 画像投稿があるかどうか
	my @imgfile = $cgi->param('upload_file') || '';
	if( $imgfile[0] ne '' ) {
		# 画像投稿があればアップロード処理
		my @rets = &modeImageup(1);

		# 画像表示タグを作る
		my $picttags = '';
		foreach my $ret (@rets) {
			if( $picttags ne '' ) {
				# 既に何かあれば半角空白を加える
				$picttags .= ' ';
			}
			if( $ret eq 'OVER' )	{ $picttags .= '[画像UPエラー:容量制限を超過]'; }
			elsif( $ret eq 'OUTEXT' )	{ $picttags .= '[画像UPエラー:許可形式外]'; }
			else {
				$picttags .= '[PICT:' . $ret . ']';
			}
		}

		# 1つ以上のPICTタグが生成できれば出力
		if( $picttags ne '' ) {
			# 挿入用文字列を生成して、コメントに追加
			my $imgbr = '';
			# コメントが1文字以上ある場合で、画像の前後に改行を加える設定なら加える
			if(( $newcomment ne '' ) && (( $setdat{'imagedefaultplace'} == 1 ) || ( $setdat{'imagedefaultplace'} == 3 ))) {
				$imgbr = "\n";
			}
			# 画像をコメントの前か後に挿入する
			if(( $setdat{'imagedefaultplace'} == 0 ) || ( $setdat{'imagedefaultplace'} == 1 )) {
				# 前に追加
				$newcomment = $picttags . $imgbr . $newcomment;
			}
			else {
				# 後に追加
				$newcomment .= $imgbr . $picttags;
			}
		}
	}

	# --------------------
	# 編集の場合の権限確認	（※これより前のI/Fで確認してリクエストを拒否しておくべき。自作フォーム等から投稿された場合の対策）
	if(( $newid ne '' ) && ( $plv < 7 )) {
		# 編集の場合で権限Lv.7未満なら確認
		&checkeditpermission( $newid, $permittedid, $plv);
	}

	# ------------------------------
	# データを追加すべきかどうか確認
	my $existnewdata = 1;
	if( $newcomment eq '' ) {
		# コメントがなければ追加の必要なし
		$existnewdata = 0;
	}

	my @editxmldata = ();

	# ------------------
	# 削除すべきIDを得る
	my @ids = $cgi->param('trydelete');		# 削除候補として指定されたID群		※ここではmulti_paramを使いたいのだが、古い環境では使えないので、今のところは保留。
	my $eid = -1;							# 編集対象として指定するID(単一)
	if( $newid ne "" ) {
		# ID名が指定されていれば「編集」なので元データは削除する
		# 編集した投稿を先頭に移動しないので、元データの位置は挿入位置として扱う
		$eid = $newid;
	}

	# --------------------
	# 削除の場合の権限確認
	if(( $#ids >= 0 ) && ( $plv < 7 )) {
		# 削除対象が存在して、権限Lv.7未満なら確認
		foreach my $oi (@ids) {
			&checkeditpermission( $oi, $permittedid, $plv);
		}
	}

	# ------------------
	# 新ツリーの作成
	my $loopxd = -1;		# ループカウンタ
	my $insertline = -1;	# 挿入位置保持用
	foreach my $oneclip (@xmldata) {
		$loopxd++;
		my $oneid = &fcts::getcontent($oneclip,'id');
		my $notdel = 1;
		# IDの一致を確認(削除対象)
		foreach my $trydel (@ids) {
			if( $flagDebug{'ShowDebugStrings'} == 1 ) { print STDERR "[Check] try:$trydel - chedkedid:$oneid<br>\n"; }
			if( $trydel == $oneid ) {
				# 一致したら削除対象なので削除(＝新ツリーにデータを追加しない)フラグ
				$notdel = 0;
				if( $flagDebug{'ShowDebugStrings'} == 1 ) { print STDERR qq|delete No.$oneid<br>|; }
			}
		}
		# IDの一致を確認(編集対象)
		if( $eid == $oneid ) {
			# 元データの代わりに挿入位置判別用のダミーデータを入れておく
			push(@editxmldata , "_INSERT_EDITED_CLIP_HERE_" );
			# その位置(挿入位置)を記憶しておく
			$insertline = $loopxd;
			# 元データは追加しない(削除)フラグ
			$notdel = 0;
		}

		# 一致しなかったら(削除対象でなければ)そのまま新ツリーにデータを追加
		if( $notdel == 1 ) {
			push(@editxmldata , $oneclip );
			if( $flagDebug{'ShowDebugStrings'} == 1 ) { print STDERR qq|copy No.$oneid<br>|; }
		}
	}

	# ----------------------------
	# 新規作成の場合：ID番号の生成
	if( $newid eq "" ) {
		my $maxid = 0;
		foreach my $oneclip (@xmldata) {
			if( &fcts::getcontent($oneclip,'id') > $maxid ) {
				$maxid = &fcts::getcontent($oneclip,'id');
			}
		}
		$newid = $maxid + 1;	# 新規エントリのID番号
		$neworedit = '新規投稿';	# 結果報告表示用
	}

	# ----------
	# データ追加
	if( $existnewdata == 1 ) {
		# 事前処理：comment要素の終了タグが書かれている場合にだけは強制エスケープする(※記録用XMLの都合で必須)
		$newcomment =~ s|</comment|&lt;/comment|g;
		# 新規データXMLの作成 ※全要素は空でも記録する(本文中のタグ文字列を誤読しないように)。
		my $newxmlline = &fcts::makerecord( 'log',
			&fcts::makeelement('date'	,	$newdate	) ,	# 記録時にエスケープはしない
			&fcts::makeelement('id'	,		$newid		) ,	
			&fcts::makeelement('user' ,		$permittedid) ,	
			&fcts::makeelement('cat' ,		join(',',@newcats)) ,	# カテゴリIDは(複数あれば)カンマ区切りで記録
			&fcts::makeelement('flag' ,		join(',',@newflags)) ,	# フラグ群は(複数あれば)カンマ区切りで記録
			&fcts::makeelement('comment',	$newcomment	)	
		);
		# データを追加
		if( $insertline >= 0 ) {
			# 編集した投稿を元の位置に挿入する（挿入位置が保持されている場合）
			$editxmldata[$insertline] =~ s/_INSERT_EDITED_CLIP_HERE_/$newxmlline/;
		}
		else {
			# 投稿を先頭に挿入する（新規投稿など挿入位置を保持していない場合）
			unshift(@editxmldata , $newxmlline);
		}
	}

	# ------------------
	# まずはバックアップ
	if( $setdat{'autobackup'} == 1 ) {
		# 自動バックアップが有効の場合のみ
		if ( &autoBackup() == 1 ) {
			# バックアップが実行できた場合は、保持日数超過分を調べて消す
			&listupBackupfiles();
		}
	}

	# ---------------------
	# データXMLファイル保存
	if( &fcts::XMLout( $bmsdata, 'tegalog', $charcode, @editxmldata ) == 0 ) {
		# 書けなかった場合
		&errormsg('データファイルへの書き込みが失敗しました。直前の操作内容は反映されていません。<br>ファイルに書き込み権限が設定されているか、ディスク容量に残量があるかなどを確認して下さい。');
	}

	# ---
	# Cookieに事前入力文字列があれば(使い終わったので)削除する
	my $prewrited = $cgi->cookie(-name=>'logsnpt') || '';
	if( length($prewrited) > 0 ) {
		# 事前文字列があった場合は、Cookieを削除する
		my $spcookie = $cgi->cookie(-name =>'logsnpt', -value => '', -expires => "-1h" );
		# 出力
		print "Set-Cookie: $spcookie\n";
	}

	# ------------------------
	# データファイルを読み直す
	@xmldata = &fcts::XMLin($bmsdata,'log');

	# --------------------------
	# 先頭固定をどうにかする処理 (※投稿を削除した場合の処理は後で)
	my $resfixed = '';
	if( $plv >= 9 ) {
		# 管理者権限がある場合のみ
		my $nowfixed = &isfixed( $newid );	# いま投稿した番号が固定されているかどうかを調べる(1=固定中/0=非固定)
		if(( $fixed == 1 ) && ( $nowfixed == 0 )) {
			# 固定するよう指定されていて、まだ固定されていないなら、固定リストに追加登録する
			&adddelfixedids( 1, $newid );
			$resfixed = '先頭に固定しました。';
		}
		elsif(( $fixed == 0 ) && ( $nowfixed == 1 )) {
			# 固定しないよう指定されていて、固定リストに載っているなら、固定リストから削除する
			&adddelfixedids( -1, $newid );
			$resfixed = '先頭固定を解除しました。';
		}
		else {
			# 固定するよう指定されていても、既に固定されている場合
			# 固定しないよう指定されていても、固定リストに載っていない場合
			# →何もしない
		}
	}

	# --------
	# 終了表示
	my $msg;
	if( $existnewdata == 1 ) {
		# 追加・編集の場合：
		$msg = qq|
			<p>No.$newid の投稿を $neworedit しました。</p>
			<ul>
				<li><a href="?postid=$newid">No.$newid の投稿だけを表示</a></li>
				<li><a href="?mode=edit&amp;postid=$newid">No.$newid の投稿を再度編集</a></li>
			</ul>
			
		|;

		# 下げる場合の後処理
		if( $rearflag ) {
			# 下げるフラグが立っていたら
			my $allrears = &makeQueryString('mode=admin','work=manage','q=rear');
			$msg = qq|
				<p>No.$newid の投稿を <b>下げる(一覧外)</b> として保存しました。</p>
				<ul>
					<li><a href="?postid=$newid">No.$newid の投稿を表示する</a><small>（誰でも閲覧できます）</small></li>
					<li><a href="?mode=edit&amp;postid=$newid">No.$newid の投稿を再度編集</a></li>
					<li><a href="$allrears">下げられているすべての投稿を一覧</a></li>
				</ul>
			|;
		}

		# 下書きの場合の後処理 (※下げる場合の後処理があっても無視して、下書き用の後処理だけを表示する)
		if( $draftflag ) {
			# 下書きフラグが立っていたら
			my $alldrafts = &makeQueryString('mode=admin','work=manage','q=draft');
			$msg = qq|
				<p>No.$newid の投稿を <b>下書き(非公開)</b> として保存しました。</p>
				<ul>
					<li><a href="?postid=$newid">No.$newid の投稿をプレビュー表示する</a><small>（あなただけが閲覧できます）</small></li>
					<li><a href="?mode=edit&amp;postid=$newid">No.$newid の投稿を再度編集</a></li>
					<li><a href="$alldrafts">すべての下書き投稿を一覧</a></li>
				</ul>
			|;
		}
	}
	else {
		if( defined($ids[0]) ) {
			# 削除の場合：（編集でも削除処理はあるけどその場合は表示しない。紛らわしいから。）
			$msg = qq|
				<p>以下の投稿を削除しました。</p>
				<table class="managetable" cellpadding="0"><tr><th>No.</th></tr>\n
			|;
			foreach my $onedelid ( @ids ) {
				$msg .= qq|<tr><td>No.$onedelid</td></tr>|;
			}
			$msg .= qq|</table>\n|;
		}
		else {
			# 追加も削除もしていない場合：（※何も書かずに投稿ボタンを押した場合や、CGIのパラメータを手動で入力した場合などに実行される可能性がある。）
			$msg = qq|<p>処理内容がありません。データファイルをリフレッシュしました。</p>|;
		}
	}

	# --------------
	# 再カウント処理
	if( $existnewdata == 1 || defined($ids[0]) ) {
		$msg .= '<div style="margin-top:2em; color:gray;"><p style="margin:0;">付随処理：</p><ul style="font-size:0.8em; margin-top:0;">';
		# ▼年月再集計
		&datadatecounter();
		$msg .= '<li>年月別該当個数を再集計しました。</li>';
		# ▼新着リストの再生成
		&updatelatestlist( $setdat{'latestlistup'} , $setdat{'latestlistparts'} , $setdat{'latesttitlecut'} );
		$msg .= '<li>新着リストを再生成しました。</li>';
		# ▼カテゴリ再集計 (カテゴリが選択されていた場合 または 投稿削除の場合)
		if( $#newcats >= 0 || defined($ids[0]) ) {
			&categorycounter();
			$msg .= '<li>カテゴリ選択数を再集計しました。</li>';
		}
		# ▼ハッシュタグのリフレッシュが必要っぽければ実施する（ハッシュタグとしては成立していない「#」記号がある場合にも実行されるが、まあ実害はないだろう。^^;）
		if( $newcomment =~ m/#/ || defined($ids[0]) ) {
			# ハッシュタグの再カウントを直接実行
			my $retdc = &datahashcounter();
			$msg .= '<li>ハッシュタグの該当個数を再集計しました。</li>';
		}
		# ▼先頭固定状況をいじった場合
		if( $resfixed ne '' ) {
			$msg .= '<li>' . $resfixed . '</li>';
		}
		$msg .= '</ul></div>';
	}

	if( $flagDebug{'ShowDebugStrings'} == 1 ) {
		print STDERR qq|<hr><p>[$newid]</p><p>$newcomment</p><p>$newdate</p><hr>\n|;
	}

	# --------------------------------
	# 先頭固定投稿を削除した場合の処理
	if(( defined($ids[0]) ) && ( $setdat{'fixedpostids'} ne '' )) {
		# 削除処理がなされていて、かつ、先頭固定設定がある場合のみ処理する

		# 先頭固定対象IDをリストアップ
		my @topnums = split(/,/,$setdat{'fixedpostids'});	# 先頭固定する投稿番号の配列を作る
		my @deltopnums = ();								# 削除する先頭固定番号の記録用

		# 削除対象が先頭固定かどうかを調べる
		foreach my $onedelid ( @ids ) {
			# もし先頭固定だったら、その固定設定を削除する
			foreach my $trytopid (@topnums) {
				if( $trytopid eq $onedelid ) {	# 番号は数値だが念のために文字として比較しておく
					# もし先頭固定対象だったら、その固定設定を削除リストに加える
					push(@deltopnums,$onedelid);
				}
			}
		}

		# 削除すべき先頭固定番号があれば削除する
		if( defined($deltopnums[0]) ) {
			# 先頭固定番号の削除専用関数を呼ぶ
			&adddelfixedids( -1 , @deltopnums );
			# 報告もする
			$msg .= '<div style="color:gray;"><p>先頭固定に指定されている投稿番号リストから ' . join('、', @deltopnums) . ' を除外しました。</p></div>';
		}
	}

	# 結果を表示せずにHOMEページに戻る(追加/編集の場合でそう設定されている場合のみ／下書きフラグ・下げるフラグが立っていない場合に限る)
	if( $existnewdata == 1 && $draftflag == 0 && $rearflag == 0 && ($setdat{'afterpost'} == 0 || $setdat{'afterpost'} == 2) ) {
		# HOMEへリダイレクト（キャッシュが表示されないよう現在時刻をクエリ文字列を加える）
		my $uq = time;	# &fcts::uniquerand();
		if($neworedit eq '編集' && $setdat{'afterpost'} == 0) { $uq = "postid=$newid&$uq"; }	# 編集後にはその単独ページに戻る設定の場合にだけ判定して移動
		my $cgipath = &getCgiPath($uq);
		print "Location: $cgipath\n\n\n";
		exit;
	}

	# 下書きの場合にNoticeを表示
	if( $draftflag ) {
		$msg .= qq|
			<p class="noticebox"><b>---【下書き編集のヒント】---</b><br>
			※この投稿 No.$newid は、<strong class="important">下書き設定を解除して保存し直すまで、ページ上には表示されません</strong>。ただし、投稿者のIDでログインされている場合はプレビュー表示できます。<br>
			※<strong class="order o1">順番そのまま:</strong>下書き設定を解除してから再投稿すれば、No.$newid の投稿位置に表示されます。（No.$newid より新しい投稿が存在する場合でも、No.$newid の掲載位置は変化しません。）<br>
			※<strong class="order o2">順番繰り上げ:</strong>下書き設定を解除すると同時に（編集画面の上部にある）<strong class="important">[新規に投稿]ラジオボタンを選択した上で、[元投稿を削除]にチェックを入れて</strong>から再投稿すれば、その瞬間の時刻を投稿日時にした<strong class="important">「最新投稿」として先頭に掲載</strong>できます。（この場合は投稿番号が再採番されるため、No.$newid より新しい投稿が存在する場合でも、先頭に表示されます。）<br>
			※詳しい操作方法は、公式マニュアルの<a href="$aif{'puburl'}usage/#howtouse-draft">下書き(非公開)保存機能の使い方</a>や<a href="$aif{'puburl'}usage/#howtouse-draft-publish">下書き状態を解除して公開する方法</a>をご覧下さい。</p>
		|;
	}
	else {
		# 下書き以外の場合
		if( $rearflag ) {
			# 下げる場合にNoticeを表示
			$msg .= qq|
				<p class="noticebox">
				※この投稿 No.$newid は、通常の一覧表示時など<strong class="important">「表示対象が何も限定されていない状況」では表示されません</strong>。しかし、この投稿を単独で閲覧すれば表示されます。<br>
				※表示対象が限定されている状況（ハッシュタグ限定表示、カテゴリ限定表示、全文検索時など）で表示されるかどうかは設定次第です。（設定は、管理画面の[設定]→[ページ設定]→[下げた投稿の表示]でできます。）<br>
				※詳しい操作方法は、公式マニュアルの<a href="$aif{'puburl'}usage/#howtouse-rear">下げる(一覧外)機能の使い方</a>もご覧下さい。</p>
			|;
		}
	}

	# CSS
	my $css = q|<style type="text/css">.order { color:white; padding:0 0.25em; border-radius:3px; margin-right:3px; display:inline-block; line-height:1.2; } .o2 { background-color:#4169e1; } .o1 { background-color:#e16941; }</style>|;

	# 結果を表示
	&showadminpage('EDITING COMPLETED','',$msg,'CA',$css);
}

# -----------------------------
# 先頭固定番号を設定へ追加/削除		引数1：1=追加／-1:削除、引数2以降：削除する先頭固定番号(リスト)
# -----------------------------
sub adddelfixedids
{
	my $type = shift @_ || 0;

	if( $type == 1 ) {
		# 追加の場合
		# 引数に指定された番号をカンマ区切りでリスト化
		my $adds = join(',', @_ );
		# それを先頭固定番号リストの先頭に追加
		$setdat{'fixedpostids'} = $adds . ',' . $setdat{'fixedpostids'};
	}
	elsif( $type == -1 ) {
		# 削除の場合
		# 引数に指定された番号を、先頭固定番号リストから探し出して削除
		foreach my $tryid ( @_ ) {
			$setdat{'fixedpostids'} =~ s/$tryid//g;		# 番号を削除
		}
	}

	# 調整
	$setdat{'fixedpostids'} =~ s/,{2,}/,/g;		# カンマ記号の連続を解消
	$setdat{'fixedpostids'} =~ s/^,//g;			# 先頭の単独カンマ記号を削除
	$setdat{'fixedpostids'} =~ s/,0?$//g;		# 最後の単独カンマ記号を削除	最後に0が付加されてしまう謎現象の対策も兼ねる(再現条件が分からんが全部消したときに0だけ記録されることがある)

	# 保存
	my @trywrites;
	push(@trywrites,"fixedpostids=$setdat{'fixedpostids'}");

	# 保存処理へ渡す
	&savesettings( @trywrites );
}

# --------------------------------------------------
# 指定番号の投稿が先頭に固定されているかどうかを判定	引数：調べたい投稿番号、返値：1=固定中、0=非固定
# --------------------------------------------------
sub isfixed
{
	my $tryid = shift @_ || 0;

	# 先頭固定リストを配列に分解
	my @nowfixes = split(/,/, $setdat{'fixedpostids'});
	foreach my $onefixnum ( @nowfixes ) {
		if( $onefixnum == $tryid ) {
			# あったら固定中なので1を返す
			return 1;
		}
	}

	# なかったら固定されていないので0を返す
	return 0;
}

# -------------------------
# 編集/削除の場合の権限確認		引数1：対象投稿ID、引数2：ユーザID、引数3：ユーザ権限
# -------------------------
sub checkeditpermission
{
	my $tid = shift @_ || die('checkeditpermission:引数が不足');
	my $permittedid = shift @_ || 0;
	my $plv = shift @_ || 9;

	# 権限Lv.3未満なら編集権がない
	&accesslevelcheck(3,$plv);
	# 権限Lv.7未満なら「自分の投稿」のみ編集可能
	if( $plv < 7 ) {
		# 編集/削除しようとしている投稿の所有者を確認して比較
		my ($orgdate,$orguser,$orgcomment,$orgcats) = &getOnePost( $tid );
		if( $permittedid ne $orguser ) {
			# 投稿の所有者とログイン者が異なる場合はエラー
			&showadminpage('NO PERMISSION','','この投稿を編集または削除する権限がありません。','BA');
			exit;
		}
	}
	# 権限Lv.7以上なら無条件で編集可能
	return;
}

# --------------------
# 自動バックアップ処理		引数：なし	返値：1=成功,0=失敗
# --------------------
sub autoBackup
{
	my $ret = 0;

	my $bupcopyfn = &getAutoBackupFilePath();	# バックアップ用ファイル名を得る
	if( $bupcopyfn ne '' ) {
		# 得られればバックアップ ※この時点の @xmldata の中身(＝1ステップ前の状態)で保存する
		$ret = &fcts::XMLout( $bupcopyfn, 'tegalog', $charcode, @xmldata );
	}

	return $ret;
}


# ===========================
# ★LICENCE MODE
# ===========================
sub modeLicence
{
	my $msg = '<p>ライセンス';
	if( $setdat{'licencecode'} eq '' ) { $msg .= 'されていません。フリー版として使用中です。</p>'; }
	elsif( &fcts::lcc($setdat{'licencecode'}) != 1 ) { $msg .= 'IDに誤りがあります。正しいライセンスIDとして認識されていません。</p>'; }
	else {	$msg .= 'ID [ <code>' . &fcts::forsafety($setdat{'licencecode'}) . '</code> ] で動作しています。</p>' . qq|<p>このIDの正当性は、<a href="$aif{'puburl'}../licence/check/?licence=| . &fcts::forsafety($setdat{'licencecode'}) . q|">公式サイトのライセンス判定ページ</a>でご確認下さい。</p>|;	}

	# META DATA:
	my @fs = stat $bmsdata;
	my $lastup = &fcts::getdatetimestring( $fs[9] ); # 更新時刻

	# 自己登録型公式ユーザリンク集に登録する際の事前自動取得用データ(※このページで使うかどうかは未定)
	my %meta = (
		VERSION => $versionnum,
		LASTUPDATE => $lastup,
		TOTALDATA => $#xmldata + 1,
		LICENCECODE => $setdat{'licencecode'},
		WEBTITLE => $setdat{'freetitlemain'},
		WEBDESCRIPTION => $setdat{'freedescription'}
	);

	# 連想配列%metaの中身をキーでソートした上で出力形式に整形して書き出す
	my $metainfo = '<!-- META: ';
	for my $name (sort keys %meta) {
		$name =~ s/\[|\]/-/g;	# 角括弧はハイフンに置き換える
		$metainfo .= '[' . $name . ']' . &fcts::forsafety( $meta{$name} ) . '[/' . $name . ']';
	}
	$metainfo .= ' :META -->';

	my $css = q|<style type="text/css">code { color: darkblue; font-family:'Courier New',monospace; }</style>| . $metainfo;
	&showadminpage('LICENCE','',$msg,'CA',$css);
}

# ===========================
# ★IMAGEUPLOAD MODE
# ===========================	※第1引数 0:単独実行(結果はその場で表示)／1:本文投稿と同時(ファイル名を返す)
sub modeImageup
{
	my $modewith = shift @_ || 0;
	my $msg = '';

	# ----------------------
	# ログイン確認・権限取得
	# ----------------------
	my $permittedid = &fcts::checkpermission();		# ログイン中ユーザのID名が得られる
	if( !$permittedid ) {
		# ユーザIDを確認できない場合はログイン画面へ送る
		&passfront( &makeQueryString('mode=admin') );
		exit;
	}
	my $plv = &fcts::getUserDetail($permittedid, 1);	# ログイン中ユーザの権限値

	# --------
	# 権限確認
	# --------
	if(( $setdat{'imageupallow'} == 0 ) || ( $plv < $setdat{'imageuprequirelevel'} )) {
		# 画像投稿が禁止されているか、または画像UPに必要な権限がなければ拒否
		$msg = '<p class="important"><strong>アップロードできません</strong></p><p>画像の投稿に必要な権限がないか、または画像の投稿が設定で禁止されています。</p>';
		&showadminpage('NO PERMISSION','',$msg,'CIA','');
		exit;
	}

	my $form = new CGI;
	my @tryfilenames = $form->param('upload_file');
#	binmode STDOUT;

	# ファイルの転送のチェック
	my $error;
	if (!@tryfilenames and $error = $form->cgi_error){			# definedを使うのをやめた(v2.4.0+)
		&errormsg("ファイルが転送できませんでした：$error");
		exit;
	}

	# ----------------------
	# 画像ファイル転送ループ
	# ----------------------
	my $loopcount = 0;
	my @ret = ();

	foreach my $filename (@tryfilenames) {

		# 拡張子
		my $fileext = '';

		# 許可拡張子のチェック
		if( $filename eq '' ) {
			# ………………………………………
			# ▼ファイル名が空なら何もしない
			# ………………………………………
			last;
		}
		elsif( $filename !~ m/\.($setdat{'imageallowext'})$/i ) {
			# ……………………………
			# ▼許可拡張子でなければ
			# ……………………………
			$msg .= '<li class="important "><b>エラー：</b>アップロードを許可されていない形式のファイルが送信されました。送信されたデータは保存されませんでした。</li>';
			push(@ret,'OUTEXT');
		}
		else {
			# ……………………………
			# ▼許可された拡張子なら
			# ……………………………
			my $imagename = '';		# 保存用ファイル名格納用(※PATHではない)
			my $newfilepath = '';	# 保存用ファイルパスの格納用

			# 拡張子だけを抜き出す処理(小文字にする)
			$fileext = lc($1);

			# ‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥
			# 元のファイル名をできるだけ維持する設定なら
			if(( $setdat{'imageupsamename'} == 1 ) && ( $filename =~ m/([A-Za-z0-9._]+)\.(.+)$/ )) {
				# ファイル名が[英数字・ドット・アンダーバー]だけで構成されていれば
				$imagename = $1 . '.' . $fileext;					# ファイル名は一旦そのまま保持(拡張子は小文字に変換されたもの)
				$newfilepath = $imagefolder . '/' . $imagename;		# ファイルパスを作って保持

				# 既に同名のファイルが存在した場合は番号を付けて別名にする
				my $i = 0;
				while( -f "$newfilepath" ){
					$i++;
					$imagename = $1 . $i . '.' . $fileext;			# ファイル名の末尾に連番を加える
					$newfilepath = $imagefolder . '/' . $imagename;	# ファイルパスも更新
					if( $i > 10000 ) { &errormsg("画像保存用のファイル名を作成できませんでした。"); exit; }	# 無限ループを防ぐ安全処理
				}
			}

			# ‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥‥
			# 元のファイル名を維持しない設定か、またはファイル名が決まらなかったなら
			if( $imagename eq '' ) {

				# ファイル名に使うための日時表記文字列を生成する処理 (ファイル名決定のループの外に作っておく)
				my $timestamp = &fcts::getNowDateForFileName(1);

				# 保存用ファイル名の作成 (＝保存先フォルダ名/日時表記-ユーザID.拡張子)
				$imagename = $timestamp . '-' . $permittedid . '.' . $fileext;		# ファイル名だけを保持
				$newfilepath = $imagefolder . '/' . $imagename;					# ファイルパスを作って保持

				# 既に同名のファイルが存在した場合は番号を付けて別名にする
				my $i = 0;
				while( -f "$newfilepath" ){
					$i++;
					$imagename = $timestamp . $i  . '-' . $permittedid . '.' . $fileext;	# ファイル名を更新
					$newfilepath = $imagefolder . '/' . $imagename;							# ファイルパスも更新
					if( $i > 10000 ) { &errormsg("画像保存用のファイル名を作成できませんでした。"); exit; }	# 無限ループを防ぐ安全処理
				}

			}

			# ‥‥‥‥‥‥‥‥‥‥‥‥‥‥
			# ファイルの保存(アップロード)
			# ‥‥‥‥‥‥‥‥‥‥‥‥‥‥
			unless( open (OUTFILE,'>',"$newfilepath") ){
				&errormsg("サーバに画像ファイルを保存できませんでした。CGIの設定を見直すか、出力先ディレクトリの書き込み権限や空き容量を確認して下さい。(※画像保存用ディレクトリを作成していない状態で画像を投稿しようとした際にもこのエラーが表示されます。)<br>→エラー詳細: [ $! ]\n");
				exit;
			}

			binmode (OUTFILE);	# 改行コードの自動変換を停止
			my $fsize = 0;
			my $buffer;
			while(read($filename,$buffer,1024)) {
				print OUTFILE $buffer;
				$fsize += 1024;
			}
			close (OUTFILE);
			close ($filename);	#ファイルハンドルをclose

			# サイズオーバーならファイルを消してエラーを表示する
			if(( $setdat{'imagemaxlimits'} == 1 ) && ( $setdat{'imagemaxbytes'} < $fsize )) {
				# 投稿上限が設定されていて、かつ、オーバーしているなら消す
				unlink($newfilepath);
				$msg .= '<li class="important">【画像アップロードエラー】送信されたファイルは、許容サイズを超えています。アップロードは拒否されました。現在の設定では、1ファイルあたりの最大サイズは <b>' . &fcts::byteswithunit($setdat{'imagemaxbytes'}) . '</b> に制限されています。</li>';
				push(@ret,'OVER');
			}
			else {
				# サイズ内なら完了報告
				$loopcount++;
				$msg .= '<li><span class="sizeinfo"><a href="#tr' . &fcts::forsafety($imagename) . '">約 ' . &fcts::byteswithunit($fsize) . 'の画像</a>をアップロードしました。</span> <!-- ' . $imagename . ' --></li>';
				push(@ret,$imagename);
			}
		}
	}

	if( $loopcount == 0 ) {
		# ファイルが転送されていない場合
		if( $msg ne '' ) {
			# 何らかのエラーが既に報告されている場合は整形する
			$msg = qq|<p class="msgtitle">【画像アップロードエラー】</p><ul>$msg</ul><p>何もアップロードされませんでした。</p>\n|;
		}
		else {
			$msg .= '<p>アップロードするファイルが指定されていません。</p>';
		}
	}
	else {
		$msg = '<p class="msgtitle">【画像アップロード完了】</p><ol>' . $msg . '</ol><p class="msgsum">計' . $loopcount . '個の画像をアップロードしました。</p>';

		# 画像拡大用のjQuery＋Lightboxの読み込み
		$msg .= &outputLightboxLoader(1,1);
	}

	# 呼び出し元に応じて結果をどうするか変える
	if( $modewith <= 0 ) {
		# 結果報告付きの画像管理画面を表示する
		&adminImages($msg, $loopcount);
	}
	else {
		# エラーがない場合はUPしたファイル名リストを返す
		return @ret;
	}
}


# ===========================
# ★ADMIN MODE
# ===========================
sub modeAdmin
{
	# データ受信内容確認
	my $awn = $cgi->param('work') || "";

	# 認証チェック前に実行する処理群：
	if( $awn eq 'logout' ) {
		# ログアウト処理
		print &fcts::logout();	# Cookieを破棄する文字列を出力
		my $msg = '<p>ログアウトしました。 - <a href="' . &makeQueryString('mode=admin') . '">再ログイン</a></p>';
		&showadminpage('LOGOUT','',$msg,'C');
		exit;
	}

	# アクセス権限の確認
	my $permittedid = &fcts::checkpermission();
	if( !$permittedid ) {
		# 権限を確認できない場合：パスワードチェック
		if( $awn eq '' ) {
			&passfront( &makeQueryString('mode=admin') );
		}
		elsif( ( $awn eq 'setting' ) && ( $cp{'page'} ne '' ) ) {
			&passfront( &makeQueryString('mode=admin','work=setting',"page=$cp{'page'}") );
		}
		else {
			&passfront( &makeQueryString('mode=admin',"work=$awn") );	# 不正な文字列が指定されている場合でもpassfrontの出力前に対処処理がある。
		}
		exit;
	}
	my $plv = &fcts::getUserDetail($permittedid, 1);	# 権限の値を得る(1:ゲスト～9:SU)

	# ADMIN：各管理種類別処理
	if(		$awn eq '' 				) { &accesslevelcheck(1,$plv); &adminMenu($permittedid,$plv); }
	elsif(	$awn eq 'manage'		) { &accesslevelcheck(3,$plv); &adminManage(); }
	elsif(	$awn eq 'images'		) { &accesslevelcheck(1,$plv); &adminImages(); }
	elsif(	$awn eq 'categories'	) { &accesslevelcheck(7,$plv); &adminCategories(); }
	elsif(	$awn eq 'trychangecatopt') { &accesslevelcheck(7,$plv); &adminTrychangecatopt(); }
	elsif(	$awn eq 'editcat'		) { &accesslevelcheck(7,$plv); &adminCatEditor(); }
	elsif(	$awn eq 'trychangecat'	) { &accesslevelcheck(7,$plv); &adminTrychangecategory(); }
	elsif(	$awn eq 'postwithimage'	) { &accesslevelcheck(1,$plv); &adminPostWithImage(); }
	elsif(	$awn eq 'imagetrydels'	) { &accesslevelcheck(3,$plv); &adminImageTrydels(); }
	elsif(	$awn eq 'deleteimages'	) { &accesslevelcheck(3,$plv); &adminDeleteImages(); }
	elsif(	$awn eq 'trydels'		) { &accesslevelcheck(3,$plv); &adminTrydels($permittedid,$plv); }
	elsif(	$awn eq 'setting'		) { &accesslevelcheck(9,$plv); &adminSetting(); }
	elsif(	$awn eq 'trychangeset'	) { &accesslevelcheck(9,$plv); &adminTrychangeset(); }
	elsif(	$awn eq 'userlist'		) { &accesslevelcheck(5,$plv); &adminUserlist(); }
	elsif(	$awn eq 'changepass'	) { &accesslevelcheck(5,$plv); &adminChangepass(); }
	elsif(	$awn eq 'trychangepass'	) { &accesslevelcheck(5,$plv); &adminTrychangepass(); }
	elsif(	$awn eq 'recount'		) { &accesslevelcheck(1,$plv); &adminRecount(); }
	elsif(	$awn eq 'backup'		) { &accesslevelcheck(7,$plv); &adminBackup(); }
	elsif(	$awn eq 'export'		) { &accesslevelcheck(7,$plv); &adminExport(); }		# 要求権限変更 5→7 (Ver 2.2.1)
	elsif(	$awn eq 'skinlist'		) { &accesslevelcheck(9,$plv); &adminSkinlist(); }		# 要求権限変更 7→9 (Ver 1.3.4)
	elsif(	$awn eq 'applyskin'		) { &accesslevelcheck(9,$plv); &adminApplySkin(); }
	elsif(	$awn eq 'panic'			) { &accesslevelcheck(9,$plv); &adminPanic(); }
	else {
		&errormsg("Admin:Work パラメータの値が不正です。");
	}
}

# ---------------------------------
# ADMIN：全ユーザ強制ログアウト処理
# ---------------------------------
sub adminPanic
{
	my $msg;

	if( $flagDemo{'RefuseToChangeSettings'} != 1 ) {
		# まず、自分をログアウト
		print &fcts::logout();	# Cookieを破棄する文字列を出力

		# 自分以外も含めてログイン情報を全破棄
		my $dels = &fcts::breakallsessions();

		$msg = '<p><strong>全ユーザのセッションを破棄しました。(全ユーザを強制ログアウトさせました。)</strong></p><p>※削除したセッション数は、合計 ' . $dels . '個です。</p><p>他の場所も含めて、これまでにログイン状態が保持されていた全ユーザのログイン状態は解除されました。<br>ただし、各ユーザは自らの操作で再ログイン可能なので注意して下さい。もし<strong class="important">不正アクセスが疑われる場合は、すぐにパスワードを変更して下さい</strong>。</p><p><a href="' . &makeQueryString('mode=admin') . '">再ログイン</a></p>';
	}
	else {
		# DEMO：設定変更を拒否
		&demomodemsg('強制ログアウト機能は使用できません。');
	}

	&showadminpage('DELETE ALL SESSIONS','',$msg,'CA');
	exit;
}


# -------------------------
# ADMIN：アクセス許可の判断		※accesslevelcheck：不可ならエラーを表示して終了
# -------------------------		※requiredlevelcheck：可=1/不可=0を返すのみ
sub accesslevelcheck
{
	my $reqlv = shift @_ || 9;	# 要求Level
	my $trylv = shift @_ || 0;	# 所有Level

	if( $reqlv > $trylv ) {
		# 権限不足ならその旨を表示
		my $msg = '<p style="color:#c00;">今ログインしているIDには、当該機能に<strong>アクセスする権限がありません</strong>。' . "(所有Lv.$trylv／必要Lv.$reqlv)" . '</p><p>別のIDでログインしなおすには、一旦ログアウトして下さい。</p>';
		&showadminpage('PERMISSION DENIED','',$msg,'COA');
		exit;
	}
	return 1;
}
sub requiredlevelcheck
{
	my $reqlv = shift @_ || 9;
	my $trylv = shift @_ || 0;
	if( $reqlv > $trylv ) { return 0; }	# 権限不足なら0
	return 1;
}

# -----------------------------
# ADMIN：事前ログイン必須の案内	※通常ならログインできているハズの場面でログインできていない場合に表示
# -----------------------------
sub loginrequired
{
	my $msg = '指定の画面を表示する権限がありません。先にログインして下さい。';
	&showadminpage('LOGIN REQUIRED','',$msg,'CO');
	exit;
}

# -------------------
# ADMIN：初期メニュー
# -------------------
sub adminMenu
{
	my $permittedid = shift @_ || '';	# アクセスユーザID
	my $permitlevel = shift @_ || 0;	# アクセス権限値(1～9)
	my $username = &fcts::forsafety(&fcts::getUserDetail($permittedid,2)) || '名前未設定';	# IDからユーザ名を得る

	# セッション期限の案内
	my $sessionmsg;
	if( $keepsession == 1 ) {
		my $timeoutlim = &fcts::sectotimestring( $sessiontimeout );
		$sessionmsg = qq|ログアウトせずにブラウザを終了すると、セッション有効期限($timeoutlim後)まではログイン状態が維持される設定になっています。|;
		# セッション数の報告
		my $logonusers = &fcts::sessioncount();
		$sessionmsg .= qq|<br>※現在、$logonusers件のログイン状態が保持されています。|;
	}
	else {
		$sessionmsg = qq|ここをクリックしなくても、ブラウザを終了すると自動ログアウトされる設定になっています。|;
	}

	# システムメニューの中身を準備
	my @smenu;
	$smenu[0][0] = '▼日々の作業：';
	$smenu[0][1] = &genSysMenuItem('新規投稿',				'Write New Post',	'新規に投稿します。',							&makeQueryString('mode=edit'),						&requiredlevelcheck(1,$permitlevel));
	$smenu[0][2] = &genSysMenuItem('投稿の削除/編集',		'Manage Posts',		'既存の投稿を削除したり編集したりします。',		&makeQueryString('mode=admin','work=manage'),		&requiredlevelcheck(3,$permitlevel));
	$smenu[0][3] = &genSysMenuItem('画像の管理',			'Manage Images',	'画像をアップロードしたり確認したりします。',	&makeQueryString('mode=admin','work=images'),		&requiredlevelcheck(1,$permitlevel));
	$smenu[0][4] = &genSysMenuItem('カテゴリ管理',			'Manage Categories','カテゴリを作成したり編集したりします。',		&makeQueryString('mode=admin','work=categories'),	&requiredlevelcheck(7,$permitlevel));
	$smenu[1][0] = '▼メンテナンス：';
	$smenu[1][1] = &genSysMenuItem('設定',					'Settings',			'各種設定をします。',							&makeQueryString('mode=admin','work=setting'),		&requiredlevelcheck(9,$permitlevel));
	$smenu[1][2] = &genSysMenuItem('ユーザIDを管理',		'Manage Users',		'ユーザIDを新規作成/編集/削除します。',			&makeQueryString('mode=admin','work=userlist'),		&requiredlevelcheck(9,$permitlevel));
	$smenu[1][3] = &genSysMenuItem('自分のIDを設定',		'Edit Own ID',		'自分のIDの設定情報を編集します。',				&makeQueryString('mode=admin','work=changepass',"userid=$permittedid"),	&requiredlevelcheck(5,$permitlevel));
	$smenu[1][4] = &genSysMenuItem('投稿を再カウント',		'Recount Posts',	'データ総数や条件別該当数を集計し直します。',	&makeQueryString('mode=admin','work=recount'),		&requiredlevelcheck(1,$permitlevel));
	$smenu[1][5] = &genSysMenuItem('スキンの切り替え',		'Switch Skin',		'スキンを一覧表示し、切り替えます。',			&makeQueryString('mode=admin','work=skinlist'),		&requiredlevelcheck(9,$permitlevel));
	$smenu[2][0] = '▼バックアップ：';
	$smenu[2][1] = &genSysMenuItem('バックアップ管理',		'Backup',			'データのバックアップ設定をします。',			&makeQueryString('mode=admin','work=backup'),		&requiredlevelcheck(7,$permitlevel));
	$smenu[2][2] = &genSysMenuItem('条件を指定して出力',	'Export',			'抽出データをHTMLファイルに出力します。',		&makeQueryString('mode=admin','work=export'),		&requiredlevelcheck(7,$permitlevel));
	$smenu[3][0] = '▼ログアウト：';
	$smenu[3][1] = &genSysMenuItem('ログアウト',			'Logout',				'今ログインしているIDをログアウトします。',			&makeQueryString('mode=admin','work=logout'),	&requiredlevelcheck(1,$permitlevel));
	$smenu[3][2] = &genSysMenuItem('全員を強制ログアウト',	'Break All Sessions',	'全てのログインユーザのアクセスを終了させます。',	&makeQueryString('mode=admin','work=panic'),	&requiredlevelcheck(9,$permitlevel), '本当に全員を強制ログアウトさせてよろしいですか？');

	# システムメニューの中身を生成
	my $menuhtml = '';
	for( my $i = 0; $i < scalar(@smenu); $i++) {
		$menuhtml .= qq|<p class="systemmenucategory">$smenu[$i][0]</p>\n<ul class="systemmenu">\n|;
		for( my $j = 1; $j < scalar(@{$smenu[$i]}); $j++) {
			$menuhtml .= qq|<li>$smenu[$i][$j]</li>\n|;
		}
		$menuhtml .= '</ul>';
	}

	# バージョン番号とアップデート案内
	my $vcimage = $aif{'puburl'} . 'ver' . $versionnum . '.gif';

	# サーバ時刻をずらす設定、ずらした現在時刻を表示
	my $nowdate = '';
	my $setshifttime = $setdat{'shiftservtime'};
	if( $setshifttime != 0 ) {
		$nowdate = &fcts::getdatetimestring();	# 現在時刻を文字列で取得
		$nowdate = &fcts::shifttime( $nowdate, $setshifttime );	# 指定時間だけずらした時刻文字列を得る
		# 表示用に整形
		if( $setshifttime > 0 ) { $setshifttime = "+$setshifttime"; }
		$nowdate = '<p class="shifttime">現在時刻は<strong>' . &fcts::forsafety( $setshifttime ) .'時間</strong>ずらす設定になっています。<br>その結果、現在時刻は以下のように取り扱われます。<br><strong>' . $nowdate .'</strong></p>';
	}

	# レンタル版なら
	my $rentalsign = '';
	if( $rentalflag == 1 ) {
		$rentalsign = '<a href="/" class="rentalsign">レンタル版</a>';
	}

	# システム画面の表示内容を作成
	my $msg = qq|
	<p>$usernameさん、作業内容を選択して下さい。(ユーザID「$permittedid」でログイン中)</p>
	<div class="systemmenubox">
		<div class="systemmenucolumn">
			$menuhtml
			<p class="sessionguide">※$sessionmsg</p>
		</div>
		<div class="systemmenucolumn">
			<div class="systemhelpbox"><span class="helpboxtitle">このCGIについて$rentalsign</span>
				<a href="$aif{'puburl'}">公式配布ページを見る</a><br>
				<a href="$aif{'puburl'}usage/"><span class="help">？</span>使い方・設定方法</a><br>
				<a href="$aif{'puburl'}custom/"><span class="help">？</span>カスタマイズ方法</a><br>
				<a href="$aif{'puburl'}faq/"><span class="help">？</span>ＦＡＱ・豆知識群</a><br>
				<a href="$aif{'puburl'}#feedback">機能要望/質問等を送る</a><br>
				<span class="nowversion">( Ver $versionnum が稼働中 )</span><br>
				<a href="$aif{'puburl'}setup/#howtovup" class="nowversion"><img src="$vcimage" alt=""></a><br class="morebr">
				<span class="smalllink"><a href="$aif{'puburl'}releasenotes/" title="最新版の更新案内です。">リリースノート(更新案内)を読む</a><br></span>
				<span class="smalllink"><a href="$aif{'puburl'}nextversion/" title="次期バージョンの開発進捗報告です。">次期バージョンの開発進捗状況</a><br></span>
				<span class="smalllink"><a href="$aif{'puburl'}coffee/" title="作者にカフェインを供給！">CGI作者にコーヒー&#9749;をおごる</a><br></span>
			</div>
			$nowdate
		</div>
	</div><!-- /.systemmenubox -->|;
	if( &fcts::checkpass('') == 2 ) {
		# パスワードが未設定なら設定を促すメッセージを表示
		$msg .= '<p style="color:#dd0000;">※全ユーザのパスワードが未設定な状態です。まずは、「<strong>自分のIDを設定</strong>」メニューを使ってパスワードを設定して下さい。もしくは、「<strong>ユーザIDを管理</strong>」メニューを使って、望みのIDをパスワード付きで作成して下さい。</p>';
	}

	# CSS追加
	my $addcss = '';
	if(( $setdat{'aboutcgibox'} != 0 ) && ( &fcts::lcc($setdat{'licencecode'}) )) {
		if( $setdat{'aboutcgibox'} >= 1 ) { $addcss .= '.smalllink { display:none; }'; }
		if( $setdat{'aboutcgibox'} >= 2 ) { $addcss .= '.systemhelpbox a, .systemhelpbox a + br { display:none; } a.nowversion { display:inline; }'; }
		if( $setdat{'aboutcgibox'} >= 3 ) { $addcss .= '.systemhelpbox { opacity: 0; }'; }
	}

	# 管理メニュー用CSS：
	my $css = '<style type="text/css">
		/* ▼管理:注釈BOX */
		.note { font-size: 0.8em; background-color: #eee; padding: 0.25em; }
		/* ▼管理:ログアウトボタン下部(1カ所) */
		.sessionguide { font-size: 80%; line-height: 1.1; margin: 1em 0; padding: 0.3em 0 0 0; color: #555; }
		/* ▼このCGIについてBOX */
		.systemhelpbox { width: 12em; border: 1px solid green; background-color:#ffffcc; border-radius: 6px; margin: auto; padding: 0.3em; text-align: center; line-height: 1.5; }
		.systemhelpbox .helpboxtitle { display:block; background-color:green; color:white; margin-bottom: 0.5em; border-radius:0.3em; }
		.help { display:inline-block; text-align:center; font-size:0.85em; vertical-align:2px; border-radius:50%; box-sizing:border-box; width:21px; height:21px; background-color:royalblue; color:white; font-weight:bold; margin:0 2px 0 0; line-height:21px; }
		a:hover .help { background-color:red; }
		.nowversion { font-size: 0.8em; border-width:0; text-decoration:none; }
		.shifttime { width: 12em; font-size: 0.8em; margin: 1em auto; padding: 0.5em 1em; text-align: center; line-height: 1.5; background-color: #f5f5f5; }
		.rentalsign { display: block; font-size: 0.8em; font-weight: bold; background-color: #0a0; border-radius: 6px; color: #fff; margin-top: 0.1em; padding: 0.3em 0;  }
		.rentalsign:hover { background-color: darkblue; color: yellow; }
		.smalllink { font-size: 0.75em; } .tinylink { font-size: 0.63em; }
		.morebr { margin-bottom: 0.5em; }
		@media all and (min-width: 600px) {
			/* 管理画面 */
			.systemmenubox { display: table; width: 100%; }
			.systemmenucolumn { display: table-cell; vertical-align: top; }
		}
	' . $addcss . '
	</style>';

	&showadminpage('ADMIN MODE','',$msg,'C',$css);
}

# -----------------------------------
# ADMIN：MENU：メニュー項目HTMLを生成
# -----------------------------------
sub genSysMenuItem
{
	my $jpn = shift @_ || '';	# 日本語名称
	my $enn = shift @_ || '';	# 英語名称
	my $hlp = shift @_ || '';	# ヘルプ
	my $lnk = shift @_ || '';	# クエリー文字列
	my $rtf = shift @_ || 0;	# 可=1 / 否=0
	my $chk = shift @_ || '';	# 確認ダイアログ用文字列

	if( $rtf == 1 ) {
		# アクセス権あり
		if( $chk ne '' ) { $chk = qq| onclick="return confirm('$chk');"|; }
		return qq|<a href="$lnk" title="$hlp"$chk><span class="jp">$jpn</span><span class="en">$enn</span></a>|;
	}
	# アクセス権なし
	return qq|<a href="#NO-PERMISSION" class="nop" title="$hlp" onclick="alert('アクセス権がありません'); return false;"><span class="jp">$jpn</span><span class="en">$enn</span></a>|;
}

# -----------------------
# ADMIN：カテゴリ管理画面
# -----------------------
sub adminCategories {
	# ログイン確認・権限取得
	my $permittedid = &fcts::checkpermission();		# ログイン中ユーザのID名が得られる
	if( !$permittedid ) {
		# ユーザIDを確認できない場合：エラーメッセージ
		&errormsg('ログインしていません。');
		exit;
	}

	my $cgipath = &getCgiPath();

	# カテゴリページ上部
	my $msg = "<p>カテゴリの一覧を確認したり、新規に追加したり、編集したりします。カテゴリを新設する場合は「新規にカテゴリを作成」ボタンを押して下さい。編集する場合は、カテゴリIDをクリックして下さい。削除する場合は、下部の削除フォームを使って下さい。（※各投稿の表示に使われるカテゴリの区切り文字等の表示に関しては、[<a href=\"?mode=admin&amp;work=setting\">設定</a>]→[ページの表示]→[<a href=\"?mode=admin&amp;work=setting#fldCategory\">カテゴリの表示</a>]から設定できます。）</p>";

	# ………………………
	# カテゴリ一覧を表示
	# ………………………
	$msg .= '<div class="categoryTableBox"><h2>カテゴリ一覧</h2>';

	my $mquery = &makeQueryString('mode=admin','work=editcat');
	$msg .= join("\n",&fcts::getCategoryTable("$mquery"));

	# ………………………………………
	# カテゴリ新規作成リンク等を表示
	# ………………………………………
	$msg .= qq|<p><a href="$mquery" class="btnlink">新規にカテゴリを作成</a> <a href="| . &makeQueryString('mode=admin','work=recount') . qq|" class="btnlink">カテゴリ該当数を再集計</a></p>\n|;

	$msg .= "</div><!-- /.categoryTableBox -->\n";

	# ……………………………………
	# カテゴリ階層プレビューを表示
	# ……………………………………
	my $addnocatitem  = &getattributeforcheckbox($setdat{'addnocatitem'});	# チェックボックス用のデータを作る
	my $addnocatlabel = &fcts::forsafety( $setdat{'addnocatlabel'} );		# 安全化

	$msg .= '<div class="categoryTreeBox"><h3>▼カテゴリ階層プレビュー</h3><div class="categoryTree">';
	$msg .= &makeCategoryTree();

	$msg .= qq|</div><!-- /.categoryTree -->
	<div class="categoryOptions">
		<h4>オプション設定</h4>
		<form action="$cgipath" method="post"><input type="hidden" value="admin" name="mode"><input type="hidden" value="trychangecatopt" name="work">
			<p><label><input type="checkbox" name="addnocatitem" value="1" $addnocatitem>末尾に「カテゴリなし」を追加</label></p>
			<p>→ <label>項目名：<input type="text" name="addnocatlabel" class="addnocatlabel" value="$addnocatlabel"></label></p>
			<p><input type="submit" value="設定変更"></p>
		</form>
	</div>
	</div><!-- /.categoryTreeBox -->\n|;

	# ………………………
	# 削除フォームを表示
	# ………………………
	my $dellist = &fcts::getCategorySelectList('tryid');	# カテゴリ一覧をHTMLのselect要素で得る

	# カテゴリ設定が初期状態なら、デフォルト設定も削除できる旨を追加表示する。
	my $addmsg = '';
	if(( $setdat{'categorylist'} eq '' ) || (  $setdat{'categorylist'} eq $firstdat{'categories'} )) {
		$addmsg = '<br><span style="color:crimson;">※初期カテゴリID「info」「memo」「diary」も削除可能です。これらは設定例を示すために存在しているに過ぎないので、削除しても何も問題ありません。</span>';
	}

	# カテゴリが1つ以上ある場合だけ、削除フォームを表示する
	if( $dellist ) {
		$msg .= qq|<form action="$cgipath" method="post" class="delform">■削除：$dellist
			<input type="hidden" name="mode" value="admin">
			<input type="hidden" name="work" value="trychangecat">
			<input type="hidden" name="idwork" value="deletecat">
			<input type="hidden" name="tryname" value="削除">
			<input type="submit" value="カテゴリを削除する" onclick="return confirm('このカテゴリを本当に削除しますか？');"></form>|;
		$msg .= q|<p class="noticebox">※カテゴリを削除しても、当該カテゴリに属している投稿データは消えません。ただし、当該カテゴリの名前(カテゴリ名)は表示されなくなります。<br>※削除したカテゴリを復活させたい場合は、同じID名でカテゴリを新規作成した後、再集計して下さい。<br>※アイコンのプレビューは仮です。実際の表示サイズはスキン側のCSSによって変化します。| . $addmsg . '</p>';
	}

	# CSS
	my $css = q|<style tyle="text/css">
		.categoryTableBox,
		.categoryTreeBox {
			display: inline-block;
			vertical-align: top;
		}
		.categoryTableBox h2 { margin-top: 0.5em; }
		.categoryTreeBox {
			margin: 0.5em 0 0 1em;
			padding: 0 1em;
			background-color:#ffd;
			border:1px solid #cca;
			border-radius:0.67em;
		}
		.catorder, .catposts { text-align: right; }
		.delform { color: crimson; }
		.categoryTree {
			background-color:white;
			border-radius: 0.5em;
			border: 1px solid #eee;
			margin: 1em 0;
			padding: 0.25em;
		}
		.categoryTree ul {
			padding-left: 30px;
			list-style-type: disc;
		}
		.categoryTree .num {
			display: inline-block;
			margin-left: 0.4em;
			font-size: 0.9em;
			color: #aaa;
		}
		.categoryOptions {
			margin: 1em 0;
			border: 1px solid #b3b310;
			background-color: #fcfce0;
			font-size: 0.9em;
		}
		.categoryOptions h4 {
			background-color: #b3b310;
			color: white;
			margin: 0 0 0.4em 0;
			padding: 1px;
			font-size: 10px;
		}
		.categoryOptions p {
			margin: 0 0.4em;
			letter-spacing: 0;
		}
		.categoryOptions p:nth-of-type(2n) { text-align: right; }
		.categoryOptions p:last-child { margin-bottom:0.4em; }
		.addnocatlabel { width: 8.5em; }
		.caticon img { height: 1.2em; width: auto; margin-right:2px; vertical-align:text-top; }
		@media (max-width: 599px) {
		}
		.delform { margin-top:2em; padding-top:1em; border-top: 2px dashed gray; }
		</style>
	|;

	&showadminpage('MANAGE CATEGORIES','',$msg,'CA',$css);
}

# -----------------------
# カテゴリツリーを生成する
# -----------------------
sub makeCategoryTree
{
	my $opt = shift @_ || '';

	# カテゴリツリーを得る
	my $ctree .= &fcts::getCategoryTree('',$opt);

	# カテゴリ末尾に「なし」を追加する設定なら追加する
	if( $setdat{'addnocatitem'} == 1 ) {
		my $nocatline = '<li><a href="?cat=-">' . &fcts::forsafety( $setdat{'addnocatlabel'} ) . '</a></li></ul>';
		$ctree =~ s|</ul><!-- End of Tree -->|$nocatline|;
	}

	return $ctree;
}

# -----------------------
# ADMIN：カテゴリ編集画面
# -----------------------
sub adminCatEditor
{
	# ………………
	# ログイン確認
	# ………………
	my $permittedid = &fcts::checkpermission();
	if( !$permittedid ) {
		# 権限を確認できない場合：エラー
		&loginrequired();
	}
	my $plv = &fcts::getUserDetail($permittedid, 1);	# 権限の値を得る(1:ゲスト～9:SU)

	# …………………
	# 表示権限の確認
	# …………………
	&accesslevelcheck(7,$plv);	# 権限Lv.7未満ならアクセス権はない

	# ……………………………………
	# 変更対象カテゴリIDと情報取得
	# ……………………………………
	my $catid  = $cgi->param('catid')  || '';		# 新規作成の場合は空文字列
	my $cname = '';
	my $cdscr = '';
	my $cicon = '';
	my $cprnt = '';
	my $chits = '';
	my $coder = int(&fcts::getCategoryLastOrder() / 10) * 10 + 10;
	if( $catid ne '' ) {
		# カテゴリIDの指定があれば情報を得る(1=表示名,2=概要文,3=親カテゴリID,4=該当個数,5=掲載順序)
		$cname = &fcts::forsafety( &fcts::getCategoryDetail($catid, 1));	# 編集対象カテゴリの表示名
		$cdscr = &fcts::forsafety( &fcts::getCategoryDetail($catid, 2));	# 編集対象カテゴリの概要文
		$cprnt = &fcts::forsafety( &fcts::getCategoryDetail($catid, 3));	# 編集対象カテゴリの親カテゴリID
		$chits = &fcts::forsafety( &fcts::getCategoryDetail($catid, 4));	# 編集対象カテゴリの該当個数
		$coder = &fcts::forsafety( &fcts::getCategoryDetail($catid, 5));	# 編集対象カテゴリの掲載順序
		$cicon = &fcts::forsafety( &fcts::getCategoryDetail($catid, 6));	# 編集対象カテゴリのアイコン
		if( $cname eq '' ) {
			# 名称が空文字列の場合はIDが存在しない
			&errormsg('カテゴリ情報編集：不正なID名が指定されました。');
		}
	}

	# ……………
	# 画面の作成
	# ……………
	my $work = '';
	my $targetid = '';
	my $idform = '';
	my $submitLabel = '';
	if( $catid eq '' ) {
		# 新規作成
		$work = 'makenewcat';
		$targetid = '<p>カテゴリを新規作成します。</p>';
		$submitLabel = '作成';
		$idform = '<input type="text" value="" name="tryid">';
	}
	else {
		# 変更なら
		$work = 'changecat';
		$targetid = '<p>カテゴリID「' . $catid . '」の登録情報を変更します。</p>';
		$submitLabel = '変更';
		$idform = qq|<input type="text" value="$catid" disabled><input type="hidden" value="$catid" name="tryid">|;
	}

	my $catselectlist = &fcts::getCategorySelectList('tryparentid',1,$cprnt,$catid);	# カテゴリ一覧をHTMLのselect要素で得る（引数：1=name属性値、2=先頭空白、3=デフォルト選択ID、4=自分自身のIDは除外対象）
	if( $catselectlist ne '' ) {
		# カテゴリが1つ以上ある場合の注釈
		$catselectlist .= ' <span class="notice">※階層構造を作る際のみ選択して下さい。深さに制限はありません。</span>';
	}
	else {
		# カテゴリが1つもない場合の注釈
		$catselectlist .= ' <span class="notice">※まだ他にカテゴリが作成されていないため、選べません。</span>';
	}

	my $cgipath = &getCgiPath();
	my $msg = qq|
		$targetid
		<form action="$cgipath" method="post"><input type="hidden" name="mode" value="admin"><input type="hidden" value="trychangecat" name="work"><input type="hidden" name="idwork" value="$work">
			<fieldset>
				<legend>カテゴリ情報</legend>
				<ul class="inputs">
					<li><label><span class="itemhead">カテゴリID：</span> $idform</label> <span class="notice">※半角英数のみ。一度決めたら変更はできません。</span></li>
					<li><label><span class="itemhead">カテゴリ名：</span> <input type="text" value="$cname" name="tryname"></label> <span class="notice">※いつでも変更できます。</span></li>
					<li><label><span class="itemhead">概要文：    </span> <input type="text" value="$cdscr" name="trydesc"></label> <span class="notice">※いつでも変更できます。(省略可)</span></li>
					<li><label><span class="itemhead">アイコン：  </span> <input type="text" value="$cicon" name="tryicon" placeholder="https://"></label> <span class="notice">※いつでも変更できます。(省略可)</span></li>
					<li><label><span class="itemhead">親カテゴリ：</span> </label>$catselectlist</li>
					<li><label><span class="itemhead">掲載順序：  </span> <input type="text" value="$coder" name="tryorder" class="num"></label> <span class="notice">※小さい順に並びます。連番でなくて構いません。</span></li>
				</ul>
			</fieldset>
			<p>
				<input type="submit" value="カテゴリを$submitLabelする" class="sendui">
			</p>
		</form>
		<p class="noticebox">※表示名の重複チェックはしませんので、複数のIDで同じカテゴリ名を使うこともできます。<br>※カテゴリ名が画面に表示されるかどうかは、表示に使うスキン次第です。<br>※親カテゴリを指定する際に、階層構造が無限ループになるような指定はしないで下さい（それらのカテゴリ設定が一括して消滅してしまいます）。<br>※掲載順序は「<strong class="important">同一階層の中での</strong>最も小さい値」から順に並びます。小数や負数も使えます。</p>
	|;

	if( $catid ne '' ) {
		# 新規作成ではない場合だけ、削除ボタンを表示する
		my $delbtnpos = '';	# 削除ボタンの配置調整
		if( $setdat{'sysdelbtnpos'} == 1 ) {
			# 右寄せ指定ならCSSを追加
			$delbtnpos = ' style="text-align:right;"';
		}
		$msg .= "<div$delbtnpos>" . '<div class="deletions"><p>【カテゴリ削除】<small>このカテゴリを削除する場合は下記のボタンを押して下さい。</small></p>';
		$msg .= qq|<form action="$cgipath" method="post" class="delform">
			<input type="hidden" name="tryid" value="$catid">
			<input type="hidden" name="mode" value="admin">
			<input type="hidden" name="work" value="trychangecat">
			<input type="hidden" name="idwork" value="deletecat">
			<input type="hidden" name="tryname" value="削除">
			<input type="submit" value="このカテゴリを削除する" onclick="return confirm('このカテゴリを本当に削除しますか？');"></form></div></div>|;
	}

	my $css = '<style type="text/css">
		.itemhead { min-width: 6.15em; display: inline-block; }
		.inputs { margin: 0.5em 0; padding: 0 0 0 20px; }
		.deletions { color: crimson; font-weight:bold; border: 2px dotted crimson; padding: 5px; margin: 1em 0 1em; display: inline-block; }
		.deletions p, .deletions form { margin: 0; }
		.note { margin-bottom: 0; }
		input:placeholder-shown { color: #555; }
		input:focus:placeholder-shown { color: #ccc; }
		.sendui { font-size:1.2em; }
		.num { width: 3em; }
	</style>';
	&showadminpage('EDIT CATEGORY','',$msg,'CGA',$css);
}

# -----------------------------
# ADMIN：カテゴリ情報変更の試行		[情報パラメータ] カテゴリID：tryid、カテゴリ名：tryname、概要文：trydesc、親カテゴリ：tryparentid、掲載順序：tryorder
# -----------------------------		[動作パラメータ] idwork = makenewcat(カテゴリ新設), changecat(カテゴリ変更), deletecat(カテゴリ削除)
sub adminTrychangecategory {

	my $result = '';

	# 不正送信の確認
	&fcts::postsecuritycheck('work=trychangecat');

	# ログインの確認
	my $permittedid = &fcts::checkpermission();
	if( !$permittedid ) {
		# ログインしていなければエラー
		&loginrequired();
	}
	my $plv = &fcts::getUserDetail($permittedid, 1);	# 権限の値を得る(1:ゲスト～9:SU)

	# 権限レベル確認
	&accesslevelcheck(7,$plv);

	# ……………………………
	# ▼送信された情報の取得
	# ……………………………
	# カテゴリ情報の作成処理(TRY)
	my $tryid			= &fcts::deleteseparators( $cgi->param('tryid') ) || "";
	my $tryname			= &fcts::deleteseparators( &fcts::safetycutter( scalar $cgi->param('tryname') )) || "";
	my $trydesc			= &fcts::deleteseparators( $cgi->param('trydesc') )  || "";
	my $tryicon			= &fcts::deleteseparators( $cgi->param('tryicon') )  || "";
	my $tryparentid		= &fcts::deleteseparators( $cgi->param('tryparentid') )  || "";
	my $tryorder		= &fcts::deleteseparators( $cgi->param('tryorder') )  || "";

	# ……………………………………………………
	# 準備：既存のカテゴリID名リストを得ておく
	# ……………………………………………………
	my @existingIdData = &fcts::getCategoryList(1);	# カテゴリID＋名称リストを得る
	my @existIds;
	foreach my $ou (@existingIdData) {
		my @catinfo = split(/<>/, $ou);
		push( @existIds, lc($catinfo[0]) );
	}
	# ※この時点で、配列 @existIds の中には、カテゴリID名が小文字で入る。

	# ……………………………
	# ▼送信された情報の確認
	# ……………………………
	my $errMsg = '';

	# カテゴリIDが：
	if( $tryid eq '' ) {
		# 未指定なら
		$errMsg .= '<li>カテゴリIDが入力されていません。</li>';
	}
	elsif( $tryid =~ /\W/ ) {
		# IDに英数字以外があったら中止
		$errMsg .= '<li>カテゴリIDには半角英数字だけが使えます。</li>';
	}

	# カテゴリ名称が：
	if( $tryname eq '' ) {
		# 未指定なら
		$errMsg .= '<li>カテゴリ名が入力されていません。</li>';
	}

	# 親カテゴリIDが： ※親カテゴリIDが指定されている場合だけ確認
	if(( $tryparentid ne '' ) && ( $tryparentid ne '-')) {

		# 親カテゴリに指定したカテゴリの親が自分だったら
		if( lc($tryid) eq lc(&fcts::getCategoryDetail($tryparentid,3)) ) {
			$errMsg .= '<li>この親カテゴリの選択では、階層構造が<strong>無限ループになってしまう</strong>ため、設定できません。<br>（カテゴリAの親がカテゴリBのとき、カテゴリBの親をカテゴリAに設定することはできません。）</li>';
		}
		# 自分自身を自分の親にする指定だったら
		if( lc($tryid) eq lc($tryparentid) ) {
			$errMsg .= '<li>自分自身を自分の親カテゴリに指定することはできません。</li>';	# 正規のフォームから送信されていれば、この行が実行されることはないハズ。
		}

		# 存在しないIDが親カテゴリに指定されていたら
		my $tryparentExist = 0;
		foreach my $oid (@existIds) {
			if( lc($tryparentid) eq $oid ) {
				$tryparentExist++;	# 指定された親カテゴリIDが存在したら加算
			}
		}
		if( $tryparentExist == 0 ) {
			# 指定された親カテゴリIDが存在しなければ
			$errMsg .= '<li>存在しないカテゴリIDが親カテゴリとして指定されています。</li>';		# 正規のフォームから送信されていても、別窓でカテゴリを削除していた場合には、この行が実行される可能性がある。
		}

	}

	# 順序に数字以外があったら（ただし入力省略は可）
	if( $tryorder ne '' && $tryorder !~ /[\d０１２３４５６７８９]/ ) {
		$errMsg .= '<li>掲載順序には数字だけが使えます。</li>';
	}
	else {
		$tryorder = &fcts::nozenkaku($tryorder);	# 全角数字を(あれば)半角にする（数字以外は消える）
	}

	# エラーがあれば表示して処理中止
	if( $errMsg ne '' ) {
		$errMsg = '<h2>カテゴリ情報の更新失敗</h2><p>以下の理由で処理を継続できませんでした。</p><ul style="color:crimson;">' . $errMsg . '</ul>';
		&showadminpage('CATEGORY EDIT ERROR','',$errMsg,'B');
		exit;
	}

	# ………………………………………………
	# ▼作業種別の把握（＋権限レベル確認）（新規作成はLv.9のみ／Lv.5～8は自分のIDだけ／Lv.3以下は拒否）
	# ………………………………………………
	my $work = $cgi->param('idwork') || &errormsg('adminTrychangecategory:作業種別がありません。');
	my $wlabel = '';
	if( $work eq 'makenewcat' ) {
		# 新規作成
		$wlabel = '新規作成';

		# 既存のカテゴリID名との重複を確認
		foreach my $oid (@existIds) {
			if( lc($tryid) eq $oid ) {
				# 一致していたら新規追加を拒否
				my $msg = '<h2>重複ID</h2><p>指定されたカテゴリIDは既に存在します。新規作成はできませんでした。</p>';
				&showadminpage('Existing ID','',$msg,'BG');
				exit;
			}
		}
	}
	elsif( $work eq 'changecat' ) {
		# 強制変更なら
		$wlabel = '変更';
	}
	elsif( $work eq 'deletecat' ) {
		# ID削除なら
		$wlabel = '削除';
		$tryorder = 'DEL';	# 削除フラグを立てておく
	}
	else {
		&errormsg('adminTrychangecategory:作業種別が不正です。');
	}


	# ………………………………………………
	# ▼情報更新（パスワードとユーザ情報）
	# ………………………………………………
	$result .= '<ul>';

	# ‥‥‥‥‥‥‥‥‥‥‥
	# カテゴリ情報の変更処理
	# ‥‥‥‥‥‥‥‥‥‥‥
	if( $flagDemo{'RefuseToChangeSettings'} != 1 ) {

		# カテゴリ情報を更新/追加/削除
		my $newidline = &fcts::makeLineForCategoryDat( $tryid, $tryname, $trydesc, $tryparentid, '＾維', $tryorder, $tryicon );		# カテゴリID：tryid、カテゴリ名：tryname、概要文：trydesc、親カテゴリ：tryparentid、該当個数：維持、掲載順序：tryorder、アイコン：tryicon	（ID以外の各値に「＾維」を指定すると、既存IDなら前の値を維持する）

		if( $newidline eq '' ) {
			# もしカテゴリが1つもなければ（デフォルト値が適用されるのを防ぐために）区切り文字だけを1つ入れる
			$newidline = '<,>';
		}

		# 保存
		my @trywrites;
		push(@trywrites,"categorylist=$newidline");

		# 保存処理へ渡す
		&savesettings( @trywrites );

		# 報告用文字列
		$result .= '<li>カテゴリID「 ' . &fcts::forsafety($tryid) . ' 」の情報を' . $wlabel . 'しました。</li>';

	}
	else {
		# DEMOモード：カテゴリ情報の変更を拒否
		&demomodemsg('カテゴリ情報の変更はできませんでした。');
	}

	$result .= "</ul>\n";
	my $msg = "<h2>カテゴリ管理作業を完了</h2><p>$result</p>";
	&showadminpage('Updated','',$msg,'CGA');

}

# ------------------------
# カテゴリオプションの保存
# ------------------------
sub adminTrychangecatopt {

	if( $flagDemo{'RefuseToChangeSettings'} == 1 ) {
		# デモモードなら実行を拒否
		&demomodemsg('カテゴリオプションの変更はできませんでした。');
		exit;
	}

	# パラメータから値を得る
	my $tryaddnocatitem  = $cgi->param('addnocatitem' ) || 0 ,
	my $tryaddnocatlabel = $cgi->param('addnocatlabel') || 'なし' ,

	# ユーザ情報の更新・追加・削除用関数を作成しておいて、それを呼ぶ。
	my @trywrites;
	push(@trywrites,"addnocatitem=$tryaddnocatitem");
	push(@trywrites,"addnocatlabel=$tryaddnocatlabel");

	# 保存処理へ渡す
	&savesettings( @trywrites );

	# カテゴリ管理画面を再表示する
	&adminCategories();
}

# --------------------------
# カテゴリの該当数をカウント
# --------------------------
sub categorycounter
{
	my %counter;	# カテゴリカウント用の連想配列
	my $done = 0;	# カテゴリが存在した投稿件数
	my $msg = '';	# 結果表示用の文字列 (※必ずしも表示に使われるとは限らない)

	# カテゴリが1件も登録されていない場合は、集計処理自体をしないようにする
	if( $setdat{'categorylist'} eq '<,>' ) {
		return '<p>カテゴリが1件も登録されていません。</p>';
	}

	# データ全体を走査(データXMLをループで読み込む)
	foreach my $oneclip (@xmldata) {

		# 下書きだったらカウントしない
		my $flags = &fcts::forsafety( &fcts::getcontent($oneclip,'flag') );
		if( $flags =~ m/draft/ ) {
			next;
		}

		# 分解(カテゴリcat要素を抜き出す)
		my $cat	= &fcts::getcontent($oneclip,'cat');

		# カテゴリがなければ次のループへ
		if( $cat eq '' ) { next; }
		else { $done++; }

		# カテゴリCSVを配列に分解する
		my @cats = split(/,/,$cat);

		# カテゴリを1つずつカウント(※カウント値は、連想配列で「カテゴリID：該当個数」の形式で蓄積する)
		foreach my $onecat ( @cats ) {
			if( $counter{$onecat} ) {
				# 既に定義されていれば1を足す
				$counter{$onecat}++;
			}
			else {
				# まだ定義されていなければ1を入れる
				$counter{$onecat} = 1;
			}
		}

	}

	# 既存のカテゴリの該当個数を、まずはゼロリセットしておく
	$setdat{'categorylist'} = &fcts::makeLineForCategoryDat('*ZERORESET');
	@fcts::catdata = &fcts::tidyDat( $setdat{'categorylist'} );		# カテゴリデータを再展開

	# カテゴリが1つでもあれば		memo L.8268あたりを右ペインに表示しつつ書くと良いかも知れない。
	if( $done >= 1 ) {

		$msg .= '<ul>';	# 結果表示用

		# カテゴリ更新関数をカテゴリの数だけ呼び出して更新する (やや無駄が多い気もするが）
		foreach my $key (keys(%counter) ){
			# 記録用変数に入れる
			$setdat{'categorylist'} = &fcts::makeLineForCategoryDat( $key, '＾維', '＾維', '＾維', $counter{$key}, '＾維', '＾維' );		# 値「＾維」は前の値を維持する指定
			@fcts::catdata = &fcts::tidyDat( $setdat{'categorylist'} );		# カテゴリデータを再展開

			# 結果表示用文字列
			$msg .= '<li>カテゴリID：' . $key . ' ：' . $counter{$key} . '</li>';
		}

		# 更新したカテゴリ情報をiniに保存する
		my @trywrites;
		push(@trywrites,"categorylist=$setdat{'categorylist'}");
		&savesettings( @trywrites );

		$msg .= '</ul>';	# 結果表示用
	}
	else {
		$msg = '<p>カテゴリは1つも使われていませんでした。</p>';
	}

	# 画面表示が必要な状況から呼び出された場合のために、結果ステータス表示文字列を返す。
	return $msg;
}

# -------------------		※アップロード処理後にも呼ばれる
# ADMIN：画像管理画面		引数1：結果報告HTML、引数2：新規UP画像の総数
# -------------------
sub adminImages
{
	my $resmsg = shift @_ || '';
	my $newimgs = shift @_ || 0;

	# ログイン確認・権限取得
	my $permittedid = &fcts::checkpermission();		# ログイン中ユーザのID名が得られる
	if( !$permittedid ) {
		# ユーザIDを確認できない場合：エラーメッセージ
		&errormsg('ログインしていません。');
		exit;
	}
	my $plv = &fcts::getUserDetail($permittedid, 1);	# ログイン中ユーザの権限値
	my $username = &fcts::forsafety(&fcts::getUserDetail($permittedid,2)) || '名前未設定';	# IDからユーザ名を得る

	# ディレクトリの存在確認
	if(!( -d $imagefolder )) {
		# 画像UP用ディレクトリがなければ
		my $err .= '<p class="important"><strong>[エラー] 画像保存用ディレクトリが見つかりません。</strong></p><p>画像の保存用に指定されたディレクトリ(フォルダ)がサーバ上に見つかりませんでした。<br>画像をアップロードしたり管理したりするには、まずはサーバ上に画像保存用ディレクトリ(※)を作り、そこに書き込み権限を付与して下さい。</p><p>※現在の設定では、画像保存用ディレクトリ名は、<b>' . &fcts::forsafety($imagefolder) . '</b> になっています。</p>';
		&showadminpage('DIRECTORY NOT FOUND','',$err,'CA','');
		exit;
	}

	my $msg = '';
	my $addcss = '';

	# …………………………………………
	# ▼結果表示があるなら先に表示する
	# …………………………………………
	if( $resmsg ne '' ) {
		$msg .= '<div id="resultMsg">' . $resmsg . q|
			<p class="moreup"><input type="button" value="さらに他の画像をアップロードする" onclick="document.getElementById('defaultTopMsg').style.display = 'block'; document.getElementById('resultMsg').style.display = 'none';"></p>
			</div><!-- /#resultMsg -->
		|;
		my $checktrs = $newimgs * 2 + 1;
		$addcss = '#defaultTopMsg { display:none; } table.images tr:nth-of-type(-n+' . $checktrs . ') .imgid::after { content:"\ANEW"; font-weight: bold; color:#f55; white-space:pre; font-size:0.67em; }';
	}

	# ………………………………………………………………
	# ▼デフォルト上部案内＋アップロードフォームを生成
	# ………………………………………………………………
	$msg .= '<div id="defaultTopMsg">';
	$msg .= "<p>$usernameさん、あなたのIDでは『投稿に使う画像の選択";
	if( $plv >= $setdat{'imageuprequirelevel'}	) { $msg .= '、画像の新規アップロード'; }
	if( $plv >= 3 && $plv < 7					) { $msg .= '、自分でUPした画像の削除'; }
	if( $plv >= 7 								) { $msg .= '、任意の画像の削除'; }
	$msg .= "』ができます。(ユーザID「$permittedid」でログイン中)</p>";

	# --------------------------
	# 画像ファイルのリストアップ
	my $ifilelist = &listupImageFiles();

	# ------------------------
	# 画像アップロードフォーム
	if( $plv >= $setdat{'imageuprequirelevel'} ) {
		# 画像をUPする権限があれば
		my $cgipath = &getCgiPath();
		$msg .= '<div class="imageuploadarea">';
		if(( $setdat{'imagemaxlimits'} == 0 ) || ( $setdat{'imagelimitflag'} == 0 )) {
			# 上限が設定されていないか、または上限到達フラグが立っていなければUPフォームを表示
			my $attmultiple = '';
			my $multipleguide = '';
			if( $setdat{'imageupmultiple'} == 1 ) { $attmultiple = 'multiple'; $multipleguide = q|<p class="uploadformguide">※複数ファイルの同時選択も可能です。<a href="#" onclick="alert('Windowsの場合は、[Ctrl]キーを押しっぱなしにした状態で複数のファイルをクリックすれば、クリックしたすべてのファイルを同時に選択できます。Macの場合は[Command]キーを使います。iOSやAndroidでは、何もせずにそのままタップするだけで複数選択できます。'); return false;">複数選択するには？</a></p>|; }
			$msg .= qq|
				<form action="$cgipath" method="post" class="postform" enctype="multipart/form-data">
					<fieldset>
						<legend>画像の新規アップロード</legend>
						<input type="file" name="upload_file" $attmultiple>
						<input type="hidden" value="imageup" name="mode">
						<input type="submit" value="アップロード"><br>
						$multipleguide
					</fieldset>
				</form>
			|;
		}
		else {
			$msg .= '<p class="important"><strong>画像総数または保存可能容量が最大値に達しているため、これ以上のアップロードはできません。</strong><br>さらにアップロードするには、上限設定を変更するか、または既存の画像ファイルを削除する必要があります。</p>';
		}

		# 上限の案内
		if( $setdat{'imagemaxlimits'} == 1 ) {
			$msg .= '<p>●現在の設定では、画像1ファイルあたりのサイズは最大 <b>' . &fcts::byteswithunit($setdat{'imagemaxbytes'}) . ' </b>に制限されています。<br>●投稿可能総数は  <b>' . $setdat{'imagefilelimit'} . ' </b>枚まで、総容量は  <b>' . &fcts::byteswithunit($setdat{'imagestoragelimit'}) . ' </b>までです。</p><p class="upnotice">※制限を超過しても自動削除はされません（新規アップロードができなくなるだけです）。</p>';
		}
		else {
			$msg .= '<p>●現在の設定では、画像1ファイルあたりの最大サイズは <b>無制限</b> です。<br>●投稿可能枚数は <b>無制限</b> で、総容量の上限は <b>設定されていません</b>。</p>';
		}

		$msg .= '</div>';
	}
	else {
		$msg .= '<p>※ゲスト権限での画像アップロードはできません。</p>';
	}
	$msg .= '</div><!-- /#defaultTopMsg -->';
	# ……………
	# ▲ここまで
	# ……………

	# Hover時装飾用スクリプト
	$msg .= "\n" . &fcts::tooneline(qq|
	<script>
		function doubleHover(targetclass) {
			var targets = document.querySelectorAll('.' + targetclass);
			targets.forEach(function(oneTarget) {
				oneTarget.classList.add("nowHover");
			});
		}
		function doubleOut(targetclass) {
			var targets = document.querySelectorAll('.' + targetclass);
			targets.forEach(function(oneTarget) {
				oneTarget.classList.remove("nowHover");
			});
		}
	</script>|) . "\n";

	# ------------------------
	# 画像ファイルリストの表示
	$msg .= '<div class="imagetablearea">' . $ifilelist . '</div><p class="noticebox ">※<b>誰でも使用可：</b>どのIDでUPされた画像でも、誰でも何度でも投稿文中に埋め込んで掲載できます。<br>※<b>削除の条件：</b>管理者・編集者権限のあるIDなら、どの画像でも削除できます。それ未満の権限では、自分でUPした画像だけを削除できます。ただし、ゲスト権限では一切削除できません。<br>※<b>一覧表示対象</b>：設定で許可された拡張子以外のファイルは、この一覧には表示されません。FTP等の別手段でUPされたファイルも表示されますが、サブディレクトリにあるファイルは表示されません。<br>※設定で投稿可能総数を無制限にしても、サーバ側のディスクスペースに上限があります。<br>※アップロードはできるのに<strong class="important">画像が表示されない</strong>場合は、<a href="' . $aif{'puburl'} . 'setup/#imagenotshow">トラブルシューティング</a>をご参照下さい。</p>';

	# --------------------------------------
	# 画像拡大用のjQuery＋Lightboxの読み込み
	$msg .= &outputLightboxLoader(1,1);

	# CSS
	my $css = q|<style tyle="text/css">
		html { scroll-behavior: smooth; }
		.imageuploadarea { border-width: 1px 0; border-style: dashed; border-color: gray; margin: 1em 0; padding: 1.75em 0.75em; background-color: #ffd; }
		.imagetablearea { max-width: 100%; overflow: auto; } .thumbnail { width:auto; max-width: 200px; height: auto; max-height: 200px; vertical-align: middle; font-size:0.6em; } .size { text-align: right; }
		.upnotice { font-size: 0.85em; margin:0; color:#555; }
		.uploadformguide { margin: 1em 0 0 0; font-size: 0.8em; color: #888; display: inline-block; }
		.checkedCtrl { display:inline-block; }
		.uselink { font-size:0.75em; display:block; max-width:5em; margin:0.5em auto; }
		.embcode { font-size:0.8em; background-color:#f0fff0; }
		.embcode span { display:inline-block; }
		.embcode input { font-size:0.95em; max-width:18em; width:27vw; vertical-align:middle; }
		.embcopy { font-size:0.75em; margin:0 0 0 0.25em; vertical-align:middle; }
		.widthheight { margin:3px 0 0 0; padding:1px 0.25em; text-align:right; font-size: 0.9em; background-color:#e5e5e5; }
		.widthheight.nosize { font-size:0.6em; color:#777; }
		.sunit { font-size:0.8em; }
		.nowHover { background-color:#fffff0; }
		.nowHover .embcode { background-color:#ffc; }
		#resultMsg { border:1px solid royalblue; margin: 1em 0; padding: 1em; background-color: #f8f8ff; border-radius:0.75em; }
		.msgtitle { margin:0; font-weight:bold; background-color:royalblue; color:white; padding:0.4em 0.25em; line-height:1.1; border-radius:0.25em; }
		.msgsum { border-top:1px dotted gray; margin-top:1em; padding-top:1em; }
		.moreup { margin:0; }
		@media (max-width: 599px) {
			table.images { font-size: 0.75em; }
			.thumbnail { max-width: 100px; max-height: 100px; }
			.checkedCtrl { margin-top:0.5em; }
			.imguptime { line-height:1.1; font-size:0.85em; min-width: 4em; }
			.uselink { min-width: 3em; }
			.embcode input { font-size:0.8em; width:15vw; }
			#resultMsg { font-size:0.8em; }
		}
	| . $addcss . '</style>';

	&showadminpage('MANAGE IMAGES','',$msg,'CA',$css);
}

# ---------------------------------
# ADMIN：既存の画像を使って新規投稿
# ---------------------------------
sub adminPostWithImage
{
	# 使いたい既存画像のリストを、挿入用文字列に変換する
	my $prestr = '';

	my @selectedfiles = $cgi->param('filename');	# 指定されたファイル名一覧

	# 不正送信の確認
	&fcts::postsecuritycheck('work=postwithimage');

	if( $selectedfiles[0] ne '' ) {
		# 候補が1つ以上存在すれば
		foreach my $onefile ( @selectedfiles ) {
			$prestr .= '[PICT:' . $onefile . ']';
		}

		# 編集画面を呼び出す
		&modeEdit($prestr);
	}
	else {
		# 候補が指定されていなければ
		my $msg = '<p>画像が選択されていません。</p>';
		&showadminpage('NO SELECTED IMAGES','',$msg,'CIA','');
	}
}

# ----------------------------------------
# Lightbox関連ファイルの読み込みHTMLを出力	引数1：1=jQuery必要, 0=jQuery不要、引数2：Lightboxを強制(1=する/0=しない)
# ----------------------------------------
sub outputLightboxLoader
{
	my $jq = shift @_ || 0;
	my $forceLightbox = shift @_ || 0;
	my $ret = '';

	# jQueryが要る場合
	if( $jq == 1 ) {
		$ret .= '<script type="text/javascript" src="' . $libdat{'urljqueryjs'} . '"></script>';
	}

	# 読み込むスクリプトの選択
	my $loadjs  = $libdat{'urllightboxjs'};		# Lightbox JS
	my $loadcss = $libdat{'urllightboxcss'};	# Lightbox CSS

	if(( $setdat{'isuselightbox'} == 2 ) && ( $forceLightbox != 1 )) {
		# 設定でLightbox以外が選択されていて、かつ、Lightboxを強制する場面でなければ、指定のスクリプトを読む
		if( $setdat{'imageexpandingjs'} ne '' ) {
			# JavaScriptが空欄でなければ、指定のJavaScriptとCSSを読むよう指定する（CSSの指定があるかどうかは気にしない）
			$loadjs  = &fcts::forsafety( $setdat{'imageexpandingjs'}  );
			$loadcss = &fcts::forsafety( $setdat{'imageexpandingcss'} );
		}
	}

	# Lightbox本体JS＋CSSの読み込み
	$ret .= q|
		<script type="text/javascript">
			var delaycss = document.createElement('link');
			delaycss.rel = 'stylesheet';
			delaycss.href = '| . $loadcss  . q|';
			document.head.appendChild(delaycss);
		</script>
		<script src="| . $loadjs . q|" type="text/javascript"></script>
	|;

	return &fcts::tooneline($ret);
}

# ---------------------------------------
# ADMIN:IMAGES:画像ファイルのリストアップ		※ファイル数の個数上限とファイルサイズの総計上限も計算して、フラグを操作する
# ---------------------------------------
sub listupImageFiles
{
	# --------------------------------------
	# 画像用ディレクトリのファイル一覧を得る
	opendir( DIRECTORY, $imagefolder ) or &errormsg("画像UP用ディレクトリを開けませんでした。");
	my @filelist = readdir( DIRECTORY );
	closedir( DIRECTORY );

	# ------------------------------------------
	# 画像ファイルだけをリストアップして情報取得
	my @ifiles;
	my $totalfiles = 0;	# ファイル総数(兼カウンタ)
	my $totalsize = 0;	# ファイルサイズの集計用

	foreach my $of (@filelist) {
		# 画像ファイルかどうか（※指定拡張子で終わるファイル名）
		if( $of =~ m/\.($setdat{'imageallowext'})/i ) {
			# 対象拡張子だったら情報を取得して配列に格納
			my $fp = "$imagefolder/$of";
			my @fs = stat $fp;
			$ifiles[$totalfiles][1] = $of;			# ファイル名
			$ifiles[$totalfiles][2] = $fs[7]; 		# サイズ(Bytes)
			$totalsize += $fs[7];	# ファイルサイズの合計を計算する
			$ifiles[$totalfiles][3] = &fcts::datetojpstyle( &fcts::getdatetimestring( $fs[9] )); # 更新時刻（表示用）
			if( $of =~ m/(\d{14,})-\w+/ ) {
				# ファイル名の先頭に日付数字があればそれをソート用日付として採用する
				$ifiles[$totalfiles][0] = $1;
			}
			else {
				# ファイル更新時刻からソート用の日付文字列を作る（YYYYMMDDhhmmss）
				$ifiles[$totalfiles][0] = &fcts::getNowDateForFileName( 1, $fs[9] );
			}
			$totalfiles++;	# 画像個数カウンタを進める
		}
	}

	# ソート(辞書順で降順)
	@ifiles = sort { $b->[0] cmp $a->[0] } @ifiles;		# 2次元配列を1要素目の値を文字列としてソート (注:数値として比較すると同時投稿時の15桁数値が先に出てしまって意図通りのソートにならない。)

# foreach my $ref(@ifiles){
# 	&fcts::DEBUGOUT("@$ref");
# }

	# ページネーション計算
	my( $startid, $endid, $endpage );
	( $startid, $endid, $endpage, $cp{'page'} ) = &fcts::calcpagenation( $totalfiles, $setdat{'imageperpage'}, $cp{'page'} );

	# ------------------------------
	# 画像ファイルリスト表の表示準備
	my $cgipath = &getCgiPath();
	my $res = q|
		<script type="text/javascript">
			function allcheck( tf ) {
			   var ElementsCount = document.imageform.elements.length;
			   for( i=0 ; i<ElementsCount ; i++ ) {
			      document.imageform.elements[i].checked = tf;
			   }
			}
		</script>
	| . qq|
		<form action="$cgipath" method="post" name="imageform">
	| . "\n";

	my $resctrl = q|
			<p class="ctrlbox">
				<input type="button" value="全部選択" onclick="allcheck(true);">
				<input type="button" value="全部解除" onclick="allcheck(false);">
				：
				<span class="checkedCtrl">選択した画像を
				<select name="work">
					<option value="postwithimage">新規投稿に使う</option>
					<option value="imagetrydels">削除する</option>
				</select>
				<input type="hidden" value="admin" name="mode">
				<input type="submit" value="実行"></span>
			</p>
	| . "\n";

	# テーブルHTML格納用
	my $restable = q|<table class="images standard"><tr><th>＼</th><th>画像</th><th>投稿ID</th><th>UP日時</th><th>サイズ</th><th>使用場所</th></tr>| . "\n";

	# ファイル情報から表示用のテーブル中身を作る
	my $count = 0;
	foreach my $onefile (@ifiles) {
		# ファイル情報を得る
		my $of = @{$onefile}[1];	# Filename
		my $os = @{$onefile}[2];	# Size
		my $ot = @{$onefile}[3];	# Time
		# ファイルパスを作る
		my $fp = "$imagefolder/$of";
		# 表示対象ページ内の場合にだけ、文字列を作成
		$count++;
		if( $count >= $startid && $count <= $endid ) {
			# 画像サイズを得る
			my ($iwidth,$iheight) = &fcts::getImageWidthHeight($fp);
			my $imgwh = '<p class="widthheight nosize">縦横サイズ取得できず</p>';
			my $imgatts = '';
			if( $iwidth > 0 && $iheight > 0 ) {
				$imgwh = qq|<p class="widthheight">$iwidth × $iheight <span class="sunit">(px)</span></p>|;
				$imgatts = qq| width="$iwidth" height="$iheight"|;
			}

			# その他の処理
			my $fsu = &fcts::byteswithunit( $os );	# ファイルサイズを単位付き容量に変換
			my $imgupid = '－';
			if( $of =~ /\d+-(\w+)\..*/ ) { $imgupid = $1; }	# ファイル名から投稿IDを抽出
			$of = &fcts::forsafety($of);
			my $usepostlink = &makeQueryString("q=[PICT:$of]");	# その画像を使用している投稿を探して見るためのURLを作る
			my $uselistlink = &makeQueryString('mode=admin','work=manage',"q=[PICT:$of]");	# その画像を使用している投稿を管理画面の一覧で見るためのURLを作る
			$restable .= qq|<tr onmouseover="doubleHover('i$count');" onmouseout="doubleOut('i$count');" class="i$count" id="tr$of"><td class="imgid" rowspan="2"><label><input type="checkbox" name="filename" value="$of">$count</label></td><td rowspan="2"><a href="$fp" data-lightbox="tegalogimage" data-title="埋め込む際の記述&#10145; [PICT:$of]"><img src="$fp"$imgatts class="thumbnail" alt="※画像が表示されない場合はトラブルシューティング(リンクはこのページ下部)をご参照下さい。" loading="lazy"></a>$imgwh</td><td class="imgupid" >$imgupid</td><td class="imguptime">$ot</td><td class="size">$fsu</td><td rowspan="2"><a href="$usepostlink" class="btnlink uselink">投稿を見る</a><a href="$uselistlink" class="btnlink uselink">一覧で見る</a></td></tr>\n|;
			$restable .= qq|<tr onmouseover="doubleHover('i$count');" onmouseout="doubleOut('i$count');" class="i$count"><td class="embcode" colspan="3">埋込コード：<span><input type="text" id="pcode$count" value="[PICT:$of]" readonly><a href="#" class="btnlink embcopy" onclick="copyTextToClipboard('pcode$count'); return false;">COPY</a></span></td></tr>\n|;
		}
		# 表示する分が過ぎたらループを終わる
		if( $count > $endid ) {
			last;
		}
	}

	# 埋め込みコードコピー用JavaScript
	$restable .= '<script>function copyTextToClipboard( targetId ) { var targetEmt = document.getElementById(targetId); targetEmt.select(); document.execCommand("copy"); }</script>';

	# 制限超過確認：ファイル総数またはファイルサイズ総量が制限値に達したらフラグを操作
	my $befflag = $setdat{'imagelimitflag'};
	if(( $totalfiles >= $setdat{'imagefilelimit'} ) || ( $totalsize >= $setdat{'imagestoragelimit'} )) {
		$setdat{'imagelimitflag'} = 1;
	}
	else {
		$setdat{'imagelimitflag'} = 0;
	}

	# フラグが変わったら、設定ファイルのフラグを更新
	if( $befflag != $setdat{'imagelimitflag'} ) {
		my @trywrites;
		push( @trywrites, "imagelimitflag=" . $setdat{'imagelimitflag'} );
		&savesettings( @trywrites );
	}

	# 画像ファイルが1つもない場合
	if( $totalfiles == 0 ) {
		$restable .= '<tr><td colspan="6">※まだ1つもアップロードされていません。</td></tr>';
	}

	$restable .= '</table>' . "\n";

	# ページリンク用のベースリンクを生成
	my $baselink = &makeQueryString('mode=admin', 'work=images', 'page=');

	# (複数ページある場合は)ページ番号リストリンクを生成する
	my $pagenumomission = $setdat{'syspagelinkomit'} || 0;	# P番号の途中を省略(1:する/0:しない)
	my $respagelist = '<p class="pagelist">' . &fcts::outputPageListLinks(
		$endpage, $cp{'page'}, '', '', '',		# 引数1:総ページ数、引数2:現在P番号、引数3:P番号左側記号、引数4:P番号右側記号、引数5:P番号境界記号
		1, $pagenumomission, '…', 'btnlink',	# 引数6:番号の表示精度、引数7:P番号の途中を省略(1:する/0:しない)、引数8:途中P省略記号、引数9:付加class名
		$baselink	# 引数10以降:リンクに付加するパラメータベース
	) . "</p>\n";

	# (複数ページある場合は)ページ移動リンクを表示：次ページがあれば出力。前ページがあれば出力。先頭へボタン・末尾へボタンもあると望ましい。
	my $pagelink = &fcts::outputPagenationLinks( $cp{'page'}, $endpage, $setdat{'imageperpage'}, $baselink );

	# 使用量ステータス
	my $resstatus = '<p class="storageStatus">(使用容量: <b>' . &fcts::byteswithunit($totalsize) . '</b> / 全 ' . $totalfiles . '個)</p></form><!-- /.imageform -->';

	return $res . $respagelist . $resctrl . $restable . $pagelink . $resstatus;
}

# --------------------------------------
# 画像削除(確認＋本番)共通の事前確認処理	※sub adminImageTrydels と adminDeleteImages から呼ばれる。
# --------------------------------------	返値：削除対象ファイルが限定されている場合に限って、許可対象のユーザ名を返す。限定されない場合は空文字を返す。
sub commonPrepForDeleteImage
{
	# 設定確認
	if( $setdat{'imageupallow'} == 0 ) {
		my $msg = '<p class="important"><strong>削除できません</strong></p><p>画像の投稿が設定で禁止されている間は、削除もできません。<br>設定を変更するか、または別途FTPなどの手段で削除して下さい。</p>';
		&showadminpage('NO PERMISSION','',$msg,'CIA','');
		exit;
	}

	# ----------------------
	# ログイン確認・権限取得
	# ----------------------
	my $permittedid = &fcts::checkpermission();		# ログイン中ユーザのID名が得られる
	if( !$permittedid ) {
		# ユーザIDを確認できない場合はログイン画面へ送る
		&passfront( &makeQueryString('mode=admin') );
		exit;
	}
	my $plv = &fcts::getUserDetail($permittedid, 1);	# ログイン中ユーザの権限値

	# --------
	# 権限確認
	# --------
	if( $plv < $setdat{'imageuprequirelevel'} ) {
		# 画像UPに必要な権限がなければ、削除も拒否
		my $msg = '<p class="important">画像の投稿に必要な権限がないため、削除もできません。</p>';
		&showadminpage('NO PERMISSION','',$msg,'CIA','');
		exit;
	}

	# 削除対象ファイルが限定される権限のIDでログインしている場合に限って、許可対象のユーザ名を返す。
	if( $plv < 7 ) {
		return $permittedid;
	}

	# 削除対象ファイルが限定されない場合は空文字を返す。
	return '';
}

# -----------------------------
# ADMIN：既存画像の削除確認画面		※メモ：呼び出し元(modeAdmin)の制限で、Lv.1ではこのサブルーチンは実行されないハズ。(実行されても問題はないが。)
# -----------------------------
sub adminImageTrydels
{
	# 画像の削除(TRY)
	my @trydels = $cgi->param('filename');	# 指定されたファイル名一覧
	my $msg = '';

	# 不正送信の確認
	&fcts::postsecuritycheck('work=imagetrydels');

	# 画像削除時の共通事前確認処理(※削除可能ファイルが限定される場合には、限定対象ユーザ名が返る。限定されなければ空文字。)
	my $dellimit = &commonPrepForDeleteImage();

	# --------------
	# 削除候補の表示
	# --------------
	if( $trydels[0] ne '' ) {
		# 削除候補が1つ以上存在すれば
		my $cgipath = &getCgiPath();
		$msg = qq|
			<p>画像保存用ディレクトリの中から、以下の画像ファイルを削除します。よろしいですか？（削除すると取り消せません。）</p>
			<form action="$cgipath" method="post">
				<table class="managetable" cellpadding="0"><tr><th>ファイル名</th><th>プレビュー</th></tr>
		|;
		foreach my $oi (@trydels) {
			# 削除対象をチェック
			if( $dellimit ne '' ) {
				# 削除可能なファイル名が限定されている場合
				if( $oi =~ /\d+-(\w+)\..*/ ) {
					# ユーザID付きのファイル名ならチェック
					if( $1 eq $dellimit ) {
						# 削除が許可されているファイルなら、削除処理対象に加える
						$msg .= qq|<tr><td>$oi</td><td><img src="$imagefolder/$oi" class="thumbnail" alt="削除可能画像"><input type="hidden" value="$oi" name="trydelete"></td></tr>|;
					}
					else {
						# 許可されていないファイルなら拒否
						$msg .= qq|<tr><td class="important">他者がUPした画像は、<br>現在のIDの権限では削除できません</td><td><img src="$imagefolder/$oi" class="thumbnail" alt="削除不可画像"></td></tr>|;
					}
				}
				else {
					# ユーザ名の付かない汎用ファイル名なら拒否
					$msg .= qq|<tr><td class="important">投稿者不明の画像は、<br>現在のIDの権限では削除できません</td><td><img src="$imagefolder/$oi" class="thumbnail" alt="削除不可画像"></td></tr>|;
				}
			}
			else {
				# 削除可能ファイルが限定されていなければ、全部削除可能
				$msg .= qq|<tr><td>$oi</td><td><img src="$imagefolder/$oi" class="thumbnail" alt=""><input type="hidden" value="$oi" name="trydelete"></td></tr>|;
			}
		}
		$msg .= qq|
				</table>
				<input type="hidden" value="admin" name="mode">
				<input type="hidden" value="deleteimages" name="work">
				<input type="submit" value="上記の画像を削除する">
				&nbsp;<input type="button" value="中止して戻る" onClick="history.back();"><br>
			</form>
		|;
	}
	else {
		# 削除候補が1つもなければ
		$msg = qq|<p>削除する画像が1つも選択されていません。</p>|;
	}

	my $css = '<style type="text/css">.thumbnail { width:auto; max-width: 150px; height: auto; max-height:300px; vertical-align: middle; }</style>';

	&showadminpage('DELETE IMAGES','',$msg,'CIA',$css);
}

# -------------------------
# ADMIN：既存画像の削除処理		※メモ：呼び出し元(modeAdmin)の制限で、Lv.1ではこのサブルーチンは実行されない。(実行されても問題はないが。)
# -------------------------
sub adminDeleteImages
{
	# 画像の削除(TRY)
	my @trydels = $cgi->param('trydelete');	# 指定されたファイル名一覧
	my $msg = '<p>削除処理結果：</p><ul class="deletelist">';

	# 不正送信の確認
	&fcts::postsecuritycheck('work=deleteimages');

	# 画像削除時の共通事前確認処理(※削除可能ファイルが限定される場合には、限定対象ユーザ名が返る。限定されなければ空文字。)
	my $dellimit = &commonPrepForDeleteImage();

	if( $dellimit ne '' ) {
		# 削除可能なファイル名が限定されている場合は、削除候補をチェックして許可ファイル以外を除外する
		foreach my $oi (@trydels) {
			if( $oi =~ /\d+-(\w+)\..*/ ) {
				# ユーザID付きのファイル名ならチェック
				if( $1 ne $dellimit ) {
					# 削除が許可されていないファイル(＝ログイン中のIDでUPした画像ではない)なら削除対象から除外
					$oi = '';
				}
			}
			else {
				# ユーザIDなしのファイルなら削除対象から除外
				$oi = '';
			}
		}
	}

	# ファイルが存在していれば消す
	my $count = 0;
	foreach my $of ( @trydels ) {
		if( $of ne '' ) {
			# 文字列があれば、画像用ディレクトリ名を加えてファイルパスを作る
			$of = $imagefolder . '/' . $of;
			# そのファイルの存在を確認
			if( -f $of ) {
				# あれば消す
				unlink( $of );
				$msg .= '<li>削除しました: ' . &fcts::forsafety($of) . "</li>\n";
				$count++;
			}
			else {
				# ない場合は報告
				$msg .= '<li>見つかりません: ' . &fcts::forsafety($of) . "</li>\n";
			}
		}
	}

	$msg .= '</ul><p>計 ' . $count . '個の画像ファイルを削除しました。</p>';

	# CSS
	my $css = q|<style tyle="text/css">
		@media (max-width: 599px) {
			.deletelist { font-size:0.8em; margin: 0.75em 0; padding: 0 0 0 1em; line-height: 1; }
			.deletelist li { margin-bottom:1em; }
		}
		</style>
	|;

	&showadminpage('DELETED','',$msg,'CIA',$css);
}

# -----------------------
# ADMIN：編集削除一覧画面
# -----------------------
sub adminManage
{
	# ログイン確認・権限取得
	my $permittedid = &fcts::checkpermission();		# ログイン中ユーザのID名が得られる
	if( !$permittedid ) {
		# ユーザIDを確認できない場合：エラーメッセージ
		&errormsg('ログインしていません。');
		exit;
	}
	my $plv = &fcts::getUserDetail($permittedid, 1);	# ログイン中ユーザの権限値

	# --------------------
	# 既存投稿の管理(削除)
	my $cgipath = &getCgiPath();
	my $msg = qq|
		<p>既存の投稿を削除/再編集/表示します。</p>
		<ul class="sysguide">
			<li>投稿を<strong>削除</strong>したい場合は、左端のNo.欄にチェック<input type="checkbox" checked>を入れて、「選択した投稿を削除」ボタンを押して下さい。（複数の投稿を同時に削除できます。）</li>
			<li>投稿を<strong>編集</strong>したい場合は、右端の編集欄にある<span class="smallbutton">Edit.00</span>ボタンをクリックして下さい。</li>
			<li>投稿を<strong>表示</strong>したい場合は、投稿内容抜粋をクリックして下さい。（その投稿の単独ページに移動します。）</li>
		</ul>
	| . "\n";

	# 絞り込み検索語の事前調整
	$cp{'search'} =~ s/　/ /g;		# 全角空白を半角空白にする
	$cp{'search'} =~ s/\s+/ /g;		# 空白系文字の連続を半角空白1つにする
	my $searchInput = &fcts::forsafety( $cp{'search'} );
	my $searchTitle = '絞り込み';
	if( $searchInput ne '' ) { $searchTitle = q|<span class="filtered">絞り込み中</span>|; }

	# 調整ヘッダとテーブルヘッダ
	my $restable = qq|
		<div class="headForm">
			<input type="button" value="下記にチェックを入れた投稿を削除" onclick="document.getElementById('DelPostBtn').click();" style="margin-right:1em;">
			<form action="$cgipath" method="get">
				▼$searchTitle：<input type="search" name="q" value="$searchInput" placeholder="任意の検索語・カテゴリID・投稿日付等" class="filteringBox"><input type="submit" value="検索">
				<input type="hidden" value="admin" name="mode">
				<input type="hidden" value="manage" name="work">
			</form>
		</div>
		<form action="$cgipath" method="post">
			<table class="managetable" cellpadding="0"><tr><th>投稿番号</th><th>投稿内容抜粋</th><th>投稿日時</th><th>カテゴリID</th><th>ユーザID</th><th>編集</th></tr>
	| . "\n";

	# データを走査して対象投稿を表示用に整形しつつ抜き出す
	my $totalclips = 0;
	my $permittedposts = 0;
	my $filteredposts = 0;
	my @posttable = ();
	foreach my $oneclip (@xmldata) {
		# 分解
		my $id		= &fcts::forsafety( &fcts::getcontent($oneclip,'id') );
		my $date	= &fcts::forsafety( &fcts::getcontent($oneclip,'date') );
		my $user	= &fcts::forsafety( &fcts::getcontent($oneclip,'user') );
		my $cats	= &fcts::forsafety( &fcts::getcontent($oneclip,'cat') );		# カテゴリCSV
		my $flags	= &fcts::forsafety( &fcts::getcontent($oneclip,'flag') );		# フラグCSV
		my $comment	= &fcts::forsafety( &fcts::getcontent($oneclip,'comment') );
		my $comstr	= &fcts::mbSubstr( &fcts::forsafety( &deletedecos( &fcts::safetycuttag( &fcts::getcontent($oneclip,'comment') ) ) ), 90, '...');	# タグを除外した上でエスケープしたコメントから最大90文字を切り抜き
		# リンク作成
		my $postlink = &makeQueryString("postid=$id");
		my $userlink = &makeQueryString('mode=admin','work=manage',"q=$user");
		# 表示
		if(( $plv >= 7 ) || ( $user eq $permittedid )) {
			# 権限がLv.7以上か、または自分の投稿なら
			my $showflag = 1;
			if( $searchInput ne '' ) {
				# 絞り込み検索語が指定されていれば検索する
				my $searchstring = "$id $date $user $cats $flags $comment";

				# 検索を実行
				if( &fcts::wordsearch($searchstring,$cp{'search'}) == 0 ) {
					# 非該当ならフラグを下ろす
					$showflag = 0;
				}
			}
			# フラグが立っていれば追加
			if( $showflag ) {
				my $lineclass = '';
				# フラグ確認
				my $flaglinks = '';
				if( $flags =~ /draft/ )	{ $flaglinks .= '<a href="' . &makeQueryString('mode=admin','work=manage','q=draft') . '">下書き</a> '; $lineclass = ' class="draft"'; }
				if( $flags =~ /rear/ )	{ $flaglinks .= '<a href="' . &makeQueryString('mode=admin','work=manage','q=rear') . '">下げる</a> '; }
				# 追加
				push( @posttable, qq|<tr$lineclass><td class="mtid"><label class="choiceid"><input type="checkbox" name="postid" value="$id">$id</label></td><td class="mttitle"><a href="$postlink" class="mttlink">$comstr</a></td><td class="mttime">$date</td><td class="mtcat">$flaglinks$cats</td><td class="mtuser"><a href="$userlink">$user</a></td><td><a href="?mode=edit&amp;postid=$id" class="smallbutton">Edit.$id</a></td></tr>\n| );
				$filteredposts++;
			}
			$permittedposts++;
		}
		$totalclips++;
	}
	if( $totalclips == 0 ) {
		# 投稿が1件もなかったら
		push( @posttable, qq|<tr><td colspan="6">まだ1件も投稿されていません。</td></tr>\n| );
	}
	elsif( $filteredposts == 0 ) {
		# 編集可能な投稿が1件もない場合
		push( @posttable, qq|<tr><td colspan="6">条件に合致する投稿がないか、またはあなたの権限で編集可能な投稿が1件もありません。</td></tr>\n| );
	}

	# ページネーション計算
	my( $startid, $endid, $endpage );
	( $startid, $endid, $endpage, $cp{'page'} ) = &fcts::calcpagenation( $filteredposts, $setdat{'postperpageforsyslist'}, $cp{'page'} );

	# 表示すべきデータだけを出力
	for( my $i = $startid; $i <= $endid; $i++ ){
		$restable .= $posttable[($i - 1)];
	}
	$restable .= "</table>\n";

	# ページリンク用のベースリンクを生成
	my $uesearch = &fcts::urlEncode( $searchInput );	# #記号をエンコードしておく
	my $baselink = &makeQueryString('mode=admin', 'work=manage', "q=$uesearch", 'page=');

	# (複数ページある場合は)ページ番号リストリンクを生成する
	my $pagenumomission = $setdat{'syspagelinkomit'} || 0;	# P番号の途中を省略(1:する/0:しない)
	my $respagelist = '<p class="pagelist">' . &fcts::outputPageListLinks(
		$endpage, $cp{'page'}, '', '', '',		# 引数1:総ページ数、引数2:現在P番号、引数3:P番号左側記号、引数4:P番号右側記号、引数5:P番号境界記号
		1, $pagenumomission, '…', 'btnlink',	# 引数6:番号の表示精度、引数7:P番号の途中を省略(1:する/0:しない)、引数8:途中P省略記号、引数9:付加class名
		$baselink	# 引数10以降:リンクに付加するパラメータベース
	) . "</p>\n";

	# (複数ページある場合は)ページ移動リンクを表示
	my $pagelink = &fcts::outputPagenationLinks( $cp{'page'}, $endpage, $setdat{'postperpageforsyslist'}, $baselink );

	# 1ページあたりの表示投稿数
	my $postperpageforsyslist = &fcts::forsafety($setdat{'postperpageforsyslist'});

	$msg .= $respagelist . $restable;
	$msg .= qq|
			<input type="hidden" value="admin" name="mode">
			<input type="hidden" value="trydels" name="work">
			$pagelink
			<input type="submit" value="選択した投稿を削除" id="DelPostBtn"><br>
		</form>
		<p>※存在する投稿は、合計<b class="total">$totalclips</b>個です。<br>
		※あなたの権限で編集や削除が可能な投稿は、合計<b class="total">$permittedposts</b>個です。<br>
		※現在の絞り込み条件に該当する投稿は、<b class="total">$filteredposts</b>個です。</p>
		<p class="noticebox">
			※1ページあたり<b> $postperpageforsyslist </b>件を表示する設定になっています。この設定は、<a href="?mode=admin&amp;work=setting&amp;page=4">システム設定</a>画面から変更できます。
		</p>
	|;

	# CSS
	my $css = q|<style tyle="text/css">
		.headForm { margin: 1em 0; }
		.headForm form { margin: 0.5em 0 0 0; display: inline-block; }
		.filteringBox { width: 250px; max-width: 35vw; }
		.filteringBox::placeholder { color:#888; }
		.filtered { color:crimson; font-weight:bold; }
		.choiceid { cursor:pointer; } .choiceid:hover { background-color:#eff; color:blue; }
		.mttitle { min-width:7em; }
		.mttitle .mttlink { display:block; overflow:hidden; }
		.mttime { white-space:nowrap; }
		.mtcat, .mtuser { min-width:2.5em; }
		.total { margin:0 3px; }
		.draft td { background-color:#f5f5f5; }
		@media all and (max-width: 599px) {
			.mttitle .mttlink { font-size: 0.7em; max-height:5em; }
		}
		@media (min-width: 600px) and (max-width: 1200px) {
			.managetable, .mttime  { font-size:0.9em; }
		}
		@media (min-width: 600px) {
			.mttitle .mttlink { max-width:50vw; text-overflow:ellipsis; white-space:nowrap; }
		}
	</style>|;

	&showadminpage('MANAGE POSTS','',$msg,'CA',$css);
}

# --------------------
# 独自の各種記法を削除	(投稿本文の冒頭最大90文字を抜粋する用途なので、装飾記法ではない角括弧も消えてしまう「ざっくり削除」だが、まあ問題ないとしておく。)
# --------------------
sub deletedecos
{
	my $str = shift @_ || '';

	$str =~ s/\\([\[:])/$1/g;			# 開始角括弧とコロンのエスケープ記法から、先頭の「\」記号を削除

	$str =~ s/\[PICT:.+\.(.+?)\]/(画像:$1)/ig;	# 画像記法を置き換え
	$str =~ s|\[IMG:(.+?)]https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+|(画像:$1)|ig;	# 外部画像記法を置き換え
	$str =~ s|\[Tweet\]https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+|(ツイート)|ig;	# ツイート記法を置き換え
	$str =~ s|\[YouTube\]https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+|(動画)|ig;		# 動画記法を置き換え

	$str =~ s/\[>(\d+)\]/$1/g;			# 特定No.リンクのリンク部分を削除
	$str =~ s/\[>\d+:(.+?)\]/$1/g;		# ラベル付き特定No.リンクのリンク部分を削除

	$str =~ s|\[(.+?)]https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+|(リンク:$1)|ig;	# リンク記法を置き換え (あらゆるリンク記法より後に実行する必要がある)

	$str =~ s/\[[A-Z]:[A-Za-z0-9]+://g;	# 英大文字1文字＋オプションによる装飾記法の開始部分を削除
	$str =~ s/\[[A-Z]://g;				# 英大文字1文字による装飾記法の開始部分を削除

	$str =~ s/\[([^\[\]]+?)\]/髜馞$1靏驎/g;	# 対応が取れている半角角括弧を一時的にエスケープしておく
	$str =~ s/[\[\]]//g;					# 半角角括弧を全部削除(主に閉じ角括弧を削除する目的)
	$str =~ s/髜馞([^\[\]]+?)靏驎/[$1]/g;	# 対応が取れている半角角括弧のエスケープを解除する

	return $str;
}

# -------------------------
# ADMIN：削除処理の確認画面
# -------------------------
sub adminTrydels
{
	my $permittedid = shift @_ || '';	# アクセスユーザID
	my $permitlevel = shift @_ || 0;	# アクセス権限値(1～9)

	# 投稿の削除(TRY)
	my @ids = $cgi->param('postid');	# ※ここではmulti_paramを使いたいのだが、古い環境では使えないので、今のところは保留。
	my $msg;

	if( $#ids > 0 ) {
		# 不正送信の確認 (削除対象が1つだけの場合はこの方法でのチェックはしない。個別削除ボタン用URLでの呼び出しに対応するため。)
		&fcts::postsecuritycheck('work=trydels');
	}

	if( $flagDebug{'ShowDebugStrings'} == 1 ) {
		my $trydeletes = join( "," , @ids );
		print STDERR "[TRYDELETES] $trydeletes\n\n";
	}

	if( $ids[0] ne '' ) {
		# 削除候補が1つ以上存在すれば
		my $cgipath = &getCgiPath();
		$msg = qq|
			<form action="$cgipath" method="post">
				<table class="managetable" cellpadding="0"><tr><th></th><th>投稿本文の冒頭</th><th>日付</th><th>ユーザID</th></tr>
		|;
		my $listupItems = 0;
		foreach my $oneclip (@xmldata) {
			foreach my $tryid ( @ids ) {
				if( $tryid eq &fcts::getcontent($oneclip,'id') ) {
					# 削除候補と一致したら
					# 分解
					my $id		= &fcts::forsafety( &fcts::getcontent($oneclip,'id') );
					my $date	= &fcts::forsafety( &fcts::getcontent($oneclip,'date') );
					my $user	= &fcts::forsafety( &fcts::getcontent($oneclip,'user') );
					my $comstr	= &fcts::mbSubstr( &fcts::forsafety( &fcts::getcontent($oneclip,'comment') ), 36);	# コメントを36文字だけ切り抜き

					if(( $permitlevel >= 7 ) || ( $permittedid eq $user )) {
						# 権限がLv.7以上 または 投稿IDとログインIDが同じ場合のみリストアップする
						$msg .= qq|<tr><td class="mtid">No.$id<input type="hidden" value="$id" name="trydelete"></td><td class="mttitle"><a href="?postid=$id" target="_blank">$comstr</a></td><td class="mttime">$date</td><td class="mtuser">$user</td></tr>|;
						$listupItems++;
					}
					else {
						# 削除権限がない場合
						$msg .= qq|<tr><td class="mtid">No.$id</td><td class="mttitle" colspan="2"><strong class="important">この投稿の削除権限がありません。</strong></td><td class="mtuser">$user</td></tr>|;
					}
				}
			}
		}
		$msg .= '</table>';

		# 削除可能な数に応じた表示
		if( $listupItems > 0 ) {
			# 削除権限のある対象が1件以上ある場合のみ、確認文章と削除用ボタンを出力
			$msg = qq|<p>以下の投稿を<strong class="important">削除</strong>します。よろしいですか？</p>| . $msg . qq|<input type="hidden" value="write" name="mode"><input type="submit" value="削除する">&nbsp;|;
		}
		else {
			# 削除権限のある対象がない場合
			$msg = qq|<p>下記の投稿は、あなたに削除する権限がありません。</p>| . $msg;
		}

		# 共通の末尾HTML
		$msg .= qq|
				<input type="button" value="中止して戻る" onClick="history.back();"><br>
			</form>
		|;
	}
	else {
		# 削除候補が1つもなければ
		$msg = qq|<p>削除する投稿が1つも選択されていません。</p>|;
	}

	&showadminpage('DELETE POSTS','',$msg,'CA');
}

# ---------------
# ADMIN：設定画面
# ---------------
sub adminSetting
{
	# ------------------------
	# 設定ファイルの更新(FORM)
	# ------------------------
	$setdat{'freespace'} =~ s/<br>/\r\n/g;	# フリースペースの改行変換

	# プルダウンメニューの設定状況を反映
	my @separatepoint = ('','','','');		$separatepoint[$setdat{'separatepoint'}] = 'selected';
	my @separateoption = ('','');			$separateoption[$setdat{'separateoption'}] = 'selected';
	my @utilitycat = ('','','');			$utilitycat[$setdat{'utilitycat'}] = 'selected';
	my @hashtagsort = ('','','','','');		$hashtagsort[$setdat{'hashtagsort'}] = 'selected';
	my @readmorestyle = ('','','');			$readmorestyle[$setdat{'readmorestyle'}] = 'selected';
	my @ogdescription = ('','');			$ogdescription[$setdat{'ogdescription'}] = 'selected';
	my @ogtype = ('','','');				$ogtype[$setdat{'ogtype'}] = 'selected';
	my @twittercard = ('','');				$twittercard[$setdat{'twittercard'}] = 'selected';
	my @freehomeatt = ('','','');			$freehomeatt[$setdat{'freehomeatt'}] = 'selected';
	my @conpanecolortheme = ('','','','','','','');	$conpanecolortheme[$setdat{'conpanecolortheme'}] = 'selected';
	my @aboutcgibox = ('','','','');		$aboutcgibox[$setdat{'aboutcgibox'}] = 'selected';

	# ラジオボタンの設定状況を反映
	my @situationvariation = ('','','');	$situationvariation[$setdat{'situationvariation'}] = 'checked';
	my @rssskin = ('','','');				$rssskin[$setdat{'rssskin'}] = 'checked';
	my @urllinktarget = ('','','');			$urllinktarget[$setdat{'urllinktarget'}] = 'checked';
	my @urlexpandtwtheme = ('','','');		$urlexpandtwtheme[$setdat{'urlexpandtwtheme'}] = 'checked';
	my @nocatshow = ('','','');				$nocatshow[$setdat{'nocatshow'}] = 'checked';
	my @usericonsource = ('','');			$usericonsource[$setdat{'usericonsource'}] = 'checked';
	my @unknownusericon = ('','');			$unknownusericon[$setdat{'unknownusericon'}] = 'checked';
	my @fixedpostdate = ('','','','');		$fixedpostdate[$setdat{'fixedpostdate'}] = 'checked';
	my @alwaysshowquickpost = ('','');		$alwaysshowquickpost[$setdat{'alwaysshowquickpost'}] = 'checked';
	my @afterpost = ('','','');				$afterpost[$setdat{'afterpost'}] = 'checked';
	my @imagedefaultplace = ('','','','');	$imagedefaultplace[$setdat{'imagedefaultplace'}] = 'checked';
	my @isuselightbox = ('','','');			$isuselightbox[$setdat{'isuselightbox'}] = 'checked';
	my @showImageUpBtn = ('','','');		$showImageUpBtn[$setdat{'showImageUpBtn'}] = 'checked';
	my @showDecoBtnStyle = ('','','');		$showDecoBtnStyle[$setdat{'showDecoBtnStyle'}] = 'checked';
	my @showLinkBtnStyle = ('','','');		$showLinkBtnStyle[$setdat{'showLinkBtnStyle'}] = 'checked';
	my @showHashtagBtnStyle = ('','','');	$showHashtagBtnStyle[$setdat{'showHashtagBtnStyle'}] = 'checked';
	my @showCategoryBtnStyle = ('','','');	$showCategoryBtnStyle[$setdat{'showCategoryBtnStyle'}] = 'checked';
	my @showFuncBtnStyle = ('','','');		$showFuncBtnStyle[$setdat{'showFuncBtnStyle'}] = 'checked';
	my @howtogetfullpath = ('','');			$howtogetfullpath[$setdat{'howtogetfullpath'}] = 'checked';
	my @howtogetdocroot = ('','');			$howtogetdocroot[$setdat{'howtogetdocroot'}] = 'checked';

	# チェックボックス(1:ON/0:OFFで記録)用の属性値を作る
	$setdat{'onepostpagesituation'}	= &getattributeforcheckbox($setdat{'onepostpagesituation'});
	$setdat{'onepostpageutilitybox'}= &getattributeforcheckbox($setdat{'onepostpageutilitybox'});
	$setdat{'situationcount'}		= &getattributeforcheckbox($setdat{'situationcount'});
	$setdat{'situationpage'}		= &getattributeforcheckbox($setdat{'situationpage'});
	$setdat{'situationalwayspage'}	= &getattributeforcheckbox($setdat{'situationalwayspage'});
	$setdat{'utilitystate'}			= &getattributeforcheckbox($setdat{'utilitystate'});
	$setdat{'utilityrandom'}		= &getattributeforcheckbox($setdat{'utilityrandom'});
	$setdat{'utilitydates'}			= &getattributeforcheckbox($setdat{'utilitydates'});
	$setdat{'utilitydateymd'}		= &getattributeforcheckbox($setdat{'utilitydateymd'});
	$setdat{'utilitydateym'}		= &getattributeforcheckbox($setdat{'utilitydateym'});
	$setdat{'utilitydatey'}			= &getattributeforcheckbox($setdat{'utilitydatey'});
	$setdat{'utilitydatemd'}		= &getattributeforcheckbox($setdat{'utilitydatemd'});
	$setdat{'utilitydated'}			= &getattributeforcheckbox($setdat{'utilitydated'});
	$setdat{'utilityedit'}			= &getattributeforcheckbox($setdat{'utilityedit'});
	$setdat{'rssoutput'}			= &getattributeforcheckbox($setdat{'rssoutput'});
	$setdat{'xmlsitemapoutput'}		= &getattributeforcheckbox($setdat{'xmlsitemapoutput'});
	$setdat{'sitemappageoutput'}	= &getattributeforcheckbox($setdat{'sitemappageoutput'});
	$setdat{'sitemappagedatebar'}	= &getattributeforcheckbox($setdat{'sitemappagedatebar'});
	$setdat{'sitemappagefixed'}		= &getattributeforcheckbox($setdat{'sitemappagefixed'});
	$setdat{'sitemapsituation'}		= &getattributeforcheckbox($setdat{'sitemapsituation'});
	$setdat{'galleryoutput'}		= &getattributeforcheckbox($setdat{'galleryoutput'});
	$setdat{'gallerydatebar'}		= &getattributeforcheckbox($setdat{'gallerydatebar'});
	$setdat{'gallerysituation'}		= &getattributeforcheckbox($setdat{'gallerysituation'});
	$setdat{'pagelinkuse'}			= &getattributeforcheckbox($setdat{'pagelinkuse'});
	$setdat{'pagelinknum'}			= &getattributeforcheckbox($setdat{'pagelinknum'});
	$setdat{'pagelinkuseindv'}		= &getattributeforcheckbox($setdat{'pagelinkuseindv'});
	$setdat{'pagelinknextindvn'}	= &getattributeforcheckbox($setdat{'pagelinknextindvn'});
	$setdat{'pagelinkprevindvn'}	= &getattributeforcheckbox($setdat{'pagelinkprevindvn'});
	$setdat{'pagenumfigure'}		= &getattributeforcheckbox($setdat{'pagenumfigure'});
	$setdat{'pagenumomission'}		= &getattributeforcheckbox($setdat{'pagenumomission'});
	$setdat{'separatebarreverse'}	= &getattributeforcheckbox($setdat{'separatebarreverse'});
	$setdat{'separatebaroutput'}	= &getattributeforcheckbox($setdat{'separatebaroutput'});
	$setdat{'eppoverride'}			= &getattributeforcheckbox($setdat{'eppoverride'});
	$setdat{'postidlinkize'}		= &getattributeforcheckbox($setdat{'postidlinkize'});
	$setdat{'postidlinkgtgt'}		= &getattributeforcheckbox($setdat{'postidlinkgtgt'});
	$setdat{'allowdecorate'}		= &getattributeforcheckbox($setdat{'allowdecorate'});
	$setdat{'readherebtnuse'}		= &getattributeforcheckbox($setdat{'readherebtnuse'});
	$setdat{'readmorebtnuse'}		= &getattributeforcheckbox($setdat{'readmorebtnuse'});
	$setdat{'readmoreonsearch'}		= &getattributeforcheckbox($setdat{'readmoreonsearch'});
	$setdat{'readmorecloseuse'}		= &getattributeforcheckbox($setdat{'readmorecloseuse'});
	$setdat{'imagelazy'}			= &getattributeforcheckbox($setdat{'imagelazy'});
	$setdat{'imagetolink'}			= &getattributeforcheckbox($setdat{'imagetolink'});
	$setdat{'imagefullpath'}		= &getattributeforcheckbox($setdat{'imagefullpath'});
	$setdat{'imageaddclass'}		= &getattributeforcheckbox($setdat{'imageaddclass'});
	$setdat{'imagelightbox'}		= &getattributeforcheckbox($setdat{'imagelightbox'});
	$setdat{'imagewhatt'}			= &getattributeforcheckbox($setdat{'imagewhatt'});
	$setdat{'imagewhmax'}			= &getattributeforcheckbox($setdat{'imagewhmax'});
	$setdat{'imageoutdir'}			= &getattributeforcheckbox($setdat{'imageoutdir'});
	$setdat{'imageouturl'}			= &getattributeforcheckbox($setdat{'imageouturl'});
	$setdat{'imageshowallow'}		= &getattributeforcheckbox($setdat{'imageshowallow'});
	$setdat{'imageupallow'}			= &getattributeforcheckbox($setdat{'imageupallow'});
	$setdat{'imageupmultiple'}		= &getattributeforcheckbox($setdat{'imageupmultiple'});
	$setdat{'imageupsamename'}		= &getattributeforcheckbox($setdat{'imageupsamename'});
	$setdat{'imagemaxlimits'}		= &getattributeforcheckbox($setdat{'imagemaxlimits'});
	$setdat{'urlautolink'}			= &getattributeforcheckbox($setdat{'urlautolink'});
	$setdat{'urlnofollow'}			= &getattributeforcheckbox($setdat{'urlnofollow'});
	$setdat{'urlnoprotocol'}		= &getattributeforcheckbox($setdat{'urlnoprotocol'});
	$setdat{'urlexpandimg'}			= &getattributeforcheckbox($setdat{'urlexpandimg'});
	$setdat{'embedonlysamedomain'}	= &getattributeforcheckbox($setdat{'embedonlysamedomain'});
	$setdat{'urlimagelazy'}			= &getattributeforcheckbox($setdat{'urlimagelazy'});
	$setdat{'urlimageaddclass'}		= &getattributeforcheckbox($setdat{'urlimageaddclass'});
	$setdat{'urlimagelightbox'}		= &getattributeforcheckbox($setdat{'urlimagelightbox'});
	$setdat{'urlexpandyoutube'}		= &getattributeforcheckbox($setdat{'urlexpandyoutube'});
	$setdat{'urlexpandspotify'}		= &getattributeforcheckbox($setdat{'urlexpandspotify'});
	$setdat{'urlexpandtweet'}		= &getattributeforcheckbox($setdat{'urlexpandtweet'});
	$setdat{'allowlinebreak'}		= &getattributeforcheckbox($setdat{'allowlinebreak'});
	$setdat{'keepserialspaces'}		= &getattributeforcheckbox($setdat{'keepserialspaces'});
	$setdat{'hashtaglinkize'}		= &getattributeforcheckbox($setdat{'hashtaglinkize'});
	$setdat{'hashtagnokakko'}		= &getattributeforcheckbox($setdat{'hashtagnokakko'});
	$setdat{'searchoption'}			= &getattributeforcheckbox($setdat{'searchoption'});
	$setdat{'catidinsearch'}		= &getattributeforcheckbox($setdat{'catidinsearch'});
	$setdat{'usericonsize'}			= &getattributeforcheckbox($setdat{'usericonsize'});
	$setdat{'caladdweekrow'}		= &getattributeforcheckbox($setdat{'caladdweekrow'});
	$setdat{'fixedseparatepoint'}	= &getattributeforcheckbox($setdat{'fixedseparatepoint'});
	$setdat{'rearappearcat'}		= &getattributeforcheckbox($setdat{'rearappearcat'});
	$setdat{'rearappeartag'}		= &getattributeforcheckbox($setdat{'rearappeartag'});
	$setdat{'rearappeardate'}		= &getattributeforcheckbox($setdat{'rearappeardate'});
	$setdat{'rearappearsearch'}		= &getattributeforcheckbox($setdat{'rearappearsearch'});
	$setdat{'datelistShowYear'}		= &getattributeforcheckbox($setdat{'datelistShowYear'});
	$setdat{'datelistShowZero'}		= &getattributeforcheckbox($setdat{'datelistShowZero'});
	$setdat{'postphloginname'}		= &getattributeforcheckbox($setdat{'postphloginname'});
	$setdat{'postareaexpander'}		= &getattributeforcheckbox($setdat{'postareaexpander'});
	$setdat{'postcharcounter'}		= &getattributeforcheckbox($setdat{'postcharcounter'});
	$setdat{'postchangeidlink'}		= &getattributeforcheckbox($setdat{'postchangeidlink'});
	$setdat{'postautofocus'}		= &getattributeforcheckbox($setdat{'postautofocus'});
	$setdat{'postbuttonshortcut'}	= &getattributeforcheckbox($setdat{'postbuttonshortcut'});
	$setdat{'ogpoutput'}			= &getattributeforcheckbox($setdat{'ogpoutput'});
	$setdat{'ogimageuse1st'}		= &getattributeforcheckbox($setdat{'ogimageuse1st'});
	$setdat{'insertalttext'}		= &getattributeforcheckbox($setdat{'insertalttext'});
	$setdat{'allowbrinfreespace'}	= &getattributeforcheckbox($setdat{'allowbrinfreespace'});
	$setdat{'autobackup'}			= &getattributeforcheckbox($setdat{'autobackup'});
	$setdat{'conpanegallerylink'}	= &getattributeforcheckbox($setdat{'conpanegallerylink'});
	$setdat{'syspagelinkomit'}		= &getattributeforcheckbox($setdat{'syspagelinkomit'});
	$setdat{'sysdelbtnpos'}			= &getattributeforcheckbox($setdat{'sysdelbtnpos'});
	$setdat{'exportpermission'}		= &getattributeforcheckbox($setdat{'exportpermission'});
	$setdat{'loadeditcssjs'}		= &getattributeforcheckbox($setdat{'loadeditcssjs'});
	$setdat{'envlistonerror'}		= &getattributeforcheckbox($setdat{'envlistonerror'});
	$setdat{'funcrestreedit'}		= &getattributeforcheckbox($setdat{'funcrestreedit'});
	$setdat{'datelimitreedit'}		= &getattributeforcheckbox($setdat{'datelimitreedit'});
	$setdat{'coexistflag'}			= &getattributeforcheckbox($setdat{'coexistflag'});

	$setdat{'showLinkBtnUrl'} = &getattributeforcheckbox($setdat{'showLinkBtnUrl'});
	$setdat{'showLinkBtnNum'} = &getattributeforcheckbox($setdat{'showLinkBtnNum'});
	$setdat{'showLinkBtnImg'} = &getattributeforcheckbox($setdat{'showLinkBtnImg'});
	$setdat{'showLinkBtnTwe'} = &getattributeforcheckbox($setdat{'showLinkBtnTwe'});
	$setdat{'showLinkBtnYtb'} = &getattributeforcheckbox($setdat{'showLinkBtnYtb'});
	$setdat{'showLinkBtnSpt'} = &getattributeforcheckbox($setdat{'showLinkBtnSpt'});

	$setdat{'showDecoBtnBonA'} = &getattributeforcheckbox($setdat{'showDecoBtnBonA'});		$setdat{'showDecoBtnBonQ'} = &getattributeforcheckbox($setdat{'showDecoBtnBonQ'});
	$setdat{'showDecoBtnConA'} = &getattributeforcheckbox($setdat{'showDecoBtnConA'});		$setdat{'showDecoBtnConQ'} = &getattributeforcheckbox($setdat{'showDecoBtnConQ'});
	$setdat{'showDecoBtnDonA'} = &getattributeforcheckbox($setdat{'showDecoBtnDonA'});		$setdat{'showDecoBtnDonQ'} = &getattributeforcheckbox($setdat{'showDecoBtnDonQ'});
	$setdat{'showDecoBtnEonA'} = &getattributeforcheckbox($setdat{'showDecoBtnEonA'});		$setdat{'showDecoBtnEonQ'} = &getattributeforcheckbox($setdat{'showDecoBtnEonQ'});
	$setdat{'showDecoBtnFonA'} = &getattributeforcheckbox($setdat{'showDecoBtnFonA'});		$setdat{'showDecoBtnFonQ'} = &getattributeforcheckbox($setdat{'showDecoBtnFonQ'});
	$setdat{'showDecoBtnHonA'} = &getattributeforcheckbox($setdat{'showDecoBtnHonA'});		$setdat{'showDecoBtnHonQ'} = &getattributeforcheckbox($setdat{'showDecoBtnHonQ'});
	$setdat{'showDecoBtnIonA'} = &getattributeforcheckbox($setdat{'showDecoBtnIonA'});		$setdat{'showDecoBtnIonQ'} = &getattributeforcheckbox($setdat{'showDecoBtnIonQ'});
	$setdat{'showDecoBtnMonA'} = &getattributeforcheckbox($setdat{'showDecoBtnMonA'});		$setdat{'showDecoBtnMonQ'} = &getattributeforcheckbox($setdat{'showDecoBtnMonQ'});
	$setdat{'showDecoBtnQonA'} = &getattributeforcheckbox($setdat{'showDecoBtnQonA'});		$setdat{'showDecoBtnQonQ'} = &getattributeforcheckbox($setdat{'showDecoBtnQonQ'});
	$setdat{'showDecoBtnRonA'} = &getattributeforcheckbox($setdat{'showDecoBtnRonA'});		$setdat{'showDecoBtnRonQ'} = &getattributeforcheckbox($setdat{'showDecoBtnRonQ'});
	$setdat{'showDecoBtnSonA'} = &getattributeforcheckbox($setdat{'showDecoBtnSonA'});		$setdat{'showDecoBtnSonQ'} = &getattributeforcheckbox($setdat{'showDecoBtnSonQ'});
	$setdat{'showDecoBtnTonA'} = &getattributeforcheckbox($setdat{'showDecoBtnTonA'});		$setdat{'showDecoBtnTonQ'} = &getattributeforcheckbox($setdat{'showDecoBtnTonQ'});
	$setdat{'showDecoBtnUonA'} = &getattributeforcheckbox($setdat{'showDecoBtnUonA'});		$setdat{'showDecoBtnUonQ'} = &getattributeforcheckbox($setdat{'showDecoBtnUonQ'});
	$setdat{'showFreeDateBtn'}	= &getattributeforcheckbox($setdat{'showFreeDateBtn'});
	$setdat{'allowillegaldate'}	= &getattributeforcheckbox($setdat{'allowillegaldate'});
	$setdat{'allowblankdeco'}	= &getattributeforcheckbox($setdat{'allowblankdeco'});

	$setdat{'showImageBtnNewUp'} = &getattributeforcheckbox($setdat{'showImageBtnNewUp'});
	$setdat{'showImageBtnExist'} = &getattributeforcheckbox($setdat{'showImageBtnExist'});

	$setdat{'showHashBtnHash'}	= &getattributeforcheckbox($setdat{'showHashBtnHash'});

	$setdat{'showFuncBtnSpeech'}	= &getattributeforcheckbox($setdat{'showFuncBtnSpeech'});
	$setdat{'showFuncBtnStaytop'}	= &getattributeforcheckbox($setdat{'showFuncBtnStaytop'});
	$setdat{'showFuncBtnDraft'}		= &getattributeforcheckbox($setdat{'showFuncBtnDraft'});
	$setdat{'showFuncBtnRear'}		= &getattributeforcheckbox($setdat{'showFuncBtnRear'});

	$setdat{'outputlinkfullpath'}	= &getattributeforcheckbox($setdat{'outputlinkfullpath'});
	$setdat{'outputlinkkeepskin'}	= &getattributeforcheckbox($setdat{'outputlinkkeepskin'});
	$setdat{'signhider'}			= &getattributeforcheckbox($setdat{'signhider'});

	# アップロード可能画像形式フォーム用
	my $imageextlist = &fcts::forsafety( $setdat{'imageallowext'} );	# データを受け取る
	$imageextlist =~ s/\|/\n/g;	# 区切り縦棒記号を改行に変換
	$imageextlist .= "\n";		# 最後に改行を加える

	# 画像の表示
	my $noimageicon = '<img src="' . NOIMAGEDEFAULTICON . '" alt="NO IMAGE ICON" style="vertical-align:middle; margin:0 3px;">';
	my $mpconfirm = MOVEPAGECONFIRM;

	# 初期値を作る
	if( $setdat{'fixedfullpath'} eq '' ) { $setdat{'fixedfullpath'} = $cgifullurl; }	# フルパス
	if( $setdat{'fixeddocroot'} eq '' ) { $setdat{'fixeddocroot'} = &fcts::forsafety($ENV{DOCUMENT_ROOT}); }	# ドキュメントルート

	# 時刻をずらす選択肢を作る
	my @optionsforshiftservtime;
	for( my $i = -23.5 ; $i <= 23.5 ; $i+=0.5 ) {
		my $selected = '';
		my $plus = '';
		if( $setdat{'shiftservtime'} == $i) { $selected = ' selected'; }
		if( $i > 0 ) { $plus = '+'; }
		push( @optionsforshiftservtime, qq|<option value="$i"$selected>$plus$i</option>| );
	}

	# セッション維持設定によるメッセージを作成
	my $sessionkeepmsg = '<p class="inputinfo alertinfo">※ブラウザを終了すると<strong class="important">自動ログアウトする設定になっている</strong>ため、上記の設定に意味はありません。<br>(ブラウザを終了してもログイン状態を維持できるよう設定を変更するには、CGIソース内の設定項目の値を変更して下さい。)</p>';
	if( $keepsession == 1 ) {
		$sessionkeepmsg = '<p class="inputinfo">※ブラウザを終了しても、上記の時間が経過するまではログイン状態が維持されます。<br>(上記の期間よりも短い頻度で管理画面にアクセスし続けていれば、永久にログアウトしません。)<br>(ブラウザの終了と同時に自動ログアウトさせたい場合は、CGIソース内の設定項目の値を変更して下さい。)</p>';
	}

	# ………………………………………………
	# 入力欄に掲載する変数の一括エスケープ （※数値の 0 が記録されている場合、ここで空文字列になってしまう弊害に注意）
	foreach my $key ( keys(%setdat) ){
		$setdat{$key} = &fcts::forsafety( $setdat{$key} );
	}

	# 自由入力で数値0が設定されていると空白に置き換わってしまう弊害仕様への対策
	if( $setdat{'rssentries'} eq '' ) { $setdat{'rssentries'} = '0'; }
	if( $setdat{'hashtagBtnListupMax'} eq '' ) { $setdat{'hashtagBtnListupMax'} = '0'; }

	# ………………………
	# 初期選択タブの設定
	my @checkedtab = ('','','','','','');
	if(( $cp{'page'} > 1 ) && ( $cp{'page'} <= 5 )) { $checkedtab[$cp{'page'}] = 'checked'; }
	else { $checkedtab[1] = 'checked'; }	# デフォルトなら先頭タブ(1)を開く

	# ………………………
	# セーフモードLv別表示
	my $allowhtmlmsg = 'HTML使用可';
	my $safemodemsg = '';
	my $alerthtmlmsg = '<span class="inputguide"><strong class="important">※記号「&lt;」や「&gt;」などはHTMLタグとしてそのまま出力される点にご注意下さい。</strong></span>';
	my $hideinsafemode9 = '';
	if( $safemode >= 9 ) {
		$allowhtmlmsg = '<strong class="important">HTML使用不可</strong>';
		$safemodemsg = '<strong class="safemode">このCGIは現在、セーフモードLv.9で動作しているため、どの入力欄にもHTMLタグは一切使用できません。</strong>';
		$alerthtmlmsg = '';
		$hideinsafemode9 = 'style="display:none;"';
	}

	# …………………
	# レンタルモードなら隠す要素には $hideinrental を属性として加えておく
	my $hideinrental = '';
	if( $rentalflag == 1 ) { $hideinrental = 'style="display:none;"'; }

	# デモモードの場合
	if( $flagDemo{'RefuseToChangeSettings'} == 1 ) {
		$setdat{'fixeddocroot'} = '(DOCUMENT ROOT)';
	}

	# LCC関連
	my $hideinfreever = '';
	if( $setdat{'licencecode'} eq '' ) { $hideinfreever = 'style="display:none;"'; }
	elsif ( &fcts::lcc($setdat{'licencecode'}) != 1 ) {
		# LicenceCodeの文法が正しくなければ挿入しない(ただし確認リンクは表示)
		$setdat{'licencecode'} = '(登録ミス)';
	}
	else { $setdat{'licencecode'} = &fcts::safetycutter($setdat{'licencecode'}); }	# 不要だけども念のため

	# 単位変換
	$setdat{'imagemaxbytes'} = int( $setdat{'imagemaxbytes'} / 10.24 ) / 100;				# Bytes→KB (画像1枚あたりの最大サイズ)
	$setdat{'imagestoragelimit'} = int( $setdat{'imagestoragelimit'} / 10485.76 ) / 100;	# Bytes→MB (画像保存に使える最大容量)

	# ………………………
	# 設定フォームの生成
	# ………………………
	# HTML:
	my $cgipath = &getCgiPath();
	my $msg = qq|
		<p class="headGuide">
			CGIの動作設定を行います。必要な設定を変更したら、最下部の「設定を保存する」ボタンをクリックして下さい。（※各タブは、設定の保存前に切り替えられます。）<br />$safemodemsg
		</p>
		<p class="onlyNarrowMobile mobileSetGuide">※スマートフォンを使って設定する際は、端末を<strong>横長に持つ</strong>と各フォームが多少は見やすくなるのでお勧めです。</p>
		<form action="$cgipath" method="post">
			<input type="radio" name="tabset" class="tabcheck" id="tabcheck1" $checkedtab[1]><label for="tabcheck1" class="tab" id="tab1"><span class="stdtabname">ページ</span><span class="longtabname">の表示</span></label>
			<input type="radio" name="tabset" class="tabcheck" id="tabcheck2" $checkedtab[2]><label for="tabcheck2" class="tab" id="tab2"><span class="stdtabname">投稿欄</span><span class="longtabname">の表示</span></label>
			<input type="radio" name="tabset" class="tabcheck" id="tabcheck3" $checkedtab[3]><label for="tabcheck3" class="tab" id="tab3"><span class="stdtabname">フリー</span><span class="longtabname">スペース</span></label>
			<input type="radio" name="tabset" class="tabcheck" id="tabcheck5" $checkedtab[5]><label for="tabcheck5" class="tab" id="tab5"><span class="stdtabname">補助</span><span class="longtabname">出力</span></label>
			<input type="radio" name="tabset" class="tabcheck" id="tabcheck4" $checkedtab[4]><label for="tabcheck4" class="tab" id="tab4"><span class="stdtabname">システム</span><span class="longtabname">設定</span></label>

			<div class="tabcontent" id="tabcontent1">
				<div class="shortcuslinkbox">
					<p class="shortcutlinktitle">ショートカット：</p>
					<ul class="shortcutlinklist">
						<li><a href="#fldPageWhole">ページの表示／全体</a></li>
						<li><a href="#fldPageSolo">ページの表示／投稿単独</a></li>
						<li><a href="#fldSituation">状況に応じた見出しの表示</a></li>
						<li><a href="#fldNaviLink">ナビゲーションリンクの表示</a></li>
						<li><a href="#fldPostText">投稿本文の表示／テキスト</a></li>
						<li><a href="#fldPostImage">投稿本文の表示／画像</a></li>
						<li><a href="#fldPostUrl">投稿本文内のURL処理</a></li>
						<li><a href="#fldHashtag">ハッシュタグの表示</a></li>
						<li><a href="#fldCategory">カテゴリの表示</a></li>
						<li><a href="#fldSearch">全文検索機能</a></li>
						<li><a href="#fldLatestlist">新着投稿リストの表示</a></li>
						<li><a href="#fldCalendar">カレンダーの表示</a></li>
						<li><a href="#fldUserinfo">ユーザ情報の表示</a></li>
						<li><a href="#fldHeadfixed">先頭に固定表示する投稿</a></li>
						<li><a href="#fldRear">下げた投稿の表示</a></li>
						<li><a href="#fldNewsign">直近投稿を示すサインの表示</a></li>
						<li><a href="#fldJargon">システムメッセージ・表示用語</a></li>
						<li><a href="#fldShortcutkey">移動用ショートカットキー</a></li>
						<li><a href="#fldDatelist">日付リストの構成</a></li>
					</ul>
				</div>
				<fieldset>
					<legend id="fldPageWhole">【ページの表示／全体】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizecss-daysepbar">？</a></span>
					<p>
						▼1ページあたりの表示投稿数：
					</p>
					<ul class="list">
						<li><label><input type="text" value="$setdat{'entryperpage'}" name="entryperpage" size="5">個</label> <span class="inputguide">※1以上の整数で指定して下さい。</span></li>
						<li class="addeditem">(<label><input type="checkbox" name="eppoverride" value="1" $setdat{'eppoverride'}>スキン側に指定されている表示数を優先採用する</label>)</li>
					</ul>
					<p class="withseparator">
						▼日付境界バーの挿入位置：
					</p>
					<ul class="list">
						<li>原則の表示位置：<select name="separatepoint"><option value="0" $separatepoint[0]>挿入しない</option><option value="1" $separatepoint[1]>年の境界で挿入</option><option value="2" $separatepoint[2]>月の境界で挿入</option><option value="3" $separatepoint[3]>日の境界で挿入</option></select><br></li>
						<li>日付別の表示時：<select name="separateoption"><option value="0" $separateoption[0]>原則の表示と同じ位置</option><option value="1" $separateoption[1]>年別表示時なら月ごとに、月別表示時なら日ごとに挿入</option></select></li>
						<li>日付の表記形式：<input type="text" placeholder="年表記" value="$setdat{'separateyear'}" name="separateyear" class="halfinput">
											<input type="text" placeholder="月表記" value="$setdat{'separatemonth'}" name="separatemonth" class="halfinput">
											<input type="text" placeholder="日表記" value="$setdat{'separatedate'}" name="separatedate" class="halfinput"> <span class="inputguide">(※1)</span>
						</li>
						<li>バーに表示する機能：<br>
							<label><input type="checkbox" name="separatebarreverse" value="1" $setdat{'separatebarreverse'}>この範囲を逆順で表示するリンク</label><br>
							<label><input type="checkbox" name="separatebaroutput" value="1" $setdat{'separatebaroutput'}>この範囲をファイルに出力するリンク(エクスポート機能)</label><br>
						</li>
					</ul>
					<p class="inputguide">
						※1:スキン用に使える日付専用記法で指定できます。詳しくは<a href="$aif{'puburl'}custom/#customizecss-daysepbar-set-formattable" $mpconfirm>こちら</a>。<br>
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldPageSolo">【ページの表示／投稿単独】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizecss-utilitylinkbox">？</a></span>
					<p>
						▼1投稿の単独表示ページに掲載する情報：
					</p>
					<ul class="list">
						<li><label><input type="checkbox" name="onepostpagesituation" value="1" $setdat{'onepostpagesituation'}>状況に応じた見出しとして投稿番号を表示する</label> <span class="inputguide">(※1)</span></li>
						<li><input type="checkbox" name="onepostpageutilitybox" id="onepostpageutilitybox" value="1" $setdat{'onepostpageutilitybox'}><label for="onepostpageutilitybox">本文の下に、ユーティリティリンク枠を表示する</label>
							<ul class="list">
								<li><label><input type="checkbox" name="utilityrandom" value="1" $setdat{'utilityrandom'}>ランダム継続リンクを表示</label> <span class="inputguide">(※2)</span></li>
								<li><label><input type="checkbox" name="utilitystate" value="1" $setdat{'utilitystate'}>同一ユーザ限定リンクを表示</label></li>
								<li><label>カテゴリ別リンクを<br>→ <select name="utilitycat"><option value="0" $utilitycat[0]>表示しない</option><option value="1" $utilitycat[1]>1つ以上のカテゴリに属している場合だけ表示</option><option value="2" $utilitycat[2]>常に表示する</option></select></label><br></li>
								<li><input type="checkbox" name="utilitydates" id="utilitydates" value="1" $setdat{'utilitydates'}><label for="utilitydates">日付別リンクを表示</label> <span class="inputguide">(同じ日付の投稿を見るリンク群)</span>
									<ul class="list">
										<li><label><input type="checkbox" name="utilitydateymd" value="1" $setdat{'utilitydateymd'}>同一<strong>年月日</strong>限定リンクを表示</label> <span class="inputguide">(1日分の投稿だけを見る)</span></li>
										<li><label><input type="checkbox" name="utilitydateym" value="1" $setdat{'utilitydateym'}>同一<strong>年月</strong>限定リンクを表示</label> <span class="inputguide">(その月の投稿だけを見る)</span></li>
										<li><label><input type="checkbox" name="utilitydatey" value="1" $setdat{'utilitydatey'}>同一<strong>年</strong>限定リンクを表示</label> <span class="inputguide">(その年の投稿だけを見る)</span></li>

										<li><label><input type="checkbox" name="utilitydatemd" value="1" $setdat{'utilitydatemd'}>全年の<strong>同一月日</strong>限定リンクを表示</label> <span class="inputguide">(＝長年日記／※3)</span></li>
										<li><label><input type="checkbox" name="utilitydated" value="1" $setdat{'utilitydated'}>全年全月の<strong>同一日</strong>限定リンクを表示</label> <span class="inputguide">(＝n年m月日記／※4)</span></li>
									</ul>
								</li>
								<li><label><input type="checkbox" name="utilityedit" value="1" $setdat{'utilityedit'}>再編集リンクを表示</label></li>
							</ul>
						</li>
					</ul>
					<p class="inputguide" style="max-width:38em;">
						※1:スキン内の [[SITUATION:～]] の位置に No.123 の形式で番号を表示します。スキンによってはページタイトルにも使われているため、ここをOFFにするとタイトルの区別ができなくなります。<br>
						※2:ランダム表示時にだけ「さらにランダムに表示する」リンクを出力します。<br>
						※3:例えば、2021年6月11日、2020年6月11日、2019年6月11日……のように、過去年も含めた同一月日の投稿を一括して閲覧できる機能です。<br>
						※4:例えば、12月5日、11月5日、10月5日、9月5日……のように、先月以前も含めた過去月の同一日の投稿を一括して閲覧できる機能です。<br>
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldSituation">【状況に応じた見出しの表示】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizecss-situationline">？</a></span>
					<p>
						▼状況に応じた見出しの表示形態：<span class="inputguide">(※1)</span>
					</p>
					<ul class="subopt optmc5">
						<li>
							<label><input type="radio" name="situationvariation" value="0" $situationvariation[0]>文章</label> <span class="inputguide">※状況を文章で表示します。</span>
							<div class="situationPreviewBox" id="satPrevA">カテゴリ「雑記」に属する投稿に限定した、検索語「テスト」の検索結果</div>
						</li>
						<li>
							<label><input type="radio" name="situationvariation" value="1" $situationvariation[1]>ラベル</label> <span class="inputguide">※状況をラベルと値だけで表示します。</span>
							<div class="situationPreviewBox" id="satPrevB">カテゴリ「雑記」、検索語「テスト」</div>
						</li>
						<li>
							<label><input type="radio" name="situationvariation" value="2" $situationvariation[2]>列挙</label> <span class="inputguide">※状況を値だけの列挙で表示します。(※2)</span>
							<div class="situationPreviewBox" id="satPrevC">雑記 テスト</div>
						</li>
					</ul>
					<p style="font-size:0.8em; margin:1em 0 0;">
						例示の切替：<input type="button" value="ハッシュタグ" onclick="situationPrev(0);"> <input type="button" value="日付" onclick="situationPrev(1);"> <input type="button" value="複数カテゴリ" onclick="situationPrev(2);"> <input type="button" value="カテゴリ＋検索" onclick="situationPrev(3);">
					</p>
					<script>
						function situationPrev(words) {
							var sA = 'カテゴリ「雑記」に属する投稿に限定した、検索語「テスト」の検索結果';
							var sB = 'カテゴリ「雑記」、検索語「テスト」';
							var sC = '雑記 テスト';
							if( words == 0 ) {
								sA = 'タグ「思いつき」を含む投稿';
								sB = 'タグ「思いつき」';
								sC = '思いつき';
							}
							else if( words == 1 ) {
								sA = '2022年5月の投稿';
								sB = '2022年5月';
								sC = '2022年5月';
							}
							else if( words == 2 ) {
								sA = 'カテゴリ「日記」・「情報」・「雑記」のどれかに属する投稿';
								sB = 'カテゴリ「日記」・「情報」・「雑記」';
								sC = '日記 情報 雑記';
							}
							document.getElementById('satPrevA').innerHTML = sA;
							document.getElementById('satPrevB').innerHTML = sB;
							document.getElementById('satPrevC').innerHTML = sC;
						}
					</script>
					<p class="withseparator">
						▼表示条件が限定されている場合に表示する付加情報：
					</p>
					<ul class="list">
						<li><label><input type="checkbox" name="situationcount" value="1" $setdat{'situationcount'}>該当件数を表示　</label> ：<input type="text" value="$setdat{'situationcountlabel1'}" name="situationcountlabel1" class="halfinput">＋件数＋<input type="text" value="$setdat{'situationcountlabel2'}" name="situationcountlabel2" class="halfinput"></label></li>
						<li><label><input type="checkbox" name="situationpage" value="1" $setdat{'situationpage'}>ページ番号を表示</label> ：<input type="text" value="$setdat{'situationpagelabel1'}" name="situationpagelabel1" class="halfinput">＋番号＋<input type="text" value="$setdat{'situationpagelabel2'}" name="situationpagelabel2" class="halfinput"></label> <span class="inputguide">(※3)</span></li>
						<li><label><input type="checkbox" name="situationalwayspage" value="1" $setdat{'situationalwayspage'}>表示条件が限定されていない場合でもページ番号を表示</label> <span class="inputguide">(※3)</span></li>
					</ul>
					<p class="inputguide" style="max-width:36em;">
						※1:スキン内の [[SITUATION:～]] の位置に表示されます。<br>
						※2:これは、CSSで項目別に配色等をカスタマイズすることが前提です。何も装飾を用意しないままでこの設定を使うと、状況の判別が困難になる点にご注意下さい。ギャラリーモード等を含め、使用する全スキンに装飾を用意してからご使用下さい。<br>
						※3:表示されているページが、2ページ目以降の場合にのみ表示されます。
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldNaviLink">【ナビゲーションリンクの表示】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizecss-pagenum">？</a></span>
					<p>
						▼ページ移動リンク： <span class="inputguide">※スキン内の [[NAVI:PREVNEXT]] の位置に出力。</span><br>
					</p>
					<ul class="list withshortseparation">
						<li><input type="checkbox" name="pagelinkuse" id="pagelinkuse" value="1" $setdat{'pagelinkuse'}><label for="pagelinkuse">前後のページへ移動するリンクを表示する<small>（投稿単独表示時を<strong class="important">除く</strong>)</small></label>
							<ul class="list">
								<li><label>文言「次の」：<input type="text" value="$setdat{'pagelinknext'}" name="pagelinknext"></label></li>
								<li><label>文言「前の」：<input type="text" value="$setdat{'pagelinkprev'}" name="pagelinkprev"></label></li>
								<li><input type="checkbox" name="pagelinknum" id="pagelinknum" value="1" $setdat{'pagelinknum'}><label for="pagelinknum">1ページに表示される件数を数値で表示する</label>
									<ul class="list">
										<li><label>文言「件」：<input type="text" value="$setdat{'pagelinkunit'}" name="pagelinkunit"></label></li>
									</ul>
								</li>
								<li><label>右矢印「»」：<input type="text" value="$setdat{'pagelinkarrownext'}" name="pagelinkarrownext"></label></li>
								<li><label>左矢印「«」：<input type="text" value="$setdat{'pagelinkarrowprev'}" name="pagelinkarrowprev"></label></li>
							</ul>
						</li>
						<li><input type="checkbox" name="pagelinkuseindv" id="pagelinkuseindv" value="1" $setdat{'pagelinkuseindv'}><label for="pagelinkuseindv">前後の投稿へ移動するリンクを表示する<small>（投稿単独表示時<strong class="important">のみ</strong>）</small></label>
							<ul class="list">
								<li>最新方向：<input type="text" value="$setdat{'pagelinknextindv1'}" name="pagelinknextindv1" class="halfinput">＋<label><input type="checkbox" name="pagelinknextindvn" value="1" $setdat{'pagelinknextindvn'}>投稿番号</label>＋<input type="text" value="$setdat{'pagelinknextindv2'}" name="pagelinknextindv2" class="halfinput"></li>
								<li>古い方向：<input type="text" value="$setdat{'pagelinkprevindv1'}" name="pagelinkprevindv1" class="halfinput">＋<label><input type="checkbox" name="pagelinkprevindvn" value="1" $setdat{'pagelinkprevindvn'}>投稿番号</label>＋<input type="text" value="$setdat{'pagelinkprevindv2'}" name="pagelinkprevindv2" class="halfinput"></li>
							</ul>
						</li>
						<li><label>前後ページ移動リンク間の境界記号：<input type="text" value="$setdat{'pagelinkseparator'}" name="pagelinkseparator" class="halfinput"></label></li>
					</ul>
					<p class="withseparator">
						▼ページ番号リンク： <span class="inputguide">※スキン内の [[NAVI:PAGELIST]] の位置に出力。</span><br>
					</p>
					<ul class="list">
						<li><label><input type="checkbox" name="pagenumfigure" value="1" $setdat{'pagenumfigure'}>ページ番号の桁数を揃える</label> <span class="inputguide">※必要に応じて番号の先頭に「0」を付加</span></li>
						<li><input type="checkbox" name="pagenumomission" id="pagenumomission" value="1" $setdat{'pagenumomission'}><label for="pagenumomission">総ページ数が多い場合に途中のページ番号リンクを省略する</label>
							<ul class="list">
								<li><label>省略する際の記号：<input type="text" value="$setdat{'pagenumomitmark'}" name="pagenumomitmark" class="halfinput"></label></li>
							</ul>
						</li>
						<li><label>各ページ番号の左側に挿入する記号：<input type="text" value="$setdat{'pagenumbracket1'}" name="pagenumbracket1" class="halfinput"></label></li>
						<li><label>各ページ番号の右側に挿入する記号：<input type="text" value="$setdat{'pagenumbracket2'}" name="pagenumbracket2" class="halfinput"></label></li>
						<li><label>ページ番号とページ番号との間に挿入する記号：<input type="text" value="$setdat{'pagenumseparator'}" name="pagenumseparator" class="halfinput"></label></li>
					</ul>
					<p class="withseparator">
						▼HOMEに戻るリンク： <span class="inputguide">※必要に応じて [[NAVI:TOPPAGE]] の位置に出力。</span><br>
					</p>
					<ul class="list">
						<li><label>リンクラベル：<input type="text" value="$setdat{'pagelinktop'}" name="pagelinktop"></label><span class="inputguide">(標準：初期表示に戻る)</span></li>
					</ul>
					<p class="inputguidebox">
						<span class="inputguide">※標準値の記載がある項目は、省略すれば標準値が使われます。$allowhtmlmsg。</span><br>
						$alerthtmlmsg
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldPostText">【投稿本文の表示／テキスト】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizecss-postnum">？</a> <a class="help ch" href="$aif{'puburl'}custom/#customizecss-readmore">？</a></span>
					<p>
						▼文章の表示：<br>
					</p>
					<ul class="list">
						<li><label><input type="checkbox" name="allowlinebreak" value="1" $setdat{'allowlinebreak'}>改行を許可 (入力された改行は、表示上でも改行する)</label></li>
						<li><label><input type="checkbox" name="keepserialspaces" value="1" $setdat{'keepserialspaces'}>空白の連続を再現 (半角空白文字の連続をそのまま見せる)</label></li>
						<li>
							<input type="checkbox" name="postidlinkize" id="postidlinkize" value="1" $setdat{'postidlinkize'}><label for="postidlinkize">指定の投稿番号へリンクできる記法を許可</label> <span class="inputguide">(※1)</span>
							<ul class="list">
								<li><label><input type="checkbox" name="postidlinkgtgt" value="1" $setdat{'postidlinkgtgt'}>書式「&gt;&gt;123」形式でのリンク記法も許可</label> <span class="inputguide">(※2)</span></li>
							</ul>
						</li>
						<li>
							<input type="checkbox" name="allowdecorate" id="allowdecorate" value="1" $setdat{'allowdecorate'}><label for="allowdecorate">文字の装飾(専用記法での記述)を許可</label> <span class="inputguide">(※3)</span>
							<ul class="list">
								<li><label><input type="checkbox" name="readherebtnuse" value="1" $setdat{'readherebtnuse'}>指定範囲だけを隠す装飾機能の使用を許可</label> <span class="inputguide">(※4,6)</span></li>
							</ul>
						</li>
						<li><label><input type="checkbox" name="readmorebtnuse" id="readmorebtnuse" value="1"  $setdat{'readmorebtnuse'}>指定位置以後の全てを隠す「続きを読む」記法を許可</label> <span class="inputguide">(※5,6)</span></li>
					</ul>
					<p class="inputguide">
						※1:本文中の [&gt;123] または [&gt;123:ラベル] を No.123 へのリンクにします。<br>
						※2:本文中の &gt;&gt;123 を No.123 へのリンクにします。<br>
						※3:入力欄への装飾ボタンの表示は「投稿欄の表示」タブ側で設定できます。<br>
						※4:本文中に書かれた [H: ～ ] の範囲内だけを隠す機能です。<br>
						※5:本文中に書かれた区切り文字 &lt;&gt; 以降のすべてを隠す機能です。<br>
						※6:JavaScriptが無効な環境では、設定にかかわらず全文が表示されます。<br>
					</p>
					<p class="withseparator">
						▼続きを読む・指定範囲を隠す 共通設定： <span class="inputguide">(※6)</span><br>
					</p>
					<ul class="list">
						<li><label><input type="checkbox" name="readmoreonsearch" value="1"  $setdat{'readmoreonsearch'}>全文検索時でも隠す機能を有効にする</label><span class="inputguide">(※7)</span></li>
						<li><label><input type="checkbox" name="readmorecloseuse" value="1"  $setdat{'readmorecloseuse'}>展開した後に「畳む」ボタンを表示する</label></li>
						<li><label>続きを読むラベル：<input type="text" value="$setdat{'readmorebtnlabel'}" name="readmorebtnlabel"></label><span class="inputguide">(標準：続きを読む)</span></li>
						<li><label>読後に畳むラベル：<input type="text" value="$setdat{'readmorecloselabel'}" name="readmorecloselabel"></label><span class="inputguide">(標準：畳む)</span></li>
						<li>展開する範囲の表示方法：<select name="readmorestyle"><option value="0" $readmorestyle[0]>inline</option><option value="1" $readmorestyle[1]>inline-block</option><option value="2" $readmorestyle[2]>block</option></select><span class="inputguide">(標準：inline)</span></li>
					</ul>
					<p class="inputguide">
						※6:それぞれの機能が許可されている場合のみ、ここでの設定が使われます。<br>
						※7:この項目をONにしない限り、検索結果の表示時には全文が表示されます。
					</p>
					<p class="withseparator">
						▼テキストリンクの出力調整：<br>
					</p>
					<ul>
						<li><label><input type="checkbox" name="outputlinkfullpath" id="outputlinkfullpath" value="1" $setdat{'outputlinkfullpath'}>本文中のテキストリンクを絶対URL(フルパス)で出力する</label><span class="inputguide">(※8,10)</span></li>
						<li><label><input type="checkbox" name="outputlinkkeepskin" id="outputlinkkeepskin" value="1" $setdat{'outputlinkkeepskin'}>一時適用中のスキンを維持できるリンクを出力する</label><span class="inputguide">(※9,10,11)</span></li>
					</ul>
					<p class="inputguide" style="max-width:36em;">
						※8:ここがONだとエクスポート時にも絶対URLで出力される点に注意して下さい。なお、画像パスの出力には影響しません(その設定は別項目です)。<br>
						※9:ここがOFFだと常にデフォルトスキンで表示されるリンクを出力します。<br>
						※10:投稿本文<strong>以外</strong>の場所にあるリンクの出力には<strong>影響しません</strong>。<br>
						※11:パーマリンクのリンク先で一時適用中のスキンを維持するかしないかは、スキン側に記述する [[PARMAURL:***]] の各記法で選択できます。
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldPostImage">【投稿本文の表示／画像】</legend> <span class="helpbox"><a class="help uh" href="$aif{'puburl'}usage/#howtopostimage">？</a></span>
					<p>
						▼画像の表示：<br>
					</p>
					<ul class="list">
						<li><input type="checkbox" name="imageshowallow" id="imageshowallow" value="1" $setdat{'imageshowallow'}><label for="imageshowallow">画像の表示を許可</label><span class="inputguide">(※1,2)</span>
							<ul class="subopt">
								<li><label><input type="checkbox" name="imagefullpath" value="1" $setdat{'imagefullpath'}>画像パスに絶対URL(フルパス)を使う</label><span class="inputguide">(※3)</span></li>
								<li><label><input type="checkbox" name="imagelazy" value="1" $setdat{'imagelazy'}>img要素に遅延読込(LazyLoad)用の属性を付加する</label></li>


								<li><input type="checkbox" name="imagewhatt" id="imagewhatt" value="1" $setdat{'imagewhatt'}><label for="imagewhatt">可能ならimg要素にwidth属性とheight属性を付加する<span class="inputguide">(※4)</span></label>
									<ul class="subopt">
										<li><input type="checkbox" name="imagewhmax" id="imagewhmax" value="1" $setdat{'imagewhmax'}><label for="imagewhmax">縦横サイズの最大値を指定する<span class="inputguide">(※5/<small>注意</small>)</span></label>
											<ul class="list">
												<li>
													<label>横幅最大：<input type="text" value="$setdat{'imagemaxwidth'}" name="imagemaxwidth" size="3"></label>px ／
													<label>高さ最大：<input type="text" value="$setdat{'imagemaxheight'}" name="imagemaxheight" size="3"></label>px
												</li>
											</ul>
										</li>
									</ul>
								</li>


								<li><input type="checkbox" name="imagetolink" id="imagetolink" value="1" $setdat{'imagetolink'}><label for="imagetolink">画像を(原寸画像への)リンクにする</label>
									<ul class="subopt">
										<li><input type="checkbox" name="imagelightbox" id="imagelightbox" value="1" $setdat{'imagelightbox'}><label for="imagelightbox">画像リンクにLightbox系用の属性を付加する<span class="inputguide">(※6)</span></label>
											<ul class="list">
												<li><label>属性：<input type="text" value="$setdat{'imagelightboxatt'}" name="imagelightboxatt"></label><span class="inputguide">(標準：data-lightbox=&quot;tegalog&quot;)</span></li>
												<li>代替文字がある場合にキャプションを作る属性名<br><label>属性名：<input type="text" value="$setdat{'imagelightboxcap'}" name="imagelightboxcap"></label><span class="inputguide">(標準：data-title)</span></li>
											</ul>
										</li>
										<li><input type="checkbox" name="imageaddclass" id="imageaddclass" value="1" $setdat{'imageaddclass'}><label for="imageaddclass">画像リンクに独自のclass属性値を追加する</label><span class="inputguide">(※7)</span></label>
											<ul class="list">
												<li><label>属性：class=&quot;<input type="text" value="$setdat{'imageclass'}" name="imageclass">&quot;</label></li>
											</ul>
										</li>
									</ul>
								</li>
							</ul>
							<p class="innersubtitle withseparator">▼投稿画像保存用ディレクトリの<strong class="important">外に</strong>ある画像の表示：</p>
							<ul class="list">
								<li><label><input type="checkbox" name="imageoutdir" value="1" $setdat{'imageoutdir'}>任意のディレクトリにある画像の表示を許可する<span class="inputguide">(※8)</span></label></li>
								<li><label><input type="checkbox" name="imageouturl" value="1" $setdat{'imageouturl'}>画像をURLで指定可能にする<span class="inputguide">(※9)</span></label></li>
							</ul>
						</li>
					</ul>
					<p class="inputguide" style="max-width:37em;">
						※1:画像投稿ボタンや投稿時の配置は「投稿欄の表示」タブで設定できます。<br>
						※2:画像容量(ファイルサイズ)の制限は「システム設定」タブで設定できます。<br>
						※3:この項目がOFFだと、img要素のsrc属性値には相対パスで挿入されます。<br>
						※4:縦横サイズを取得できた場合のみ出力。対応形式：GIF, PNG, JPEG, SVG。異なるドメインにある画像のサイズは取得できません。<br>
						※5:最大値の指定が不要な項目は空欄にして下さい。縦横比を維持したまま最大値の範囲に収まるよう属性値を自動調整します。<strong class="important">《注意》</strong>スキン側CSSで画像サイズが指定されていれば、実際の表示には<strong class="important">CSSの方が採用される</strong>ため、ここでの最大値の指定は<strong class="important">使われません</strong>。※標準添付の各スキンはCSS側で指定しています。<br>
						※6:Lightbox以外のスクリプトを使う場合の記述にも使えます。読み込むスクリプトは、[システム設定]→【画像拡大スクリプトの選択】区画で指定できます。<br>
						※7:この項目のON/OFFに関係なく、常に class="imagelink" は出力されます。<br>
						※8:画像の指定に「../」を含む相対パスや「/」で始まる絶対パスが使えます。<br>
						※9:画像の指定に「http://」か「https://」で始まるURLが使えます。この指定方法では、画像の拡張子はチェックされません。<br>
					</p>
					<p class="withseparator">
						▼画像が省略される場面での表示：<span class="inputguide">(※1)</span><br>
					</p>
					<ul class="list">
						<li><label><input type="checkbox" name="insertalttext" value="1" $setdat{'insertalttext'}>画像の代わりに「(画像省略)」という文字列を出力する</label><span class="inputguide">(※2)</span><br></li>
					</ul>
					<p class="inputguide">
						※1:本文を指定文字数に切り詰める抜粋表示時には、画像の出力が省略されます。<br>
						（たとえば、「RSSフィード(抜粋収録)」スキンなどで使われています。）<br>
						※2:OFFにすると、抜粋表示時には（画像の代わりには）何も出力されません。<br>
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldPostUrl">【投稿本文内のURL処理】</legend> <span class="helpbox"><a class="help uh" href="$aif{'puburl'}usage/#howtouse-linkbutton">？</a></span>
					<p>
						▼URLが書かれた場合の表示：<br>
					</p>
					<ul class="list">
						<li><input type="checkbox" name="urlautolink" id="urlautolink" value="1" $setdat{'urlautolink'}><label for="urlautolink">URLを自動でリンクにする</label><span class="inputguide">(※1)</span>
							<ul class="subopt">
								<li>
									<label><input type="radio" name="urllinktarget" value="0" $urllinktarget[0]>リンク先は同一ウインドウ(タブ)で開く</label><br>
									<label><input type="radio" name="urllinktarget" value="1" $urllinktarget[1]>リンク先は新規ウインドウ(タブ)で開く</label><br>
									<label><input type="radio" name="urllinktarget" value="2" $urllinktarget[2]>リンク先はフレームを解除して開く</label><br>
								</li>
							</ul>
							<p class="innersubtitle withseparator">▼リンクの出力仕様：</p>
							<ul class="list">
								<li><label><input type="checkbox" name="urlnofollow" value="1" $setdat{'urlnofollow'}>自動リンクには rel="nofollow" 属性を付加する</label></li>
								<li><label><input type="checkbox" name="urlnoprotocol" value="1" $setdat{'urlnoprotocol'}>URLの表示ではプロトコル名(httpなど)を省略する</label></li>
								<li>長すぎるURLの表示は、<input type="text" value="$setdat{'longurlcutter'}" name="longurlcutter" size="3">文字目で切る<span class="inputguide">(標準：40)</span></li>
							</ul>
							<p class="innersubtitle withseparator">▼URL自動リンクの特殊表示化：</p>
							<ul class="list">
								<li><input type="checkbox" name="urlexpandtweet" id="urlexpandtweet" value="1" $setdat{'urlexpandtweet'}><label for="urlexpandtweet">URLの直前に[Tweet]ラベルがあればツイートを埋め込む</label>
									<ul class="list">
										<li>Twitterカラーテーマ：
											<ul>
												<li><label><input type="radio" name="urlexpandtwtheme" value="0" $urlexpandtwtheme[0]>Light</label></li>
												<li><label><input type="radio" name="urlexpandtwtheme" value="1" $urlexpandtwtheme[1]>Dark</label></li>
											</ul>
										</li>
									</ul>
								</li>
								<li><label><input type="checkbox" name="urlexpandyoutube" value="1" $setdat{'urlexpandyoutube'}>URLの直前に[YouTube]ラベルがあれば動画を埋め込む</label></li>
								<li><label><input type="checkbox" name="urlexpandspotify" value="1" $setdat{'urlexpandspotify'}>URLの直前に[Spotify]ラベルがあれば音楽を埋め込む</label></li>
							</ul>
							<p id="urlcompatiblebtn">
								<input type="button" value="古い機能の設定も表示する" onclick="document.getElementById('urlcompatiblebtn').style.display='none'; document.getElementById('urlcompatiblesets').style.display='block'; document.getElementById('urlcompatiblenotes').style.display='inline';">
							</p>
							<div id="urlcompatiblesets">
							<ul class="list">
								<li><input type="checkbox" name="urlexpandimg" id="urlexpandimg" value="1" $setdat{'urlexpandimg'}><label for="urlexpandimg">URLの直前に[IMG:*]ラベルがあれば画像として掲載</label><span class="inputguide">(※2)</span>
									<ul class="subopt">
										<li><label><input type="checkbox" name="embedonlysamedomain" value="1" $setdat{'embedonlysamedomain'}>埋め込む画像は、同一ドメイン下にある画像に限る</label></li>
										<li><label><input type="checkbox" name="urlimagelazy" value="1" $setdat{'urlimagelazy'}>img要素に遅延読込(LazyLoad)用の属性を付加する</label></li>
										<li><input type="checkbox" name="urlimagelightbox" id="urlimagelightbox" value="1" $setdat{'urlimagelightbox'}><label for="urlimagelightbox">画像リンクにLightbox系用の属性を付加する</label><span class="inputguide">(※3)</span>
											<ul class="list">
												<li><label>属性：<input type="text" value="$setdat{'urlimagelightboxatt'}" name="urlimagelightboxatt"></label><span class="inputguide">(※4／標準：data-lightbox=&quot;tegalog&quot;)</span></li>
												<li><label>キャプション用属性名：<input type="text" value="$setdat{'urlimagelightboxcap'}" name="urlimagelightboxcap"></label><span class="inputguide">(標準：data-title)</span></li>
											</ul>
										</li>
										<li><input type="checkbox" name="urlimageaddclass" id="urlimageaddclass" value="1" $setdat{'urlimageaddclass'}><label for="urlimageaddclass">画像リンクに独自のclass属性値を追加する</label><span class="inputguide">(※5)</span></label>
											<ul class="list">
												<li><label>属性：class=&quot;<input type="text" value="$setdat{'urlimageclass'}" name="urlimageclass">&quot;</label></li>
											</ul>
										</li>
									</ul>
								</li>
							</ul>
							</div><!-- /#urlcompatiblesets -->
						</li>
					</ul>
					<p class="inputguide" style="max-width:40em;">
						※1:URLの直前に[ラベル]を書けば、任意の文字列でテキストリンクを作れます。<br>
						<span id="urlcompatiblenotes">
						※2:投稿画像の表示が無効でも、この方法での画像表示は可能です。<br>
						※3:Lightbox以外のスクリプトを使う場合の記述にも使えます。読み込むスクリプトは、[システム設定]→【画像拡大スクリプトの選択】区画で指定できます。<br>
						※4:テキストリンクにLightbox属性を付加する[ラベル:LB]記法でも使われます。<br>
						※5:この項目のON/OFFに関係なく、常に class="imagelink" は出力されます。<br>
						</span>
					</p>
					<script>document.getElementById('urlcompatiblesets').style.display='none'; document.getElementById('urlcompatiblenotes').style.display='none';</script>
				</fieldset>
				<fieldset>
					<legend id="fldHashtag">【ハッシュタグの表示】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizecss-hashtaglist">？</a></span>
					<p>
						▼ハッシュタグ一覧表示の掲載順序:
					</p>
					<ul>
						<li>
							<select name="hashtagsort"><option value="0" $hashtagsort[0]>0:出現順</option><option value="1" $hashtagsort[1]>1:出現数の多い順（同位なら出現順）</option><option value="2" $hashtagsort[2]>2:出現数の少ない順（同位なら出現順）</option><option value="3" $hashtagsort[3]>3:出現数の多い順（同位なら文字コード順）</option><option value="4" $hashtagsort[4]>4:出現数の少ない順（同位なら文字コード順）</option></select><br>
							<p class="inputguide">※出現順とは、新投稿→旧投稿の方向に走査して見つけた順序のことです。</p>
							<!-- 前の状態 --><input type="hidden" name="befhashts" value="$setdat{'hashtagsort'}">
						</li>
					</ul>
					<p class="withseparator">
						▼ハッシュタグ表示時の調整：
					</p>
					<ul class="list">
						<li><input type="checkbox" name="hashtaglinkize" id="hashtaglinkize" value="1" $setdat{'hashtaglinkize'}><label for="hashtaglinkize">本文中のハッシュタグをリンクにする</label>
							<ul class="list">
								<li><label>ハッシュタグのリンクは、<input type="text" value="$setdat{'hashtagcut'}" name="hashtagcut" size="5">文字目で切る</label><span class="inputguide">(標準：25／※1)</span></li>
								<li><label><input type="checkbox" name="hashtagnokakko" value="1" $setdat{'hashtagnokakko'}>ハッシュタグリンクの表示時では角括弧を省略する</label><span class="inputguide">(※2)</span></li>
							</ul>
						</li>
					</ul>
					<p class="inputguide" style="max-width:37em;">
						※1：リンクとして掲載する場合の文字数制限です。ハッシュタグ自体に文字数の上限はありません。<br>
						※2：表示時に角括弧を非表示にするだけです。全角と半角など文字種の混在するハッシュタグを書きたい場合には、ここでの設定に関係なく常に半角角括弧で囲む必要があります。<br>
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldCategory">【カテゴリの表示】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizecss-post-catid">？</a></span>
					<p>
						▼1投稿に複数のカテゴリが設定されている場合：
					</p>
					<ul class="list">
						<li><label>カテゴリ間の区切り文字：<input type="text" value="$setdat{'catseparator'}" name="catseparator" class="shortinput"></label> <span class="inputguide">(標準：カンマ「,」)</span></li>
					</ul>
					<p class="withseparator">
						▼1投稿にカテゴリが1つも設定されていない場合：
					</p>
					<ul class="list">
						<li>カテゴリ名として表示する内容：
							<ul class="subopt">
								<li>
									<label><input type="radio" name="nocatshow" value="0" $nocatshow[0]>何も表示しない</label><br>
									<label><input type="radio" name="nocatshow" value="1" $nocatshow[1]>文字列 <input type="text" value="$setdat{'nocatlabel'}" name="nocatlabel"> を表示する</label><br>
								</li>
							</ul>
						</li>
					</ul>
					<p class="inputguide withseparator">
						※カテゴリそのものの設定は、管理画面の「<a href="?mode=admin&amp;work=categories" $mpconfirm>カテゴリ管理</a>」からできます。
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldSearch">【全文検索機能】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#specification-complexsearch">？</a></span>
					<p>
						▼検索窓の表示：
					</p>
					<ul class="list">
						<li><label>検索ボタン表面のラベル：<input type="text" value="$setdat{'searchlabel'}" name="searchlabel"></label><span class="inputguide">(標準：検索)</span></li>
						<li><label>検索窓のプレースホルダ：<input type="text" value="$setdat{'searchholder'}" name="searchholder"></label></li>
						<li><label><input type="checkbox" name="searchoption" value="1" $setdat{'searchoption'}>状況に応じた検索オプションを表示する</label><span class="inputguide">(※1)</span></li>
					</ul>
					<p class="inputguide">
						※1:投稿者別検索・ハッシュタグ限定検索・日付別検索・ギャラリー内に<br>限定した検索ができるチェックボックスが、状況に応じて表示されます。<br>OFFにすると、常に全投稿が検索対象になります。<br>
					</p>
					<p class="withseparator">
						▼複合検索窓のオプション項目ラベル：
					</p>
					<ul class="list">
						<li><label>投稿者名の選択：<input type="text" value="$setdat{'cslabeluser'}" name="cslabeluser"></label></li>
						<li><label>投稿年月の選択：<input type="text" value="$setdat{'cslabeldate'}" name="cslabeldate"></label></li>
						<li><label>ﾊｯｼｭタグの選択：<input type="text" value="$setdat{'cslabeltag'}" name="cslabeltag"></label></li>
						<li><label>カテゴリの選択：<input type="text" value="$setdat{'cslabelcat'}" name="cslabelcat"></label></li>
						<li><label>出力順序の選択：<input type="text" value="$setdat{'cslabelorder'}" name="cslabelorder"></label></li>
					</ul>
					<p class="inputguide">
						※各項目の表示/非表示は、スキン側の記述で選択できます。
					</p>
					<p class="withseparator">
						▼全文検索対象の設定：
					</p>
					<ul class="list">
						<li><label><input type="checkbox" name="catidinsearch" value="1" $setdat{'catidinsearch'}>全文検索対象にカテゴリIDを含める</label></li>
					</ul>
				</fieldset>

				<fieldset>
					<legend id="fldLatestlist">【新着投稿リストの表示】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizecss-latestlist">？</a></span>
					<p>
						▼直近の投稿として表示する件数：
					</p>
					<ul class="list">
						<li><label><input type="text" value="$setdat{'latestlistup'}" name="latestlistup" size="5">件</label> <span class="inputguide">※1以上の整数で指定して下さい。</span></li>
					</ul>
					<p class="withseparator">
						▼それぞれに表示する内容：
					</p>
					<ul class="list">
						<li><label>内容と順序：<input type="text" value="$setdat{'latestlistparts'}" name="latestlistparts" size="10"></label><span class="inputguide">(標準：HBDTU／※1)</span></li>
						<li>タイトルは、<input type="text" value="$setdat{'latesttitlecut'}" name="latesttitlecut" size="3">文字目までを表示。<span class="inputguide">(標準：15／※2)</span></li>
					</ul>
					<p class="inputguide">
						※1:以下の英字が使えます。取捨選択・順序は自由です。<br>
						<b>H</b>(必須)=タイトルとリンク／ <b>D</b>=投稿日付／ <b>T</b>=投稿時刻／ <b>U</b>=投稿者名／<br> <b>I</b>=投稿者ID／ <b>N</b>=投稿番号／ <b>L</b>=本文の文字数／ <b>B</b>=改行<br>（上記以外の文字は、その文字がそのまま表示されます。）<br>
						※2:本文1行目の先頭から指定文字数がタイトルとして採用されますが、<br>1行目が空行や画像のみなら投稿番号がタイトルになります。<br>
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldCalendar">【カレンダーの表示】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizecss-calendar">？</a></span>
					<p>
						▼ボックス型カレンダーでの表示<br>
					</p>
					<ul class="list">
						<li><input type="checkbox" name="caladdweekrow" id="caladdweekrow" value="1" $setdat{'caladdweekrow'}><label for="caladdweekrow">カレンダーの先頭行に曜日名を表示する</label>
							<ul class="list">
								<li><label>日曜日：<input type="text" value="$setdat{'calsun'}" name="calsun" size="3"></label> <span class="inputguide">(標準：日)</span></li>
								<li><label>月曜日：<input type="text" value="$setdat{'calmon'}" name="calmon" size="3"></label> <span class="inputguide">(標準：月)</span></li>
								<li><label>火曜日：<input type="text" value="$setdat{'caltue'}" name="caltue" size="3"></label> <span class="inputguide">(標準：火)</span></li>
								<li><label>水曜日：<input type="text" value="$setdat{'calwed'}" name="calwed" size="3"></label> <span class="inputguide">(標準：水)</span></li>
								<li><label>木曜日：<input type="text" value="$setdat{'calthu'}" name="calthu" size="3"></label> <span class="inputguide">(標準：木)</span></li>
								<li><label>金曜日：<input type="text" value="$setdat{'calfri'}" name="calfri" size="3"></label> <span class="inputguide">(標準：金)</span></li>
								<li><label>土曜日：<input type="text" value="$setdat{'calsat'}" name="calsat" size="3"></label> <span class="inputguide">(標準：土)</span></li>
							</ul>
						</li>
					</ul>
				</fieldset>

				<fieldset>
					<legend id="fldUserinfo">【ユーザ情報の表示】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizecss-usericon">？</a></span>
					<p>
						▼ユーザアイコンの表示<br>
					</p>
					<ul class="list">
						<li><input type="checkbox" name="usericonsize" id="usericonsize" value="1" $setdat{'usericonsize'} onclick="if(!this.checked){ alert('ここをOFFにすると、アイコン画像は（各画像の）原寸サイズで表示されます。大きな画像が指定されると、ページの表示が崩れる可能性がある点にご注意下さい。'); }"><label for="usericonsize">ユーザアイコンの縦横サイズを指定する</label> <span class="inputguide">(※1)</span>
							<ul class="list">
								<li>サイズ：
									横<input type="text" value="$setdat{'usericonsizew'}" name="usericonsizew" size="3">px ×
									縦<input type="text" value="$setdat{'usericonsizeh'}" name="usericonsizeh" size="3">px <span class="inputguide">(標準：32×32)</span></li>
								<li>指定サイズの出力方法：
									<ul class="subopt">
										<li>
											<label><input type="radio" name="usericonsource" value="0" $usericonsource[0]>HTMLで出力</label> <span class="inputguide">(通常適用／※2)</span><br>
											<label><input type="radio" name="usericonsource" value="1" $usericonsource[1]>CSSで出力</label> <span class="inputguide">(強制適用／※3)</span><br>
										</li>
									</ul>
								</li>
							</ul>
						</li>
					</ul>
					<p class="inputguide" style="max-width:30em;">
						※1：OFFにすると、アイコンは原寸サイズで表示されます。<br>
						※2：こちらを選択すると、スキン側でサイズが指定されていれば<strong class="important">スキン側のサイズが採用</strong>されます。<br>
						※3：こちらを選択すると、スキン側でサイズが指定されていても<strong class="important">ここでの設定サイズが優先採用</strong>されます。(たいていは)<br>
					</p>
					<p id="headerstrings" class="withseparator">
						▼情報が未設定なユーザの表示<br>
					</p>
					<ul class="list">
						<li><label>表示名：<input type="text" value="$setdat{'unknownusername'}" name="unknownusername"></label><span class="inputguide">(標準：？)</span></li>
						<li>アイコン
							<ul class="subopt">
								<li>
									<label><input type="radio" name="unknownusericon" value="0" $unknownusericon[0]>標準アイコン($noimageicon)</label><br>
									<label><input type="radio" name="unknownusericon" value="1" $unknownusericon[1]>URL</label>
									<input type="text" value="$setdat{'unknownusericonurl'}" name="unknownusericonurl" placeholder="https://"><br>
								</li>
							</ul>
						</li>
					</ul>
					<p class="inputguide">
						※削除済みIDによる過去投稿の表示にも使われます。
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldHeadfixed">【先頭に固定表示する投稿】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizecss-headfixed">？</a></span>
					<p>
						▼常に先頭に固定して表示する投稿
					</p>
					<ul class="list">
						<li><label>固定表示する投稿番号：<input type="text" value="$setdat{'fixedpostids'}" name="fixedpostids"></label><span class="inputguide">(複数指定可／※1)</span></li>
						<li><label>固定表示を示すラベル：<input type="text" value="$setdat{'fixedpostsign'}" name="fixedpostsign"></label><span class="inputguide">(標準：(先頭固定)／※2)</span></li>
						<li>先頭に固定する投稿の日付表示：
							<ul class="subopt">
								<li>
									<label><input type="radio" name="fixedpostdate" value="1" $fixedpostdate[1]>本来の投稿日時を表示</label><br>
									<label><input type="radio" name="fixedpostdate" value="2" $fixedpostdate[2]>現在日時(アクセスされた瞬間の日時)を表示</label><br>
									<label><input type="radio" name="fixedpostdate" value="3" $fixedpostdate[3]>上記の「固定表示を示すラベル」欄の値を表示</label> <span class="inputguide">(※3,4)</span><br>
									<label><input type="radio" name="fixedpostdate" value="0" $fixedpostdate[0]>何も表示しない</label> <span class="inputguide">(※3)</span><br>
								</li>
							</ul>
						</li>
					</ul>
					<p class="inputguide" style="max-width:37em;">
						※1：投稿番号を半角カンマ記号「,」で区切れば複数指定できます。上限なし。<br>
						（先頭に固定されるのは、表示対象が何も限定されていない状況でのみです。）<br>
						※2：内側スキンの中に [[NEW]] と書いた場所に表示されます。<br>
						（先頭固定されている投稿には「直近投稿を示すサイン」は表示されません。）<br>
						※3：スキン側に指定されている日時フォーマットは無視されます。<br>
						※4：1投稿に2つ以上の日付を表示するスキンの場合は、1つ目だけに表示され、残りには何も表示されません。
					</p>
					<p class="withseparator">
						▼先頭固定投稿が表示される状況での表示
					</p>
					<ul class="list">
						<li><input type="checkbox" name="fixedseparatepoint" id="fixedseparatepoint" value="1" $setdat{'fixedseparatepoint'}><label for="fixedseparatepoint">直前に日付境界バーを表示する</label>
							<ul class="list">
								<li><label>日付境界バーのラベル：<input type="text" value="$setdat{'fixedseparatelabel'}" name="fixedseparatelabel"></label> <span class="inputguide">(標準：先頭固定)</span></li>
							</ul>
						</li>
					</ul>
					<p class="inputguide">
						※先頭に固定される投稿が複数ある場合でも、日付境界バーの表示は1度だけです。
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldRear">【下げた投稿の表示】</legend> <span class="helpbox"><a class="help uh" href="$aif{'puburl'}usage/#howtouse-rear">？</a></span>
					<p>
						▼下げた投稿<sup class="inputguide">(※1)</sup>を表示する状況を選択 <span class="inputguide">(※2)</span>
					</p>
					<ul class="list">
						<li class="disableitem"><label><input type="checkbox" disabled>表示条件が限定されていない状況</label> <span class="inputguide">(<strong class="important">常に非表示</strong>)</span></li>
						<li><label><input type="checkbox" name="rearappearcat" value="1" $setdat{'rearappearcat'}>カテゴリ限定表示時</label></li>
						<li><label><input type="checkbox" name="rearappeartag" value="1" $setdat{'rearappeartag'}>ハッシュタグ限定表示時</label></li>
						<li><label><input type="checkbox" name="rearappeardate" value="1" $setdat{'rearappeardate'}>日付指定表示時</label></li>
						<li><label><input type="checkbox" name="rearappearsearch" value="1" $setdat{'rearappearsearch'}>全文検索時</label></li>
						<li class="disableitem"><label><input type="checkbox" checked disabled>1投稿の単独表示時</label> <span class="inputguide">(<strong class="important">常に表示</strong>)</span></li>
					</ul>
					<p class="inputguide" style="max-width:30em;">
						※1：投稿時に「下げる(一覧外)」が選択された投稿のことです。<br>
						※2：「表示条件が限定されていない状況」では常に非表示になり、「1投稿の単独表示時」では常に表示されます。それ以外の状況でどう表示するかを選択できます。
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldNewsign">【直近投稿を示すサインの表示】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizecss-latestlist">？</a></span>
					<ul class="list">
						<li><label>サインを表示する制限時間：<input type="text" value="$setdat{'newsignhours'}" name="newsignhours" size="5">時間</label> <span class="inputguide">(標準：72)</span></li>
						<li><label>サインの表記：<input type="text" value="$setdat{'newsignhtml'}" name="newsignhtml"></label> <span class="inputguide">※$allowhtmlmsg。(標準：New!)</span></li>
					</ul>
					<p class="inputguide">
						※上記の表記は、内側スキンの中に [[NEW]] を書いた位置に挿入されます。<br>
						※内側スキンの中に [[NEW]] を書いていない場合は、どこにも表示されません。<br>
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldJargon">【システムメッセージ・表示用語】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#edit-system-messages">？</a></span>
					<p>
						▼表示対象がない場合に表示されるシステムメッセージ <span class="inputguide">※$allowhtmlmsg。</span>
					</p>
					<ul class="list">
						<li><label>表示対象が１件もない場合：<input type="text" value="$setdat{'msgnolist'}" name="msgnolist" class="longinput"></label><span class="inputguide">(標準：表示できる投稿が1件も見つかりませんでした。)</span></li>
						<li><label>指定の単独投稿がない場合：<input type="text" value="$setdat{'msgnopost'}" name="msgnopost" class="longinput"></label><span class="inputguide">(標準：指定された番号の投稿は存在しません。まだ作成されていないか、または削除されました。)</span></li>
						<li><label>まだ何も投稿されていない場合：<input type="text" value="$setdat{'msgnodata'}" name="msgnodata" class="longinput"></label><span class="inputguide">(標準：まだ1件も投稿されていません。)</span></li>
					</ul>
					<p id="headerstrings" class="withseparator">
						▼表示順序を示す用語：
					</p>
					<ul class="list">
						<li><label>降順での表示時：<input type="text" value="$setdat{'showstraightheader'}" name="showstraightheader"></label><span class="inputguide">(標準：新しい順)</span></li>
						<li><label>昇順での表示時：<input type="text" value="$setdat{'showreverseheader'}" name="showreverseheader"></label><span class="inputguide">(標準：時系列順)</span></li>
					</ul>
				</fieldset>

				<fieldset>
					<legend id="fldShortcutkey">【移動用ショートカットキー】</legend>
					<ul class="list">
						<li><label>投稿欄へ移動するキー：<input type="text" value="$setdat{'postareakey'}" name="postareakey" class="onechar" maxlength="1"></label><span class="inputguide">(標準：p)</span></li>
						<li><label>検索窓へ移動するキー：<input type="text" value="$setdat{'searchinputkey'}" name="searchinputkey" class="onechar" maxlength="1"></label><span class="inputguide">(標準：k)</span></li>
					</ul>
					<p class="inputguide" style="max-width:24em;">
						※英字1文字だけを指定できます。キーの組み合わせはブラウザによって異なりますが、Windows版のChromeやFirefoxでは [Alt]+[Shift]+[英字] で移動できます。<br>
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldDatelist">【日付リストの構成】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizecss-datelist">？</a></span>
					<ul>
						<li><label><input type="checkbox" name="datelistShowYear" value="1" $setdat{'datelistShowYear'}>日付リストに年単独の階層を加える</label></li>
						<li><label><input type="checkbox" name="datelistShowZero" value="1" $setdat{'datelistShowZero'}>月が1桁の場合は、先頭に0を加えて2桁にする</label></li>
					</ul>
					<!-- 前の状態 --><input type="hidden" name="befdatelistSY" value="$setdat{'datelistShowYear'}">
					<!-- 前の状態 --><input type="hidden" name="befdatelistSZ" value="$setdat{'datelistShowZero'}">
				</fieldset>
			</div>
			<div class="tabcontent" id="tabcontent2">
				<div class="shortcuslinkbox">
					<p class="shortcutlinktitle">ショートカット：</p>
					<ul class="shortcutlinklist">
						<li><a href="#fldQuickpost">QUICKPOSTの表示</a></li>
						<li><a href="#fldPostForm">投稿入力欄の表示と動作</a></li>
						<li><a href="#fldPostBox">投稿コントロール枠内の設定</a></li>
						<li><a href="#fldButtonDate">日時ボタンの表示設定</a></li>
						<li><a href="#fldButtonImage">画像ボタンの表示と動作</a></li>
						<li><a href="#fldButtonDecorate">装飾ボタンの表示設定</a></li>
						<li><a href="#fldButtonLink">リンクボタンの表示設定</a></li>
						<li><a href="#fldEasyHashtag">既存ハッシュタグ簡単入力機能</a></li>
						<li><a href="#fldCheckCategory">カテゴリ選択の表示設定</a></li>
						<li><a href="#fldCheckFunc">機能ボタンの表示設定</a></li>
						<li><a href="#fldBtnCommonSet">文字装飾・リンク挿入機能の動作設定</a></li>
					</ul>
				</div>
				<fieldset>
					<legend id="fldQuickpost">【QUICKPOSTの表示】</legend>
					<p>
						▼QUICKPOST(ページ内に埋め込む投稿欄)の表示：<br>
					</p>
					<ul>
						<li>
							<label><input type="radio" name="alwaysshowquickpost" value="0" $alwaysshowquickpost[0]>ログインしている際にのみ表示する</label><br>
							<label><input type="radio" name="alwaysshowquickpost" value="1" $alwaysshowquickpost[1]>ログインしていなくても表示する</label><br>
						</li>
					</ul>
					<p class="inputguide" style="max-width:29em;">
						※「ログインしていなくても表示する」を選択すると、すべてのアクセス者にQUICKPOSTが見えます。その場合でも、投稿ボタンを押した後にログイン画面が表示されます。<br><strong>（ログインせずに投稿できるわけではありません。）</strong>
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldPostForm">【投稿入力欄の表示と動作】</legend>
					<p>
						▼プレースホルダ(空欄の際に薄く表示する文字列)：<br>
					</p>
					<ul class="list">
						<li><label><input type="checkbox" name="postphloginname" value="1" $setdat{'postphloginname'}>プレースホルダにログイン中のユーザ名を表示する</label></li>
						<li><label>続く文言：<input type="text" class="longinput" value="$setdat{'postplaceholder'}" name="postplaceholder"></label><span class="inputguide">(標準：さん、いまなにしてる？)</span></li>
					</ul>
					<p class="withseparator">
						▼入力欄の高さ(編集領域の表示行数)と動作：<br>
					</p>
					<ul class="list">
						<li><label><span style="display:inline-block;min-width:9em;">管理画面内の入力欄</span>：<input type="text" value="$setdat{'textareasizenormal'}" name="textareasizenormal" size="4">行</label> <span class="inputguide">(標準:12行／最低:4行／※1)</span></li>
						<li><label><span style="display:inline-block;min-width:9em;">QUICKPOST入力欄</span>：<input type="text" value="$setdat{'textareasizequick'}"  name="textareasizequick"  size="4">行</label> <span class="inputguide">(標準:4.3行／最低:1.8行／※1)</span></li>
						<li><label><input type="checkbox" name="postareaexpander" value="1" $setdat{'postareaexpander'}>入力欄の高さを <strong class="key">[Ctrl]＋[↓] キー</strong>で拡張できるようにする</label> <span class="inputguide">(※2)</span></li>
						<li><label><input type="checkbox" name="postautofocus" value="1" $setdat{'postautofocus'}>管理画面内の入力欄には最初からカーソルを入れておく</label> <span class="inputguide">(※3)</span></li>
					</ul>
					<p class="inputguide" style="max-width:42em;">
						※1:入力欄の右下端をマウスでドラッグすれば、一時的に(縦横に)サイズを変えられます。<br>
						※2:入力欄内にカーソルがあるとき、[Ctrl]＋[↓]キーを押すたびに入力欄の高さが2倍に拡張されます（最大でブラウザの高さまで）。[Ctrl]＋[↑]キーだと半分に縮小されます。<br>
						※3:管理画面内での新規投稿(または既存投稿の編集)画面のみ。(QUICKPOSTは対象外)<br>
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldPostBox">【投稿コントロール枠内の設定】</legend>
					<p>
						▼投稿枠内に表示する項目の設定・選択：<br>
					</p>
					<ul class="list">
						<li><label>投稿送信ボタンのラベル：<input type="text" value="$setdat{'postbuttonlabel'}" name="postbuttonlabel"></label><span class="inputguide">(標準：投稿する)</span>
							<ul class="list">
								<li><label><input type="checkbox" name="postbuttonshortcut" value="1" $setdat{'postbuttonshortcut'}>ボタンを <strong class="key">[Ctrl]＋[Enter] キー</strong>でも押せるようにする</label></li>
							</ul>
						</li>
						<li><label><input type="checkbox" name="postcharcounter" value="1" $setdat{'postcharcounter'}>入力文字数のカウンタを表示</label></li>
						<li>
							<input type="checkbox" name="postchangeidlink" id="postchangeidlink" value="1" $setdat{'postchangeidlink'}><label for="postchangeidlink">他のIDに切り替えるリンクを表示</label>
							<ul class="list">
								<li><label>ラベル：<input type="text" value="$setdat{'postchangeidlabel'}" name="postchangeidlabel"></label><span class="inputguide">(標準：他のIDに切り替える)</span></li>
							</ul>
						</li>
					</ul>
				</fieldset>

				<fieldset>
					<legend id="fldButtonDate">【日時ボタンの表示設定】</legend>
					<p>
						▼投稿日時ボタンの表示と動作：<br>
					</p>
					<ul class="list">
						<li><input type="checkbox" name="showFreeDateBtn" value="1" $setdat{'showFreeDateBtn'} id="showFreeDateBtn"><label for="showFreeDateBtn">投稿日時の自由入力ボタン「<input type="text" value="$setdat{'datebuttonlabel'}" name="datebuttonlabel" class="shortinput">」を表示する</label></li>
						<li><label><input type="checkbox" name="allowillegaldate" value="1" $setdat{'allowillegaldate'}>存在しない日時での投稿も許可する</label> <span class="inputguide">※例「15月63日」のような。</span></li>
					</ul>
					<p class="inputguide">
						※この機能を使っても、投稿の表示は「投稿順」です。日時順にソートはされません。<br>
						※存在しない日時を許可する場合でも、月別に集計されるのは1月～12月だけです。<br>
						※曜日を表示するスキンでは、存在しない日付に対する曜日は「？」と表示されます。<br>
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldButtonImage">【画像ボタンの表示と動作】</legend>
					<p>
						▼画像掲載ボタンの表示：<br>
					</p>
					<ul>
						<li>
							<label><input type="radio" name="showImageUpBtn" value="1" $showImageUpBtn[1]>ボタン「<input type="text" value="$setdat{'imagebuttonlabel'}"  name="imagebuttonlabel" class="shortinput">」の押下で展開</label><br>
							<label><input type="radio" name="showImageUpBtn" value="2" $showImageUpBtn[2]>最初から展開しておく(常時表示)</label><br>
							<label><input type="radio" name="showImageUpBtn" value="0" $showImageUpBtn[0]>一切表示しない(常時非表示)</label><br>
						</li>
					</ul>
					<p class="inputguide" style="max-width: 25.5em;">
						※ボタンを非表示にしても、システム設定で画像投稿が許可されていれば、管理画面の「画像の管理」を使って画像ファイルをアップロードできます。<br>
						※システム設定で画像投稿が禁止されていれば、設定に関係なくボタンは表示されません。<br>
					</p>
					<p class="withseparator">
						▼本文と同時に画像を投稿した場合の配置<br>
					</p>
					<ul>
						<li>
							<label><input type="radio" name="imagedefaultplace" value="0" $imagedefaultplace[0]>本文より前に画像を挿入する</label><br>
							<label><input type="radio" name="imagedefaultplace" value="1" $imagedefaultplace[1]>本文より前に画像を挿入して直後を改行する</label><br>
							<label><input type="radio" name="imagedefaultplace" value="2" $imagedefaultplace[2]>本文の後に画像を挿入する</label><br>
							<label><input type="radio" name="imagedefaultplace" value="3" $imagedefaultplace[3]>本文の後を改行してから画像を挿入する</label><br>
						</li>
					</ul>
					<p class="inputguide">
						※画像の配置は、後から編集すれば自由に変更できます。<br>（ここではデフォルトの配置を決めるだけです。）<br>
					</p>
					<p class="withseparator">
						▼表示する画像ボタンの選択：<br>
					</p>
					<table class="decBtnTable standard">
						<tr><th>画像ボタンの種類</th><th>ラベル</th></tr>
						<tr><td><label><input type="checkbox" name="showImageBtnNewUp" value="1" $setdat{'showImageBtnNewUp'}><span>新規画像の投稿 </span></label></td><td>－</td></tr>
						<tr><td><label><input type="checkbox" name="showImageBtnExist" value="1" $setdat{'showImageBtnExist'}><span>任意画像の挿入 </span></label></td><td><input type="text" value="$setdat{'imageBtnExistLabel'}"  name="imageBtnExistLabel" size="12"></td></tr>
					</table>
					<p class="inputguide" style="max-width:25.5em;">
						※「ページの表示」設定側で、画像の表示関連機能を無効化していれば、それぞれの機能に対応するボタンは設定に関係なく常に非表示になります。<br>
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldButtonDecorate">【装飾ボタンの表示設定】</legend>
					<p>
						▼装飾ボタンの表示： <span class="inputguide">(※1)</span><br>
					</p>
					<ul>
						<li>
							<label><input type="radio" name="showDecoBtnStyle" value="0" $showDecoBtnStyle[0]>ボタン「<input type="text" value="$setdat{'decobuttonlabel'}"  name="decobuttonlabel" class="shortinput">」の押下で展開</label><br>
							<label><input type="radio" name="showDecoBtnStyle" value="1" $showDecoBtnStyle[1]>最初から展開しておく(常時表示)</label><br>
							<label><input type="radio" name="showDecoBtnStyle" value="2" $showDecoBtnStyle[2]>一切表示しない(常時非表示)</label><br>
						</li>
					</ul>
					<p class="withseparator">
						▼表示する装飾ボタンの選択： <span class="inputguide">(※2,3)</span><br>
					</p>
					<table class="decBtnTable standard">
						<tr><th>新規/編集画面</th><th>QUICKPOST</th><th>ラベル</th></tr>
						<tr><td><label><input type="checkbox" name="showDecoBtnEonA" value="1" $setdat{'showDecoBtnEonA'}><span>強調	</span></label></td><td><label><input type="checkbox" name="showDecoBtnEonQ" value="1" $setdat{'showDecoBtnEonQ'}><span>強調	</span></label></td><td><input type="text" value="$setdat{'decoBtnLabelE'}"  name="decoBtnLabelE" size="3"></td></tr>
						<tr><td><label><input type="checkbox" name="showDecoBtnBonA" value="1" $setdat{'showDecoBtnBonA'}><span>太字	</span></label></td><td><label><input type="checkbox" name="showDecoBtnBonQ" value="1" $setdat{'showDecoBtnBonQ'}><span>太字	</span></label></td><td><input type="text" value="$setdat{'decoBtnLabelB'}"  name="decoBtnLabelB" size="3"></td></tr>
						<tr><td><label><input type="checkbox" name="showDecoBtnIonA" value="1" $setdat{'showDecoBtnIonA'}><span>斜体	</span></label></td><td><label><input type="checkbox" name="showDecoBtnIonQ" value="1" $setdat{'showDecoBtnIonQ'}><span>斜体	</span></label></td><td><input type="text" value="$setdat{'decoBtnLabelI'}"  name="decoBtnLabelI" size="3"></td></tr>
						<tr><td><label><input type="checkbox" name="showDecoBtnUonA" value="1" $setdat{'showDecoBtnUonA'}><span>下線	</span></label></td><td><label><input type="checkbox" name="showDecoBtnUonQ" value="1" $setdat{'showDecoBtnUonQ'}><span>下線	</span></label></td><td><input type="text" value="$setdat{'decoBtnLabelU'}"  name="decoBtnLabelU" size="3"></td></tr>
						<tr><td><label><input type="checkbox" name="showDecoBtnQonA" value="1" $setdat{'showDecoBtnQonA'}><span>引用	</span></label></td><td><label><input type="checkbox" name="showDecoBtnQonQ" value="1" $setdat{'showDecoBtnQonQ'}><span>引用	</span></label></td><td><input type="text" value="$setdat{'decoBtnLabelQ'}"  name="decoBtnLabelQ" size="3"></td></tr>
						<tr><td><label><input type="checkbox" name="showDecoBtnDonA" value="1" $setdat{'showDecoBtnDonA'}><span>取消線	</span></label></td><td><label><input type="checkbox" name="showDecoBtnDonQ" value="1" $setdat{'showDecoBtnDonQ'}><span>取消線	</span></label></td><td><input type="text" value="$setdat{'decoBtnLabelD'}"  name="decoBtnLabelD" size="3"></td></tr>
						<tr><td><label><input type="checkbox" name="showDecoBtnSonA" value="1" $setdat{'showDecoBtnSonA'}><span>小さめ	</span></label></td><td><label><input type="checkbox" name="showDecoBtnSonQ" value="1" $setdat{'showDecoBtnSonQ'}><span>小さめ	</span></label></td><td><input type="text" value="$setdat{'decoBtnLabelS'}"  name="decoBtnLabelS" size="3"></td></tr>
						<tr><td><label><input type="checkbox" name="showDecoBtnTonA" value="1" $setdat{'showDecoBtnTonA'}><span>極小	</span></label></td><td><label><input type="checkbox" name="showDecoBtnTonQ" value="1" $setdat{'showDecoBtnTonQ'}><span>極小	</span></label></td><td><input type="text" value="$setdat{'decoBtnLabelT'}"  name="decoBtnLabelT" size="3"></td></tr>
						<tr><td><label><input type="checkbox" name="showDecoBtnRonA" value="1" $setdat{'showDecoBtnRonA'}><span>ルビ	</span></label></td><td><label><input type="checkbox" name="showDecoBtnRonQ" value="1" $setdat{'showDecoBtnRonQ'}><span>ルビ	</span></label></td><td><input type="text" value="$setdat{'decoBtnLabelR'}"  name="decoBtnLabelR" size="3"></td></tr>
						<tr><td><label><input type="checkbox" name="showDecoBtnConA" value="1" $setdat{'showDecoBtnConA'}><span>文字色	</span></label></td><td><label><input type="checkbox" name="showDecoBtnConQ" value="1" $setdat{'showDecoBtnConQ'}><span>文字色	</span></label></td><td><input type="text" value="$setdat{'decoBtnLabelC'}"  name="decoBtnLabelC" size="3"></td></tr>
						<tr><td><label><input type="checkbox" name="showDecoBtnMonA" value="1" $setdat{'showDecoBtnMonA'}><span>背景色	</span></label></td><td><label><input type="checkbox" name="showDecoBtnMonQ" value="1" $setdat{'showDecoBtnMonQ'}><span>背景色	</span></label></td><td><input type="text" value="$setdat{'decoBtnLabelM'}"  name="decoBtnLabelM" size="3"></td></tr>
						<tr><td><label><input type="checkbox" name="showDecoBtnHonA" value="1" $setdat{'showDecoBtnHonA'}><span>隠す	</span></label></td><td><label><input type="checkbox" name="showDecoBtnHonQ" value="1" $setdat{'showDecoBtnHonQ'}><span>隠す	</span></label></td><td><input type="text" value="$setdat{'decoBtnLabelH'}"  name="decoBtnLabelH" size="3"></td></tr>
						<tr><td><label><input type="checkbox" name="showDecoBtnFonA" value="1" $setdat{'showDecoBtnFonA'}><span>自由装飾</span></label></td><td><label><input type="checkbox" name="showDecoBtnFonQ" value="1" $setdat{'showDecoBtnFonQ'}><span>自由装飾</span></label></td><td><input type="text" value="$setdat{'decoBtnLabelF'}"  name="decoBtnLabelF" size="3"></td></tr>
					</table>
					<p class="inputguide" style="max-width:22.5em;">
						※1:「ページの表示」設定側で装飾機能を無効化していれば、常に非表示です。<br>
						※2:ボタンを非表示にしても、装飾記法を直接記述すればすべての装飾が使えます。<br>
						※3:自由装飾は事前準備が必須。<a href="$aif{'puburl'}usage/#howtouse-chardecoration-class" $mpconfirm>詳細はこちら</a>。
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldButtonLink">【リンクボタンの表示設定】</legend>
					<p>
						▼リンクボタンの表示： <span class="inputguide">(※1)</span><br>
					</p>
					<ul>
						<li>
							<label><input type="radio" name="showLinkBtnStyle" value="0" $showLinkBtnStyle[0]>ボタン「<input type="text" value="$setdat{'linkbuttonlabel'}"  name="linkbuttonlabel" class="shortinput">」の押下で展開</label><br>
							<label><input type="radio" name="showLinkBtnStyle" value="1" $showLinkBtnStyle[1]>最初から展開しておく(常時表示)</label><br>
							<label><input type="radio" name="showLinkBtnStyle" value="2" $showLinkBtnStyle[2]>一切表示しない(常時非表示)</label><br>
						</li>
					</ul>
					<p class="withseparator">
						▼表示するリンクボタンの選択： <span class="inputguide">(※2)</span><br>
					</p>
					<table class="decBtnTable standard">
						<tr><th>リンクボタンの種類</th><th>ラベル</th></tr>
						<tr><td><label><input type="checkbox" name="showLinkBtnUrl" value="1" $setdat{'showLinkBtnUrl'}><span>任意URLリンク </span></label></td><td><input type="text" value="$setdat{'linkBtnUrlLabel'}"  name="linkBtnUrlLabel" size="12"></td></tr>
						<tr><td><label><input type="checkbox" name="showLinkBtnNum" value="1" $setdat{'showLinkBtnNum'}><span>指定No.リンク </span></label></td><td><input type="text" value="$setdat{'linkBtnNumLabel'}"  name="linkBtnNumLabel" size="12"></td></tr>
						<tr><td><label><input type="checkbox" name="showLinkBtnImg" value="1" $setdat{'showLinkBtnImg'}><span>画像埋込リンク</span><span class="inputguide">(※3)</span></label></td><td><input type="text" value="$setdat{'linkBtnImgLabel'}"  name="linkBtnImgLabel" size="12"></td></tr>
						<tr><td><label><input type="checkbox" name="showLinkBtnTwe" value="1" $setdat{'showLinkBtnTwe'}><span>ツイート埋込  </span></label></td><td><input type="text" value="$setdat{'linkBtnTweLabel'}"  name="linkBtnTweLabel" size="12"></td></tr>
						<tr><td><label><input type="checkbox" name="showLinkBtnYtb" value="1" $setdat{'showLinkBtnYtb'}><span>YouTube埋込   </span></label></td><td><input type="text" value="$setdat{'linkBtnYtbLabel'}"  name="linkBtnYtbLabel" size="12"></td></tr>
						<tr><td><label><input type="checkbox" name="showLinkBtnSpt" value="1" $setdat{'showLinkBtnSpt'}><span>Spotify埋込   </span></label></td><td><input type="text" value="$setdat{'linkBtnSptLabel'}"  name="linkBtnSptLabel" size="12"></td></tr>
					</table>
					<p class="inputguide" style="max-width:22.5em;">
						※1:「ページの表示」設定側で、URLの自動リンク機能を無効化していれば、設定に関係なく常に非表示になります。<br>
						※2:「任意URLリンク」以外の各ボタンは、それぞれの機能が無効に設定されている場合は上記の設定に関係なく非表示になります。<br>
						<br>
						※3：この機能で画像を埋め込んでもギャラリーモードには表示されません。この項目は過去との互換性のために残してあるだけです。画像をURLで指定して表示するには、『画像』ボタン側の「任意画像を挿入」機能を使う方が便利です。
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldEasyHashtag">【既存ハッシュタグ簡単入力機能】</legend>
					<p>
						▼既存ハッシュタグ入力ボタンの表示：<br>
					</p>
					<ul>
						<li>
							<label><input type="radio" name="showHashtagBtnStyle" value="0" $showHashtagBtnStyle[0]>ボタン「<input type="text" value="$setdat{'hashbuttonlabel'}"  name="hashbuttonlabel" class="shortinput">」の押下で展開</label><br>
							<label><input type="radio" name="showHashtagBtnStyle" value="1" $showHashtagBtnStyle[1]>最初から展開しておく(常時表示)</label><br>
							<label><input type="radio" name="showHashtagBtnStyle" value="2" $showHashtagBtnStyle[2]>一切表示しない(常時非表示)</label><br>
						</li>
					</ul>
					<p class="withseparator">
						▼リストアップする最大個数：<br>
					</p>
					<ul class="list">
						<li><label>最大 <input type="text" value="$setdat{'hashtagBtnListupMax'}"  name="hashtagBtnListupMax" size="4">個までリストアップ</label> <span class="inputguide">(標準:20個)</span></li>
					</ul>
					<p class="inputguide" style="max-width:25em;">
						※個数を制限しない場合は「0」を指定して下さい。<br>
						※ハッシュタグが1つもない(または未集計な)状況では設定に関係なくボタンは常に非表示になります。
					</p>
					<p class="withseparator">
						▼リストに追加する項目：
					</p>
					<ul>
						<li><label><input type="checkbox" name="showHashBtnHash" value="1" $setdat{'showHashBtnHash'}><span>「#」記号だけを挿入する項目を先頭に追加</span></label></li>
					</ul>
				</fieldset>

				<fieldset>
					<legend id="fldCheckCategory">【カテゴリ選択の表示設定】</legend>
					<p>
						▼カテゴリボタンの表示：<br>
					</p>
					<ul>
						<li>
							<label><input type="radio" name="showCategoryBtnStyle" value="0" $showCategoryBtnStyle[0]>ボタン「<input type="text" value="$setdat{'categorybuttonlabel'}"  name="categorybuttonlabel" class="shortinput">」の押下で展開</label><br>
							<label><input type="radio" name="showCategoryBtnStyle" value="1" $showCategoryBtnStyle[1]>最初から展開しておく(常時表示)</label><br>
							<label><input type="radio" name="showCategoryBtnStyle" value="2" $showCategoryBtnStyle[2]>一切表示しない(常時非表示)</label><br>
						</li>
					</ul>
					<p class="inputguide" style="max-width:21em;">
						※カテゴリが1つも存在しない状況では、設定に関係なくボタンは常に非表示になります。
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldCheckFunc">【機能ボタンの表示設定】</legend>
					<p>
						▼機能ボタンの表示：<br>
					</p>
					<ul>
						<li>
							<label><input type="radio" name="showFuncBtnStyle" value="0" $showFuncBtnStyle[0]>ボタン「<input type="text" value="$setdat{'funcbuttonlabel'}"  name="funcbuttonlabel" class="shortinput">」の押下で展開</label><br>
							<label><input type="radio" name="showFuncBtnStyle" value="1" $showFuncBtnStyle[1]>最初から展開しておく(常時表示)</label><br>
							<label><input type="radio" name="showFuncBtnStyle" value="2" $showFuncBtnStyle[2]>一切表示しない(常時非表示)</label><br>
						</li>
					</ul>
					<p class="withseparator">
						▼表示する機能の選択：
					</p>
					<ul>
						<li><label><input type="checkbox" name="showFuncBtnSpeech" value="1" $setdat{'showFuncBtnSpeech'}><span>読み上げ</span></label></li>
						<li><label><input type="checkbox" name="showFuncBtnStaytop" value="1" $setdat{'showFuncBtnStaytop'}><span>先頭に固定</span></label> <span class="inputguide">(※1)</span></li>
						<li><label><input type="checkbox" name="showFuncBtnDraft" value="1" $setdat{'showFuncBtnDraft'}><span>下書き(非公開)</span></label> <span class="inputguide">(※2)</span></li>
						<li><label><input type="checkbox" name="showFuncBtnRear" value="1" $setdat{'showFuncBtnRear'}><span>下げる(一覧外)</span></label> <span class="inputguide">(※3)</span></li>
					</ul>
					<p class="inputguide" style="max-width:22em;">
						※1：管理者権限のないユーザでログインしている場合では、設定に関係なく常に非表示です。<br>
						※2：ゲスト権限では表示されません。<br>
						※3：下げた投稿をどこに表示するかは、[ページの表示]→[下げた投稿の表示]で設定できます。<br>
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldBtnCommonSet">【文字装飾・リンク挿入機能の動作設定】</legend>
					<p>
						▼ボタンを押した際の動作：<br>
					</p>
					<ul class="list">
						<li><label><input type="checkbox" name="allowblankdeco" value="1" $setdat{'allowblankdeco'}>事前に範囲選択していなくても各種記法を挿入する</label></li>
					</ul>
					<p class="inputguide" style="max-width:40em;">
						※ここをONにすると、装飾対象やリンク対象を事前に範囲選択して<strong>いない</strong>状態でも、「範囲選択して下さい」というエラーを<strong>出さずに</strong>各種記法を編集領域に挿入します。<br>※画面幅が1024px以下の場合は、ここの設定に関係なく常に挿入できます。
					</p>
				</fieldset>

			</div>
			<div class="tabcontent" id="tabcontent3">
				<fieldset>
					<legend>【ヘッダ用フリースペース】</legend>
					<p>
						▼ページのヘッダ部分に表示する文言：<br>
					</p>
					<ul class="list">
						<li><label>主タイトル：<input type="text" class="longinput" value="$setdat{'freetitlemain'}" name="freetitlemain"></label> <span class="inputguide">(Title 前半)</span></li>
						<li><label>副タイトル：<input type="text" class="longinput" value="$setdat{'freetitlesub'}" name="freetitlesub"></label> <span class="inputguide">(Title 後半)</span></li>
						<li><label>一行概要文：<input type="text" class="longinput" value="$setdat{'freedescription'}" name="freedescription"></label> <span class="inputguide">(Description)</span></li>
					</ul>
					<p class="inputguide">
						※想定は「ヘッダ掲載」用途ですが、スキン次第でどこにでも表示できます。<br>※上記の設定は、RSSフィードやOGP＋Twitter Cardの出力にも使われます。
					</p>
				</fieldset>
				<fieldset>
					<legend>【フッタ用フリースペース】</legend>
					<p>
						▼ページのフッタ部分に表示するリンク：<br>
					</p>
					<ul class="list">
						<li><label>リンクラベル：<input type="text" class="longinput" value="$setdat{'freehomename'}" name="freehomename"></label></li>
						<li><label>リンク先URL：<input type="text" class="longinput" value="$setdat{'freehomeurl'}" name="freehomeurl"></label></li>
						<li>リンク表示先：<select name="freehomeatt"><option value="0" $freehomeatt[0]>同一ウインドウ(タブ)</option><option value="1" $freehomeatt[1]>新規ウインドウ(タブ)</option><option value="2" $freehomeatt[2]>フレーム解除</option></select></li>
					</ul>
					<p class="inputguide" style="max-width:30em;">
						※フッタに掲載する「サイトのHOMEへ戻る」リンクとしての使用を想定していますが、スキン次第でどこにでも表示できます。
					</p>
				</fieldset>
				<fieldset style="display:block;">
					<legend>【多目的フリースペース】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#specification-freespace">？</a></span>
					<p>
						▼多目的フリースペース欄の設定
					</p>
					<ul class="list">
						<li><label>見出し：<input type="text" class="longinput" value="$setdat{'freesptitle'}" name="freesptitle"></label></li>
					</ul>
					<p class="withseparator">
						◆多目的フリースペースに掲載する内容: <span class="inputguide">※$allowhtmlmsg。改行をそのまま反映するかどうかは、下部の設定項目で選択できます。</span><br>
						<textarea name="freespace" cols="45" rows="10" id="fsp">$setdat{'freespace'}</textarea><br>
					</p>
					<p class="skinguide">
						※上記のフリースペース欄に入力した内容は、スキンファイル内に <strong>[[FREESPACE]]</strong> と記述した位置に挿入されます。
						<button href="#freespaceDetailGuide" onclick="document.getElementById('freespaceDetailGuide').style.display='block'; this.style.display='none'; return false;">簡易ヘルプを見る</button>
					</p>
					<p class="skinguide hidedetail" id="freespaceDetailGuide">
						※フリースペース内には、区切り文字 <input type="text" value="&lt;&gt;" style="width:3em;" readonly> が使えます。使用個数に制限はありません。(半角で入力)<br>
						※スキン内に <strong>[[FREESPACE:<strong class="important">0</strong>]]</strong> と記述すれば、<strong class="important">先頭から</strong>最初の区切り文字までの内容だけが挿入されます。<br>
						※スキン内に <strong>[[FREESPACE:<strong class="important">1</strong>]]</strong> と記述すれば、<strong class="important">1つ目の区切り文字から</strong>次の区切り文字までの内容だけが挿入されます。<br>
						※詳しい仕様は、<a href="$aif{'puburl'}#howtouse">オンラインヘルプ</a>の「<a href="$aif{'puburl'}#specification-freespace">フリースペースの書き方</a>」欄をご参照下さい。<br>
					</p>
					<p class="withseparator">
						▼多目的フリースペース欄の表示方法
					</p>
					<ul>
						<li><label><input type="checkbox" name="allowbrinfreespace" value="1" $setdat{'allowbrinfreespace'}>入力した改行は、実際の表示上でも改行する</label></li>
					</ul>
					<p class="inputguide" $hideinsafemode9>
						※上記のチェックをOFFにすると、入力した改行は（表示される際には）すべて無視されます。その場合、改行したい箇所には &lt;br /&gt; タグを書いて下さい。<br>
						フリースペース内に<strong class="important">HTMLソースを記述する場合は、このチェックはOFFにしておく</strong>ことをお勧め致します。（HTMLソースの途中で改行している際に、改行タグが自動挿入されると、表示が崩れる可能性があるため。）
					</p>
				</fieldset>
			</div>
			<div class="tabcontent" id="tabcontent5">
				<div class="shortcuslinkbox">
					<p class="shortcutlinktitle">ショートカット：</p>
					<ul class="shortcutlinklist">
						<li><a href="#fldSubGallery">ギャラリーの出力</a></li>
						<li><a href="#fldSubRss">RSSフィードの出力</a></li>
						<li><a href="#fldSubOgpTwitter">OGP＋Twitter Cardの出力</a></li>
						<li><a href="#fldSubSitemapPage">サイトマップページの出力</a></li>
						<li><a href="#fldSubSitemapXml">SITEMAP XMLの出力</a></li>
					</ul>
				</div>
				<fieldset>
					<legend id="fldSubGallery">【ギャラリーの出力】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizeinfo-galleryskin">？</a></span>
					<p>
						▼ギャラリーの基本設定： <span class="inputguide">(<a href="?mode=gallery" target="_blank">ギャラリーページを見る</a>)</span>
					</p>
					<ul class="list">
						<li><input type="checkbox" name="galleryoutput" id="galleryoutput" value="1" $setdat{'galleryoutput'}><label for="galleryoutput">ギャラリー表示機能を使う</label> <span class="inputguide">(※1)</span>
							<ul class="list">
								<li><label>スキン格納ディレクトリ名：<input type="text" value="$setdat{'galleryskindir'}" name="galleryskindir"></label><span class="inputguide">(標準:skin-gallery／※2)</span></li>
								<li><label>ギャラリーの名称：<input type="text" value="$setdat{'galleryname'}" name="galleryname"></label></li>
								<li><label><input type="checkbox" name="gallerydatebar" value="1" $setdat{'gallerydatebar'}>日付境界バーを挿入する</label> <span class="inputguide">(※3)</span></li>
								<li><label><input type="checkbox" name="gallerysituation" value="1" $setdat{'gallerysituation'}>該当件数とページ番号を表示する</label> <span class="inputguide">(※4)</span></li>
							</ul>
							<p class="innersubtitle withseparator">
								▼1ページあたりに表示される投稿数： <span class="inputguide">(※5)</span>
							</p>
							<ul class="list">
								<li><label><input type="text" value="$setdat{'galleryentries'}" name="galleryentries" size="5">個</label></li>
							</ul>
						</li>
					</ul>
					<p class="inputguide" style="max-width: 42em;">
						※1：画像の含まれる投稿だけを、専用スキンで一覧表示できる機能です。<br>
						※2：CGI直下のディレクトリのみ指定可能。「-」と「_」以外の記号は使えません。ここで指定したスキン以外でも、skinパラメータを使えば複数のスキンを併用できます。<br>
						※3：挿入条件や挿入内容は「ページの表示／全体」での設定が使われます。<br>
						※4：状況表示部分に件数を表示し、2ページ目以降ではページ番号も表示します。<br>
						※5：スキン側に収録個数が指定されている場合はそちらが優先されます。
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldSubRss">【RSSフィードの出力】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizeinfo-rssfeed">？</a></span>
					<p>
						▼RSSフィードの基本設定： <span class="inputguide">(<a href="?mode=rss" target="_blank">RSSフィードを見る</a>)</span>
					</p>
					<ul class="list">
						<li><input type="checkbox" name="rssoutput" id="rssoutput" value="1" $setdat{'rssoutput'}><label for="rssoutput">RSSフィードを出力する</label>
							<ul class="subopt">
								<li>
									<label><input type="radio" name="rssskin" value="0" $rssskin[0]>内蔵のRSSスキン(抜粋収録)を使う</label> <span class="inputguide">(※1)</span><br>
									<label><input type="radio" name="rssskin" value="1" $rssskin[1]>内蔵のRSSスキン(全文収録)を使う</label> <span class="inputguide">(※2)</span><br>
									<label><input type="radio" name="rssskin" value="2" $rssskin[2]>自作のRSSスキンを使う</label> <span class="inputguide">(※3)</span><br>
									<ul class="subopt">
										<li><label>スキン格納ディレクトリ名：<input type="text" value="$setdat{'rssskindir'}" name="rssskindir"></label><span class="inputguide">(標準:rss)</span></li>
									</ul>
								</li>
							</ul>
							<p class="innersubtitle withseparator">
								▼RSSフィードに含める投稿数： <span class="inputguide">(※4)</span>
							</p>
							<ul class="list">
								<li><label><input type="text" value="$setdat{'rssentries'}" name="rssentries" size="5">個</label></li>
							</ul>
						</li>
					</ul>
					<p class="inputguide" style="max-width: 36em;">
						※1：先頭120文字だけを収録します。画像や装飾は省略されます。<br>
						※2：全文を収録します。画像を埋め込むHTMLも含まれます。<br>
						※3：CGI直下のディレクトリのみ指定可能。「-」と「_」以外の記号は使えません。ここで指定したスキン以外でも、skinパラメータを使えば複数のスキンを併用できます。<br>
						※4：スキン側に収録個数が指定されている場合はそちらが優先されます。
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldSubOgpTwitter">【OGP＋Twitter Cardの出力】</legend> <span class="helpbox"><a class="help uh" href="$aif{'puburl'}usage/#howtouse-ogp">？</a></span>
					<p>
						▼OGP＋Twitter Card用meta要素の出力：<br>
					</p>
					<ul class="list">
						<li><input type="checkbox" name="ogpoutput" id="ogpoutput" value="1" $setdat{'ogpoutput'}><label for="ogpoutput">OGP＋Twitter Cardを出力する</label><span class="inputguide">(※1)</span>
							<p class="innersubtitle withseparator">▼OGPの設定：</p>
							<ul class="list">
								<li><label><span class="ogn">og:title</span>：<select disabled><option>自動取得</option></select><span class="inputguide">(※A)</span></li>
								<li><label><span class="ogn">og:description</span>：<select name="ogdescription"><option value="0" $ogdescription[0]>自動取得</option><option value="1" $ogdescription[1]>og:titleと同じ内容</option></select><span class="inputguide">(※A)</span></li>
								<li><label><span class="ogn">og:url</span>：<select disabled><option>自動取得</option></select></li>
								<li><label><span class="ogn">og:locale</span>：<input type="text" value="$setdat{'oglocale'}" name="oglocale"></label><span class="inputguide">(※B)</span></li>
								<li><label><span class="ogn">og:site_name</span>：<input type="text" value="$setdat{'ogsitename'}" name="ogsitename"></label><span class="inputguide">(※B)</span></li>
								<li><label><span class="ogn">og:type</span>：</label><select name="ogtype"><option value="0" $ogtype[0]>単独投稿ページは article、それ以外は website</option><option value="1" $ogtype[1]>常に article</option><option value="2" $ogtype[2]>常に website</option></select></li>
								<li>og:image
									<ul class="subbox">
										<li><input type="checkbox" checked disabled><label>共通画像のURL：<input type="text" value="$setdat{'ogimagecommonurl'}" name="ogimagecommonurl" placeholder="https://"></label><span class="inputguide">(※2)</span></li>
										<li><label><input type="checkbox" name="ogimageuse1st" value="1" $setdat{'ogimageuse1st'}>投稿に画像が含まれる場合は、1つ目の画像URLを指定<span class="inputguide">(※3)</span><br>（投稿に画像が含まれない場合は、共通画像URLを指定）</label></li>
									</ul>
								</li>
							</ul>
							<p class="innersubtitle withseparator">▼Twitter Cardの設定：</p>
							<ul class="list">
								<li><label><span class="ogn">twitter:card</span>：</label><select name="twittercard"><option value="0" $twittercard[0]>summary (小画像)</option><option value="1" $twittercard[1]>summary_large_image (大画像)</option></select></li>
								<li><label><span class="ogn">twitter:site</span>：<input type="text" value="$setdat{'twittersite'}" name="twittersite" placeholder="@"></label><span class="inputguide">(※B)</span></li>
								<li><label><span class="ogn">twitter:creator</span>：<input type="text" value="$setdat{'twittercreator'}" name="twittercreator" placeholder="@"></label><span class="inputguide">(※B)</span></li>
							</ul>
						</li>
					</ul>
					<p class="inputguide">
						※1:ここをONにしても、外側スキン内に [[OGP]] の記述がなければ出力されません。<br>一度表示された後はSNS側でキャッシュされるため、変更はすぐには反映されません。<br>
						※2:投稿単独ページではない場合は、常にここに指定した画像URLが出力されます。<br>何も指定しなかった場合は、<a href="$libdat{'ogimagedefault'}" target="_blank">デフォルトの共通画像</a>が使われます。<br>
						※3:[PICT:～]記法で挿入された画像のみが対象で、[IMG:*]URL記法は対象外です。<br>
						※A:単独投稿ページでは本文の抜粋を、それ以外ではフリースペースの記述を使用。<br>
						※B:空欄にすると、この要素自体の出力を省略します。(必須項目ではありません)<br>
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldSubSitemapPage">【サイトマップページの出力】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizeinfo-sitemappage">？</a></span>
					<p>
						▼サイトマップページの基本設定： <span class="inputguide">(<a href="?mode=sitemap" target="_blank">サイトマップページを見る</a>)</span>
					</p>
					<ul class="list">
						<li><input type="checkbox" name="sitemappageoutput" id="sitemappageoutput" value="1" $setdat{'sitemappageoutput'}><label for="sitemappageoutput">サイトマップページ表示機能を使う</label> <span class="inputguide">(※1)</span>
							<ul class="list">
								<li><label>スキン格納ディレクトリ名：<input type="text" value="$setdat{'sitemappageskindir'}" name="sitemappageskindir"></label><span class="inputguide">(標準:skin-sitemap／※2)</span></li>
								<li><label>サイトマップページの名称：<input type="text" value="$setdat{'sitemappageyname'}" name="sitemappageyname"></label></li>
								<li><label><input type="checkbox" name="sitemappagedatebar" value="1" $setdat{'sitemappagedatebar'}>日付境界バーを挿入する</label> <span class="inputguide">(※3)</span></li>
								<li><label><input type="checkbox" name="sitemappagefixed" value="1" $setdat{'sitemappagefixed'}>先頭固定設定を反映する</label> <span class="inputguide">(※4)</span></li>
								<li><label><input type="checkbox" name="sitemapsituation" value="1" $setdat{'sitemapsituation'}>該当件数とページ番号を表示する</label> <span class="inputguide">(※5)</span></li>
							</ul>
							<p class="innersubtitle withseparator">
								▼1ページあたりに表示される投稿数： <span class="inputguide">(※6)</span>
							</p>
							<ul class="list">
								<li><label><input type="text" value="$setdat{'sitemappageentries'}" name="sitemappageentries" size="5">個</label></li>
							</ul>
						</li>
					</ul>
					<p class="inputguide" style="max-width: 42em;">
						※1：人間向けの目次ページのことです。検索エンジン用のSITEMAP XMLとは異なります。<br>
						※2：CGI直下のディレクトリのみ指定可能。「-」と「_」以外の記号は使えません。ここで指定したスキン以外でも、skinパラメータを使えば複数のスキンを併用できます。<br>
						※3：挿入条件や挿入内容は「ページの表示／全体」での設定が使われます。<br>
						※4：ここがOFFだと、先頭固定に指定されていても無視して新着順に並びます。<br>
						※5：状況表示部分に件数を表示し、2ページ目以降ではページ番号も表示します。<br>
						※6：スキン側に収録個数が指定されている場合はそちらが優先されます。
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldSubSitemapXml">【SITEMAP XMLの出力】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#customizeinfo-xmlsitemap">？</a></span>
					<p>
						▼SITEMAP XMLの基本設定： <span class="inputguide">(<a href="?mode=xmlsitemap" target="_blank">SITEMAP XMLを見る</a>)</span>
					</p>
					<ul class="list">
						<li><input type="checkbox" name="xmlsitemapoutput" id="xmlsitemapoutput" value="1" $setdat{'xmlsitemapoutput'}><label for="xmlsitemapoutput">SITEMAP XMLを出力する</label></li>
					</ul>
					<p class="inputguide" style="max-width: 36em;">
						※URLだけが列挙されるXML形式のサイトマップファイルを出力します。<br>
						※5万件単位でページ分割されます。<br>
					</p>
				</fieldset>
			</div>
			<div class="tabcontent" id="tabcontent4">
				<div class="shortcuslinkbox">
					<p class="shortcutlinktitle">ショートカット：</p>
					<ul class="shortcutlinklist">
						<li><a href="#fldSysAfterPost">投稿動作</a></li>
						<li><a href="#fldSysServertime">時刻設定</a></li>
						<li><a href="#fldSysFullpath">フルパス設定</a></li>
						<li><a href="#fldSysDocRoot">サーバパス設定</a></li>
						<li><a href="#fldSysImagepost">画像投稿機能</a></li>
						<li><a href="#fldSysImageSupport">許可する画像の種類</a></li>
						<li><a href="#fldSysLightboxScript">画像拡大スクリプトの選択</a></li>
						<li><a href="#fldSysBackup">バックアップの設定</a></li>
						<li><a href="#fldSysControlpanel">管理画面内の表示</a></li>
						<li><a href="#fldSysFuncRestriction">機能制限／高度な設定</a></li>
						<li><a href="#fldSysLoginKeep">ログイン維持設定</a></li>
					</ul>
				</div>
				<fieldset>
					<legend id="fldSysAfterPost">【投稿動作】</legend>
					<p>
						▼投稿や編集直後の動作(移動先)：<br>
					</p>
					<ul>
						<li>
							<label><input type="radio" name="afterpost" value="0" $afterpost[0]>HOME または 単独ページに戻る</label> <span class="inputguide">(※1)</span><br>
							<label><input type="radio" name="afterpost" value="1" $afterpost[1]>常に「投稿結果のステータス画面」を表示</label> <span class="inputguide">(※2)</span><br>
							<label><input type="radio" name="afterpost" value="2" $afterpost[2]>常に「てがろぐHOME」へ戻る</label>
						</li>
					</ul>
					<p class="inputguide">※1：新規投稿後ならHOMEに、編集後なら投稿単独ページに。<br>※2：スキン側に編集ボタンを表示<strong>せずに使う</strong>場合にお勧め。</p>
				</fieldset>
				<fieldset>
					<legend id="fldSysServertime">【時刻設定】</legend>
					<ul>
						<li>サーバの時刻から
							<select name="shiftservtime">
								@optionsforshiftservtime
							</select>
							時間ずらした時刻を現在日時にする
						</li>
					</ul>
					<p class="inputguide">
						※サーバの時刻設定が現在時刻とずれている場合に調整できます。<br>
						※過去の投稿も含めてすべて一律にずらします。<br>
						（表示時に時刻をずらすだけで、記録データは元の日時のままです。）<br>
						※サーバ時刻がGMTなら、「+9」でJSTになります。<br>
						※時刻が正しくて、ずらす必要がないなら「0」のままにして下さい。<br>
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldSysFullpath">【フルパス設定】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#howtoembedskin">？</a></span>
					<p>
						▼CGIの設置位置：<br>
					</p>
					<ul>
						<li>
							<label><input type="radio" name="howtogetfullpath" value="0" $howtogetfullpath[0]>自動取得</label> <span class="inputguide">(推奨)</span><br>
							<label><input type="radio" name="howtogetfullpath" value="1" $howtogetfullpath[1]>固定：</label>
							<input type="text" value="$setdat{'fixedfullpath'}" name="fixedfullpath" class="longinput" placeholder="https://"></label><br>
						</li>
					</ul>
					<p class="inputguide" style="max-width:24em;">※必要性がなければ「自動取得」を推奨致します。<br>※SSI等で埋め込んで使う場合は固定して下さい。<br>※ドメイン名を省略した、「/」から始めるフルパスでの記述も可能(その方が無難)です。</p>
				</fieldset>

				<fieldset>
					<legend id="fldSysDocRoot">【サーバパス設定】</legend>
					<p>
						▼ドキュメントルートの位置：<br>
					</p>
					<ul>
						<li>
							<label><input type="radio" name="howtogetdocroot" value="0" $howtogetdocroot[0]>環境変数から自動取得</label><br>
							<label><input type="radio" name="howtogetdocroot" value="1" $howtogetdocroot[1]>固定：</label>
							<input type="text" value="$setdat{'fixeddocroot'}" name="fixeddocroot" class="longinput"></label><br>
						</li>
					</ul>
					<p class="inputguide" style="max-width:25em;">※画像保存用ディレクトリ以外の位置にある同一サーバ内（同一ドメイン内）の画像ファイルの縦横サイズが取得できない場合は、正しいドキュメントルートのパスを入力して固定して下さい。<br>※てがろぐCGIまでのパスでは<strong>なく</strong>、Webサイトの最上階層(＝DOCUMENT ROOT)を示すサーバパスを指定しなければならない点に注意して下さい。</p>
				</fieldset>

				<fieldset>
					<legend id="fldSysImagepost">【画像投稿機能】</legend>
					<p>
						▼画像アップロードの基本設定
					</p>
					<ul class="list">
						<li><input type="checkbox" name="imageupallow" id="imageupallow" value="1" $setdat{'imageupallow'}><label for="imageupallow">画像の投稿を許可する</label>
							<ul class="list">
								<li><label><input type="checkbox" name="imageupmultiple" value="1" $setdat{'imageupmultiple'}>複数枚の画像を同時に投稿可能にする</label>
								<li><label><input type="checkbox" name="imageupsamename" value="1" $setdat{'imageupsamename'}>元のファイル名をできるだけ維持する</label> <span class="inputguide">(※1,2)</span>
							</ul>
						</li>
<!--						<li>画像投稿は <select name="imageuprequirelevel"><option value="1">1:ゲスト</option></select> 以上の権限にのみ許可する</li>	-->
					</ul>
					<p class="inputguide" style="max-width:35em;">
						※1：ファイル名が<strong>英数字だけ</strong>なら、ファイル名を変更せずアップロードします。この場合、編集者権限未満のユーザは（自分がUPした画像でも）自分では<strong>削除できなくなります</strong>のでご注意下さい。<br>※2：同名のファイルが既にある場合は、ファイル名に連番を付加します。<br>
					</p>
					<p class="withseparator">
						▼画像保存容量の設定
					</p>
					<ul class="list">
						<li><input type="checkbox" name="imagemaxlimits" id="imagemaxlimits" value="1" $setdat{'imagemaxlimits'}><label for="imagemaxlimits">投稿できる画像サイズや画像の保存容量に上限を設ける</label><br>
							<span class="inputguide">※以下の設定は、上限を設ける場合にのみ有効（単位に注意）</span>
							<ul class="list">
								<li><label>画像1枚あたりの最大サイズ：<input type="text" value="$setdat{'imagemaxbytes'}" name="imagemaxbytes" size="6"><b class="unit unitKB">KB</b></label> <span class="inputguide">(標準：5120KB)</span></li>
								<li><label>保存可能な画像の最大枚数：<input type="text" value="$setdat{'imagefilelimit'}" name="imagefilelimit" size="6">枚</label> <span class="inputguide">(標準：10000枚)</span></li>
								<li><label>画像保存に使える最大容量：<input type="text" value="$setdat{'imagestoragelimit'}" name="imagestoragelimit" size="6"><b class="unit unitMB">MB</b></label> <span class="inputguide">(標準：300MB)</span></li>
							</ul>
						</li>
					</ul>
					<p class="inputguide">
						※画像の表示を許可するかどうかは「ページの表示」タブ側で設定できます。<br>
						※設定を変更しても、既にUPされた画像は消えません。<br>
						※投稿を禁止しても、表示が許可されていれば、既存画像の掲載は可能です。<br>
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldSysImageSupport">【許可する画像の種類】</legend>
					<p>
						▼アップロードを許可する画像形式
					</p>
					<p>1行1個でファイル拡張子を列挙：</p>
					<textarea name="imageallowext" style="font-size:1em; width:6em; height:12em;">$imageextlist</textarea>
					<p class="inputguide" style="max-width:19em;">
						※大文字・小文字は区別しません。<br>
						※ドット記号「.」は入力不要です。<br>
						※英数字のみ指定可能です。(記号不可)<br>
						<br>
						※リストにない拡張子のファイルは、新規アップロードができないだけでなく、<strong class="important">既にアップロードしてある画像も表示されなくなります</strong>。
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldSysLightboxScript">【画像拡大スクリプトの選択】</legend> <span class="helpbox"><a class="help ch" href="$aif{'puburl'}custom/#lightbox-like-script">？</a></span>
					<p>
						▼画像拡大表示に使うスクリプト <span class="inputguide">(※1)</span>
					</p>
					<ul>
						<li><label><input type="radio" name="isuselightbox" value="1" $isuselightbox[1]>Lightboxを使う</label> <span class="inputguide">(※2)</span></li>
						<li><input type="radio" name="isuselightbox" id="isuselightbox0" value="2" $isuselightbox[2]><label for="isuselightbox0">他のスクリプトを使う</label> <span class="inputguide">(※3,4)</span>
							<ul class="list imageexpanding">
								<li><label><span class="imageexpanding">JavaScriptのURL</span>：<input type="text" value="$setdat{'imageexpandingjs'}" name="imageexpandingjs" class="longinput" placeholder="https://"></label> <span class="inputguide"></span></li>
								<li><label><span class="imageexpanding">CSSのURL</span>：<input type="text" value="$setdat{'imageexpandingcss'}" name="imageexpandingcss" class="longinput" placeholder="https://"></label> <span class="inputguide"></span></li>
							</ul>
						</li>
					</ul>
					<p class="inputguide" style="max-width:38em;">
						※1：jQueryは別途CDNから読み込まれます。(注:スキンの書き方次第)<br>
						※2：LightboxはCDNから読み込まれるため、何も設置せずに使えます。<br>
						※3：他のスクリプトを使う場合は、リンク(a要素)に加える必要のある属性値を、[設定]→[ページの表示]→【投稿本文の表示／画像】や【投稿本文内のURL処理】項目等に指定して下さい。これをしないと、スクリプトは意図通りに働きません。<br>
						※4：2つ以上のJavaScriptファイル（jQueryを除く）を読み込む必要があるなら、ここではLightboxを選択しておき、直接スキンHTML内に望みのJavaScriptを読み込む記述を加えて下さい。<br>
					</p>
				</fieldset>

				<fieldset>
					<legend id="fldSysBackup">【バックアップの設定】</legend>
					<p>
						▼自動バックアップ機能：<br>
					</p>
					<ul>
						<li><input type="checkbox" name="autobackup" id="autobackup" value="1" $setdat{'autobackup'}><label for="autobackup">投稿のたびに過去データを自動バックアップする</label>
							<ul class="list">
								<li>保持ファイル数：<label><input type="text" value="$setdat{'backupfilehold'}" name="backupfilehold" size="3" maxlength="3">個</label> <span class="inputguide">(※標準30／範囲:2～366)</span></li>
							</ul>
						</li>
					</ul>
					<p class="inputguide" style="max-width: 30em;">
						※自動バックアップ機能は、バックアップ用ディレクトリが存在しなければ、設定に関係なく実行されません。<br>
						※保持ファイル数を減らすと、次回の自動バックアップ時に<strong class="important">超過分のバックアップファイルは自動的に消されます</strong>のでご注意下さい。<br>
						※バックアップ状況は、管理画面の「<a href="?mode=admin&amp;work=backup" $mpconfirm>自動バックアップ</a>」項目で確認できます。<br>
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldSysControlpanel">【管理画面内の表示】</legend>
					<p>
						▼管理画面の配色：
					</p>
					<script type="text/javascript">
						var colors = [['#aaccaa','#000080,#0080ff'],['#c0b76a','#505000,#bbbb50'],['#95c664','#005000,#00c050'],['#f7cdd4','#f04061,#f8aab9'],['#88a4cc','#0e1a39,#877fac'],['#eebd7c','#ef6b04,#febe78'],['#f0f0f0','#000000,#aaaaaa']];
						function themePreview( themenum ) {
							document.getElementById('colorTheme1').style.backgroundColor = colors[themenum][0];
							document.getElementById('colorTheme2').style.background = 'linear-gradient( 0deg,' + colors[themenum][1] + ')';
						}
					</script>
					<ul class="list">
						<li>カラーテーマ：<select name="conpanecolortheme" onchange="themePreview(this.value);" id="conpanecolortheme"><option value="0" $conpanecolortheme[0]>デフォルト配色</option><option value="1" $conpanecolortheme[1]>砂金</option><option value="2" $conpanecolortheme[2]>新緑</option><option value="3" $conpanecolortheme[3]>桃桜</option><option value="4" $conpanecolortheme[4]>葡萄</option><option value="5" $conpanecolortheme[5]>蜜柑</option><option value="6" $conpanecolortheme[6]>灰石</option></select><span id="colorTheme1"></span><span id="colorTheme2"></span></li>
					</ul>
					<script type="text/javascript">document.getElementById('conpanecolortheme').onchange();</script>
					<p class="withseparator">
						▼管理画面のタイトル先頭に挿入される識別名：<br>
					</p>
					<ul class="list">
						<li><label><input type="text" value="$setdat{'conpanedistinction'}" name="conpanedistinction" class="halfinput"></label> <span class="inputguide">(標準:なし)</span></li>
					</ul>
					<p class="withseparator">
						▼管理画面の最下部に表示される「戻る」リンク：<br>
					</p>
					<ul>
						<li><input type="checkbox" disabled checked>初期表示ページに移動するリンクを表示
							<ul class="list">
								<li><label>ラベル：<input type="text" value="$setdat{'conpaneretlinklabel'}" name="conpaneretlinklabel"></label> <span class="inputguide">(標準:てがろぐHOMEへ戻る)</span></li>
							</ul>
						</li>
						<li class="readablespace"><input type="checkbox" name="conpanegallerylink" id="conpanegallerylink" value="1" $setdat{'conpanegallerylink'}><label for="conpanegallerylink">ギャラリーページに移動するリンクを表示</label>
							<ul class="list">
								<li><label>ラベル：<input type="text" value="$setdat{'conpanegallerylabel'}" name="conpanegallerylabel"></label> <span class="inputguide">(標準:ギャラリーへ戻る)</span></li>
							</ul>
						</li>
					</ul>
					<p class="withseparator">
						▼管理画面内のUI：
					</p>
					<ul class="list">
						<li><label><input type="checkbox" name="syspagelinkomit" value="1" $setdat{'syspagelinkomit'}>総ページ数が多い場合に途中のページ番号リンクを省略する</label> <span class="inputguide">(※1)</span></li>
						<li><label><input type="checkbox" name="sysdelbtnpos" value="1" $setdat{'sysdelbtnpos'}>投稿削除・カテゴリ削除ボタンを右寄せで表示する</label> <span class="inputguide">(※2)</span></li>
						<li><label>投稿一覧画面で1ページに表示する投稿数：<input type="text" value="$setdat{'postperpageforsyslist'}" name="postperpageforsyslist" size="3" maxlength="5">件</label> <span class="inputguide">(標準100)</span></li>
						<li><label>画像管理画面で1ページに表示する画像枚数：<input type="text" value="$setdat{'imageperpage'}" name="imageperpage" size="3">枚</label> <span class="inputguide">(標準15)</span></li>
					</ul>
					<p class="inputguide" style="max-width: 39em;">
						※1：投稿一覧画面や画像管理画面で、ページ数が多い場合に途中を省略します。この設定は管理画面内のUIのみが対象です。管理画面外のページネーションは、「ページの表示」タブ内の【ナビゲーションリンクの表示】→「ページ番号リンク」区画内で設定できます。<br>
						※2：赤色で目立つ削除ボタンが左側にあると間違えて押してしまう！という場合に。
					</p>
				</fieldset>
				<fieldset>
					<legend id="fldSysFuncRestriction">【機能制限／高度な設定】</legend>
					<p>
						▼機能制限：
					</p>
					<ul>
						<li><label><input type="checkbox" name="exportpermission" id=" exportpermission" value="1" $setdat{'exportpermission'}>エクスポート機能の使用は、ログイン者のみに限定する</label></li>
						<li><label><input type="checkbox" name="funcrestreedit" id="funcrestreedit" value="1" $setdat{'funcrestreedit'}>管理者や編集者IDでも、他者の投稿の再編集を禁止する</label> <span class="inputguide">(※1)</span></li></li>
						<li><label><input type="checkbox" name="datelimitreedit" id="datelimitreedit" value="1" $setdat{'datelimitreedit'}>投稿時点から<input type="text" value="$setdat{'datelimitreeditdays'}" name="datelimitreeditdays" size="3" maxlength="3">日を過ぎた投稿の再編集を禁止する</label> <span class="inputguide">(※2)</span></li></li>
					</ul>
					<p class="inputguide" style="max-width: 35em;">
						※1：この項目がOFFだと、管理者や編集者は他者の投稿を再編集できます。ただし、再編集すると投稿者名は編集したユーザの名前に変わりますから、他者の投稿を他者名義のままで改変できるわけではありません。<br>
						※2：12時間に設定したい場合は「0.5」を指定して下さい。値を「0」にはできません。値を「1」にすると、投稿時点から24時間後に再編集できなくなります。
					</p>
					<p class="withseparator">
						▼高度な設定：
						<span id="highsetbtn"><input type="button" value="設定を表示する" onclick="document.getElementById('highsetbtn').style.display='none'; document.getElementById('highsets').style.display='block';"></span>
					</p>
					<ul id="highsets">
						<li><label><input type="checkbox" name="loadeditcssjs" id=" loadeditcssjs" value="1" $setdat{'loadeditcssjs'}>編集画面で、edit.cssとedit.jsを(あれば)読み込む</label></li>
						<li><label><input type="checkbox" name="envlistonerror" id=" envlistonerror" value="1" $setdat{'envlistonerror'}>エラー発生時の参考情報の表示を省略する</label></li>
					</ul>
					<script>document.getElementById('highsets').style.display='none';</script>
				</fieldset>
				<fieldset>
					<legend id="fldSysLoginKeep">【ログイン維持設定】</legend> <span class="helpbox"><a class="help uh" href="$aif{'puburl'}setup/#multiplecgis-set">？</a></span>
					<p>
						▼ログイン状態を維持する期限： <span class="inputguide">※最短0.1日・最長366日（標準31日）</span><br>
					</p>
					<ul>
						<li>
							<input type="text" value="$setdat{'sessiontimenum'}" name="sessiontimenum" size="7">日<br>
							$sessionkeepmsg
						</li>
					</ul>
					<p class="withseparator">
						▼複数CGIの共存設定：<br>
					</p>
					<ul>
						<li><input type="checkbox" name="coexistflag" id="coexistflag" value="1" $setdat{'coexistflag'}><label for="coexistflag">同一ドメイン下に設置された複数の「てがろぐ」CGIを共存可能にする</label> <span class="inputguide">(推奨)</span>
							<ul class="list">
								<li>このCGI固有の識別文字列：<input type="text" value="$setdat{'coexistsuffix'}" name="coexistsuffix" size="7" maxlength="12"> <span class="inputguide">(※英数字のみ／Cookieの接尾辞に使われます)</span></li>
							</ul>
						</li>
					</ul>
					<p class="inputguide">
						※てがろぐCGIを同一ドメイン下に複数個設置する場合は、それぞれの設定画面で<strong class="important">異なる識別文字列</strong>を<br>
						設定して下さい。すると、それぞれのCGIで個別にログイン状態を維持できるようになります。<br>
						※この機能をOFFにしたり、同じ文字列を指定したりすると、異なる「てがろぐ」にアクセスする度に<br>
						自動ログアウトしてしまいます。（※同じ文字列を指定しても、IDを共用できるわけでは<strong>ありません</strong>）
					</p>
				</fieldset>
				<fieldset style="vertical-align:bottom;">
					<legend id="fldSysMode">【動作種別】</legend>
					<p>
						ライセンス：<input type="text" value="$setdat{'licencecode'}" name="licencecode" size="18" placeholder="フリー版" class="licencebox"><br>
						バージョン：$versionnum
					</p>
					<ul class="list licenceopt" $hideinfreever>
						<li><label>Powered-by表記：<input type="checkbox" name="signhider" value="1" $setdat{'signhider'}>非表示</label></li>
						<li><label for="aboutcgibox">このCGIについて：</label><select name="aboutcgibox" id="aboutcgibox" style="font-size:0.9em;"><option value="0" $aboutcgibox[0]>全表示</option><option value="1" $aboutcgibox[1]>下部のみ消す</option><option value="2" $aboutcgibox[2]>Ver以外を消す</option><option value="3" $aboutcgibox[3]>全部を非表示</option></select></li>
					</ul>
					<p class="inputguide" $hideinfreever>
						※<a href="?mode=licence" $mpconfirm>ライセンスの確認</a>
					</p>
				</fieldset>
			</div>
			<label for="tabcheck1" class="tab tabbtm" id="tabbtm1"><span class="stdtabname">ページ</span><span class="longtabname">の表示</span></label>
			<label for="tabcheck2" class="tab tabbtm" id="tabbtm2"><span class="stdtabname">投稿欄</span><span class="longtabname">の表示</span></label>
			<label for="tabcheck3" class="tab tabbtm" id="tabbtm3"><span class="stdtabname">フリー</span><span class="longtabname">スペース</span></label>
			<label for="tabcheck5" class="tab tabbtm" id="tabbtm5"><span class="stdtabname">補助</span><span class="longtabname">出力</span></label>
			<label for="tabcheck4" class="tab tabbtm" id="tabbtm4"><span class="stdtabname">システム</span><span class="longtabname">設定</span></label>
			<p id="bottom">
				すべての設定が終わったら、下記のボタンを押して保存して下さい。（タブの切り替えは、保存前に可能です。）<br>
			</p>
			<p id="buttons">
				<input type="hidden" value="admin" name="mode">
				<input type="hidden" value="trychangeset" name="work">
				<input type="submit" value="設定を保存する" id="sendinputs">
			</p>
			<p class="noticebox">
				※上記の設定以外にも、スキンHTMLを直接編集することで様々なカスタマイズができます。詳しくは、<a href="$aif{'puburl'}custom/" $mpconfirm>カスタマイズ方法</a>をご参照下さい。<br>
				<span $hideinrental>※セキュリティ面に関する設定など、一部の高度な設定はCGIのソースコード先頭付近に直接記述する仕様です。CGIのソースをテキストエディタで編集して下さい。<br></span>
				※保存しようとすると<strong>Not Foundエラー</strong>になってしまうなど、<strong class="important">正常に保存処理ができない場合</strong>は、<a href="$aif{'puburl'}setup/#partialerror" $mpconfirm>トラブルシューティング</a>をご参照下さい。<br>
			</p>
		</form>
		<p class="scrollBtns">
			<script>
				function scrollbtn( stpos ) {
					window.scrollTo({ top: stpos, left: 0, behavior: 'smooth' });
				}
			</script>
			<a href="#top" class="totopBtn" onclick="scrollbtn(0); return false;"><span class="btnexp">上端へ</span><span class="arrow">▲</span></a>
			<a href="#bottom" class="tobtmBtn" onclick="scrollbtn(document.getElementById('main').clientHeight); return false;"><span class="arrow">▼</span><span class="btnexp">下端へ</span></a>
		</p>
		<script>
			var svgq = '<svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 0 24 24" width="18px"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"/></svg>';
			var chItems = document.querySelectorAll("a.help.ch");	// Custom Help
			chItems.forEach(function(aItem) {
				aItem.innerHTML = svgq + '<span class="label">カスタムヘルプ</span>';
				aItem.setAttribute("target", "_blank");
				aItem.setAttribute("title", "公式カスタマイズ方法を見る");
			});
			var uhItems = document.querySelectorAll("a.help.uh");	// Usage Help
			uhItems.forEach(function(aItem) {
				aItem.innerHTML = svgq + '<span class="label">使い方ヘルプ</span>';
				aItem.setAttribute("target", "_blank");
				aItem.setAttribute("title", "公式ヘルプを見る");
			});
		</script>
	|;

	# CSS：
	my $css = '<style type="text/css">
		.scrollBtns { position:fixed; bottom:0.67em; left: calc( 100vw - 2.75em - 20px ); }
		.scrollBtns a { display:block; margin:0 0 3px 0; background-color:blue; color:white; border-radius:12px; padding:0.4em 0.3em; line-height:1; opacity:0.6; text-decoration:none; text-align:center; }
		.scrollBtns a:hover { background-color:red; }
		.scrollBtns span { display:block; }
		.btnexp { font-size:0.67em; }
		.arrow { font-size:1.5em; }
		fieldset { margin: 1em; border: 1px solid #ccc; border-radius: 12px; background-color: white; }
		fieldset p { margin: 0.5em 0; }
		fieldset ul { list-style-type: none; margin:0; padding:0; }
		fieldset ul.list { list-style-type: disc; padding-left: 1.2em; }
		fieldset ul.subopt { padding-left: 1.2em; }
		.optmc5 label { display:inline-block; min-width:5em; }
		fieldset legend + p,
		.helpbox + p { font-weight: bold; }
		.innersubtitle { font-weight: bold; }
		.addeditem { list-style-type: none; }
		strong.safemode { color: #c00; }
		strong.key { color: #08a; }
		b.unit { display:inline-block; margin-left: 2px; }
		b.unitKB { color:#c80; }
		b.unitMB { color:#00c; }
		.licencebox { border: 1px solid white; font-size:0.95em; }
		.licencebox:focus { border: 1px solid gray; }
		.licenceopt { font-size:0.8em; color:#555;  }
		.longinput { width: 240px; }
		.halfinput { width: 4.5em; }
		.shortinput { width: 3em; }
		.onechar { width: 1.5em; }
		.ogn { min-width: 7.2em; display: inline-block; }
		/* ▼セパレータ付きBOX */
		.withseparator { margin-top: 1em; padding-top: 1em; border-top: 1px dashed gray; font-weight: bold; }
		.withshortseparation > li:not(:first-child) { margin-top: 1em; }
		/* ▼上方空間調整 */
		.readablespace { margin-top: 0.75em; }
		/* ▼入力案内 */
		.inputguide { font-size: smaller; color: #808080; line-height: 1.2; font-weight: normal; }
		p.inputguide { margin-top: 1.5em; }
		.inputguidebox { line-height: 1.2; border-top: 1px dashed crimson; margin-top: 1.25em; padding-top: 0.75em; }
		/* ▼装飾ボタン選択状態 */
		.decBtnTable input:checked + span { color: purple; font-weight: bold; }
		/* ▼フリスペ編集 */
		#fsp { width: 100%; height: 15em; box-sizing:border-box; }
		.skinguide { margin: 1em 1.1em; line-height:1.3; font-size: smaller; color: #555; }
		/* ▼セッション維持MSG */
		.inputinfo { font-size: 0.8em; line-height: 1.3; margin: 0.5em 0; padding: 0.25em; border-radius: 9px; background-color: #efc; }
		.inputinfo.alertinfo { background-color: #fdd; }
		/* ▼テーマプレビュー */
		#colorTheme1, #colorTheme2 { display: inline-block; width: 1.8em; height: 1.2em; vertical-align: middle; }
		#colorTheme1 { margin-left: 0.75em; background: #aaccaa; }
		#colorTheme2 { margin-left: 0.25em; background: linear-gradient( 0deg, #000080, #0080ff ); border-radius: 5px; }

		/* ▼タブ機能制御用ラジオボタンは非表示 */
		input.tabcheck { display: none; }
		/* ▼タブ(共通装飾＋非選択状態の装飾) */
		.tab {
			display: inline-block; padding: 0.67em 0.75em; border-width: 1px 1px 0 1px; border-style: solid; border-color: black; border-radius: 0.75em 0.75em 0 0;
			background-color: #e0e0e0; color: black; font-weight: bold;
			display: none\9;	/* IE8対策:全部非表示 */
		}
		.tab.tabbtm {
			border-width: 0 1px 1px 1px; border-radius: 0 0 0.75em 0.75em; margin-top: -1px; z-index: 10;
		}
		.longtabname { display: none; }
		.tab:hover {
			background-color: #ccffcc; color: green; cursor: pointer;
		}
		/* ▼チェックが入っているラジオボタンの隣にあるタブの装飾(＝選択状態のタブ) */
		input:checked + .tab {
			z-index: 10;
		}
		input:checked + #tab1 , #tabcheck1:checked ~ #tabbtm1 { background-color: #fdd; color: #d00; 	position:relative; }
		input:checked + #tab2 , #tabcheck2:checked ~ #tabbtm2 { background-color: #f5f5b5; color: #880; position:relative; }
		input:checked + #tab3 , #tabcheck3:checked ~ #tabbtm3 { background-color: #e0f0b0; color: #680; position:relative; }
		input:checked + #tab4 , #tabcheck4:checked ~ #tabbtm4 { background-color: #ddf; color: #00b; 	position:relative; }
		input:checked + #tab5 , #tabcheck5:checked ~ #tabbtm5 { background-color: #e0fcf7; color: #097; position:relative; }
		/* ▼タブの中身(共通装飾＋非選択状態の装飾) */
		.tabcontent {
			display: none; border: 1px solid gray; margin-top: -1px; position: relative; z-index: 0;
			display: block\9;	/* IE8対策:全部表示 */
		}
		/* ▼チェックが入っているラジオボタンに対応するタブの中身を表示する */
		#tabcheck1:checked ~ #tabcontent1,
		#tabcheck2:checked ~ #tabcontent2,
		#tabcheck3:checked ~ #tabcontent3,
		#tabcheck4:checked ~ #tabcontent4,
		#tabcheck5:checked ~ #tabcontent5 { display: block; }
		/* ▼タブ背景 */
		#tabcontent1 { background-color: #fdd; }
		#tabcontent2 { background-color: #f5f5b5; }
		#tabcontent3 { background-color: #e0f0b0; }
		#tabcontent4 { background-color: #ddf; }
		#tabcontent5 { background-color: #e0fcf7; }
		/* ▼チェックボックス連動サブ項目の表示 */
		input:not(:checked) ~ ul,
		input:not(:checked) ~ table { opacity: 0.42; }
		/* ▼ショートカットリンク群 */
		.shortcuslinkbox { margin:1em; display:flex; background-color:snow; line-height:1.5; font-size:0.95em; }
		.shortcutlinktitle { margin:0; padding:10px; font-size:0.67em; }
		.shortcutlinklist { list-style-type:none; margin:0; padding:6px 0; }
		.shortcutlinklist li { display:inline-block; }
		.shortcutlinklist li a { display:inline-block; color:#058; }
		.shortcutlinklist li a:hover { color:red; font-weight:bold; }
		.shortcutlinklist li a::before { content:"▼"; display:inline-block; }
		/* 個別 */
		ul.imageexpanding { margin-left:1em; }
		span.imageexpanding { display:inline-block; min-width:8em; }
		.disableitem { opacity: 0.42; }
		/* プレビューBOX */
		.situationPreviewBox { background-color:#fffff0; color:#050; border:1px dotted #880; font-size:0.67em; padding:0.67em 0.75em 0.5em; line-height:1.1; margin:0 0 0.75em 1.75em; }
		/* ▼モバイル調整 */
		.onlyNarrowMobile { display:none; }
		@media all and (min-width: 720px) {
			.tab li a { padding: 0.5em 0.5em 0.25em 0.5em; }
			.longtabname { display: inline; }
			fieldset ul.list { padding-left: 1.5em; }
		}
		@media (max-width: 599px) {
			.tab { padding: 0.67em 0.65em; }
			.stdtabname { font-size: 0.7rem; letter-spacing: -1px; }
			.onlyNarrowMobile { display:block; }
			.headGuide { font-size:0.9em; line-height:1.3; }
			.shortcuslinkbox { display:block; font-size:0.75em; line-height:1.6; }
			.shortcutlinktitle { padding:0; }
		}
		@media (max-width: 479px) {
			.mobileSetGuide { line-height:1.3; background:#ffc; padding:0.5em; border:1px dashed #cc8; }
			.mobileSetGuide strong { color:#a00; text-decoration: underline; text-decoration-style: wavy; }
		}
		@media (max-width: 320px) {
			.tab { padding: 0.67em 0.45em; }
			.stdtabname { font-size: 0.67rem; }
			.longinput { width: 180px; }
		}
	</style>';

	&showadminpage('SETTING','',$msg,'Z',$css);
}

# -------------------------------
# ADMIN：設定ファイルの更新を試行
# -------------------------------
sub adminTrychangeset
{
	# 不正送信の確認
	&fcts::postsecuritycheck('work=trychangeset');

	# 設定ファイルの更新(TRY)　※ここにはデフォルトの値を書くのではなく、データが来なかった場合の値を書く。(例:チェックボックスはOFFだとデータが来ない) 空欄を許さない自由入力欄の場合はデフォルト値を書く(＝入力が省略された場合はリセット扱い)。
	# HTMLフォーム側で適当に作られた項目を設定ファイルに記録してしまうのを防ぐために、ここでは想定済みの項目名だけをチェックして、それらだけを保存処理へ通すようにする。安全のため。

	my %trySetdat = (
		entryperpage		=> $cgi->param('entryperpage'		) || -1 , 	# 0はエラーにする
		separatepoint		=> $cgi->param('separatepoint'		) || 0 ,
		separateoption		=> $cgi->param('separateoption'		) || 0 ,
		separateyear		=> $cgi->param('separateyear'		) || 'Y年' ,
		separatemonth		=> $cgi->param('separatemonth'		) || 'G月' ,
		separatedate		=> $cgi->param('separatedate'		) || 'N日' ,
		separatebarreverse	=> $cgi->param('separatebarreverse'	) || 0 ,
		separatebaroutput	=> $cgi->param('separatebaroutput'	) || 0 ,

		situationvariation	=> $cgi->param('situationvariation'		) || 0 ,
		situationcount		=> $cgi->param('situationcount'			) || 0 ,
		situationpage		=> $cgi->param('situationpage'			) || 0 ,
		situationalwayspage	=> $cgi->param('situationalwayspage'	) || 0 ,
		situationcountlabel1=> $cgi->param('situationcountlabel1'	) || '' ,
		situationcountlabel2=> $cgi->param('situationcountlabel2'	) || '' ,
		situationpagelabel1	=> $cgi->param('situationpagelabel1'	) || '' ,
		situationpagelabel2	=> $cgi->param('situationpagelabel2'	) || '' ,

		eppoverride			=> $cgi->param('eppoverride'		) || 0 ,
		onepostpagesituation	=> $cgi->param('onepostpagesituation'	) || 0 ,
		onepostpageutilitybox	=> $cgi->param('onepostpageutilitybox'	) || 0 ,
		utilitystate		=> $cgi->param('utilitystate'		) || 0 ,
		utilityrandom		=> $cgi->param('utilityrandom'		) || 0 ,
		utilitycat			=> $cgi->param('utilitycat'			) || 0 ,
		utilitydates		=> $cgi->param('utilitydates'		) || 0 ,
		utilitydateymd		=> $cgi->param('utilitydateymd'		) || 0 ,
		utilitydateym		=> $cgi->param('utilitydateym'		) || 0 ,
		utilitydatey		=> $cgi->param('utilitydatey'		) || 0 ,
		utilitydatemd		=> $cgi->param('utilitydatemd'		) || 0 ,
		utilitydated		=> $cgi->param('utilitydated'		) || 0 ,
		utilityedit			=> $cgi->param('utilityedit'		) || 0 ,
		rssoutput			=> $cgi->param('rssoutput'		)	 || 0 ,
		rssskin				=> $cgi->param('rssskin'		)	 || 0 ,
		rssskindir			=> $cgi->param('rssskindir'		)	 || 'rss' ,
		rssentries			=> $cgi->param('rssentries'		)	 || 0 ,
		xmlsitemapoutput	=> $cgi->param('xmlsitemapoutput'	)	 || 0 ,

		sitemappageoutput	=> $cgi->param('sitemappageoutput'		)	 || 0 ,
		sitemappageyname	=> $cgi->param('sitemappageyname'		)	 || '' ,
		sitemappageskindir	=> $cgi->param('sitemappageskindir'		)	 || 'skin-sitemap' ,
		sitemappagedatebar	=> $cgi->param('sitemappagedatebar'		)	 || 0 ,
		sitemappageentries	=> $cgi->param('sitemappageentries'		)	 || 1 ,
		sitemappagefixed	=> $cgi->param('sitemappagefixed'	)	 || 0 ,
		sitemapsituation	=> $cgi->param('sitemapsituation'	)	 || 0 ,

		galleryoutput		=> $cgi->param('galleryoutput'		)	 || 0 ,
		galleryname			=> $cgi->param('galleryname'		)	 || '' ,
		galleryskindir		=> $cgi->param('galleryskindir'		)	 || 'skin-gallery' ,
		gallerydatebar		=> $cgi->param('gallerydatebar'		)	 || 0 ,
		gallerysituation	=> $cgi->param('gallerysituation'	)	 || 0 ,
		galleryentries		=> $cgi->param('galleryentries'		)	 || 1 ,

		unknownusername		=> $cgi->param('unknownusername'	) || '？' ,
		unknownusericon		=> $cgi->param('unknownusericon'	) || 0 ,
		unknownusericonurl	=> $cgi->param('unknownusericonurl'	) || '' ,

		pagelinkuse			=> $cgi->param('pagelinkuse'		) || 0 ,
		pagelinknext		=> $cgi->param('pagelinknext'		) || '' ,	# 次の (空白可)
		pagelinkprev		=> $cgi->param('pagelinkprev'		) || '' ,	# 前の (空白可)
		pagelinknum			=> $cgi->param('pagelinknum'		) || 0 ,
		pagelinkunit		=> $cgi->param('pagelinkunit'		) || '' ,	# 件 (空白可)
		pagelinkarrownext	=> $cgi->param('pagelinkarrownext'	) || '' ,	# » (空白可)
		pagelinkarrowprev	=> $cgi->param('pagelinkarrowprev'	) || '' ,	# « (空白可)

		pagelinkuseindv		=> $cgi->param('pagelinkuseindv'	) || 0 ,
		pagelinknextindv1	=> $cgi->param('pagelinknextindv1'	) || '' ,	# No. (空白可)
		pagelinknextindv2	=> $cgi->param('pagelinknextindv2'	) || '' ,	#  » (空白可)
		pagelinknextindvn	=> $cgi->param('pagelinknextindvn'	) || 0 ,
		pagelinkprevindv1	=> $cgi->param('pagelinkprevindv1'	) || '' ,	# « No. (空白可)
		pagelinkprevindv2	=> $cgi->param('pagelinkprevindv2'	) || '' ,
		pagelinkprevindvn	=> $cgi->param('pagelinkprevindvn'	) || 0 ,

		pagelinkseparator	=> $cgi->param('pagelinkseparator'	) || '' ,	# / (空白可)

		pagenumfigure		=> $cgi->param('pagenumfigure'		) || 0 ,
		pagenumomission		=> $cgi->param('pagenumomission'	) || 0 ,
		pagenumomitmark		=> $cgi->param('pagenumomitmark'	) || '' ,	# … (空白可)
		pagenumbracket1		=> $cgi->param('pagenumbracket1'	) || '' ,
		pagenumbracket2		=> $cgi->param('pagenumbracket2'	) || '' ,
		pagenumseparator	=> $cgi->param('pagenumseparator'	) || '' ,
		pagelinktop			=> $cgi->param('pagelinktop'		) || '初期表示に戻る' ,
		msgnolist			=> $cgi->param('msgnolist'			) || '表示できる投稿が1件も見つかりませんでした。' ,
		msgnopost			=> $cgi->param('msgnopost'			) || '指定された番号の投稿は存在しません。まだ作成されていないか、または削除されました。' ,
		msgnodata			=> $cgi->param('msgnodata'			) || 'まだ1件も投稿されていません。' ,
		showstraightheader	=> $cgi->param('showstraightheader'	) || '新しい順' ,
		showreverseheader	=> $cgi->param('showreverseheader'	) || '時系列順' ,
		fixedpostids		=> $cgi->param('fixedpostids'		) || '' ,
		fixedpostsign		=> $cgi->param('fixedpostsign'		) || '' ,
		fixedseparatepoint	=> $cgi->param('fixedseparatepoint'	) || 0 ,
		fixedseparatelabel	=> $cgi->param('fixedseparatelabel'	) || '' ,
		fixedpostdate		=> $cgi->param('fixedpostdate'		) || 0 ,

		rearappearcat		=> $cgi->param('rearappearcat'		) || 0 ,
		rearappeartag		=> $cgi->param('rearappeartag'		) || 0 ,
		rearappeardate		=> $cgi->param('rearappeardate'		) || 0 ,
		rearappearsearch	=> $cgi->param('rearappearsearch'	) || 0 ,

		imageshowallow		=> $cgi->param('imageshowallow'		) || 0 ,
		imageupallow		=> $cgi->param('imageupallow'		) || 0 ,
		imageupmultiple		=> $cgi->param('imageupmultiple'	) || 0 ,
		imageupsamename		=> $cgi->param('imageupsamename'	) || 0 ,
		imagemaxlimits		=> $cgi->param('imagemaxlimits'		) || 0 ,
		imagemaxbytes		=> $cgi->param('imagemaxbytes'		) || 100 ,
		imagefilelimit		=> $cgi->param('imagefilelimit'		) || 10000 ,
		imagestoragelimit	=> $cgi->param('imagestoragelimit'	) || 1 ,
		imageallowext		=> $cgi->param('imageallowext'		) || '' ,
		imageperpage		=> $cgi->param('imageperpage'		) || 15 , 	# 0は許容できない値
		showImageUpBtn		=> $cgi->param('showImageUpBtn'		) || 0 ,
		imagelazy			=> $cgi->param('imagelazy'			) || 0 ,
		imagetolink			=> $cgi->param('imagetolink'		) || 0 ,
		imagefullpath		=> $cgi->param('imagefullpath'		) || 0 ,
		imageaddclass		=> $cgi->param('imageaddclass'		) || 0 ,
		imageclass			=> $cgi->param('imageclass'			) || '' ,
		imagelightbox		=> $cgi->param('imagelightbox'		) || 0 ,
		imagelightboxatt	=> $cgi->param('imagelightboxatt'	) || 'data-lightbox="tegalog"' ,
		imagelightboxcap	=> $cgi->param('imagelightboxcap'	) || 'data-title' ,
		isuselightbox		=> $cgi->param('isuselightbox'		) || 1 ,	# 0の選択肢は今のところない
		imageexpandingjs	=> $cgi->param('imageexpandingjs'	) || '' ,
		imageexpandingcss	=> $cgi->param('imageexpandingcss'	) || '' ,
		imagewhatt			=> $cgi->param('imagewhatt'			) || 0 ,
		imagewhmax			=> $cgi->param('imagewhmax'			) || 0 ,
		imagemaxwidth		=> $cgi->param('imagemaxwidth'		) || '' ,
		imagemaxheight		=> $cgi->param('imagemaxheight'		) || '' ,
		imageoutdir			=> $cgi->param('imageoutdir'		) || 0 ,
		imageouturl			=> $cgi->param('imageouturl'		) || 0 ,

		latestlistup		=> $cgi->param('latestlistup'		) || 1 , 	# 0は許容できない値
		latestlistparts		=> $cgi->param('latestlistparts'	) || 'HBDTU' ,
		latesttitlecut		=> $cgi->param('latesttitlecut'		) || 15 , 	# 0は許容できない値

		readherebtnuse		=> $cgi->param('readherebtnuse'		) || 0 ,
		readmorebtnuse		=> $cgi->param('readmorebtnuse'		) || 0 ,
		readmoreonsearch	=> $cgi->param('readmoreonsearch'	) || 0 ,
		readmorecloseuse	=> $cgi->param('readmorecloseuse'	) || 0 ,
		readmorebtnlabel	=> $cgi->param('readmorebtnlabel'	) || '続きを読む' ,
		readmorecloselabel	=> $cgi->param('readmorecloselabel'	) || '畳む' ,
		readmorestyle		=> $cgi->param('readmorestyle'		) || 0 ,

		postidlinkize		=> $cgi->param('postidlinkize'		) || 0 ,
		postidlinkgtgt		=> $cgi->param('postidlinkgtgt'		) || 0 ,
		allowdecorate		=> $cgi->param('allowdecorate'		) || 0 ,
		urlautolink			=> $cgi->param('urlautolink'		) || 0 ,
		urllinktarget		=> $cgi->param('urllinktarget'		) || 0 ,
		urlnofollow			=> $cgi->param('urlnofollow'		) || 0 ,
		urlnoprotocol		=> $cgi->param('urlnoprotocol'		) || 0 ,
		urlexpandimg		=> $cgi->param('urlexpandimg'		) || 0 ,
		embedonlysamedomain	=> $cgi->param('embedonlysamedomain') || 0 ,
		urlimagelazy		=> $cgi->param('urlimagelazy'		) || 0 ,
		urlimageaddclass	=> $cgi->param('urlimageaddclass'	) || 0 ,
		urlimageclass		=> $cgi->param('urlimageclass'		) || '' ,
		urlimagelightbox	=> $cgi->param('urlimagelightbox'	) || 0 ,
		urlimagelightboxatt	=> $cgi->param('urlimagelightboxatt') || 'data-lightbox="tegalog"' ,
		urlimagelightboxcap	=> $cgi->param('urlimagelightboxcap') || 'data-title' ,
		urlexpandyoutube	=> $cgi->param('urlexpandyoutube'	) || 0 ,
		urlexpandspotify	=> $cgi->param('urlexpandspotify'	) || 0 ,
		urlexpandtweet		=> $cgi->param('urlexpandtweet'		) || 0 ,
		urlexpandtwtheme	=> $cgi->param('urlexpandtwtheme'	) || 0 ,
		longurlcutter		=> $cgi->param('longurlcutter'		) || 40 , 	# 0は許容できない値
		allowlinebreak		=> $cgi->param('allowlinebreak'		) || 0 ,
		keepserialspaces	=> $cgi->param('keepserialspaces'	) || 0 ,
		befhashts			=> $cgi->param('befhashts'			) || 0 ,	# ▼設定を変更する前の値
		hashtagsort			=> $cgi->param('hashtagsort'		) || 0 ,
		hashtaglinkize		=> $cgi->param('hashtaglinkize'		) || 0 ,
		hashtagcut			=> $cgi->param('hashtagcut'			) || 25 , 	# 0は許容できない値
		hashtagnokakko		=> $cgi->param('hashtagnokakko'		) || 0 ,
		catseparator		=> $cgi->param('catseparator'		) || '' ,
		nocatshow			=> $cgi->param('nocatshow'			) || 0 ,
		nocatlabel			=> $cgi->param('nocatlabel'			) || '' ,
		searchlabel			=> $cgi->param('searchlabel'		) || '検索' ,
		searchholder		=> $cgi->param('searchholder'		) || '' ,
		searchoption		=> $cgi->param('searchoption'		) || 0 ,
		cslabeluser			=> $cgi->param('cslabeluser'		) || '' ,
		cslabeldate			=> $cgi->param('cslabeldate'		) || '' ,
		cslabeltag			=> $cgi->param('cslabeltag'			) || '' ,
		cslabelcat			=> $cgi->param('cslabelcat'			) || '' ,
		cslabelorder		=> $cgi->param('cslabelorder'		) || '' ,
		catidinsearch		=> $cgi->param('catidinsearch'		) || 0 ,
		searchinputkey		=> $cgi->param('searchinputkey'		) || '' ,
		caladdweekrow		=> $cgi->param('caladdweekrow'		) || 0 ,
		calsun				=> $cgi->param('calsun'				) || '日' ,
		calmon				=> $cgi->param('calmon'				) || '月' ,
		caltue				=> $cgi->param('caltue'				) || '火' ,
		calwed				=> $cgi->param('calwed'				) || '水' ,
		calthu				=> $cgi->param('calthu'				) || '木' ,
		calfri				=> $cgi->param('calfri'				) || '金' ,
		calsat				=> $cgi->param('calsat'				) || '土' ,
		usericonsize		=> $cgi->param('usericonsize'		) || 0 ,
		usericonsizew		=> $cgi->param('usericonsizew'		) || 32 ,	# 0は許容できない値
		usericonsizeh		=> $cgi->param('usericonsizeh'		) || 32 ,	# 0は許容できない値
		usericonsource		=> $cgi->param('usericonsource'		) || 0 ,
		befdatelistSY		=> $cgi->param('befdatelistSY'		) || 0 ,	# ▼設定を変更する前の値
		befdatelistSZ		=> $cgi->param('befdatelistSZ'		) || 0 ,	# ▼設定を変更する前の値
		datelistShowYear	=> $cgi->param('datelistShowYear'	) || 0 ,
		datelistShowZero	=> $cgi->param('datelistShowZero'	) || 0 ,
		newsignhours		=> $cgi->param('newsignhours'		) || 1 ,
		newsignhtml			=> $cgi->param('newsignhtml'		) || '' ,

		alwaysshowquickpost	=> $cgi->param('alwaysshowquickpost') || 0 ,
		postphloginname		=> $cgi->param('postphloginname'	) || 0 ,
		postplaceholder		=> $cgi->param('postplaceholder'	) || 'さん、いまなにしてる？' ,
		postareaexpander	=> $cgi->param('postareaexpander'	) || 0 ,
		postcharcounter		=> $cgi->param('postcharcounter'	) || 0 ,
		postchangeidlink	=> $cgi->param('postchangeidlink'	) || 0 ,
		postchangeidlabel	=> $cgi->param('postchangeidlabel'	) || '他のIDに切り替える' ,
		postbuttonlabel		=> $cgi->param('postbuttonlabel'	) || '投稿する' ,
		postbuttonshortcut	=> $cgi->param('postbuttonshortcut'	) || 0 ,
		textareasizenormal	=> $cgi->param('textareasizenormal'	) || 4 ,	# 0は許容しない方が良い値
		textareasizequick	=> $cgi->param('textareasizequick'	) || 4 ,	# 0は許容しない方が良い値
		postareakey			=> $cgi->param('postareakey'		) || '' ,
		postautofocus		=> $cgi->param('postautofocus'		) || 0 ,

		showDecoBtnStyle	=> $cgi->param('showDecoBtnStyle') || 0 ,
		showDecoBtnBonA	=> $cgi->param('showDecoBtnBonA') || 0 ,	showDecoBtnBonQ	=> $cgi->param('showDecoBtnBonQ') || 0 ,	decoBtnLabelB	=> $cgi->param('decoBtnLabelB') || 'Ｂ' ,
		showDecoBtnConA	=> $cgi->param('showDecoBtnConA') || 0 ,	showDecoBtnConQ	=> $cgi->param('showDecoBtnConQ') || 0 ,	decoBtnLabelC	=> $cgi->param('decoBtnLabelC') || '色' ,
		showDecoBtnDonA	=> $cgi->param('showDecoBtnDonA') || 0 ,	showDecoBtnDonQ	=> $cgi->param('showDecoBtnDonQ') || 0 ,	decoBtnLabelD	=> $cgi->param('decoBtnLabelD') || '消' ,
		showDecoBtnEonA	=> $cgi->param('showDecoBtnEonA') || 0 ,	showDecoBtnEonQ	=> $cgi->param('showDecoBtnEonQ') || 0 ,	decoBtnLabelE	=> $cgi->param('decoBtnLabelE') || '強' ,
		showDecoBtnFonA	=> $cgi->param('showDecoBtnFonA') || 0 ,	showDecoBtnFonQ	=> $cgi->param('showDecoBtnFonQ') || 0 ,	decoBtnLabelF	=> $cgi->param('decoBtnLabelF') || '○' ,
		showDecoBtnHonA	=> $cgi->param('showDecoBtnHonA') || 0 ,	showDecoBtnHonQ	=> $cgi->param('showDecoBtnHonQ') || 0 ,	decoBtnLabelH	=> $cgi->param('decoBtnLabelH') || '隠す' ,
		showDecoBtnIonA	=> $cgi->param('showDecoBtnIonA') || 0 ,	showDecoBtnIonQ	=> $cgi->param('showDecoBtnIonQ') || 0 ,	decoBtnLabelI	=> $cgi->param('decoBtnLabelI') || 'Ｉ' ,
		showDecoBtnMonA	=> $cgi->param('showDecoBtnMonA') || 0 ,	showDecoBtnMonQ	=> $cgi->param('showDecoBtnMonQ') || 0 ,	decoBtnLabelM	=> $cgi->param('decoBtnLabelM') || '背' ,
		showDecoBtnQonA	=> $cgi->param('showDecoBtnQonA') || 0 ,	showDecoBtnQonQ	=> $cgi->param('showDecoBtnQonQ') || 0 ,	decoBtnLabelQ	=> $cgi->param('decoBtnLabelQ') || '”' ,
		showDecoBtnRonA	=> $cgi->param('showDecoBtnRonA') || 0 ,	showDecoBtnRonQ	=> $cgi->param('showDecoBtnRonQ') || 0 ,	decoBtnLabelR	=> $cgi->param('decoBtnLabelR') || 'ル' ,
		showDecoBtnSonA	=> $cgi->param('showDecoBtnSonA') || 0 ,	showDecoBtnSonQ	=> $cgi->param('showDecoBtnSonQ') || 0 ,	decoBtnLabelS	=> $cgi->param('decoBtnLabelS') || '小' ,
		showDecoBtnTonA	=> $cgi->param('showDecoBtnTonA') || 0 ,	showDecoBtnTonQ	=> $cgi->param('showDecoBtnTonQ') || 0 ,	decoBtnLabelT	=> $cgi->param('decoBtnLabelT') || '極' ,
		showDecoBtnUonA	=> $cgi->param('showDecoBtnUonA') || 0 ,	showDecoBtnUonQ	=> $cgi->param('showDecoBtnUonQ') || 0 ,	decoBtnLabelU	=> $cgi->param('decoBtnLabelU') || 'Ｕ' ,

		showLinkBtnStyle	=> $cgi->param('showLinkBtnStyle') || 0 ,
		showLinkBtnUrl => $cgi->param('showLinkBtnUrl') || 0 ,		linkBtnUrlLabel => $cgi->param('linkBtnUrlLabel') || '任意URLリンク' ,
		showLinkBtnNum => $cgi->param('showLinkBtnNum') || 0 ,		linkBtnNumLabel => $cgi->param('linkBtnNumLabel') || '指定No.リンク' ,
		showLinkBtnImg => $cgi->param('showLinkBtnImg') || 0 ,		linkBtnImgLabel => $cgi->param('linkBtnImgLabel') || '画像埋込リンク',
		showLinkBtnTwe => $cgi->param('showLinkBtnTwe') || 0 ,		linkBtnTweLabel => $cgi->param('linkBtnTweLabel') || 'ツイート埋込'  ,
		showLinkBtnYtb => $cgi->param('showLinkBtnYtb') || 0 ,		linkBtnYtbLabel => $cgi->param('linkBtnYtbLabel') || 'YouTube埋込'   ,
		showLinkBtnSpt => $cgi->param('showLinkBtnSpt') || 0 ,		linkBtnSptLabel => $cgi->param('linkBtnSptLabel') || 'Spotify埋込'   ,

		showImageBtnNewUp => $cgi->param('showImageBtnNewUp') || 0 ,
		showImageBtnExist => $cgi->param('showImageBtnExist') || 0 ,	imageBtnExistLabel => $cgi->param('imageBtnExistLabel') || '任意画像の挿入' ,

		decobuttonlabel		=> $cgi->param('decobuttonlabel'	) || '装飾' ,
		datebuttonlabel		=> $cgi->param('datebuttonlabel'	) || '日時' ,
		imagebuttonlabel	=> $cgi->param('imagebuttonlabel'	) || '画像' ,
		linkbuttonlabel		=> $cgi->param('linkbuttonlabel'	) || 'リンク' ,
		hashbuttonlabel		=> $cgi->param('hashbuttonlabel'	) || '＃' ,
		categorybuttonlabel	=> $cgi->param('categorybuttonlabel') || '区分' ,
		funcbuttonlabel		=> $cgi->param('funcbuttonlabel'	) || '機能' ,

		ogpoutput			=> $cgi->param('ogpoutput')			|| 0 ,
		ogdescription		=> $cgi->param('ogdescription')		|| 0 ,
		oglocale			=> $cgi->param('oglocale')			|| '' ,
		ogsitename			=> $cgi->param('ogsitename')		|| '' ,
		ogtype				=> $cgi->param('ogtype')			|| 0 ,
		ogimagecommonurl	=> $cgi->param('ogimagecommonurl')	|| '' ,
		ogimageuse1st		=> $cgi->param('ogimageuse1st')		|| 0 ,
		twittercard			=> $cgi->param('twittercard')		|| 0 ,
		twittersite			=> $cgi->param('twittersite')		|| '' ,
		twittercreator		=> $cgi->param('twittercreator')	|| '' ,
		insertalttext		=> $cgi->param('insertalttext')		|| 0 ,

		showFreeDateBtn		=> $cgi->param('showFreeDateBtn')		|| 0 ,
		allowillegaldate	=> $cgi->param('allowillegaldate')		|| 0 ,
		imagedefaultplace	=> $cgi->param('imagedefaultplace')		|| 0 ,
		showHashtagBtnStyle	=> $cgi->param('showHashtagBtnStyle')	|| 0 ,
		hashtagBtnListupMax	=> $cgi->param('hashtagBtnListupMax')	|| 0 ,
		showHashBtnHash		=> $cgi->param('showHashBtnHash')		|| 0 ,
		showCategoryBtnStyle=> $cgi->param('showCategoryBtnStyle')	|| 0 ,
		showFuncBtnStyle	=> $cgi->param('showFuncBtnStyle')		|| 0 ,
		allowblankdeco		=> $cgi->param('allowblankdeco')		|| 0 ,

		showFuncBtnSpeech	=> $cgi->param('showFuncBtnSpeech')		|| 0 ,
		showFuncBtnStaytop	=> $cgi->param('showFuncBtnStaytop')	|| 0 ,
		showFuncBtnDraft	=> $cgi->param('showFuncBtnDraft')		|| 0 ,
		showFuncBtnRear		=> $cgi->param('showFuncBtnRear')		|| 0 ,

		freesptitle			=> $cgi->param('freesptitle'		) || '' ,
		freetitlemain		=> $cgi->param('freetitlemain'		) || '' ,
		freetitlesub		=> $cgi->param('freetitlesub'		) || '' ,
		freedescription		=> $cgi->param('freedescription'	) || '' ,
		freehomename		=> $cgi->param('freehomename'		) || '' ,
		freehomeurl			=> $cgi->param('freehomeurl'		) || '' ,
		freehomeatt			=> $cgi->param('freehomeatt'		) || 0 ,
		freespace			=> $cgi->param('freespace'			) || '' ,
		allowbrinfreespace	=> $cgi->param('allowbrinfreespace'	) || 0 ,

		afterpost			=> $cgi->param('afterpost'			) || 0 ,
		shiftservtime		=> $cgi->param('shiftservtime'		) || 0 ,
		howtogetfullpath	=> $cgi->param('howtogetfullpath'	) || 0 ,
		fixedfullpath		=> $cgi->param('fixedfullpath'		) || '' ,
		howtogetdocroot		=> $cgi->param('howtogetdocroot'	) || 0 ,
		fixeddocroot		=> $cgi->param('fixeddocroot'		) || '' ,
		outputlinkfullpath	=> $cgi->param('outputlinkfullpath'	) || 0 ,
		outputlinkkeepskin	=> $cgi->param('outputlinkkeepskin'	) || 0 ,
		exportpermission	=> $cgi->param('exportpermission'	) || 0 ,
		autobackup			=> $cgi->param('autobackup'			) || 0 ,
		backupfilehold		=> $cgi->param('backupfilehold'		) || 2 , 	# 0は許容できない値
		conpanecolortheme	=> $cgi->param('conpanecolortheme'	) || 0 ,
		conpanegallerylink	=> $cgi->param('conpanegallerylink'	) || 0 ,
		syspagelinkomit		=> $cgi->param('syspagelinkomit'	) || 0 ,
		sysdelbtnpos		=> $cgi->param('sysdelbtnpos'		) || 0 ,
		postperpageforsyslist	=> $cgi->param('postperpageforsyslist') || 100 , 	# 0は許容できない値
		conpanedistinction	=> $cgi->param('conpanedistinction') || '' ,
		conpaneretlinklabel	=> $cgi->param('conpaneretlinklabel') || 'てがろぐHOMEへ戻る' ,
		conpanegallerylabel	=> $cgi->param('conpanegallerylabel') || 'ギャラリーへ戻る' ,
		funcrestreedit		=> $cgi->param('funcrestreedit'		) || 0 ,
		datelimitreedit		=> $cgi->param('datelimitreedit'	) || 0 ,
		datelimitreeditdays	=> $cgi->param('datelimitreeditdays') || 31 , 	# 0は許容できない値
		loadeditcssjs		=> $cgi->param('loadeditcssjs'		) || 0 ,
		envlistonerror		=> $cgi->param('envlistonerror'		) || 0 ,
		sessiontimenum		=> $cgi->param('sessiontimenum'		) || 31, 	# 0は許容できない値
		coexistflag			=> $cgi->param('coexistflag'		) || 0 ,
		coexistsuffix		=> $cgi->param('coexistsuffix'		) || '' ,

		signhider			=> $cgi->param('signhider'			) || 0 ,
		aboutcgibox			=> $cgi->param('aboutcgibox'		) || 0 ,
		licencecode			=> $cgi->param('licencecode'		) || ''
	);

	# --------
	# 連携判断
	# --------
	if( $trySetdat{'fixedfullpath'} eq '' ) {
		# フルパス入力欄が空なら、指定を無効化する
		$trySetdat{'howtogetfullpath'} = 0;
	}
	elsif( $trySetdat{'howtogetfullpath'} == 0 ) {
		# フルパスが自動取得なら、現在パスは保存しない（※設置場所を移転した場合に再度自動取得できるように）
		$trySetdat{'fixedfullpath'} = '';
	}

	if( $trySetdat{'fixeddocroot'} eq '' ) {
		# ドキュメントルート入力欄が空なら、指定を無効化する
		$trySetdat{'howtogetdocroot'} = 0;
	}
	elsif( $trySetdat{'howtogetdocroot'} == 0 ) {
		# ドキュメントルートが環境変数なら、現在パスは保存しない（※設置場所を移転した場合に再度自動取得できるように）
		$trySetdat{'fixeddocroot'} = '';
	}

	# ------------------------------
	# 許可ファイル拡張子リストの処理
	$trySetdat{'imageallowext'} = lc $trySetdat{'imageallowext'};	# 全部小文字に変換

	# 前処理(改行を縦棒で連結)
	$trySetdat{'imageallowext'} =~ s/\r|\n/|/g;	# 改行を縦棒記号に変換 (CR+LFの全パターンに対応させるため、個別に変換)
	$trySetdat{'imageallowext'} =~ s/\|\|/|/g;	# 2連続の縦棒記号を1つにまとめる

	# 使用禁止文字があれば消す
	$trySetdat{'imageallowext'} =~ s/[^A-Za-z0-9\|]//g;		# 英数字と縦棒以外は消す

	# 拡張子単位で区切って配列に入れる
	my @imgexts = split(/\|/,$trySetdat{'imageallowext'});

	# 警告対象拡張子があればセキュリティエラーを加えて、設定は排除する (※実際に許可される拡張子は管理画面上のホワイトリストに依るので、何でもアップロード可能な危険仕様にはなっていない。ここでは管理者が誤って設定したり、管理IDが乗っ取られてしまった場合にさすがに悪影響がありそうな拡張子をフェイルセーフ的にブラックリストとして提供する。)
	my $securitymsg = '';
	foreach my $oneext ( @imgexts ) {
		if( $oneext =~ m/(^.*htm.*$|^js$|^php$|^cgi$|^pl$|^pm$|^exe$|^py$|^rb$|^com$|^bat$|^sh$|^wsh$|^wsf$)/ ) {
			$securitymsg .= '●セキュリティ上の理由から、拡張子「' . $1 . '」はアップロード許可対象には設定できません。設定項目は自動削除されました。<br>';
			$oneext = '';	# その項目は削除する
		}
	}

	# 配列要素の重複を削除する
	my %hash	= map { $_, 1 } @imgexts;
	@imgexts	= sort keys %hash;

	# 全項目を縦棒で連結して文字列にする
	$trySetdat{'imageallowext'} = join('|',@imgexts );
	$trySetdat{'imageallowext'} =~ s/^\||\|$//g;	# 先頭や末尾の縦棒を削除

	# もし設定が空になったらデフォルトリストを適用
	if( $trySetdat{'imageallowext'} eq '' ) {
		$trySetdat{'imageallowext'} = 'png|jpg|gif|jpeg|svg|webp';
	}

	# ----------------------------------------------------
	# 数値チェック（全角→半角、非数字除外、マイナス拒否）
	# ----------------------------------------------------
	# ▼全角数字を半角に強制変換のみ
	my @zenkakunums = ('fixedpostids');
	# ▼全角数字を半角に強制変換＋非数字を除外する対象
	my @zenkakuchecks = ();	# ※今のところマイナスを許容する項目がないので、ここは空。
	# ▼さらに、マイナス数値も拒否する対象（※上記と重複指定する必要はない）
	my @nominus = ('entryperpage','rssentries','galleryentries','imagemaxwidth','imagemaxheight','longurlcutter','hashtagcut','usericonsizew','usericonsizeh','newsignhours','hashtagBtnListupMax','textareasizenormal','textareasizequick','imageperpage','latestlistup','latesttitlecut','imagemaxbytes','imagefilelimit','imagestoragelimit','datelimitreeditdays','backupfilehold','sessiontimenum','postperpageforsyslist');	# 対象群

	push @zenkakuchecks, @nominus;	# マイナスを拒否する対象は、同時に全角数値(非数値)もチェックする。

	# ▽全角数字対策（非数字はそのまま）
	foreach my $onecheck (@zenkakunums) {
		$trySetdat{$onecheck} = &fcts::nozenkakunum( $trySetdat{$onecheck} );	# 全角数字を半角に
	}
	# ▽全角数字対策（非数字対策も兼ねる）
	foreach my $onecheck (@zenkakuchecks) {
		$trySetdat{$onecheck} = &fcts::nozenkaku( $trySetdat{$onecheck} );	# 全角数字を半角に（＋数字以外は削除）
	}
	# ▽マイナス数値対策
	foreach my $onecheck (@nominus) {
		if( $trySetdat{$onecheck} < 0 ) {
			$trySetdat{$onecheck} = 1;	# マイナスだったら1に強制修正
		}
	}

	# 不正な値チェック
	if( $trySetdat{'entryperpage'} < 1 || !( $trySetdat{'entryperpage'} =~m/^\d+$/) ) { &errormsg("「1ページあたりの表示投稿数」には、1以上の整数を指定する必要があります。"); }
	if( $trySetdat{'sessiontimenum'} < 0.1 ) { $trySetdat{'sessiontimenum'} = 1; }		# セッション下限を下回っている場合は強制修正
	if( $trySetdat{'sessiontimenum'} > 366 ) { $trySetdat{'sessiontimenum'} = 366; }	# セッション上限を上回っている場合は強制修正
	if( $trySetdat{'shiftservtime'} < -23.5 || $trySetdat{'shiftservtime'} > 23.5 ) { $trySetdat{'shiftservtime'} = 0; }	# -23.5～+23.5の範囲外なら0に強制修正

	# 望ましくない値の強制修正
	if( $trySetdat{'backupfilehold'} < 2 ) { $trySetdat{'backupfilehold'} = 2; }
	if( $trySetdat{'backupfilehold'} > 366 ) { $trySetdat{'backupfilehold'} = 366; }
	if( $trySetdat{'imagemaxwidth'}  && $trySetdat{'imagemaxwidth'}  < 16 ) { $trySetdat{'imagemaxwidth'}  = ''; }	# 小さすぎる値は無視(空欄は許可)
	if( $trySetdat{'imagemaxheight'} && $trySetdat{'imagemaxheight'} < 16 ) { $trySetdat{'imagemaxheight'} = ''; }	# 小さすぎる値は無視(空欄は許可)
	if( $trySetdat{'usericonsizew'} > 500 ) { $trySetdat{'usericonsizew'} = 500; }	# 巨大すぎないように安全のため
	if( $trySetdat{'usericonsizeh'} > 500 ) { $trySetdat{'usericonsizeh'} = 500; }	# 巨大すぎないように安全のため
	if( $trySetdat{'textareasizenormal'} < 4 ) { $trySetdat{'textareasizenormal'} = 4; }
	if( $trySetdat{'textareasizenormal'} > 300 ) { $trySetdat{'textareasizenormal'} = 300; }	# 長すぎないように安全のため
	if( $trySetdat{'textareasizequick'} < 1.8 ) { $trySetdat{'textareasizequick'} = 2; }
	if( $trySetdat{'textareasizequick'} > 100 ) { $trySetdat{'textareasizequick'} = 100; }	# 長すぎないように安全のため
	if( index($trySetdat{'latestlistparts'},'H') == -1 ) { $trySetdat{'latestlistparts'} = 'H' . $trySetdat{'latestlistparts'}; }	# 英字「H」が含まれていなかったら先頭に追加
	if( $trySetdat{'postperpageforsyslist'} < 25 ) { $trySetdat{'postperpageforsyslist'} = 25; }	# 小さすぎないようにする

	# 単位変換
	$trySetdat{'imagemaxbytes'} = int($trySetdat{'imagemaxbytes'} * 1024);				# KB→Bytes (画像1枚あたりの最大サイズ)
	$trySetdat{'imagestoragelimit'} = int($trySetdat{'imagestoragelimit'} * 1048576);	# MB→Bytes (画像保存に使える最大容量)

	# --------------
	# 文字列チェック
	# --------------
	# ▼タグ括弧だけを強制削除する対象
	my @noltgt = ('imagelightboxatt','urlimagelightboxatt');

	# ▽タグ括弧の強制削除
	foreach my $onecheck (@noltgt) {
		$trySetdat{$onecheck} =~ s|[><]||g;		# 記号「>」と「<」だけを削除
	}

	# 英数字チェック
	$trySetdat{'coexistsuffix'} =~ s|[^a-zA-Z0-9]||g;		# 英数字以外を削除

	# サブディレクトリ名のチェック
	$trySetdat{'rssskindir'}     = &fcts::safetydirnamecutter( $trySetdat{'rssskindir'} );
	$trySetdat{'galleryskindir'} = &fcts::safetydirnamecutter( $trySetdat{'galleryskindir'} );

	# 各種再カウントが必要かどうかを確認して、必要なら実行。（※この処理は設定ファイルを書き換えるので、下記の設定情報の更新処理よりも前に実行する必要がある。）
	my $recountres = '';
	if( $flagDemo{'RefuseToChangeSettings'} != 1 ) {

		# ------------------------
		# ハッシュタグの再カウント
		# ------------------------
		if( $trySetdat{'befhashts'} != $trySetdat{'hashtagsort'} ) {
			# 今回のハッシュタグソート番号と、前回のハッシュタグソート番号が異なっていれば、再カウントする。
			# 今回の設定値を反映
			$setdat{'hashtagsort'} = $trySetdat{'hashtagsort'};
			# ハッシュタグの再カウントを直接実行
			&datahashcounter();
			$recountres .= '<p>ハッシュタグの掲載順序が変更されたため、再カウントしました。</p>';
		}

		# ----------------------
		# 日付リストの再カウント
		# ----------------------
		if( $trySetdat{'befdatelistSY'} =~ /checked/ ) { $trySetdat{'befdatelistSY'} = 1; }	# ※befdatelistSYには1の代わりにcheckedが入っているので修正しておく
		if( $trySetdat{'befdatelistSZ'} =~ /checked/ ) { $trySetdat{'befdatelistSZ'} = 1; }	# ※befdatelistSZも同様。

		if(( $trySetdat{'befdatelistSY'} != $trySetdat{'datelistShowYear'} ) || ( $trySetdat{'befdatelistSZ'} != $trySetdat{'datelistShowZero'} )) {
			# 2項目のうちどちらかが、今回の値と前回の値が異なっていれば、再カウントする。
			$recountres .= "\n<!-- $trySetdat{'befdatelistSY'} → $trySetdat{'datelistShowYear'} -->";
			$recountres .= "\n<!-- $trySetdat{'befdatelistSZ'} → $trySetdat{'datelistShowZero'} -->";
			# 今回の設定値を反映
			$setdat{'datelistShowYear'} = $trySetdat{'datelistShowYear'};
			$setdat{'datelistShowZero'} = $trySetdat{'datelistShowZero'};
			&datadatecounter();
			$recountres .= '<p>日付リストの設定が変更されたため、再カウントしました。</p>';
		}

	}

	# 新着リストの再生成（※この処理は設定ファイルを書き換えるので、下記の設定情報の更新処理よりも前に実行する必要がある。）
	&updatelatestlist( $trySetdat{'latestlistup'} , $trySetdat{'latestlistparts'} , $trySetdat{'latesttitlecut'} );

	# フリースペースの改行を変換（※データは1行にする必要がある）
	$trySetdat{'freespace'} =~ s/\r\n/<br>/g;

	if( $flagDebug{'ShowDebugStrings'} == 1 ) {
		# 連想配列%trySetdatの中身をすべて出力(デバッグ用)
		while( my ($key, $value) = each(%trySetdat) ) {
			print STDERR "[TRY]$key=$value\n";
		}
	}

	# 設定ファイルを更新
	my $msg;
	if( $flagDemo{'RefuseToChangeSettings'} != 1 ) {

		# 設定ファイルに書き込むための準備
		my @trywrites;
		# 連想配列%trySetdatの中身をすべて保存用形式に整形してから配列に入れる
		while( my ($key, $value) = each(%trySetdat) ) {
			push( @trywrites, "$key=$value" );
		}

		# 保存処理へ渡す
		&savesettings( @trywrites );

		# 必要なサブディレクトリがない場合の注意案内を用意
		my $nodirs = '';
		if( ($setdat{'autobackup'} == 1) && (!( -d $autobackupto )) ) {
			# 自動バックアップが有効に設定されているのに、自動バックアップ用ディレクトリがなければ
			$nodirs .= qq|<li>自動バックアップを<strong>する</strong>設定になっていますが、自動バックアップの保存先サブディレクトリが作成されていないため、現状のままでは<strong>自動バックアップは実行されません</strong>。(※現在の設定では、自動バックアップ先サブディレクトリ名は <b>$autobackupto</b> ですが、その名称のディレクトリが見つかりません。)</li>|;
		}
		if( ($setdat{'imageupallow'} == 1) && (!( -d $imagefolder )) ) {
			# 画像投稿が許可されているのに、画像UP用ディレクトリがなければ
			$nodirs .= qq|<li>画像投稿を<strong>許可する</strong>設定になっていますが、投稿画像の保存用サブディレクトリが作成されていないため、現状のままでは<strong>画像投稿時にエラーが表示されます</strong>。(※現在の設定では、画像保存用サブディレクトリ名は <b>$imagefolder</b> ですが、その名称のディレクトリが見つかりません。)</li>|;
		}
		if( ($setdat{'rssskin'} == 2) && (!( -d 'rss' )) ) {
			# 自作RSSスキンを使う設定になっているのに、rssサブディレクトリがなければ
			$nodirs .= qq|<li>RSSフィードの出力用として<strong>自作のRSSスキンを使う</strong>設定になっていますが、RSS用のスキンが見つからないため、現状のままでは<strong>デフォルトの内蔵RSSスキン(抜粋版)を使って出力されます</strong>。(※「rss」サブディレクトリに、RSSフィードを出力するためのスキンファイルを置いて下さい。)</li>|;
		}
		if( $nodirs ne '' ) {
			# 案内が存在するなら
			$nodirs = '<p class="alerts">ただし、下記の点にご注意下さい。</p><ul class="alertlist">' . $nodirs . '</ul>';
		}

		# 結果報告メッセージを用意
		$msg = qq|
			<h2>設定変更完了</h2>
			<p>設定を変更しました。</p>
			$nodirs
		|;
		if( $securitymsg ne '' ) {
			# セキュリティメッセージがあれば追加表示
			$msg .= qq|<p class="securityalerts">$securitymsg</p>|;
		}
		$msg .= $recountres;

	}
	else {
		# DEMO：設定変更を拒否
		&demomodemsg('設定の変更はできませんでした。');
	}

	my $css = q|<style type="text/css">.alerts { margin-top:1.8em; padding-top:1em; border-top: 1px dashed gray; color:#c00; } .alertlist strong { color: red; } .alertlist li { margin-bottom: 1em; } .securityalerts { color: red; }</style>|;

	&showadminpage('COMPLETE','',$msg,'CA',$css);
}

# -----------------
# ADMIN：ユーザ一覧（編集へのメニュー＆削除フォーム）
# -----------------
sub adminUserlist
{
	# ユーザ一覧
	my $msg = '<p>登録情報を変更したいユーザIDをクリックするか、「新規にユーザIDを作成」ボタンを押して下さい。</p>';

	# 既存ユーザ編集
	my $mquery = &makeQueryString('mode=admin','work=changepass');
	my @userlist = &fcts::getUserTable( $mquery );
	foreach my $oi (@userlist) {
		$msg .= $oi;
	}

	# ユーザ新規作成
	$msg .= qq|<p><a href="$mquery" class="btnlink">新規にユーザIDを作成</a></p>\n|;

	# ユーザ削除
	@userlist = &fcts::getUserList();
	my $dellist = '<select name="tryid">';
	foreach my $ul (@userlist) {
		my @ui = split(/<>/,$ul);
		$dellist .= qq|<option value="$ui[0]">$ui[1] ($ui[0])</option>|;
	}
	$dellist .= '</select>';

	if( $nopassuser < 1 ) {
		# パスワードなしユーザが許可されている場合
		$msg .= qq|<p class="noticebox">※安全のため、パスワードを未設定のままで使用するIDの権限は、Lv.1(ゲスト)に留めておくことをお勧め致します。<br>※管理者権限(Lv.9)を持つIDには、必ずパスワードを設定して下さい。<br>※管理者権限のあるIDでログインしていれば、他のユーザのパスワードを強制リセット(再設定)できます。</p>|;
	}
	else {
		# パスワードなしユーザを拒否する場合
		$msg .= qq|<p class="noticebox">※現在は、<strong>パスワードが未設定のIDではログインできない</strong>設定になっています。必ずすべてのユーザにパスワードを設定して下さい。(この設定を変更するにはCGIソース内の設定フラグを変更する必要があります。)</p>|;
	}

	my $cgipath = &getCgiPath();
	$msg .= qq|<form action="$cgipath" method="post" class="delform">ユーザ削除：$dellist <input type="hidden" name="mode" value="admin"><input type="hidden" value="trychangepass" name="work"><input type="hidden" name="idwork" value="deleteid"><input type="submit" value="IDを削除" onclick="return confirm('このユーザIDを本当に削除しますか？');"></form>|;
	$msg .= q|<p class="noticebox">※ユーザを削除しても、当該ユーザが投稿したデータは消えません。ただし、当該ユーザの名前(表示名)は表示できなくなります。<br>※削除されたユーザの投稿には、ユーザIDは投稿時のIDがそのまま表示され、ユーザの名前(表示名)は「| . &fcts::forsafety($setdat{'unknownusername'}) . q|」になります。(設定で変更できます。)<br>※削除したIDを復活させたい場合は、同じID名でユーザを新規作成して下さい。<br>※初期ID「admin」も削除可能です。初期ID「admin」は、ユーザ設定の手間を省くために存在しているに過ぎないので、削除しても何も問題ありません。</p>|;

	my $css = '<style type="text/css">
		.delform { margin-top:2em; padding-top:1em; border-top: 2px dashed gray; }
	</style>';
	&showadminpage('USER ID LIST','',$msg,'CA',$css);
}

# -----------------------------------------
# ADMIN：ユーザIDの作成＋パスワード変更画面
# -----------------------------------------
sub adminChangepass
{
	# ………………
	# ログイン確認
	# ………………
	my $permittedid = &fcts::checkpermission();
	if( !$permittedid ) {
		# 権限を確認できない場合：エラー
		&loginrequired();
	}
	my $plv = &fcts::getUserDetail($permittedid, 1);	# 権限の値を得る(1:ゲスト～9:SU)

	# ………………………………………
	# ユーザ情報変更対象IDと情報取得
	# ………………………………………
	my $userid  = $cgi->param('userid')  || '';		# 新規作成の場合は空文字列
	my $ulv = '';
	my $uin = '';
	my $uip = '';
	my $uii = '';
	if( $userid ne '' ) {
		# ユーザIDの指定があれば情報を得る
		$ulv = &fcts::forsafety( &fcts::getUserDetail($userid, 1));	# 編集対象ユーザの権限
		$uin = &fcts::forsafety( &fcts::getUserDetail($userid, 2));	# 編集対象ユーザの表示名
		$uip = &fcts::forsafety( &fcts::getUserDetail($userid, 3));	# 編集対象ユーザのプロフィール
		$uii = &fcts::forsafety( &fcts::getUserDetail($userid, 4));	# 編集対象ユーザのアイコン
		if( $ulv eq '' ) {
			# 権限が空文字列の場合はIDが存在しない
			&errormsg('ユーザ情報編集：不正なID名が指定されました。');
		}
	}

	# …………………
	# 表示権限の確認
	# …………………
	&accesslevelcheck(5,$plv);	# 権限Lv.5未満ならアクセス権はない
	if( $plv < 9 ) {
		# 権限Lv.9未満は、自分のIDだけ編集可能
		if( $permittedid ne $userid ) {
			&accesslevelcheck(9,$plv);
		}
	}

	# ……………
	# 画面の作成
	# ……………
	my $work = '';
	my $targetid = '';
	my $idform = '';
	my $oldpassform = '';
	my $pwcaption = '';
	my $newpassguide = '';
	if( $userid eq '' ) {
		# 新規作成
		$work = 'makenewid';
		$targetid = '<p>ユーザIDを新規作成します。</p>';
		$idform = '<input type="text" value="" name="tryid">';
		$oldpassform = '<input type="hidden" value="" name="nowpass">';
		$pwcaption = '作成';
		$newpassguide = '※入力を省略すれば、パスワードなしのIDを作成できます。';
	}
	elsif( $permittedid eq $userid ) {
		# 自分のIDを変更する場合なら
		$work = 'changeownid';
		$targetid = '<p>自分（ユーザID「' . $userid . '」）の登録情報を変更します。</p>';
		$idform = qq|<input type="text" value="$userid" disabled><input type="hidden" value="$userid" name="tryid">|;
		$oldpassform = '<li style="list-style-type:none;">※<strong>変更する場合のみ</strong>下記に入力：</li><li>旧パスワード: <input type="password" value="" name="nowpass"></li>';
		$newpassguide = '※新規登録の場合は「旧パスワード」欄は空で構いません。';
		$pwcaption = '変更';
	}
	else {
		# 強制変更なら
		$work = 'changeuserid';
		$targetid = '<p>ユーザID「' . $userid . '」の登録情報を<strong class="important">管理者権限で強制変更</strong>します。</p>';
		$idform = qq|<input type="text" value="$userid" disabled><input type="hidden" value="$userid" name="tryid">|;
		$oldpassform = '<li style="list-style-type:none;"><strong class="important">※強制変更するなら下記に入力：</strong><input type="hidden" value="" name="nowpass"></li>';
		$pwcaption = 'リセット';
	}

	# ユーザレベル一覧を作成
	my @ulvs;	# Select
	my @ulvg;	# ガイド表示
	for my $i ( 0 .. $#userlevels ) {
		if( $userlevels[$i][0] ) {
			my $selected = '';
			if( $i eq $ulv ) {
				# 対象IDのユーザ権限Lvと一致していたら選択状態にする
				$selected = 'selected';
			}
			if(( $plv >= 9 ) || ( $i eq $ulv ))  {
				# 権限Lv.9なら全部を表示、Lv.9でないなら現Lvと一致しているLvのみを表示
				push(@ulvs, qq|<option value="$i" $selected>$userlevels[$i][0] (Lv.$i)</option>| );
			}
			push(@ulvg, qq|<li><strong>$userlevels[$i][0]</strong>(Lv.$i)： $userlevels[$i][1]</li>| );
		}
	}


	my $cgipath = &getCgiPath();
	my $msg = qq|
		$targetid
		<form action="$cgipath" method="post"><input type="hidden" name="idwork" value="$work">
			<fieldset>
				<legend>ユーザ情報</legend>
				<ul class="inputs">
					<li><label><span class="itemhead">ユーザID: </span> $idform</label> <span class="notice">※半角英数のみ。一度決めたら変更はできません。</span></li>
					<li><label><span class="itemhead">表示名:   </span> <input type="text" value="$uin" name="tryname"></label> <span class="notice">※いつでも変更できます。</span></li>
					<li><label><span class="itemhead">アイコン：</span> <input type="text" value="$uii" name="tryicon" placeholder="https://"></label> <span class="notice">※アイコン画像のURLなど。(省略可／Base64可)</span></li>
					<li><label><span class="itemhead">権限：    </span> <select name="trypermission">@ulvs</select></label> <span class="notice">※権限の範囲はこのページの下端をご覧下さい。</span></li>
					<li><label><span class="itemhead">紹介文：  </span> <input type="text" value="$uip" name="tryintro"></label> <span class="notice">※ID識別のメモなどにご使用頂けます。(省略可)</span></li>
				</ul>
			</fieldset>
			<fieldset>
				<legend>パスワード$pwcaption</legend>
				<ul class="inputs">
					$oldpassform
					<li>新パスワード: <input type="password" value="" name="newpass1"></li>
					<li>新パスワード(再入力): <input type="password" value="" name="newpass2"></li>
				</ul>
				<p class="note">
					<input type="hidden" value="admin" name="mode">
					<input type="hidden" value="trychangepass" name="work">
					<span class="notice">※1文字以上の自由な文字と記号が使えます。<br>※パスワードは暗号化(正確にはハッシュ化)して保存されます。<br>※一度パスワードを設定すると、「なし」には戻せません。<br><strong>$newpassguide</strong></span>
				</p>
			</fieldset>
			<p>
				<input type="submit" value="ユーザIDを設定" class="sendui">
			</p>
		</form>
		<p>※表示名の重複チェックはしませんので、複数のIDで同じ表示名を使うこともできます。<br>※表示名やアイコンが画面に表示されるかどうかは、表示に使うスキン次第です。</p>
		<p class="permissions">【権限の種別】</p>
		<ul class="permissions">@ulvg</ul>
	|;
	my $css = '<style type="text/css">
		.itemhead { min-width: 5em; display: inline-block; }
		.inputs { margin: 0.5em 0; padding: 0 0 0 20px; }
		.permissions { margin: 0; }
		p.permissions { color: green; font-weight:bold; border-top: 2px solid #bdb; padding-top: 5px; }
		.note { margin-bottom: 0; }
		input:placeholder-shown { color: #555; }
		input:focus:placeholder-shown { color: #ccc; }
		.sendui { font-size:1.2em; }
	</style>';
	&showadminpage('MANAGE USER ID','',$msg,'CUA',$css);
}

# ---------------------------------------
# ADMIN：ユーザ情報＋パスワード変更の試行
# ---------------------------------------
sub adminTrychangepass
{
	my $result = '';

	# 不正送信の確認
	&fcts::postsecuritycheck('work=trychangepass');

	# ログインの確認
	my $permittedid = &fcts::checkpermission();
	if( !$permittedid ) {
		# ログインしていなければエラー
		&loginrequired();
	}
	my $plv = &fcts::getUserDetail($permittedid, 1);	# 権限の値を得る(1:ゲスト～9:SU)

	# ……………………………
	# ▼送信された情報の取得
	# ……………………………
	# ユーザ情報の作成処理(TRY)
	my $tryid			= &fcts::deleteseparators( $cgi->param('tryid') ) || "";
	my $tryname			= &fcts::deleteseparators( &fcts::safetycutter( scalar $cgi->param('tryname') )) || "";
	my $tryicon			= &fcts::deleteseparators( $cgi->param('tryicon') ) || "";
	my $trypermission	= &fcts::deleteseparators( $cgi->param('trypermission') ) || "";
	my $tryintro		= &fcts::deleteseparators( $cgi->param('tryintro') ) || "";

	# パスワードの変更処理(TRY)
	my $nowpass  = $cgi->param('nowpass')  || "";
	my $newpass1 = $cgi->param('newpass1') || "";
	my $newpass2 = $cgi->param('newpass2') || "";

	# ……………………………
	# ▼送信された情報の確認
	# ……………………………
	# IDが未指定なら中止
	if( $tryid eq '' ) {
		my $msg = '<h2>ユーザ情報更新失敗</h2><p>ユーザIDを入力して下さい。</p>';
		&showadminpage('No ID','',$msg,'BA');
		exit;
	}

	# IDに英数字以外があったら中止
	if( $tryid =~ /\W/ ) {
		my $msg = '<h2>ユーザ情報作成失敗</h2><p>ユーザIDには半角英数字だけが使えます。</p>';
		&showadminpage('Illegal ID','',$msg,'B');
		exit;
	}

	# 新パスワードの2入力が不一致なら中止（※パスワードを変更しない場合でも、空文字同士を比較するだけなので問題ない。）
	if( $newpass1 ne $newpass2 ) {
		my $msg = '<h2>パスワード変更失敗</h2><p>入力された「新パスワード」と「新パスワード(再入力)」の内容が異なります。この2つの欄には、同じパスワードを入力して下さい。</p>';
		&showadminpage('Authentication Failed','',$msg,'BA');
		exit;
	}

	# ………………………………………………
	# ▼作業種別の把握（＋権限レベル確認）（新規作成はLv.9のみ／Lv.5～8は自分のIDだけ／Lv.3以下は拒否）
	# ………………………………………………
	my $work = $cgi->param('idwork') || &errormsg('adminTrychangepass:作業種別がありません。');
	my $wlabel = '';
	if( $work eq 'makenewid' ) {
		# 新規作成
		$wlabel = '新規作成';
		# 権限レベル確認
		&accesslevelcheck(9,$plv);

		# 既存のID名との重複を確認
		my @existingIds = &fcts::getUserList();	# IDリストを得る
		foreach my $ou (@existingIds) {
			my @uin = split(/<>/, &fcts::forsafety($ou));
			if( $tryid =~ /^$uin[0]$/i ) {
				# 一致していたら新規追加を拒否
				my $msg = '<h2>重複ID</h2><p>指定されたIDは既に存在します。新規作成はできませんでした。</p>';
				&showadminpage('Existing ID','',$msg,'UA');
				exit;
			}
		}
	}
	elsif( $work eq 'changeownid' ) {
		# 自分のIDを変更する場合なら
		$wlabel = '変更';
		# 権限レベル確認
		&accesslevelcheck(5,$plv);

		# ログインIDと対象ユーザIDの一致を確認
		if( $permittedid ne $tryid ) { &errormsg('ログインIDと操作対象ユーザIDが一致していません。'); }

		# 自分で自分の権限Lvを変更することはできない
		if( $trypermission != $plv ) {
			$trypermission = $plv;
			$result .= '<p>安全のため、<strong class="important">自分で自分の権限を変更することはできません</strong>。権限は Lv.' . $plv .' のまま更新していません。<br>※管理者権限を持つIDが1つも存在しなくなるのを防ぐためです。権限を変更するには、管理者権限を持つ他のIDでログインして下さい。</p>';
			# (※処理は中止せず、権限Lv以外の項目は更新する。)
		}

		# 新パスワードが入力されている場合のみ
		if( $newpass1 ne '' ) {
			# 旧パスワードの一致確認
			if( &fcts::checkpass($nowpass,$tryid) < 0 ) {
				# 不一致
				my $msg = '<h2>パスワード変更失敗</h2><p>旧パスワード（現在のパスワード）が違います。<br>パスワードは変更できませんでした。</p>';
				&showadminpage('Authentication','',$msg,'BA');
				exit;
			}
		}
	}
	elsif( $work eq 'changeuserid' ) {
		# 強制変更なら
		$wlabel = '管理者権限で変更';
		# 権限レベル確認
		&accesslevelcheck(9,$plv);
	}
	elsif( $work eq 'deleteid' ) {
		# ID削除なら
		$wlabel = '削除';
		$newpass1 = '削除';
		# 権限レベル確認
		&accesslevelcheck(9,$plv);
		# 自分で自分は削除できない
		if( $permittedid eq $tryid ) {
			my $emsg = '<p>安全のため、<strong class="important">自分で自分を削除することはできません</strong>。<br>※管理者権限を持つIDが1つも存在しなくなるのを防ぐためです。IDを削除するには、管理者権限を持つ他のIDでログインして下さい。</p>';
			&showadminpage('Cannot Delete','',$emsg,'CUA');
			exit;
		}
	}
	else {
		&errormsg('adminTrychangepass:作業種別が不正です。');
	}

	# ………………………………………………
	# ▼情報更新（パスワードとユーザ情報）
	# ………………………………………………
	$result .= '<ul>';

	# ‥‥‥‥‥‥‥‥‥‥
	# ユーザ情報の変更処理
	# ‥‥‥‥‥‥‥‥‥‥
	if( $flagDemo{'RefuseToChangePassword'} != 1 ) {
		# ユーザ情報の更新・追加・削除用関数を作成しておいて、それを呼ぶ。
		my @trywrites;
		my $newidline = &fcts::makeLineForUserDat( $tryid, $tryname, $tryicon, $trypermission, $tryintro );		# 権限に0を渡すと削除になるので注意
		push(@trywrites,"userids=$newidline");

		# 保存処理へ渡す
		&savesettings( @trywrites );

		# 報告用文字列
		$result .= '<li>ユーザ ' . &fcts::forsafety($tryid) . ' の情報を' . $wlabel . 'しました。</li>';
	}
	else {
		# DEMOモード：パスワードの変更を拒否
		&demomodemsg('ユーザIDの変更はできませんでした。');
	}

	# ‥‥‥‥‥‥‥‥‥‥
	# パスワードの変更処理
	# ‥‥‥‥‥‥‥‥‥‥
	if( $newpass1 ne '' ) {
		# パスワードが入力されている場合だけ更新
		if( $flagDemo{'RefuseToChangePassword'} != 1 ) {
			my $recstring = '';
			if( $work eq 'deleteid') {
				# 削除の場合は消す
				&fcts::updatepwdat($tryid,$recstring);		# ハッシュ化せずに空文字を渡せば削除扱い
			}
			else {
				# 変更の場合は変更
				$recstring = &fcts::desmd5encrypt($newpass1,'');	# ハッシュ化(DES or MD5) ※キーの生成は関数側に任せる
				&fcts::updatepwdat($tryid,$recstring);
			}
			# 報告用文字列
			$result .= '<li>ユーザ ' . &fcts::forsafety($tryid) . ' のパスワードを' . $wlabel . 'しました。</li>';
		}
		else {
			# DEMOモード：パスワードの変更を拒否
			&demomodemsg('パスワードの変更はできませんでした。');
		}
	}

	$result .= "</ul>\n";
	my $msg = "<h2>ユーザID管理作業を完了</h2><p>$result</p>";
	&showadminpage('Updated','',$msg,'CUA');
}

# -----------------------------------
# ADMIN：事前カウント群のカウント処理
# -----------------------------------
sub adminRecount
{
	# 再カウント
	my $msg = '<p>全投稿を再カウントし、カウント値のキャッシュデータを更新しました。(年月別該当数、新着リスト、カテゴリ該当数、ハッシュタグ該当数)</p>' . "\n";
	$msg .= '<div class="recountBox">';
	$msg .= '<h2>▼年月集計:</h2>' . "\n";
	&datadatecounter();
	$msg .= $setdat{'datelisthtml'} . "\n";
	$msg .= '</div>';
	# 新着リストの再生成（※この処理は設定ファイルを書き換えるので、下記の設定情報の更新処理よりも前に実行する必要がある。）
	$msg .= '<div class="recountBox">';
	$msg .= '<h2>▼新着リスト生成:</h2>' . "\n";
	&updatelatestlist( $setdat{'latestlistup'} , $setdat{'latestlistparts'} , $setdat{'latesttitlecut'} );
	$msg .= $setdat{'latestlisthtml'} . "\n";
	$msg .= '</div>';
	$msg .= '<div class="recountBox">';
	$msg .= '<h2>▼カテゴリ集計:</h2>' . "\n";
	$msg .= &categorycounter() . "\n";
	$msg .= '<p class="buttonBox"><a href="' . &makeQueryString('mode=admin','work=categories') . '" class="btnlink">カテゴリ管理へ</a></p>';
	$msg .= '</div>';
	$msg .= '<div class="recountBox">';
	$msg .= '<h2>▼ハッシュタグ集計:</h2>' . "\n";
	$msg .= &datahashcounter() . "\n";
	$msg .= '</div>';

	my $css = '<style type="text/css">
		.recountBox { display: inline-block; max-width: 25vw; box-sizing:border-box; vertical-align:top; margin-right: 1em; word-break: break-all;}
		.recountBox ul { padding-right: 1em; }
		h2 { text-indent: 1em; background-color:#e0f0e0; font-size:1.1em; }
		.buttonBox { text-align:center; }
		@media all and (max-width: 1200px) {
			.recountBox { display:block; max-width: 100%; margin-right: 0; }
			.recountBox ul { padding-right: 0; }
		}
	</style>';

	&showadminpage('RECOUNTED','',$msg,'CA',$css);
}

# --------------------------------
# ADMIN：自動/手動バックアップ画面
# --------------------------------
sub adminBackup
{
	my $msg = '';

	# 最初にチェック：設定で自動バックアップが無効になっている場合を確認して表示
	if( $setdat{'autobackup'} == 0 ) {
		$msg .= '<p>自動バックアップは<strong class="important">無効化</strong>されています。<br>自動バックアップ処理は実行されません。(有効化するには設定を変更して下さい。)</p>';
	}
	else {

		# バックアップファイル保持日数の設定値を得る
		my $backupholddays = $setdat{'backupfilehold'} || 30;

		# 自動バックアップ先の存在確認
		if( -d $autobackupto ) {
			# 書き込みできるかどうかのテスト（実際に作成してみて確認。書けたらすぐ消す。）
			my $oppath = $autobackupto . '/test.txt';

			# 試験出力
			if( open( TESTOUT, ">$oppath" ) ) {		# 常に新規出力なのでロック不要
				print TESTOUT "TEST\n";
				close TESTOUT;
			}
			# 確認
			if( -f $oppath ) {
				# 書けたなら消す（消せなかった場合は考慮しない）
				unlink $oppath;
				# 既にバックアップされているファイルがあればリストアップ。（バックアップの設定自体は、「設定」側に任せる。）
				my $blist = &listupBackupfiles();
				$msg .= '<p>自動バックアップは<strong class="important">有効化</strong>されています。<br>現在のバックアップデータは下記の通りです。</p>' . $blist . '<p>※自動バックアップ処理は、データファイルに何かが書き込まれたタイミングで実行されます。<br>※バックアップファイルは1日ごとに切り替え、最大' . $backupholddays . 'ファイルが記録されます。古いバックアップファイルは自動削除されます。</p>';
			}
			else {
				# 書けなかったら報告
				$msg .= '<p>自動バックアップは<strong class="important">実行されていません</strong>。<br>※バックアップ用フォルダ ' . &fcts::forsafety( $autobackupto ) . ' への書き込みが失敗しました。自動バックアップ機能を使うためには、このフォルダに書き込み権限を付加して下さい。(または十分な空き容量があるかどうかを確認して下さい。)';
			}
		}
		else {
			# ない
			$msg .= '<p>自動バックアップは<strong class="important">実行されていません</strong>。<br>※自動バックアップ機能を使うためには、バックアップ用フォルダ ' . &fcts::forsafety( $autobackupto ) . ' を作成して下さい。';
		}

	}

	# ------------------------------
	# データの手動バックアップ操作UI
	my $bupquery = &makeQueryString('mode=getbackup');
	$msg .= qq|
		<p class="mbu">現状の最新データファイルをバックアップとしてダウンロードするには、下記のボタンを押して下さい。</p>
		<ul class="systemmenu">
			<li><a href="$bupquery"><span class="jp">バックアップデータをダウンロード</span><span class="en">Download Backup file</span></a></li>
		</ul>
		<p>※ダウンロードにならない場合(＝ブラウザ上でXMLが表示されてしまう場合)は、右クリックして「名前を付けてリンク先を保存」などのメニューを使って下さい。</p>
		<p class="noticebox">
			※万一データが失われてしまった場合には、バックアップファイルを「CGIで設定しているデータファイル名」にリネームした上でアップロードすれば、そのバックアップが取られた状態に戻せます。できるだけ頻繁にバックアップを取っておくことをお勧め致します。<br>
		</p>
	|;
	my $css = '<style type="text/css">
		.mbu { margin-top:1em; padding-top:1em; border-top: 2px solid #ada; }
		.backups a { text-decoration:none; }
		.backups a:hover { text-decoration:underline; }
		.backups td:first-child { text-align:center; }
		.backups td + td + td + td { text-align:right; }
		.filelink a { word-break:break-all; }
	</style>';
	&showadminpage('BACKUP','',$msg,'CA',$css);
}

# ----------------------------------------------------------------
# ADMIN:BACKUP:バックアップファイルのリストアップ (超過分の削除も)
# ----------------------------------------------------------------
sub listupBackupfiles
{
	# バックアップファイル保持日数の設定値を得る
	my $backupholddays = $setdat{'backupfilehold'};
	if( $backupholddays < 2 ) { $backupholddays = 30; }	# 値がおかしければデフォルト値に

	my $res = '<table class="backups standard"><tr><th>＼</th><th>バックアップファイル</th><th>自動バックアップ日時</th><th>サイズ</th></tr>';

	# ディレクトリのファイル一覧を得る
	opendir( DIRECTORY, $autobackupto ) or &errormsg("バックアップディレクトリを開けませんでした。");
	my @filelist = readdir( DIRECTORY );
	closedir( DIRECTORY );

	# バックアップファイルだけをリストアップ
	my @bupfiles;
	foreach my $of (@filelist) {
		# バックアップファイルかどうか（※backupで始まり、$bmsdataで終わるファイル名）
		if( $of =~ m/^backup.+$bmsdata/ ) {
			push( @bupfiles, $of );
		}
	}

	# ソート(辞書順で降順)
	@bupfiles = sort { $b cmp $a } @bupfiles;

	# 超過分を削除
	for my $i ( $backupholddays .. $#bupfiles ) {
		unlink ("$autobackupto/$bupfiles[$i]");
	}

	# ファイル情報を取得して表示用文字列を作る
	my $count = 1;
	foreach my $of (@bupfiles) {
		# ファイルパスを作る
		my $fp = "$autobackupto/$of";
		# ファイルがある場合だけ表示 (※超過分が直前の処理で削除された場合は、ファイルが消えているのにファイル名がリストにある状況になる。)
		if( -f $fp ) {
			# 情報取得
			my @fs = stat $fp;
			my $fsize = $fs[7]; # サイズ
			my $mtime = &fcts::datetojpstyle( &fcts::getdatetimestring( $fs[9] )); # 更新時刻
			# 文字列作成
			my $fsu = &fcts::byteswithunit( $fsize );	# 単位付き容量に変換
			$res .= qq|<tr><td>$count</td><td class="filelink"><a href="$fp" download>$of</a></td><td>$mtime</td><td>$fsu</td></tr>|;
			$count++;
		}
	}

	# バックアップが1つもない場合
	if( $#bupfiles == -1 ) {
		$res .= '<tr><td colspan="4">※まだ1度も自動バックアップされていません。</td></tr>';
	}

	$res .= '</table>';
	return $res;
}

# -------------------------------------------------
# ADMIN：BACKUP：自動バックアップ用ファイル名を返す		(ディレクトリが存在しないか、バックアップが無効化されていれば、空文字を返す)
# -------------------------------------------------
sub getAutoBackupFilePath
{
	my $ret = '';

	# 自動バックアップ先ディレクトリの存在確認（＋自動バックアップが有効化されていれば）
	if(( -d $autobackupto ) && ( $setdat{'autobackup'} == 1 )) {
		# 現在日時から年月日を得る
		my $timestamp = &fcts::getNowDateForFileName();
		# ファイル名を作成
		$ret = "$autobackupto/backup.$timestamp.$bmsdata";
	}

	return $ret;
}

# -----------------------
# ADMIN：エクスポート画面
# -----------------------
sub adminExport
{
	# ユーザ一覧を作成
	my $useropts = &getPulldownUserList();

	# 日付一覧を作成
	&datadatecounter();		# 日付を再カウント
	my $dateopts = &getPulldownDateList();

	# ハッシュタグ一覧を作成
	&datahashcounter();		# ハッシュタグを再カウント
	my $htagopts = &getPulldownHashtagList();

	# カテゴリ一覧を作成 (※カテゴリ該当数は表示しないので再カウントはしない)
	my $catopts = &getPulldownCatList(1);

	# 出力順序一覧を作成
	my $orders = &makePulldownOrderList();

	# スキン一覧を作成
	my @skins = &getSubSkinList();
	my $skinopts = '';
	foreach my $oneskin (@skins) {
		$skinopts .= qq|<option value="$oneskin">$oneskin</option>|;
	}
	if( $cp{'skindir'} ne '' ) {
		my $nowskin = &fcts::forsafety($cp{'skindir'});
		$skinopts .= qq|<option value="$nowskin">現在適用中のスキン($nowskin)</option>|;
	}
	$skinopts .= qq|<option value="#plaintext#">ほぼプレーンテキスト</option>|;

	my $cgipath = &getCgiPath();
	my $msg = qq|
		<p>指定の条件に該当する投稿を、指定の方法でエクスポートできます。条件を選択して「エクスポートする」ボタンを押して下さい。</p>
		<form action="$cgipath" method="get" class="export">
			<fieldset><legend>エクスポート対象の抽出条件</legend>
			<ul class="excond">
				<li>投稿者(ユーザID)：$useropts</li>
				<li>投稿日付：$dateopts</li>
				<li>検索語：<input type="text" name="q" value=""></li>
				<li>ハッシュタグ：$htagopts</li>
				<li>カテゴリ：$catopts</li>
				<li>出力順序：$orders</li>
			</ul>
			</fieldset>
			<fieldset><legend>エクスポート方法</legend>
			<ul class="excond">
				<li>適用スキン：
					<select name="skin"><option value="">デフォルトスキン</option>$skinopts</select>
				</li>
				<li>エクスポート形態：
					<p class="choice">
						<label><input type="radio" name="mode" value="export" checked>ファイルとしてダウンロードする</label><br>
						<label><input type="radio" name="mode" value="view">画面に表示する</label><br>
					</p>
				</li>
			</ul>
			</fieldset>
			<p>
				<input type="submit" value="エクスポートする" class="doexport">
				<input type="reset" value="選択を初期状態に戻す" onclick="return confirm('抽出条件をリセットしますか？');">
			</p>
		</form>
		<p>※何も条件を指定しなければ、全投稿が対象になります。<br>※ファイルにエクスポートする場合は、対象投稿数がどれだけあっても、ページ分割はされずに1ファイルで出力されます。</p>
	|;
	my $css = '<style type="text/css">
		form.export { margin:1em 0; padding:1em; background-color: #f0f5f0; }
		.excond { margin: 0.5em 0; padding: 0 0.5em 0 25px; }
		.excond li { border-bottom: 1px dashed #ccc; padding-bottom: 0.5em; margin-bottom: 0.5em; }
		.excond li:last-child { margin-bottom:0; padding-bottom:0; border-bottom:none; }
		.choice { margin: 0.35em 0; }
		.doexport { font-size: 1.2em; }
		select { max-width: 250px; }
	</style>
	';
	&showadminpage('EXPORT','',$msg,'CA',$css);
}

# ----------------------
# 複合検索フォームを作成	引数：掲載オプションフラグ群(掲載順序の指定も兼ねる)文字列	U:ユーザ、D:日付、H:ハッシュタグ、C:カテゴリ、O:出力順序
# ----------------------	返値：フォームHTMLソース
sub complexsearchform
{
	my $optflags = shift @_ || 'UDHCO';	# 指定がなければデフォルト順序を使う

	# 検索フォーム用select要素群を生成
	my $useropts = &getPulldownUserList();		# ユーザ一覧を作成
	my $dateopts = &getPulldownDateList();		# 日付一覧を作成
	my $htagopts = &getPulldownHashtagList();	# ハッシュタグ一覧を作成
	my $catopts  = &getPulldownCatList(0);		# カテゴリ一覧を作成 (IDは見せない)
	my $orders   = &makePulldownOrderList();	# 出力順序一覧を作成

	# 挿入要素群
	my $searchword = &fcts::forsafety($cp{'search'});	# 現在の検索語
	my $placeholder = &fcts::forsafety($setdat{'searchholder'});	# 検索語欄プレースホルダ
	my $swaccesskey = &fcts::forsafety($setdat{'searchinputkey'});	# 検索語欄アクセスキー
	my $searchlabel = &fcts::forsafety($setdat{'searchlabel'});		# 検索ボタンラベル

	# 複合検索フォームHTMLを作る
	my $cgipath = &getCgiPath();
	my $htmlform = qq|
		<form action="$cgipath" method="get" class="complexsearch">
			<p class="searchbox"><input type="text" name="q" value="$searchword" accesskey="$swaccesskey" placeholder="$placeholder" class="queryinput"><input type="submit" value="$searchlabel" class="submitbutton"></p>
			<ul class="searchoptions">|;

	foreach my $flag (split //, $optflags) {
		# フラグがあるだけループ
		if(    $flag eq 'U' )	{ $htmlform .= qq|\n<li class="souser"><span class="solabel">|	. &fcts::forsafety( $setdat{'cslabeluser'} )	. qq|</span>$useropts</li>|; }
		elsif( $flag eq 'D' )	{ $htmlform .= qq|\n<li class="sodate"><span class="solabel">|	. &fcts::forsafety( $setdat{'cslabeldate'} )	. qq|</span>$dateopts</li>|; }
		elsif( $flag eq 'H' )	{ $htmlform .= qq|\n<li class="sotag"><span class="solabel">|	. &fcts::forsafety( $setdat{'cslabeltag'} )		. qq|</span>$htagopts</li>|; }
		elsif( $flag eq 'C' )	{ $htmlform .= qq|\n<li class="socat"><span class="solabel">|	. &fcts::forsafety( $setdat{'cslabelcat'} )		. qq|</span>$catopts</li>|; }
		elsif( $flag eq 'O' )	{ $htmlform .= qq|\n<li class="soorder"><span class="solabel">|	. &fcts::forsafety( $setdat{'cslabelorder'} )	. qq|</span>$orders</li>|; }
		else { $htmlform .= "\n<li>不明な識別子:" . &fcts::forsafety( $flag ) . '</li>'; }
	}

	$htmlform .= qq|
			</ul>
		</form>
	|;

	return $htmlform;
}

# ------------------------------------------------------------
# プルダウンメニュー用のユーザリスト文字列(select要素群)を得る
sub getPulldownUserList
{
	my @users = &fcts::getUserList();
	my $useropts = '';
	foreach my $ou (@users) {
		my @uin = split(/&lt;&gt;/, &fcts::forsafety($ou));
		my $sel = '';
		if( $uin[0] eq $cp{'userid'} ) { $sel = ' selected'; }
		$useropts .= qq|<option value="$uin[0]"$sel>$uin[1] ($uin[0])</option>|;
	}
	return '<select name="userid" class="select-userid"><option value="">全員</option>' . $useropts . '</select>';
}

# ------------------------------------------------------------
# プルダウンメニュー用の投稿日リスト文字列(select要素群)を得る
sub getPulldownDateList
{
	my $dateopts = '';
	my $datetemp = $setdat{'dateselecthtml'};
	if( $datetemp =~ m|.*<select name="date".*?>(.+?)</select>.*| ) {
		# 日付プルダウンメニューHTMLからoption要素部分だけを抜き出す(＝ $1 )
		# その中から、今日の日付の項目にだけselectedを加える
		$dateopts = &addSelectedForPulldownDateList( $1 );
	}
	else {
		$dateopts = '<option value="">指定しない</option>';		# 抜き出せなかったら
	}
	return '<select name="date" class="select-date">' . $dateopts . '</select>';
}

# 日付プルダウンメニューの中から、今日の日付の項目にだけselectedを加える (※複数箇所で使うので独立関数にしてある)
sub addSelectedForPulldownDateList
{
	my $str = shift @_ || '';

	# 現在表示中の日付限定項目を表す文字列を作る
	my $checkdate = '<option value="' . &fcts::forsafety( $cp{'datelim'} ) . '"';
	# それにselectedを加えたバージョンを作る
	my $selectdate = '<option selected value="' . &fcts::forsafety( $cp{'datelim'} ) . '"';
	# それを探して置き換える
	$str =~ s/$checkdate/$selectdate/;		# 1回だけで充分

	return $str;
}

# ------------------------------------------------------------------
# プルダウンメニュー用のハッシュタグリスト文字列(select要素群)を得る
sub getPulldownHashtagList
{
	my @hashtagdata = split(/<<<--->>>/,$setdat{'hashtagcount'});
	my $htagopts = '';
	foreach my $oh (@hashtagdata) {
		my @ohn = split(/:::---:::/, &fcts::forsafety($oh));	# ハッシュタグの名称とカウンタを分離
		my $sel = '';
		if( $ohn[0] eq $cp{'hasgtag'} ) { $sel = ' selected'; }
		$htagopts .= qq|<option value="$ohn[0]"$sel>$ohn[0] ($ohn[1])</option>|;
	}
	return '<select name="tag" class="select-tag"><option value="">全ハッシュタグ</option>' . $htagopts . '</select>';
}

# --------------------------------------------------------------
# プルダウンメニュー用のカテゴリリスト文字列(select要素群)を得る
sub getPulldownCatList
{
	my $showid = shift @_ || 0;	# 1＝ID名を含める／0＝ID名は含めない

	my @cats = &fcts::getCategoryList(2);
	my $catopts = '';
	foreach my $oc (@cats) {
		my @onecat = split(/&lt;&gt;/, &fcts::forsafety($oc));	# カテゴリのIDと名称を分離
		my $sel = '';
		if( $onecat[0] eq $cp{'cat'} ) { $sel = ' selected'; }
		my $showedid = '';
		if( $showid ) { $showedid = " ($onecat[0])"; }
		$catopts .= qq|<option value="$onecat[0]"$sel>$onecat[1]$showedid ($onecat[2])</option>|;
	}

	# 「どれにも属していない」に対応する文字列が登録されていればそれを使う
	my $otherlabel = 'どれにも属していない';
	if(( $setdat{'addnocatitem'} == 1 ) && ( $setdat{'addnocatlabel'} ne '' )) {
		# カテゴリツリーに「どれにも属していない」項目を追加する設定で、かつ、自由入力ラベルが空でなければ
		$otherlabel = &fcts::forsafety($setdat{'addnocatlabel'});
	}

	return '<select name="cat" class="select-cat"><option value="">全カテゴリ</option>' . $catopts . '<option value="-">' . $otherlabel . '</option></select>';
}

# --------------------------------------------------------
# プルダウンメニュー用の出力順序文字列(select要素群)を得る
sub makePulldownOrderList
{
	# ラベルのエスケープ
	my $straightname = &fcts::forsafety($setdat{'showstraightheader'});
	my $reversename  = &fcts::forsafety($setdat{'showreverseheader'});
	if( $straightname !~ /降順/ ) { $straightname .= '（降順）'; }	# 降順という単語が使われていなければ補足として追加
	if( $reversename  !~ /昇順/ ) { $reversename  .= '（昇順）'; }	# 昇順という単語が使われていなければ補足として追加

	# 逆順が選択中なら反映する
	my $sel = '';
	if( $cp{'order'} eq 'reverse' ) { $sel = ' selected'; }

	return qq|<select name="order" class="select-order"><option value="">$straightname</option><option value="reverse"$sel>$reversename</option></select>|;
}

# -------------------------
# ADMIN：別スキンの一覧画面
# -------------------------
sub adminSkinlist
{
	# CGI PATH:
	my $cgipath = $cginame;		# 注：恒常付加パラメータを排するので &getCgiPath() は呼ばない。

	# 別スキンの存在を確認
	my @skins = &getSubSkinList();

	# チェックしてリストアップ
	my $msg = '';
	my $skinlinks = '<table class="skindirectories"><thead><tr><th>スキン格納ディレクトリ</th><th colspan="2">スキンの適用操作</th></tr></thead><tbody>' . "\n";
	my $skincount = 0;
	foreach my $oneskin (@skins) {
		if( $setdat{'skindirectory'} eq $oneskin ) {
			# 今適用中なら
			$skinlinks .= qq|<tr class="nowapplied"><th>$oneskin</th><td colspan="2">簡易本番適用中 <form action="$cgipath" method="post" class="releaseform"><input type="hidden" name="mode" value="admin"><input type="hidden" name="work" value="applyskin"><input type="hidden" name="newskin" value=""><input type="submit" value="解除"></form></td></tr>\n|;
		}
		elsif( $oneskin eq $setdat{'rssskindir'} ) {
			# RSS用に指定されているディレクトリ名と一致したら
			$skinlinks .= qq|<tr><th>$oneskin</th><td colspan="2"><small class="otherpurpose">※<a href="?mode=rss">RSSフィード</a>用に指定されています。</small></td></tr>\n|;
		}
		elsif( $oneskin eq $setdat{'galleryskindir'} ) {
			# ギャラリー用に指定されているディレクトリ名と一致したら
			$skinlinks .= qq|<tr><th>$oneskin</th><td colspan="2"><small class="otherpurpose">※<a href="?mode=gallery">ギャラリーモード</a>用に指定されています。</small></td></tr>\n|;
		}
		elsif( $oneskin eq $setdat{'sitemappageskindir'} ) {
			# サイトマップページ用に指定されているディレクトリ名と一致したら
			$skinlinks .= qq|<tr><th>$oneskin</th><td colspan="2"><small class="otherpurpose">※<a href="?mode=sitemap">サイトマップページ</a>用に指定されています。</small></td></tr>\n|;
		}
		else {
			# 適用候補なら
			$skinlinks .= qq|<tr><th>$oneskin</th><td><a href="?skin=$oneskin">適用結果をプレビュー</a></td><td><form action="$cgipath" method="post"><input type="hidden" name="mode" value="admin"><input type="hidden" name="work" value="applyskin"><input type="hidden" name="newskin" value="$oneskin"><input type="submit" value="本番適用(簡易)"></form></td></tr>\n|;
		}
		$skincount++;
	}
	$skinlinks .= '</tbody></table>';

	# ………………………
	# リセット用の表示
	# ………………………
	if( $cp{'skindir'} ne '' ) {
		# 別スキンのプレビュー状態なら
		$msg .= qq|
			<div class="skinpreviewed">
				<p>現在の表示に使われている別スキンの一時適用(プレビュー状態)を解除したい場合は、下記のボタンを押して下さい。</p>
				<ul class="systemmenu">
					<li><a href="$cginame"><span class="jp">デフォルトスキンでの表示に戻る</span><span class="en">Back to Default Skin</span></a></li>
				</ul>
			</div>
		|;
	}
	if( $setdat{'skindirectory'} ne '' ) {
		# 本番適用中のスキンがあれば
		my $skinname = &fcts::forsafety( $setdat{'skindirectory'} );
		$msg .= qq|
			<div class="skinapplied">
				<p class="skinname">★現在は、スキン <b>$skinname</b> が簡易本番適用されています。</p><p>このスキンの本番適用(簡易)状態を解除して、デフォルトのスキンに戻したい場合は、下記のボタンを押して下さい。</p>
				<form action="$cgipath" method="post"><input type="hidden" name="mode" value="admin"><input type="hidden" name="work" value="applyskin"><input type="hidden" name="newskin" value=""><input type="submit" value="デフォルトスキンの適用に戻す"></form>
			</div>
		|;
	}

	if( $skincount > 0 ) {
		# ………………………………………………
		# 適用可能なスキンが1つ以上あれば
		# ………………………………………………
		$msg .= q|
			<p>下記の別スキンが見つかりました。</p>
			<ul class="sysguide">
				<li><b>プレビューしたい場合：</b>「適用結果をプレビュー」リンクをクリックして下さい。あなた以外の閲覧者には影響しません。(ただし、適用結果のURLに直接アクセスすれば、あなた以外の閲覧者でも適用結果を閲覧可能です。)</li>
				<li><b>本番適用したい場合：</b>
		|;
		if( $rentalflag == 1 ) {
			# レンタルモードなら
			$msg .= q|「本番適用(簡易)」ボタンを押して下さい。</li>|;
		}
		else {
			# 通常動作モードなら
			$msg .= q|
					<ul class="sysguide">
						<li><strong class="important">本則</strong>：スキン構成ファイル群を「CGIと同じディレクトリ」に置いて下さい。</li>
						<li><strong class="important">簡易</strong>：「本番適用(簡易)」ボタンを押すことでも本番適用できます。ただし、スキンHTML内に相対パスの記述があると正しく表示できない可能性があります。</li>
					</ul>
				</li>
			|;
		}
		$msg .= '</ul>' . $skinlinks;
	}
	else {
		# ………………………………………………
		# 適用可能なスキンがなければ
		# ………………………………………………
		$msg .= q|<p>適用可能な別スキンファイルは見つかりませんでした。</p>|;
	}

	# ………………………
	# 共通表示
	# ………………………
	if( $rentalflag == 1 ) {
		# レンタルモードなら
		$msg .= q|<p class="noticebox">※この画面には、レンタル環境にセットアップされている別スキンファイルだけが一覧表示されます。</p>|;
	}
	else {
		# 通常モードなら
		$msg .= q|<p class="noticebox">※この画面には、CGI設置ディレクトリ内の『サブディレクトリに格納された別スキンファイル』が一覧表示されます。<br>※「1スキン＝1サブディレクトリ」でアップロードすると、ここに一覧で現れます。(孫サブディレクトリ以降の階層は走査しません)<br>※プレビューや本番適用(簡易)では、スキンHTMLの記述方法によっては、CSSが正しく適用できない場合があります。<br>※CGIの設定でスキンファイル名を変更している場合は、その変更後のスキンファイル名で存在しているスキンのみを認識します。</p>|;
	}

	my $css = '<style type="text/css">
		.skinapplied { background-color: #fafacc; border-radius: 1em; padding: 1em; margin: 0 0 1.5em 0; }
		.skinname { background-color: #fff; color: darkblue; padding: 0.8em; }
		.skinpreviewed { border-bottom: 1px dashed gray; padding-bottom: 1em; margin-bottom: 1.5em; }
		.releaseform { display: inline-block; }
		.skindirectories { border-collapse: collapse; border: 2px solid green; }
		.skindirectories tr:hover { background-color: #ffc; }
		.skindirectories tbody th,td { border: 1px solid #ccc; padding: 0.34em 0.5em; text-align: left; font-weight: normal; }
		.skindirectories thead th { background-color:green; color:white; border-bottom: 1px solid green; font-size: 0.8em; padding: 0.25em 0.4em; }
		.skindirectories a { font-size: 0.9em; display: inline-block; line-height: 1.1; }
		.nowapplied { background-color: #f5f5cc; }
		.nowapplied td { text-align: center; font-size: 0.9em; }
		.otherpurpose { display: block; line-height:1.2; font-size: 0.8em; }
		@media all and (max-width: 600px) {
			.skindirectories { font-size: 0.9em; }
		}
		@media all and (max-width: 400px) {
			.skindirectories { font-size: 0.8em; }
		}
	</style>
	';
	&showadminpage('SKIN LIST','',$msg,'CA',$css);
}

# ----------------------------
# 存在する別スキンの一覧を返す	返値：スキンディレクトリ名の配列
# ----------------------------
sub getSubSkinList
{
	my @ret;

	# 別スキンが既に適用済みの場合は、スキンファイル名だけを抜き出す
	if( $skinfilecover  =~ m|^.+/(.+)| ) { $skinfilecover = $1; }
	if( $skinfileinside =~ m|^.+/(.+)| ) { $skinfileinside = $1; }

	# ディレクトリのファイル一覧を得る
	opendir( DIRECTORY, './' ) or &errormsg("ディレクトリが開けませんでした。");
	my @filelist = readdir( DIRECTORY );
	closedir( DIRECTORY );

	# チェックしてリストアップ
	my $skincount = 0;
	foreach my $onefile (@filelist) {
		if(( $onefile !~ m/^\./ ) && ( -d $onefile )) {
			# ディレクトリだったら、スキンファイルの存在を確認 (※先頭が.記号のディレクトリ名は除く)
			my $tryskin1 = $onefile . '/' . $skinfilecover;
			my $tryskin2 = $onefile . '/' . $skinfileinside;
			if(( -f $tryskin1 ) && ( -f $tryskin2 )) {
				# スキンファイルが2つとも存在したらピックアップ
				push(@ret,$onefile);
			}
		}
	}

	return @ret;
}

# -------------------------
# ADMIN：別スキンの本番適用
# -------------------------
sub adminApplySkin
{
	my $msg = '';

	# 不正送信の確認
	&fcts::postsecuritycheck('work=applyskin');

	# スキンの本番適用指示を受け取る(安全化して)
	my $newskin = &fcts::forsafety( $cgi->param('newskin') ) || '';

	# 本番適用の除外条件を確認
	if( $newskin =~ /\Arss\z/ ) {
		# RSSだったら拒否
		&showadminpage('NOT FOR VIEW','','<p>RSSフィード用に作成されたスキンを、ページ表示用スキンとして本番適用することはできません。</p><p>RSS用スキンは、ただアップロードしておくだけで<a href="?mode=rss">RSSフィード</a>として機能します。（※ただし、管理画面の［設定］から、あらかじめ「内蔵RSSスキン」ではなく「独自RSSスキン」を使用してRSSフィードを出力する設定に切り替えておく必要があります。）</p>','CSA','');
		exit;
	}

	if( $flagDemo{'RefuseToChangeSettings'} != 1 ) {

		# 適用するスキン名を設定データに書き加える。
		$setdat{'skindirectory'} = $newskin;

		# 設定ファイルに書き込み
		my @trywrites;
		push( @trywrites, "skindirectory=" . $setdat{'skindirectory'} );
		&savesettings( @trywrites );

		if( $newskin ne '' ) {
			# newskin に値があれば簡易本番適用処理
			$msg .= qq|<p>スキン <b>$newskin</b> を<strong class="important">簡易</strong>本番適用しました。</p>|;
			$msg .= q|
				<p>下記の注意事項もご一読下さい。</p>
				<p class="noticebox">
					※<strong>より高速な動作のために：</strong><br>この<strong class="important">簡易</strong>本番適用機能を使ってスキンを本番適用すると、CGIの動作時に毎回「スキンの切り替え」作業が発生します。処理はほんの一瞬ですから特に気にはならないでしょうが、より高速に動作させるためには、本番適用したいスキンの構成ファイルを、<strong class="important">CGIと同じディレクトリに手動で格納</strong>した上で、スキンの表示設定を「デフォルトスキン」に戻して下さい。そうすると、スキンの切り替え処理が発生しなくなるので、動作が遅くならずに済みます。<br><br>
					※<strong>正常に閲覧できない場合：</strong><br>この<strong class="important">簡易</strong>本番適用機能では、スキンHTMLの書き方によっては（相対パスの記述を自動変換できずに）正しく表示できない場合があります。その場合は、スキンの本番適用を一旦解除した後に、スキンの構成ファイルを「CGIと同じディレクトリ」に手動で移動させて、デフォルトスキンとしてご使用下さい。（スキンを自作する場合は、相対パスではなく絶対パスで記述する方が無難です。）
				</p>
			|;
		}
		else {
			# newskin に値がなければデフォルトに戻す処理
			$msg .= q|<p>適用スキンを、デフォルトスキンに戻しました。</p>|;
		}
	}
	else {
		# DEMO：設定変更を拒否
		&demomodemsg('スキンの切り替えはできませんでした。');
	}

	my $css = '<style type="text/css">
	</style>
	';
	&showadminpage('SKIN CHANGED','',$msg,'CSA',$css);
}

# --------------------------------------------------
# バックアップデータのダウンロード処理(octet-stream)
# --------------------------------------------------
sub modeGetbackupfile
{
	# まずは読み取り専用モードで認証を確認
	my $permittedid = &fcts::checkpermission(1);
	if( !$permittedid ) {
		# ログインしていなければ
		&errormsg("この操作は管理画面にログインしている間にしか実行できません。");
	}

	# ファイル名を作る
	my $dlFileName = "backup" . &fcts::getNowDateForFileName() . ".xml";

	# データファイルを開く
	open(DF, $bmsdata) or &errormsg("データファイルが開けませんでした。");
	flock(DF, 1);

	# ヘッダoctet-streamを出力
	print <<"OSHEAD";
Content-type: application/octet-stream
Content-Disposition: attachment; filename=$dlFileName

OSHEAD

	# データファイルの中身を出力
	binmode DF;
	binmode STDOUT;
	while (my $DFdata = <DF>) {
		print STDOUT $DFdata;
	}

	# ファイルを閉じる
	close DF;
}

# --------------
# PASSCHECK MODE
# --------------
sub modePasscheck
{
	my $defaultnextpage = "?mode=admin";	# デフォルトでの次の行き先

	# データ受信内容確認
	my $trypass   = $cgi->param('trystring') || '';	# 入力されたパスワード
	my $requestid = $cgi->param('requestid') || '';	# 入力されたID
	my $nexturl   = $cgi->param('nexturl') || "$defaultnextpage";

	# 不正な移動先のチェック
	if( $nexturl !~ m/^\?/  ) {
		# nexturlが「?」記号で始まっていなければ、移動先を強制修正
		$nexturl = $defaultnextpage;
	}

	# IDチェック（入力されたIDが存在するかどうかを確認して、ある場合だけパスワードチェックへ進む）
	if( $requestid eq '' ) {
		# IDの指定がないなら再入力
		&passfront($nexturl,1);
		exit;
	}
	else {
		my $userexist = &fcts::getUserDetail($requestid,1);
		if( ( &fcts::checkpass('') != 2 ) && ( $userexist eq '' )) {
			# IDの登録自体は存在する上で、指定ユーザが存在しない場合は再入力
			&passfront($nexturl,1);
			exit;
		}
	}

	# パスワードチェック
	if( &fcts::checkpass($trypass,$requestid) >= 0 ) {
		# 一致：セッションクッキーの発行

		# セッションIDの生成
		my $sessionid = &fcts::makesessionid($requestid);		# ※ここでは生成だけでなく記録更新も実行している。
		# セッションCookieの発行
		print &fcts::makesessioncookie($sessionid);		# ※Cookie自体にはユーザIDは含めない。

		# 本来のアクセス先にリダイレクト
		my $cgipath = &getCgiPath($nexturl);
		print "Location: $cgipath\n\n\n";
	}
	else {
		# 不一致：再入力の要求
		&passfront($nexturl,1);
	}
}


# -------------------------------------------- #
# 管理画面：設定：チェックボックス用の値を作成 #	引数：データファイルの登録値(1:ON／0:OFF)
# -------------------------------------------- #	返値：0なら空文字, 0以外なら文字列「checked」
sub getattributeforcheckbox
{
	my $num = shift @_ || 0;

	if( $num == 0 ) {
		return '';
	}
	return 'checked';
}

# ---------------------- #	引数：第1～第6：編集データ（前提：当該項目に何もデータがない場合は空文字''になっている）
# 投稿フォームHTMLの作成 #	　　　第7引数：「QUICK」＝クイック投稿フォーム
# ---------------------- #　※仕様：非ログイン時にフォームを表示しない設定なら、呼び出し元側でこの関数を実行しないようにする。
sub makepostform
{
	my $postid   = shift @_ || '';	# 1
	my $userid   = shift @_ || '';	# 2
	my $datetime = shift @_ || '';	# 3
	my $comment  = shift @_ || '';	# 4
	my $cats     = shift @_ || '';	# 5	(Ver.3新設)
	my $flags	 = shift @_ || '';	# 6	(3.4.6新設)
	my $formmode = shift @_ || '';

	# モードの保持（※Boolで済むので変数2つは冗長だが、ソースの読みやすさと将来に選択肢が増える可能性を考慮して、変数は2つ使っておく）
	my $isQUICK = 0;	# クイック投稿フォームの場合のフラグ
	my $isNPOST = 0;	# ノーマル投稿画面の場合のフラグ
	if( $formmode eq 'QUICK' ) {	$isQUICK = 1; }		# クイック投稿フラグ側を立てる
	else {							$isNPOST = 1; }		# ノーマル画面フラグ側を立てる

	# テキストエリアの高さを作る
	my $textareaheight = '';
	if(( $formmode eq '' ) && ( $setdat{'textareasizenormal'} > 1 )) {
		# 通常フォームの場合
		$textareaheight = 'height:' . $setdat{'textareasizenormal'} . 'em;';
	}
	if( $isQUICK && ( $setdat{'textareasizequick'} > 1 )) {
		# QUICKフォームの場合
		$textareaheight = 'height:' . $setdat{'textareasizequick'} . 'em;';
	}

	# UserIDがない場合はログインされていない

	# ………………
	# 権限チェック	※現在ログイン中のIDなどを確認する。
	# ………………
	my $loginedid = &fcts::checkpermission(1);
	my $username = '';
	my $userlevel = 0;
	if( $loginedid ) {
		# ログインされている場合は、ユーザ名と権限Lvを得る
		$username  = &fcts::getUserDetail($loginedid,2) || '名前未設定';	# ユーザ名
		$userlevel = &fcts::getUserDetail($loginedid,1) || 0;				# 権限Lv.
	}

	# ………………………………………………………………
	# 新規か編集か：編集対象IDと投稿日時フォームの作成
	# ………………………………………………………………
	my $idForm;
	if( $postid ne '' ) {
		# 編集の場合（ID選択UI＋投稿日時を維持）
		$idForm = qq|<ul class="line-postid">
			<li><input type="radio" value="$postid" name="postid" id="ide" checked onclick="resetDatetimeUNIQUERAND();"><label for="ide">No.$postidを編集</label> /</li>
			<li>
				<input type="radio" value="" name="postid" id="idn" onclick="cleanDatetimeUNIQUERAND();"><label for="idn">新規に投稿</label>
				<label class="trydelete">（<input type="checkbox" value="$postid" name="trydelete" id="trydeleteUNIQUERAND" disabled>元投稿を削除）</label>
			</li>
		</ul>|;
		# ※この記述は、後述の「※reset/clean JS」 スクリプトとの併用が前提。
	}
	else {
		# 新規の場合（ID新規＋投稿日時の指定なし）
		if( $isQUICK ) {	$idForm = qq|<input type="hidden" value="" name="postid">|;	}
		else {				$idForm = qq|<p class="line-postid">新規投稿 <input type="hidden" value="" name="postid"></p>|;	}
		$datetime = '';	# 投稿日時の中身を確実に消しておく
	}
	my $createDate = &fcts::getdatetimestring();	# フォームを生成した時点の日時(JavaScriptで使う用)
	my $dateForm = qq|<input type="hidden" value="$datetime" name="datetime" data-credate="$createDate" id="datetimeUNIQUERAND" pattern="\\d{4}/\\d{2}/\\d{2} \\d{2}:\\d{2}:\\d{2}" title="投稿日付を YYYY/MM/DD hh:mm:ss 形式で入力。投稿した瞬間の日時を自動記録するには空欄にして下さい。(存在しない日時を許容するかどうかは設定次第です。)">|;

	# …………………………………………
	# テキストエリアと送信ボタンの作成
	# …………………………………………
	my $placeholder = '';
	my $postbutton;
	my $changeid = '';
	my $inputcountset = '';
	my $datetimebuttonset = '';	# 投稿日時変更ボタン関連ソース格納用
	my $decobuttonset = '';		# 装飾ボタン関連ソース格納用
	my $imagebuttonset = '';	# 画像投稿ボタン関連ソース格納用
	my $linkbuttonset = '';		# リンクボタン関連ソース格納用
	my $hashtaginputset = '';	# 既存ハッシュタグ簡単入力関連ソース格納用
	my $categoryinputset = '';	# カテゴリ選択関連ソース格納用
	my $funcinputset = '';		# 機能ボタン関連ソース格納用

	# ▼標準(常時表示)入力欄パーツ群
	if( $username ne '' ) {
		# ログインされている場合はプレースホルダに名前を表示
		if( $setdat{'postphloginname'} == 1 ) {
			$placeholder .= &fcts::forsafety($username);
		}
		$placeholder .= &fcts::forsafety($setdat{'postplaceholder'});

		# ハッシュタグ限定モードで、コメント欄が空なら、そのハッシュタグを最初から挿入 (※角括弧付きのタグがうまくいかないので保留)
		# if(( $cp{'hasgtag'} ne '' ) && ( $comment eq '' )) {
		# 	$comment .= '#' . $cp{'hasgtag'} . ' ';
		# }

		# 投稿ボタン(送信ボタン)を作る
		my $postbuttonlabel = &fcts::forsafety($setdat{'postbuttonlabel'});
		my $postbuttontitle = '入力内容を送信';
		if( $setdat{'postbuttonshortcut'} == 1 ) {
			$postbuttontitle .= ' [Ctrl]+[Enter]';
		}
		$postbutton = qq|<input type="submit" class="postbutton" value="$postbuttonlabel" id="tegalogsubmitUNIQUERAND" title="$postbuttontitle">|;

		# 他のIDに切り替えるリンクを表示
		if( $setdat{'postchangeidlink'} != 0 ) {
			$changeid = '<small class="changelink"><a href="' . &makeQueryString('mode=admin','work=logout') . '" onclick="if( document.getElementById(\'tegalogpostUNIQUERAND\').value.length > 0) { return confirm(\'今IDを切り替えると、入力途中の内容は失われます。IDを変更しますか？\'); }">' . &fcts::forsafety($setdat{'postchangeidlabel'}) . '</a></small>';
		}
	}
	else {
		# 非ログインの場合 (※フォーム自体を表示しない場合は、この関数自体を呼ばない。)
		$placeholder = '投稿するには、ログインが必要です。';
		my $postbuttonlabel = &fcts::forsafety($setdat{'postbuttonlabel'});
		$postbutton = qq|<input type="submit" class="postbutton" value="ログインして$postbuttonlabel">|;
		$changeid = '<small class="changelink">or <a href="' . &makeQueryString('mode=admin') . '">管理画面へ</a></small>';
	}

	# - - - - - - - - - - -
	# ▼テキストエリア生成
	# - - - - - - - - - - -
	$comment =~ s|<br />|\n|g;	# 改行タグを改行コードに
	# ▽投稿欄にカーソルがある状況で動作するスクリプト
	my $scriptctrlenter = '';
	if( $setdat{'postbuttonshortcut'} == 1 || $setdat{'postareaexpander'} == 1 ) {
		# 投稿ショートカットキーまたは拡張ショートカットキーが有効ならJavaScriptを出力
		my $jslines = '';
		if( $setdat{'postbuttonshortcut'} == 1 ) {
			# CTRL+ENTERで投稿
			$jslines .= q|if( event.ctrlKey && event.keyCode == 13 ) { document.getElementById('tegalogsubmitUNIQUERAND').click(); return false; }|;
		}
		if( $setdat{'postareaexpander'} == 1 ) {
			# CTRL+↓で拡張
			$jslines .= q|
				if( event.ctrlKey && event.keyCode == 40 )		{ var nh = document.getElementById('tegalogpostUNIQUERAND').clientHeight * 2; if( nh > window.innerHeight ) { nh = window.innerHeight; window.scrollTo(0, document.getElementById('tegalogpostUNIQUERAND').offsetTop ); } document.getElementById('tegalogpostUNIQUERAND').style.height = nh + 'px'; return false; }	/* CTRL+↓で拡張 */
				else if( event.ctrlKey && event.keyCode == 38 )	{ var nh = document.getElementById('tegalogpostUNIQUERAND').clientHeight / 2; if( nh < 48 ) { nh = 48; } document.getElementById('tegalogpostUNIQUERAND').style.height = nh + 'px'; return false; }	/* CTRL+↑で縮小 */
			|;
		}
		# onkeydownイベント用文字列に結合する
		$scriptctrlenter = &fcts::tooneline( qq|onkeydown="$jslines"| );
	}
	# ▽テキストエリア出力
	my $textarea = qq|<p class="line-textarea"><textarea class="tegalogpost" name="comment" id="tegalogpostUNIQUERAND" style="$textareaheight" placeholder="$placeholder" $scriptctrlenter accesskey="| . &fcts::forsafety($setdat{'postareakey'}) . '">' . &fcts::forsafety($comment) . '</textarea></p>';

	# 入力カウンタUI
	if( $setdat{'postcharcounter'} != 0 ) {
		$inputcountset = qq|<span id="tpostcountUNIQUERAND"></span><script type="text/javascript">document.getElementById('tegalogpostUNIQUERAND').onkeyup = function(){ document.getElementById("tpostcountUNIQUERAND").innerHTML = this.value.length + "<small>文字</small>"; }</script>|;
	}

	# ▼投稿日時変更関連UI
	if( $setdat{'showFreeDateBtn'} == 1 ) {
		my $btnlabel = &fcts::forsafetybutand( $setdat{'datebuttonlabel'} );	# ボタンのラベル
		$datetimebuttonset = &fcts::tooneline( qq|
		<script type="text/javascript">
			function setDatetimeUNIQUERAND(defDatetime){
				var targetBox = document.getElementById('datetimeUNIQUERAND');
				if( targetBox.type == 'hidden' ) {
					/* 日付入力欄が消えていた場合は見せる */
					targetBox.type = 'text';
					if(targetBox.value == '') { targetBox.value = targetBox.dataset.credate; }	/* 日付指定がなければフォーム生成時点の日時を仮挿入 */
				}
				else {
					/* 日付入力欄が見えていた場合は消す */
					targetBox.type = 'hidden';
					if( document.getElementById('idn') && document.getElementById('idn').checked ) {
						/* 「新規に投稿」ラジオボタンが存在する場合で、チェックが入っていれば空欄に戻す */
						targetBox.value = '';
					}
					else {
						/* 「新規に投稿」ラジオボタンが存在すしないか、またはチェックが入ってなければ、元値(新規なら空欄)に戻す */
						targetBox.value = defDatetime;
					}
				}
			}
		</script>
		| );
		$datetimebuttonset .= qq|<span class="decoBtns"><input type="button" class="decoDoorUNIQUERAND" value="$btnlabel" onclick="setDatetimeUNIQUERAND('$datetime');" title="投稿日時を編集"></span>|;
	}

	# ▼新規投稿画面の場合で、既存投稿の編集の場合 (※reset/clean JS)
	if( $isNPOST && ( $postid ne '' )) {
		# 編集するか新規扱いで投稿し直すかで、日付を更新するかどうかを変えるJavaScriptを出力。(※このJavaScriptでは「元投稿を削除」チェックボックスの有効無効も同時に切り替える。)
		$datetimebuttonset .= &fcts::tooneline( qq|
		<script type="text/javascript">
			function resetDatetimeUNIQUERAND() { var targetBox = document.getElementById('datetimeUNIQUERAND').value = '$datetime'; document.getElementById('trydeleteUNIQUERAND').checked = false; document.getElementById('trydeleteUNIQUERAND').disabled = 'disabled'; }
			function cleanDatetimeUNIQUERAND() { var targetBox = document.getElementById('datetimeUNIQUERAND').value = '';  document.getElementById('trydeleteUNIQUERAND').disabled = ''; if(document.getElementById('draftsign')) { document.getElementById('trydeleteUNIQUERAND').checked = true; } }
		</script>
		| );
	}

	# 事前に範囲選択していなくても各種記法を挿入可能にするかどうか
	my $notrequired = '';
	if( $setdat{'allowblankdeco'} == 1 ) {
		# 範囲選択を必須にしない場合は、対象if文を不成立にさせる
		$notrequired = '&& 1==2';
	}

	# 画面幅が狭ければ範囲選択を不要にする
	my $ifthin = '&& ( window.screen.width > 1024 )';

	# ▼リンクボタン関連UI
	if( $setdat{'urlautolink'} == 1 && $setdat{'showLinkBtnStyle'} != 2 ) {
		# URL自動リンクが有効に設定されていて、かつ、リンクボタンが表示される設定なら出力する
		my $gtgtnote = '';
		if( $setdat{'postidlinkgtgt'} == 1 ) {
			# >>123 形式のリンクも有効な場合
			$gtgtnote = q|if( txtSel.match(/^>>\\d+$/) ) { alert('「>>123」の記述は、そのまま投稿すればNo.123へのリンクになります。'); tArea.focus(); return; }|;
		}
		$linkbuttonset = &fcts::tooneline( qq|
		<script type="text/javascript">
			function uisCheckUNIQUERAND(uis,tArea){
				/* uis = User Inputed String, tArea = Target Area */
				if( !uis ) { tArea.focus(); return 0; }
				if( !uis.match(/^https?:\\/\\//) ) { alert('http(s)://から始まるURL以外は指定できません。'); tArea.focus(); return 0; }
				return 1;
			}
			function insLinkUNIQUERAND(kind){
				var tArea	= document.getElementById('tegalogpostUNIQUERAND');
				var tValue	= tArea.value;
				var staPos	= parseInt(tArea.selectionStart, 10);
				var endPos	= parseInt(tArea.selectionEnd, 10);
				var txtBef	= tValue.substring(0, staPos);
				var txtAft	= tValue.substring(endPos);
				var txtSel	= tValue.substring(staPos, endPos);
				var insText = '';
				if( kind == 'U' ) {
					if( txtSel.length == 0 $ifthin $notrequired ) { alert('リンクにしたい範囲を選択して下さい。'); tArea.focus(); return; }
					if( txtSel.length == 0 ) { txtSel = 'リンク'; }	/* 選択なしでも挿入する場合の仮リンクラベル */
					if( txtSel.match(/^https?:\\/\\//) ) { alert('httpで始まるURLは、そのまま本文中に書いておくだけでリンクになります。'); tArea.focus(); return; }
					var uis = prompt('リンク先URLを入力して下さい：');
					if( uisCheckUNIQUERAND(uis,tArea) == 0 ) { return; }
					insText = '[' + txtSel + ']' + uis + ' ';
				}
				else if( kind == 'N' ) {
					$gtgtnote
					var uinote = '';
					if( txtSel.length == 0 ) { uinote = '\\n（※あらかじめ範囲選択しておけば、その範囲をリンクにできます。）'; }
					var uis = prompt('リンク先の投稿番号を数字で入力して下さい：' + uinote);
					if( !uis ) { tArea.focus(); return; }
					uis = uis.replace(/[０-９]/g, function(s){ return String.fromCharCode(s.charCodeAt(0) - 65248); });	/* 全角数字を半角に変換 */
					uis = uis.replace(/^\\s+\|\\s+\$/g, '');	/* 前後の空白を取り除く */
					if( uis == txtSel ) { txtSel = ''; }	/* 範囲選択文字列と入力数値が同じだったら短い表記にする */
					if( txtSel.length == 0 ) { insText = '[>' + uis + ']'; }
					else { insText = '[>' + uis + ':' + txtSel + ']'; }
				}
				else if( kind == 'S' ) {
					var uis = prompt('埋め込みたいSpotifyのシェア用URLを入力して下さい：');
					if( uisCheckUNIQUERAND(uis,tArea) == 0 ) { return; }
					if( !uis.match(/spotify/)) { alert('SpotifyのURLではなさそうです。\\nSpotifyのURLだと認識されなかった場合は、ただ「Spotify」という文字のテキストリンクになります。'); }
					insText = txtSel + '[Spotify]' + uis + ' ';
				}
				else if( kind == 'Y' ) {
					var uis = prompt('埋め込みたいYouTubeのURLを入力して下さい：');
					if( uisCheckUNIQUERAND(uis,tArea) == 0 ) { return; }
					if( !uis.match(/youtu/)) { alert('YouTubeのURLではなさそうです。\\nYoutubeのURLだと認識されなかった場合は、ただ「YouTube」という文字のテキストリンクになります。'); }
					insText = txtSel + '[YouTube]' + uis + ' ';
				}
				else if( kind == 'T' ) {
					var uis = prompt('埋め込みたいツイート単独のURLを入力して下さい：');
					if( uisCheckUNIQUERAND(uis,tArea) == 0 ) { return; }
					if( !uis.match(/twitter.com/)) { alert('TwitterのURLではなさそうです。\\ntwitter.comドメインのURLを入力して下さい。'); return; }
					else if( !uis.match(/status/)) { alert('TwitterのURLですが、ツイート単独のURLではなさそうです。\\nツイート単独のURLは https://twitter.com/nishishi/status/1277915695032893440 のように「status」を含むURLです。もしツイートのURLだと認識されなかった場合は、このまま保存してもツイートとしては展開されません。'); }
					insText = txtSel + '[Tweet]' + uis + ' ';
				}
				else if( kind == 'IMG' ) {
					if( txtSel.length == 0 ) { txtSel = '代替文字'; }
					var uis = prompt('掲載したい画像のURLを入力して下さい：');
					if( uisCheckUNIQUERAND(uis,tArea) == 0 ) { return; }
					insText = '[IMG:' + txtSel + ']' + uis + ' ';
				}
				tArea.value = txtBef + insText + txtAft;
				tArea.focus();
				var cursorPos = staPos + insText.length;
				tArea.setSelectionRange(cursorPos,cursorPos);
			}
			function showLinkSetUNIQUERAND() {
				document.getElementById('linkDoorUNIQUERAND').style.display = 'none';
				document.getElementById('linkSetUNIQUERAND').style.display = 'inline';
			}
		</script>
		| );

		# ボタン挿入処理
		my $btnlabel = &fcts::forsafetybutand( $setdat{'linkbuttonlabel'} );	# ボタンのラベル
		$linkbuttonset .= qq|<span class="decoBtns">|;
		if( $setdat{'showLinkBtnStyle'} == 0 ) { $linkbuttonset .= qq|<span id="linkDoorUNIQUERAND"><input type="button" class="decoDoorUNIQUERAND" value="$btnlabel" onclick="showLinkSetUNIQUERAND();" title="リンクボタンを表示"></span><span id="linkSetUNIQUERAND" style="display:none;">|; }	# 非表示から動的に表示する場合(1/2)
		if(  $setdat{'showLinkBtnUrl'} == 1 )											{	$linkbuttonset .= q|<input type="button" value="| . &fcts::forsafetybutand($setdat{'linkBtnUrlLabel'}) . q|" onclick="insLinkUNIQUERAND('U');" title="指定のURLへのリンク">|;	}
		if(( $setdat{'showLinkBtnNum'} == 1 ) && ( $setdat{'postidlinkize'} == 1 ))		{	$linkbuttonset .= q|<input type="button" value="| . &fcts::forsafetybutand($setdat{'linkBtnNumLabel'}) . q|" onclick="insLinkUNIQUERAND('N');" title="指定投稿No.へのリンク">|; }	# 指定番号リンクが有効に設定されている場合のみ
		if(( $setdat{'showLinkBtnImg'} == 1 ) && ( $setdat{'urlexpandimg'} == 1 ))		{	$linkbuttonset .= q|<input type="button" value="| . &fcts::forsafetybutand($setdat{'linkBtnImgLabel'}) . q|" onclick="insLinkUNIQUERAND('IMG');" title="外部画像を挿入する">|; }	# 画像埋込リンクが有効に設定されている場合のみ
		if(( $setdat{'showLinkBtnTwe'} == 1 ) && ( $setdat{'urlexpandtweet'} == 1))		{	$linkbuttonset .= q|<input type="button" value="| . &fcts::forsafetybutand($setdat{'linkBtnTweLabel'}) . q|" onclick="insLinkUNIQUERAND('T');" title="Twitterのツイートを埋め込む">|; }		# ツイート埋込が有効に設定されている場合のみ
		if(( $setdat{'showLinkBtnYtb'} == 1 ) && ( $setdat{'urlexpandyoutube'} == 1))	{	$linkbuttonset .= q|<input type="button" value="| . &fcts::forsafetybutand($setdat{'linkBtnYtbLabel'}) . q|" onclick="insLinkUNIQUERAND('Y');" title="YouTube動画を埋め込む">|; }			# YouTube埋込が有効に設定されている場合のみ
		if(( $setdat{'showLinkBtnSpt'} == 1 ) && ( $setdat{'urlexpandspotify'} == 1))	{	$linkbuttonset .= q|<input type="button" value="| . &fcts::forsafetybutand($setdat{'linkBtnSptLabel'}) . q|" onclick="insLinkUNIQUERAND('S');" title="Spotify音楽を埋め込む">|; }			# Spotify埋込が有効に設定されている場合のみ
		if( $setdat{'showLinkBtnStyle'} == 0 )	{	$linkbuttonset .= qq|</span><!-- /#linkSet -->|; }	# 非表示から動的に表示する場合(2/2)
		$linkbuttonset .= qq|</span><!-- /.decoBtns(Link) -->|;
	}

	# ▼装飾ボタン関連UI
	if( $setdat{'allowdecorate'} == 1 && $setdat{'showDecoBtnStyle'} != 2 ) {
		# 装飾記法が許可されていて、かつ、装飾ボタンが表示される設定なら出力する
		$decobuttonset = &fcts::tooneline( qq|
		<script type="text/javascript">
			function seldecoUNIQUERAND(decoSign,decoColor,decoName){
				var tArea	= document.getElementById('tegalogpostUNIQUERAND');
				var tValue	= tArea.value;
				var staPos	= parseInt(tArea.selectionStart, 10);
				var endPos	= parseInt(tArea.selectionEnd, 10);
				var txtBef	= tValue.substring(0, staPos);
				var txtAft	= tValue.substring(endPos);
				var txtSel	= tValue.substring(staPos, endPos);
				var newText;
				if( txtSel.length == 0 $ifthin $notrequired ) { alert('先に装飾対象を範囲選択して下さい。'); tArea.focus(); return; }
				if( decoName ) {
					if( decoSign == 'F' ) {
						decoName = prompt(( decoName + 'を半角で入力して下さい：'),decoColor);
						if( !decoName ) { tArea.focus(); return; }
						decoName = decoName.replace(/[－＿Ａ-Ｚａ-ｚ０-９]/g, function(s){ return String.fromCharCode(s.charCodeAt(0) - 65248); });	/* 全角英数記号を半角に変換 */
						newText = '[' + decoSign + ':' + decoName + ':' + txtSel + ']';	/* 専用記法で出力 */
					}
					else if( decoSign == 'R' ) {
						decoName = prompt(( decoName + 'を入力して下さい：'),decoColor);
						if( !decoName ) { tArea.focus(); return; }
						newText = '[' + decoSign + ':' + txtSel + ':' + decoName + ']';	/* 専用記法で出力 */
					}
				}
				else if( decoColor ) {
					decoColor = prompt('色名を半角英字で入力するか、RGB16進数を半角6文字で入力して下さい：',decoColor);
					if( !decoColor ) { tArea.focus(); return; }
					decoColor = decoColor.replace(/[Ａ-Ｚａ-ｚ０-９]/g, function(s){ return String.fromCharCode(s.charCodeAt(0) - 65248); });	/* 全角英数字を半角に変換 */
					newText = '[' + decoSign + ':' + decoColor.toLowerCase().replace(/#/g,"") + ':' + txtSel + ']';	/* 専用記法で出力 */
				}
				else {
					newText = '[' + decoSign + ':' + txtSel + ']';	/* 専用記法で出力 */
				}
				tArea.value = txtBef + newText + txtAft;			/* 前Text、今回の出力、後Textを結合して、新たな本文として置き換える */
				tArea.focus();
				var cursorPos = staPos + newText.length;
				if( txtSel.length == 0 ) { cursorPos--; }
				tArea.setSelectionRange(cursorPos,cursorPos);
			}
			function showDecoSetUNIQUERAND() {
				document.getElementById('decoDoorUNIQUERAND').style.display = 'none';
				document.getElementById('decoSetUNIQUERAND').style.display = 'inline';
			}
		</script>
		| );

		# ボタン挿入処理（装飾CSSは L.1628あたり）
		my $btnlabel = &fcts::forsafetybutand( $setdat{'decobuttonlabel'} );	# ボタンのラベル
		$decobuttonset .= qq|<span class="decoBtns">|;
		if( $setdat{'showDecoBtnStyle'} == 0 ) { $decobuttonset .= qq|<span id="decoDoorUNIQUERAND"><input type="button" class="decoDoorUNIQUERAND" value="$btnlabel" onclick="showDecoSetUNIQUERAND();" title="文字装飾ボタンを表示"></span><span id="decoSetUNIQUERAND" style="display:none;">|; }	# 非表示から動的に表示する場合(1/2)
		if( ( $isNPOST && $setdat{'showDecoBtnEonA'} == 1 ) || ( $isQUICK && $setdat{'showDecoBtnEonQ'} == 1  ) ) { $decobuttonset .= q|<input type="button" class="decoBtnE" value="| . &fcts::forsafetybutand( $setdat{'decoBtnLabelE'} ) . q|"  onclick="seldecoUNIQUERAND('E');" title="強調(Emphasis)">|; }
		if( ( $isNPOST && $setdat{'showDecoBtnBonA'} == 1 ) || ( $isQUICK && $setdat{'showDecoBtnBonQ'} == 1  ) ) { $decobuttonset .= q|<input type="button" class="decoBtnB" value="| . &fcts::forsafetybutand( $setdat{'decoBtnLabelB'} ) . q|"  onclick="seldecoUNIQUERAND('B');" title="太字(Bold)">|; }
		if( ( $isNPOST && $setdat{'showDecoBtnIonA'} == 1 ) || ( $isQUICK && $setdat{'showDecoBtnIonQ'} == 1  ) ) { $decobuttonset .= q|<input type="button" class="decoBtnI" value="| . &fcts::forsafetybutand( $setdat{'decoBtnLabelI'} ) . q|"  onclick="seldecoUNIQUERAND('I');" title="斜体(Italic)">|; }
		if( ( $isNPOST && $setdat{'showDecoBtnUonA'} == 1 ) || ( $isQUICK && $setdat{'showDecoBtnUonQ'} == 1  ) ) { $decobuttonset .= q|<input type="button" class="decoBtnU" value="| . &fcts::forsafetybutand( $setdat{'decoBtnLabelU'} ) . q|"  onclick="seldecoUNIQUERAND('U');" title="下線(Underline)">|; }
		if( ( $isNPOST && $setdat{'showDecoBtnQonA'} == 1 ) || ( $isQUICK && $setdat{'showDecoBtnQonQ'} == 1  ) ) { $decobuttonset .= q|<input type="button" class="decoBtnQ" value="| . &fcts::forsafetybutand( $setdat{'decoBtnLabelQ'} ) . q|"  onclick="seldecoUNIQUERAND('Q');" title="引用(Quote)">|; }
		if( ( $isNPOST && $setdat{'showDecoBtnDonA'} == 1 ) || ( $isQUICK && $setdat{'showDecoBtnDonQ'} == 1  ) ) { $decobuttonset .= q|<input type="button" class="decoBtnD" value="| . &fcts::forsafetybutand( $setdat{'decoBtnLabelD'} ) . q|"  onclick="seldecoUNIQUERAND('D');" title="取消線(Delete)">|; }
		if( ( $isNPOST && $setdat{'showDecoBtnSonA'} == 1 ) || ( $isQUICK && $setdat{'showDecoBtnSonQ'} == 1  ) ) { $decobuttonset .= q|<input type="button" class="decoBtnS" value="| . &fcts::forsafetybutand( $setdat{'decoBtnLabelS'} ) . q|"  onclick="seldecoUNIQUERAND('S');" title="小さめ(Small)">|; }
		if( ( $isNPOST && $setdat{'showDecoBtnTonA'} == 1 ) || ( $isQUICK && $setdat{'showDecoBtnTonQ'} == 1  ) ) { $decobuttonset .= q|<input type="button" class="decoBtnT" value="| . &fcts::forsafetybutand( $setdat{'decoBtnLabelT'} ) . q|"  onclick="seldecoUNIQUERAND('T');" title="極小(Tiny)">|; }
		if( ( $isNPOST && $setdat{'showDecoBtnRonA'} == 1 ) || ( $isQUICK && $setdat{'showDecoBtnRonQ'} == 1  ) ) { $decobuttonset .= q|<input type="button" class="decoBtnR" value="| . &fcts::forsafetybutand( $setdat{'decoBtnLabelR'} ) . q|"  onclick="seldecoUNIQUERAND('R','','ルビ');" title="ルビ(Ruby)">|; }
		if( ( $isNPOST && $setdat{'showDecoBtnConA'} == 1 ) || ( $isQUICK && $setdat{'showDecoBtnConQ'} == 1  ) ) { $decobuttonset .= q|<input type="button" class="decoBtnC" value="| . &fcts::forsafetybutand( $setdat{'decoBtnLabelC'} ) . q|"  onclick="seldecoUNIQUERAND('C','deepskyblue');" title="文字色(Color)">|; }
		if( ( $isNPOST && $setdat{'showDecoBtnMonA'} == 1 ) || ( $isQUICK && $setdat{'showDecoBtnMonQ'} == 1  ) ) { $decobuttonset .= q|<input type="button" class="decoBtnM" value="| . &fcts::forsafetybutand( $setdat{'decoBtnLabelM'} ) . q|"  onclick="seldecoUNIQUERAND('M','greenyellow');" title="背景色(Marker)">|; }
		if( ( $isNPOST && $setdat{'showDecoBtnHonA'} == 1 ) || ( $isQUICK && $setdat{'showDecoBtnHonQ'} == 1  ) ) { $decobuttonset .= q|<input type="button" class="decoBtnH" value="| . &fcts::forsafetybutand( $setdat{'decoBtnLabelH'} ) . q|"  onclick="seldecoUNIQUERAND('H');" title="隠す(hide)">|; }
		if( ( $isNPOST && $setdat{'showDecoBtnFonA'} == 1 ) || ( $isQUICK && $setdat{'showDecoBtnFonQ'} == 1  ) ) { $decobuttonset .= q|<input type="button" class="decoBtnF" value="| . &fcts::forsafetybutand( $setdat{'decoBtnLabelF'} ) . q|"  onclick="seldecoUNIQUERAND('F','','適用するclass名');" title="自由装飾(Free)">|; }
		if( $setdat{'showDecoBtnStyle'} == 0 ) { $decobuttonset .= qq|</span><!-- /#decoSet -->|; }	# 非表示から動的に表示する場合(2/2)
		$decobuttonset .= qq|</span><!-- /.decoBtns -->|;
	}

	# ▼画像投稿ボタン関連UI
	if(( $setdat{'showImageUpBtn'} >= 1 ) && ( $setdat{'imageupallow'} == 1 )) {
		# 画像投稿ボタンを表示する場合で、画像投稿が許可されている場合のみ
		my $confirmmsg = '・投稿画像保存用ディレクトリにある画像（ファイル名）\\n・投稿画像保存用ディレクトリのサブディレクトリ以下にある画像（相対パス）\\n';
		if( $setdat{'imageoutdir'} == 1 ) { $confirmmsg .= '・任意のディレクトリにある画像（絶対パスでも相対パスでも）\\n'; }
		if( $setdat{'imageouturl'} == 1 ) { $confirmmsg .= '・URLの指定（http://またはhttps://で始まるURL）\\n'; }

		$imagebuttonset = &fcts::tooneline( qq|
		<script type="text/javascript">
			function insPictUNIQUERAND(){
				var tArea	= document.getElementById('tegalogpostUNIQUERAND');
				var tValue	= tArea.value;
				var staPos	= parseInt(tArea.selectionStart, 10);
				var endPos	= parseInt(tArea.selectionEnd, 10);
				var txtBef	= tValue.substring(0, staPos);
				var txtAft	= tValue.substring(endPos);
				var txtSel	= tValue.substring(staPos, endPos);
				var insText = '';

				var uis = prompt('表示したい画像のファイル名を入力して下さい。現在の設定では、以下の指定が可能です：\\n\\n$confirmmsg\\n');
				if( !uis ) { tArea.focus(); return; }

				if( txtSel.length == 0 ) {
					insText = txtSel + '[PICT:' + uis + ']';
				}
				else {
					insText = '[PICT:' + txtSel + ':' + uis + ']';
				}

				tArea.value = txtBef + insText + txtAft;
				tArea.focus();
				var cursorPos = staPos + insText.length;
				tArea.setSelectionRange(cursorPos,cursorPos);
			}
		</script>
		| );

		my $attmultiple = '';
		my $multipleguide = '';
		if( $setdat{'imageupmultiple'} == 1 ) { $attmultiple = 'multiple'; $multipleguide = '(複数個の同時選択も可能)' }

		# ボタン挿入処理
		my $btnlabel = &fcts::forsafetybutand( $setdat{'imagebuttonlabel'} );	# ボタンのラベル
		$imagebuttonset .= '<span class="decoBtns">';
		if( $setdat{'showImageUpBtn'} == 1 ) {
			# 非表示から動的に表示する場合(1/2)
			$imagebuttonset .= qq|<input type="button" class="imgUrl" value="$btnlabel" onclick="getElementById('imageBtnsUNIQUERAND').style.display='inline'; this.style.display='none';" title="画像掲載ボタンを表示"><span id="imageBtnsUNIQUERAND" style="display:none;">|;
		}
		if(  $setdat{'showImageBtnNewUp'} == 1 )	{	$imagebuttonset .= qq|<input id="newImgUpUNIQUERAND" style="max-width:300px;" type="file" name="upload_file" $attmultiple accept="image/*" title="画像を新規にUPする$multipleguide">|;	}	# 新規画像アップロードボタン
		if(  $setdat{'showImageBtnExist'} == 1 )	{	$imagebuttonset .= q|<input type="button" value="| . &fcts::forsafetybutand($setdat{'imageBtnExistLabel'}) . q|" onclick="insPictUNIQUERAND();" title="既存の画像を表示する">|;	}		# 既存画像表示ボタン
		if( $setdat{'showImageUpBtn'} == 1 ) {
			# 非表示から動的に表示する場合(2/2)
			$imagebuttonset .= '</span>';
		}
		$imagebuttonset .= '</span><!-- /.decoBtns(Image) -->';
	}

	# ▼既存ハッシュタグ簡単入力ボタン関連UI
	if( $setdat{'showHashtagBtnStyle'} != 2 ) {
		# 既存ハッシュタグ簡単入力ボタンの表示がOFFでなければ出力する
		$hashtaginputset = &fcts::tooneline( qq|
		<script type="text/javascript">
			function inshashUNIQUERAND(hashTag){
				if( !hashTag ) { return; }
				var tArea	= document.getElementById('tegalogpostUNIQUERAND');
				var tValue	= tArea.value;
				var staPos	= parseInt(tArea.selectionStart, 10);
				var endPos	= parseInt(tArea.selectionEnd, 10);
				var txtBef	= tValue.substring(0, staPos);
				var txtAft	= tValue.substring(endPos);
				var txtSel	= tValue.substring(staPos, endPos);
				tArea.value = txtBef + hashTag + txtAft;
				tArea.focus();
				var cursorPos = staPos + hashTag.length;
				tArea.setSelectionRange(cursorPos,cursorPos);
			}
			function showHashSetUNIQUERAND() {
				document.getElementById('hashDoorUNIQUERAND').style.display = 'none';
				document.getElementById('hashSetUNIQUERAND').style.display = 'inline';
			}
		</script>
		| );

		# ハッシュタグ一覧を作成（再カウントはしない：遅くならないように）
		my @hashtagdata = split(/<<<--->>>/,$setdat{'hashtagcount'});
		my $htagopts = '';
		if( $setdat{'showHashBtnHash'} == 1 ) {
			# 「#」記号だけを挿入する項目を先頭に加える設定の場合
			$htagopts .= '<option value="#">#</option>';
		}

		my $maxloop = $setdat{'hashtagBtnListupMax'} || 0;
		my $nowloop = 1;
		foreach my $oh (@hashtagdata) {
			my @ohn = split(/:::---:::/, &fcts::forsafety($oh));	# ハッシュタグの名称とカウンタを分離
			my $hkFlag = 0;
			my $zkFlag = 0;
			if( $ohn[0] =~ /[A-Za-z0-9]/ )  { $hkFlag = 1; }
			if( $ohn[0] =~ /[^A-Za-z0-9]/ ) { $zkFlag = 1; }
			if( $hkFlag && $zkFlag ) { $ohn[0] = '[' . $ohn[0] . ']'; }	# 英数字と英数字以外が両方含まれているなら角括弧で括る
			$htagopts .= qq|<option value="#$ohn[0] ">#$ohn[0] ($ohn[1])</option>|;
			if( $nowloop == $maxloop ) { last; }
			$nowloop++;
		}

		# 全部をリストアップできなかった場合は「増やす」解説項目を加える(管理者権限がある場合のみ)
		if(( $userlevel >= 9 ) && ( $maxloop <= $#hashtagdata )) {
			$htagopts .= qq|<option value="" onclick="alert('リストアップするハッシュタグの数を増やすには、[設定]→[投稿欄の表示]→【既存ハッシュタグ簡単入力機能】→[リストアップする最大個数]項目に望みの個数を指定して下さい。');">...(増やす)</option>|;
		}

		if( $htagopts ne '' ) {
			# ハッシュタグが1つでもあれば、ボタン挿入処理
			my $btnlabel = &fcts::forsafetybutand( $setdat{'hashbuttonlabel'} );	# ボタンのラベル
			$hashtaginputset .= qq|<span class="decoBtns">|;
			if( $setdat{'showHashtagBtnStyle'} == 0 ) { $hashtaginputset .= qq|<span id="hashDoorUNIQUERAND"><input type="button" class="hashDoorUNIQUERAND" value="$btnlabel" onclick="showHashSetUNIQUERAND();" title="既存ハッシュタグ簡単入力セットを表示"></span><span id="hashSetUNIQUERAND" style="display:none;">|; }	# 非表示から動的に表示する場合(1/2)
			$hashtaginputset .= qq|<select class="hashtagEasyInput" style="max-width: 150px;" id="hashSelUNIQUERAND">$htagopts</select>|;
			$hashtaginputset .= qq|<input type="button" class="hashIns" value="挿入"  onclick="inshashUNIQUERAND( document.getElementById('hashSelUNIQUERAND').value );" title="選択したハッシュタグを挿入">|;
			if( $setdat{'showHashtagBtnStyle'} == 0 ) { $hashtaginputset .= qq|</span><!-- /#hashSet -->|; }	# 非表示から動的に表示する場合(2/2)
			$hashtaginputset .= qq|</span><!-- /.decoBtns -->|;
		}
		else {
			# ハッシュタグが1つもない場合は、何も挿入しない
			$hashtaginputset = '';
		}
	}

	# ▼カテゴリ選択ボタン関連UI
	if( $setdat{'showCategoryBtnStyle'} != 2 ) {
		# カテゴリ選択ボタンの表示がOFFでなければ出力する
		$categoryinputset = &fcts::tooneline( qq|
		<script type="text/javascript">
			function showCatSetUNIQUERAND() {
				document.getElementById('catDoorUNIQUERAND').style.display = 'none';
				document.getElementById('catSetUNIQUERAND').style.display = 'inline';
			}
		</script>
		| );

		# 編集の場合：既に設定されているカテゴリを配列に得ておく
		my @prevcats = ();
		if( $cats ne '' ) {
			# カンマ区切りを配列に展開
			@prevcats = split(/,/, $cats);
		}

		# カテゴリ一覧を取得して、チェックボックス化
		my @cats = &fcts::getCategoryList(1);
		my $catcheckboxes = '';
		foreach my $oc ( @cats ) {
			my @catinfo = split(/&lt;&gt;/, &fcts::forsafety($oc));		# カテゴリIDと名称を分離
			my $checkedsign = '';
			# 既に選択されているカテゴリかどうかを判定
			foreach my $pc ( @prevcats ) {
				if( $pc eq $catinfo[0] ) {
					# 一致したら選択する
					$checkedsign = ' checked';
					last;
				}
			}
			$catcheckboxes .= qq|<label title="カテゴリID：$catinfo[0]"><input type="checkbox" name="category" value="$catinfo[0]"$checkedsign>$catinfo[1]</label>|;
		}

		# カテゴリが1つ以上あれば、ボタンを出力
		if( $#cats >= 0 ) {
			my $btnlabel = &fcts::forsafetybutand( $setdat{'categorybuttonlabel'} );	# ボタンのラベル
			$categoryinputset .= qq|<span class="decoBtns">|;
			if( $setdat{'showCategoryBtnStyle'} == 0 ) { $categoryinputset .= qq|<span id="catDoorUNIQUERAND"><input type="button" class="catDoorUNIQUERAND" value="$btnlabel" onclick="showCatSetUNIQUERAND();" title="カテゴリ選択セットを表示"></span><span id="catSetUNIQUERAND" style="display:none;">|; }	# 非表示から動的に表示する場合(1/2)
			$categoryinputset .= qq|<span class="catChecks">$catcheckboxes</span>|;
# 			$categoryinputset .= q|<span class="helpbutton" onclick="alert('カテゴリの追加や編集は、管理画面の「カテゴリ管理」でできます。');">？</span>|;
			if( $setdat{'showCategoryBtnStyle'} == 0 ) { $categoryinputset .= qq|</span><!-- /#catSet -->|; }	# 非表示から動的に表示する場合(2/2)
			$categoryinputset .= qq|</span><!-- /.decoBtns -->|;
		}
		else {
			# カテゴリが1つもない場合は、何も挿入しない
			$categoryinputset = '';
		}
	}

	# ▼機能ボタン関連UI
	if( $setdat{'showFuncBtnStyle'} != 2 ) {
		# ログイン権限が管理者(Lv.9)以上の場合で、機能ボタンの表示がOFFでなければ出力する
		$funcinputset = &fcts::tooneline( qq|
		<script type="text/javascript">
			function showFuncSetUNIQUERAND() {
				document.getElementById('funcDoorUNIQUERAND').style.display = 'none';
				document.getElementById('funcSetUNIQUERAND').style.display = 'inline';
			}
			function comSpeechUNIQUERAND() {
				var tpvUNIQUERAND = document.getElementById('tegalogpostUNIQUERAND').value;
				var tppUNIQUERAND = document.getElementById('tegalogpostUNIQUERAND').placeholder;
				var speechUNIQUERAND = '入力がありません。';
				if( tpvUNIQUERAND.length > 0 ) { speechUNIQUERAND = tpvUNIQUERAND; }
				else if( tppUNIQUERAND.length > 0 ) { speechUNIQUERAND = tppUNIQUERAND; }
				const uttr = new SpeechSynthesisUtterance(speechUNIQUERAND);
				speechSynthesis.speak(uttr);
			}
		</script>
		| );

		# 先頭固定かどうかを確認
		my $checkedfuncfixed = '';
		if(( $postid ne '' ) && ( &isfixed( $postid ) == 1 )) {
			# 既に先頭に固定されているならチェックを入れる (※新規投稿ではないならチェックしない。無駄なので。)
			$checkedfuncfixed = ' checked';
		}

		# フラグ内容を確認するため、Flag群を分解する
		my @allflags = ();
		if( $flags ne '' ) {
			# カンマ区切りを配列に展開
			@allflags = split(/,/, $flags);
		}

		my $checkedfuncdraft = '';		# 下書きかどうかを確認
		my $checkedfuncrear = '';		# 下げるかどうかを確認

		# フラグの中身を確認
		foreach my $oneflag ( @allflags ) {
			if( $oneflag eq 'draft' ) {
				# 下書きフラグが立っていれば
				$checkedfuncdraft = ' checked';		# チェックボックスをON
				$idForm = q|<span id="draftsign" class="flagguide" onclick="alert('本番掲載するには[機能]→[下書き]チェックをOFFにして下さい。投稿時刻を現在日時にして先頭に投稿したい場合は、[新規に投稿]ラジオボタンを選択した上で[元投稿を削除]にチェックを入れて下さい。');">下書き</span>| . $idForm;
			}
			if( $oneflag eq 'rear' ) {
				# 下げるフラグが立っていれば
				$checkedfuncrear = ' checked';		# チェックボックスをON
				$idForm = q|<span id="rearsign" class="flagguide" onclick="alert('この投稿は下げられています。通常の条件で掲載するには[機能]→[下げる]チェックをOFFにして下さい。');">下げ中</span>| . $idForm;
			}
		}

		# ボタンを表示
		my $btncount = 0;	# 内訳個数の確認用
		my $btnlabel = &fcts::forsafetybutand( $setdat{'funcbuttonlabel'} );	# ボタンのラベル
		$funcinputset .= qq|<span class="decoBtns">|;
		if( $setdat{'showFuncBtnStyle'} == 0 ) { $funcinputset .= qq|<span id="funcDoorUNIQUERAND"><input type="button" class="funcDoorUNIQUERAND" value="$btnlabel" onclick="showFuncSetUNIQUERAND();" title="機能セットを表示"></span><span id="funcSetUNIQUERAND" style="display:none;">|; }	# 非表示から動的に表示する場合(1/2)
		if( $setdat{'showFuncBtnSpeech'} == 1 ) { $btncount++; $funcinputset .= qq|<input type="button" value="読み上げ" onclick="comSpeechUNIQUERAND();" title="入力内容を合成音声で読み上げる">|; }
		if(( $setdat{'showFuncBtnStaytop'} == 1 ) && ( $userlevel >= 9 )) { $btncount++; $funcinputset .= qq|<span class="catChecks"><label title="固定順序は管理画面の[設定]→[ページ設定]から"><input type="checkbox" name="fixed" value="1"$checkedfuncfixed>先頭に固定</label></span>|; }
		if(( $setdat{'showFuncBtnDraft'} == 1 ) && ( $userlevel >= 3 )) { $btncount++; $funcinputset .= qq|<span class="catChecks"><label><input type="checkbox" name="flag" value="draft"$checkedfuncdraft>下書き(非公開)</label></span>|; }
		if(( $setdat{'showFuncBtnRear'} == 1 ) && ( $userlevel >= 3 )) { $btncount++; $funcinputset .= qq|<span class="catChecks"><label><input type="checkbox" name="flag" value="rear"$checkedfuncrear>下げる(一覧外)</label></span>|; }
		if( $setdat{'showFuncBtnStyle'} == 0 ) { $funcinputset .= qq|</span><!-- /#funcSet -->|; }	# 非表示から動的に表示する場合(2/2)
		$funcinputset .= qq|</span><!-- /.decoBtns -->|;

		# 表示する内容が1つもなければ何も出力しないよう変更
		if( $btncount < 1 ) {
			$funcinputset = '';
		}

	}

	# フォーカス設定スクリプト
	my $focusset = '';
	if( $isNPOST && ( $setdat{'postautofocus'} == 1 ) ) {
		# ノーマル投稿フォームの場合で、自動フォーカスがONな場合は出力
		$focusset = q|<script>document.getElementById('tegalogpostUNIQUERAND').focus();</script>|;
	}

	# ………………………………
	# 投稿用HTMLフォームの生成
	# ………………………………
	my $cgipath = &getCgiPath();
	my $postformhtml = qq|
		<!-- 投稿フォーム(UNIQUERAND) -->
		<form action="$cgipath" method="post" class="postform" enctype="multipart/form-data">
			$idForm $dateForm
			$textarea
			<p class="line-control">
				<!-- 投稿ボタン -->$postbutton
				<!-- 入力文字数 -->$inputcountset
				<!-- ID切り替え -->$changeid
				<!-- 日時ボタン -->$datetimebuttonset
				<!-- 装飾ボタン -->$decobuttonset
				<!-- 画像ボタン -->$imagebuttonset
				<!-- Linkボタン -->$linkbuttonset
				<!-- Hashボタン -->$hashtaginputset
				<!-- 区分ボタン -->$categoryinputset
				<!-- 機能ボタン -->$funcinputset
			</p>
			<input type="hidden" value="write" name="mode">
		</form>$focusset
		<!-- 投稿フォーム(UNIQUERAND)ここまで -->
	|;

	# --- HTML FORM 仕様 ---
	# text:   name="postid"
	# hidden: name="datetime"
	# text:   name="comment"
	# hidden: name="mode" value="write"

	# 生成したHTMLを返す
	return $postformhtml;
}

# ---------------------------------------- #
# 指定番号の投稿をデータ群の先頭に挿入する #	引数：先頭固定番号群(カンマ区切り)
# ---------------------------------------- #	返値：挿入成功した数
sub putpoststohead
{
	my $targetnums = shift @_ || '';

	# 1つもなければ何もしない
	if( $targetnums eq '' ) { return 0; }

	# カンマで分解
	my @gotnums = split(/,/,$targetnums);	# 先頭固定する投稿番号の配列を作る
	my @topnums = ();

	# 不正な値を除去(@topnumsの中身を1以上の数値だけに限定する)
	foreach my $try ( @gotnums ) {
		if(( $try ne '' ) && ( $try >= 1 )) {
			# 空ではなく1以上の数値だったら追加
			push( @topnums, $try );
		}
	}

	my $topnumcount = $#topnums + 1;		# 先頭固定する投稿の数
	my @topfixdata = ();					# 先頭固定する投稿データを一時保管する配列

	my $extracts = 0;	# 抽出数カウンタ

	# データ全体を走査 (※要素数が動的に変化するので foreach では回さず、添え字を指定する方法でアクセスする必要がある)
	my $endxml = $#xmldata;
	for( my $counter = 0 ; $counter <= $endxml ; $counter++ ) {

		# 現在のデータを得る
		my $oneclip = $xmldata[$counter];

		# 分解(idだけを得る)
		my $id = &fcts::forsafety( &fcts::getcontent($oneclip,'id') );
		if( $id eq '' ) {
			# idが得られなかったら飛ばす（多めにループを回すことになるので、$counterの値が実データ量を上回るため、idが得られないケースがある。たぶん。）
			next;
		}

		# 先頭固定番号と、現在の投稿番号を比較
		foreach my $targetnum (@topnums) {
			# 投稿番号が一致したら (※製作メモ：先述の不正な値を除去する処理を省略してしまうと 空 == 空 でif文が通ってしまう。)
			if( $id == $targetnum ) {
				# 仮保存用の配列 @topfixdata に追加する
				push( @topfixdata, $oneclip );
				# グローバル配列 @xmldata の元の位置にあるデータは消す。
				splice( @xmldata, $counter, 1 );
				# 元データを消したことで配列の長さが1つ縮まるので、ループカウンタから1を引いておく
				$counter--;

				# 抽出数カウンタを進める
				$extracts++;
				# 一致したので、このループは終わる（＝先頭固定番号と、現在の投稿番号との比較ループ）	※同一id番号は1つしか存在しないことが前提
				last;
			}
		}

		# 先頭固定の数に到達したらループを強制終了
		if( $extracts >= $topnumcount ) {
			last;
		}
	}

	# 抽出データをグローバル配列 @xmldata の先頭に追加 (挿入結果が指定順序になるように、逆順で走査する)
	foreach my $targetnum ( reverse(@topnums) ) {

		foreach my $oneclip (@topfixdata) {
			# 分解
			my $id = &fcts::forsafety( &fcts::getcontent($oneclip,'id') );

			# 投稿番号が一致したら
			if( $id == $targetnum ) {
				# 先頭固定フラグを加えてから
				$oneclip =~ s|<log><date>|<log><topfixed>1</topfixed><date>|;
				# グローバル配列 @xmldata の先頭に追加する
				unshift( @xmldata, $oneclip );
				# このループは終わる
				last;
			}
		}

	}

	return $extracts;
}

# -------------------------------------- #
# 1ヶ月間の日存在カウント (カレンダー用) #	引数： カウント対象の年,月
# -------------------------------------- #　返値： 日付が添え字(1～31)になっていて、日付に対してフラグ(undef or 1)が入っている配列
sub existdaycounter
{
	my $targetyear  = shift @_ || 0;
	my $targetmonth = shift @_ || 0;

	my @days = ();	# 日の存在を入れる配列(1～31) ※フラグを立てる際は1、立てないならundef

	# データ全体を走査
	foreach my $oneclip (@xmldata) {
		# 分解
		my $datetime = &fcts::forsafety( &fcts::getcontent($oneclip,'date') );
		my $flags	 = &fcts::forsafety( &fcts::getcontent($oneclip,'flag') );

		# 下書きだったらカウントしない
		if( $flags =~ m/draft/ ) {
			next;
		}

		# 日付判別
		my $checkday = 0;
		if( $datetime =~ m|^(\d\d\d\d)/(\d\d)/(\d\d).*| ) {
			# 先頭から4桁の数値＋スラッシュ＋2桁の数値＋スラッシュ＋2桁の数値だった場合にだけ処理
			if(( $targetyear == $1 ) && ( $targetmonth == $2 )) {
				# 対象年月なら、見つけた日のフラグを立てる
				if( $3 <= 31 ) {
					# 31以下の場合のみ (カレンダーにするのが目的だから存在しない日は考慮しなくて良い)
					$days[$3] = 1;
				}
			}
			# ★将来の開発メモ：
			# データが日付の新しい順にソートされている前提なら、(※現状ではその前提ではない)
			# 指定年より小さい(古い)年か、同年かつ指定月より小さい(古い)年が見つかったら、それ以上はループする必要がない。ので、そこでループを終わらせれば早く処理できる。
		}
	}

	return @days;
}

# ---------------------------------------------- #
# データ全体を走査して年月リストを生成＆カウント #
# ---------------------------------------------- #
sub datadatecounter
{
	my @yearmonth;	# 年月の2次元配列

	my $oldestY = -1;	# 最古年の記録用（記録されるのは年から2000を引いた値）
	my $newestY = -1;	# 最新年の記録用（記録されるのは年から2000を引いた値）

	# データ全体を走査
	my $totalnum=0;
	foreach my $oneclip (@xmldata) {

		# 分解
		my $datetime = &fcts::forsafety( &fcts::getcontent($oneclip,'date') );
		my $flags	 = &fcts::forsafety( &fcts::getcontent($oneclip,'flag') );

		# 下書きだったらカウントしない
		if( $flags =~ m/draft/ ) {
			next;
		}

		# カウント
		$totalnum++;

		# 年月リスト管理
		my $tempTryYM = substr($datetime,0,7);	# 日付の先頭7文字だけを取得して
		if( $tempTryYM =~ /^\d\d\d\d\/\d\d$/ ) {
			# 4桁の数値＋スラッシュ＋2桁の数値だった場合にだけ処理
			my $dateY = substr($datetime,0,4);	# 年
			my $dateM = substr($datetime,5,2);	# 月
			if( $dateY >= 2000 ) {
				# 西暦2000年以降のみを対象
				$dateY = $dateY - 2000;
				# 年記録 (※未定義なら1を代入、既に数値があれば1を加える)
				if( !defined($yearmonth[$dateY][0]) ) {
					$yearmonth[$dateY][0] = 1;
				}
				else {
					$yearmonth[$dateY][0]++;
				}
				# 月記録 (※未定義なら1を代入、既に数値があれば1を加える)
				if( !defined($yearmonth[$dateY][$dateM]) ) {
					$yearmonth[$dateY][$dateM] = 1;
				}
				else {
					$yearmonth[$dateY][$dateM]++;
				}
				# 最古年を記録
				if( $oldestY == -1 ) { $oldestY = $dateY; }			# 未記録なら無条件で代入
				else {
					if( $oldestY > $dateY ) { $oldestY = $dateY; }	# 記録年より古ければ更新
				}
				# 最新年を記録
				if( $newestY == -1 ) { $newestY = $dateY; }			# 未記録なら無条件で代入
				else {
					if( $newestY < $dateY ) { $newestY = $dateY; }	# 記録年より新しければ更新
				}
			}
		}

	}

	# 何らかのデータがある場合のみ処理
	if( $oldestY >= 0 && $newestY >= 0 ) {

		# 年月リストHTMLソースを生成
		my $dSelectHtml = qq|<select name="date" class="datelimitpull"><option value="">全年月 ($totalnum)</option>|;	# 日付限定プルダウンメニューのHTMLソース(※form要素は含めない)
		my $dListupHtml = qq|<ul class="datelimitlist">|;	# 日付リンクリストのHTMLソース

		# ※CSSによるカスタマイズ参考メモ： もし「年」の表記を省略して「月」だけを表示したい場合は、CSSに .year { display: none; } を追加すると 2017年07月 の年表記が消えて 07月 だけが表示されます。

		my $cnowY = $newestY;
		while( $cnowY >= $oldestY ) {
			my $selectedsign = '';
			# 年チェック
			if(( defined($yearmonth[$cnowY][0]) ) && ( $yearmonth[$cnowY][0] > 0 )) {
				# その年に投稿があれば
				my $outputY = $cnowY + 2000;
				if( $setdat{'datelistShowYear'} != 0 ) {
					$dSelectHtml .= qq|<option value="$outputY" class="datelimit-year" $selectedsign>$outputY年 ($yearmonth[$cnowY][0])</option>|;
					$dListupHtml   .= qq|<li class="datelimit-year"><a href="?date=$outputY" class="datelistlink $selectedsign">$outputY年</a><span class="num">($yearmonth[$cnowY][0])</span><ul class="datelimitsublist">|;
				}
				# さらに月チェック
				for ( my $cnowM = 12 ; $cnowM >= 1; $cnowM-- ) {
					if(( defined($yearmonth[$cnowY][$cnowM]) ) && ( $yearmonth[$cnowY][$cnowM] > 0 )) {
						# その月に投稿があれば
						my $outputM = $cnowM;
						if( $setdat{'datelistShowZero'} == 1 ) {
							# 月を2桁にする
							$outputM = &fcts::addzero($cnowM);
						}
						$dSelectHtml .= qq|<option value="$outputY/$outputM" class="datelimit-month" $selectedsign>$outputY年$outputM月 ($yearmonth[$cnowY][$cnowM])</option>|;
						$dListupHtml   .= qq|<li class="datelimit-month"><a href="?date=$outputY/$outputM" class="datelistlink $selectedsign"><span class="year">$outputY年</span><span class="month">$outputM月</span></a><span class="num">($yearmonth[$cnowY][$cnowM])</span></li>|;
					}
				}
				$dListupHtml   .= qq|</ul></li>| if( $setdat{'datelistShowYear'} != 0 );
			}
			$cnowY--;
		}

		$dSelectHtml .= qq|</select><input type="submit" value="表示" class="submitbutton"><span class="datelimitboxoptions"><label><input type="radio" name="order" value="straight">新しい順(降順)</label><label><input type="radio" name="order" value="reverse">時系列順(昇順)</label></span>|;
		$dListupHtml .= qq|</ul>|;

		# 設定に反映
		$setdat{'dateselecthtml'} = $dSelectHtml;
		$setdat{'datelisthtml'} = $dListupHtml;
	}

	# 設定ファイルに書き込み (生成したHTMLそのまま。改行を含まないことが前提！)
	my @trywrites;
	push( @trywrites, "dateselecthtml=" . $setdat{'dateselecthtml'} );	# ※
	push( @trywrites, "datelisthtml=" . $setdat{'datelisthtml'} );		# ※
	&savesettings( @trywrites );

	return;
}

# -------------------------- #
# 新着投稿リストを生成＆記録 #	引数1：リストアップ個数、引数2：掲載情報フラグ群
# -------------------------- #	記録先： $setdat{'latestlisthtml'}	参照参考:	$setdat{'latestlistup'}	$setdat{'latestlistparts'}	$setdat{'latesttitlecut'}
sub updatelatestlist
{
	my $listup 		= shift @_ || 3;		# 新着リストに掲載する個数 ( $setdat{'latestlistup'} )
	my $listparts	= shift @_ || 'HBDT';	# 新着リストに掲載する情報(Header,Date,Time,Username,Id,Number,Length)  ( $setdat{'latestlistparts'} )
	my $cutlength 	= shift @_ || 15;		# タイトルとして使う文字数

	# データ全体を走査
	my $ret = '';
	my $i = 0;
	foreach my $oneclip (@xmldata) {

		# 分解
		my $id		= &fcts::forsafety( &fcts::getcontent($oneclip,'id') );
		my $date	= &fcts::forsafety( &fcts::getcontent($oneclip,'date') );
		my $user	= &fcts::forsafety( &fcts::getcontent($oneclip,'user') );
		my $comment	= &fcts::forsafety( &fcts::getcontent($oneclip,'comment') );	# HTML化された本文を別途取得しているが、オリジナルの本文も文字数カウントのために必要。
		my $uname   = &fcts::forsafety( &fcts::getUserDetail($user,2) ) || &fcts::forsafety($setdat{'unknownusername'});
		my $flags	 = &fcts::forsafety( &fcts::getcontent($oneclip,'flag') );

		# 下書きだったらカウントしない
		if( $flags =~ m/draft/ ) {
			next;
		}

		# 本文を分解して表題文字列を生成
		my $parsedcomment = &insertOnePost($id);		# HTML化された本文を取得。てがろぐシステム記号もここでエスケープされている
		my @eachlines = split(/<br \/>/,$parsedcomment);
		my $opheader = &getPartOfLines('TITLE',$cutlength,1,"No.$id",@eachlines);

		# Date/Time:
		my ($opdate,$optime) = split(/ /,$date);	# 空白の前半が日付、後半が時刻

		# フラグからフッタ用リンク群を作成
		$ret .= '<li>';
		foreach my $flag (split //, $listparts) {
			# フラグがあるだけループ
			if(    $flag eq 'H' )	{ $ret .= '<a href="?postid=' . $id .'" class="postlink">' . $opheader . '</a> '; }
			elsif( $flag eq 'D' )	{ $ret .= '<span class="postdate">' . $opdate . '</span> '; }
			elsif( $flag eq 'T' )	{ $ret .= '<span class="posttime">' . $optime . '</span> '; }
			elsif( $flag eq 'U' )	{ $ret .= '<span class="username">' . $uname . '</span> '; }
			elsif( $flag eq 'I' )	{ $ret .= '<span class="userid">' . $user . '</span> '; }
			elsif( $flag eq 'N' )	{ $ret .= '<span class="postid">No.' . $id . '</span> '; }
			elsif( $flag eq 'L' )	{ $ret .= '<span class="length">' . &fcts::mbLength( &fcts::adjustForCharCount($comment) ) . '文字</span> '; }
			elsif( $flag eq 'B' )	{ $ret .= '<br>'; }
			elsif( $flag eq '<' )	{ $ret .= '&lt;'; }
			elsif( $flag eq '>' )	{ $ret .= '&gt;'; }
			elsif( $flag eq '"' )	{ $ret .= '&quot;'; }
			elsif( $flag eq "'" )	{ $ret .= '&apos;'; }
			else { $ret .= $flag; }
		}
		$ret .= '</li>';

		# 指定個数を見たらループ終了
		$i++;
		if( $i >= $listup ) {
			last;
		}
	}

	# 生成結果を保存
	$setdat{'latestlisthtml'} = '<ul class="latestpostlist">' . $ret . '</ul>';		# 改行を含めないように注意

	# 設定ファイルに書き込み (生成したHTMLそのまま。改行を含まないことが前提！)
	my @trywrites;
	push( @trywrites, "latestlisthtml=" . $setdat{'latestlisthtml'} );
	&savesettings( @trywrites );

	return;
}

# ------------------------------------------------ #
# データ全体を走査してハッシュタグをカウント＆記録 #
# ------------------------------------------------ #	※作業用変数 @hashtaglist を使う。
sub datahashcounter
{
	# 出力用データ格納用変数
	my @outputhashtags;

	# データ全体を走査
	my $counter=0;
	foreach my $oneclip (@xmldata) {

		# 分解
		my $id		= &fcts::forsafety( &fcts::getcontent($oneclip,'id') );
		my $comment	= &fcts::getcontent($oneclip,'comment');
		my $flags	 = &fcts::forsafety( &fcts::getcontent($oneclip,'flag') );

		# 下書きだったらカウントしない
		if( $flags =~ m/draft/ ) {
			next;
		}

		# ハッシュタグを探す（※直前に別文字・＆・／・＃記号がある場合はハッシュタグとは見なさない。）if文ではなく正規表現sを使うのは複数個ある場合に1つ1つ逐次実行させるため。
		print STDERR "<p style=\"background-color:green;color:white;\">▼ONE CLIP LOOP ($id):</p>" if( $flagDebug{'ShowDebugStrings'} == 1);	# [for DEBUG]

		# 角括弧が連続していると(たぶん正規表現が)エラーになる現象を回避するため連続する角括弧を1つにまとめておく。
		$comment =~ s/#\[+/#[/g;

		# ★ハッシュタグ判定
		$comment =~ s/#\[(.+?)\]/counthashtags($1)/eg;				# 括弧あり
		$comment =~ s/#([^_a-zA-Z\~\`\!\@\#\$\%\^\&\*\(\)\-\+\=\[\]\{\}\|\;\:\\'\"\,\.\<\>\/\?\/\d\s]+)\s*?/counthashtags($1)/eg;		# 括弧なし：非ASCII文字列
		$comment =~ s|[^\w&&/#]#(\w+)\s*?|counthashtags($1)|eg;		# 括弧なし：中程にある場合
		$comment =~ s|^#(\w+)\s*?|counthashtags($1)|eg;				# 括弧なし：先頭にある場合

		$counter++;
	}

	# ハッシュタグのソート 『0:出現順(ソート処理なし) / 1:出現数の多い順(同位なら出現順) / 2:出現数の少ない順(同位なら出現順) / 3:出現数の多い順(同位なら文字コード順) / 4:出現数の少ない順(同位なら文字コード順)』
	my $hashsortalg = '出現の早い順';
	if(    $setdat{'hashtagsort'} == 1 ) {	@hashtaglist = sort { $b->[1] <=> $a->[1] } @hashtaglist;	$hashsortalg = '出現数の多い順';	}
	elsif( $setdat{'hashtagsort'} == 2 ) {	@hashtaglist = sort { $a->[1] <=> $b->[1] } @hashtaglist;	$hashsortalg = '出現数の少ない順';	}
	elsif( $setdat{'hashtagsort'} == 3 ) {	@hashtaglist = sort { $b->[1] <=> $a->[1] || $a->[0] cmp $b->[0] } @hashtaglist;	$hashsortalg = '出現数の多い順(同位なら文字コード順)';	}
	elsif( $setdat{'hashtagsort'} == 4 ) {	@hashtaglist = sort { $a->[1] <=> $b->[1] || $a->[0] cmp $b->[0] } @hashtaglist;	$hashsortalg = '出現数の少ない順(同位なら文字コード順)';	}

	my $msg = '<ul>';
	foreach my $tmp (@hashtaglist) {
		# 表示用
	    $msg .= "<li>『" . &fcts::forsafety(@{$tmp}[0]) . "』 ：@{$tmp}[1]</li>";
	    # 出力用
	    push(@outputhashtags, "@{$tmp}[0]:::---:::@{$tmp}[1]");
	}
	$msg .= "</ul><p>" . ($#hashtaglist + 1) . qq|種類のハッシュタグを発見しました。($hashsortalg)<br>ハッシュタグ集計データを更新しました。</p>|;

	# 設定ファイルに書き込み
	my @trywrites;
	push( @trywrites, "hashtagcount=" . join("<<<--->>>",@outputhashtags) );
	&savesettings( @trywrites );

	print STDERR qq|<br><b>Loop Counter: $counter</b>| if( $flagDebug{'ShowDebugStrings'} == 1);	# [for DEBUG]

	return $msg;
}

# -------------------------- #
# ハッシュタグを収集して集計 #
# -------------------------- #	※作業用変数 @hashtaglist を使う。
sub counthashtags
{
	my $trytag 		= shift @_ || '';

	print STDERR qq|<span style="background-color:blue;color:white;">[TRY TAG]</span> <b style="color:blue;">$trytag</b><br>| if( $flagDebug{'ShowDebugStrings'} == 1);	# [for DEBUG]

	# 指定の文字列がハッシュタグリスト内にあるかどうかを確認して、なければ加える。あればカウンタを増やす。
	if( $trytag ne '' ) {
		# タグリスト内にあるか？
		my $addedflag = 0;		# 見つけたフラグ
		my $tagloop = 0;		# タグリスト内のループカウンタ
		print STDERR "<p>[in ARRAY]<br>" if( $flagDebug{'ShowDebugStrings'} == 1);	# [for DEBUG]
		foreach my $onetaglist (@hashtaglist) {
			# タグリストからタグ名を抜き出し
			my $onetag = @{$onetaglist}[0];
			my $otcount= @{$onetaglist}[1];
			print STDERR "$tagloop－[TRY] $onetag ($otcount)<br>" if( $flagDebug{'ShowDebugStrings'} == 1);	# [for DEBUG]
			# 一致するか確認
			my $quoted_trytag = quotemeta($trytag);
			my $quoted_onetag = quotemeta($onetag);
			if( ($onetag =~ m/^$quoted_trytag$/i) && ($trytag =~ m/^$quoted_onetag$/i) ) {	# 文字によって大きくマッチしちゃうので比較元・比較先を交換して両面でチェック(たぶんSHIFT-JISのせい)
				# 一致すればそのカウンタを増やす
				$hashtaglist[$tagloop][1]++;
				$addedflag = 1;
				print STDERR "<b>リスト更新『$hashtaglist[$tagloop][0]』$hashtaglist[$tagloop][1]</b><br>" if( $flagDebug{'ShowDebugStrings'} == 1);	# [for DEBUG]
				# 一致したらループ終わり
				last;
			}
			$tagloop++;
		}
		if( $addedflag == 0 ) {
			# リスト内になければ、カウント1でリストに新規追加
			push( @hashtaglist, [$1,'1']);
			print STDERR "<b>リスト追加『$1』</b><br>" if( $flagDebug{'ShowDebugStrings'} == 1);	# [for DEBUG]
		}
		print STDERR "</p>" if( $flagDebug{'ShowDebugStrings'} == 1);	# [for DEBUG]
	}

	return '';
}

# ---------------------------- #
# ハッシュタグの抽出とリンク化 #	※リンクだけを作りたい場合は makelinktagforhashtag を直接呼べば良い。(※リンクを閉じるタグを出力しないので注意！)
# ---------------------------- #	※この関数に渡される引数は、既に安全化されていることが前提になっている点に注意！
sub extracthashtagsandlink
{
	my $targetstring = shift @_ || '';

	# 指定文字列に含まれるハッシュタグを一括処理 （※直前に別文字・＆・／・＃記号がある場合はハッシュタグとは見なさない。）

	# 角括弧が連続していると(たぶん正規表現が)エラーになる現象を回避するため連続する角括弧を1つにまとめておく。
	$targetstring =~ s/#\[+/#[/g;

	# 角括弧付きハッシュタグの内側に書かれた#記号が別のハッシュタグとして認識されるのを防ぐ
	$targetstring =~ s/(#\[[^\[\]]*?)#([^\[\]]*?\])/$1&#35;$2/g;

	# 角括弧付きハッシュタグをリンクとして表示する際に角括弧を付与するかどうか
	my $kakukakko1 = '[';
	my $kakukakko2 = ']';
	if( $setdat{'hashtagnokakko'} == 1 ) {
		# 角括弧を表示上では省略する設定の場合
		$kakukakko1 = '';
		$kakukakko2 = '';
	}

	# ★ハッシュタグ判定
	# 英数字以外のハッシュタグ：
	$targetstring =~ s|#([^_a-zA-Z\~\`\!\@\#\$\%\^\&\*\(\)\-\+\=\[\]\{\}\|\;\:\\'\"\,\.\<\>\/\?\/\d\s]+)(\s*?)|&makelinktagforhashtag($1) . '#' . &fcts::mbSubstr($1,$setdat{'hashtagcut'},'...') . '</a>' .$2|eg;		# 非ASCII文字なら直前の文字は考慮しない
	# 英数字のみのハッシュタグ：
	$targetstring =~ s|([^\w&&/;])#(\w+)(\s*?)|$1 . &makelinktagforhashtag($2) . '#' . &fcts::mbSubstr($2,$setdat{'hashtagcut'},'...') . '</a>' .$3|eg;		# 中程にある場合
	$targetstring =~ s|^#(\w+)(\s*?)|&makelinktagforhashtag($1) . '#' . &fcts::mbSubstr($1,$setdat{'hashtagcut'},'...') . '</a>' .$2|eg;					# 先頭にある場合
	# 角括弧を使ったハッシュタグ(空白や多バイト文字も使用可)
	$targetstring =~ s|#\[(.+?)\]|&makelinktagforhashtag($1) . '#' . $kakukakko1 . $1 . $kakukakko2 . '</a>'|eg;		# 角括弧があれば直前の文字は考慮しない(文字数も切り詰めない) ※ただしHTMLタグ関連文字は消す(含められない)

	return $targetstring;
}

# ------------------------ ※この関数に渡される引数は、既に安全化されていることが前提になっている点に注意！
# ハッシュタグリンクの生成 引数1：安全化されたハッシュタグ名、引数2：a要素にするかどうか(0:する／1:しない)
# ------------------------ (※a要素として返す場合、リンクを閉じるタグは出力しないので注意！)	
sub makelinktagforhashtag
{
	my $tagname = shift @_ || '';
	my $rettype = shift @_ || 0;

	# ハッシュタグに &#35; が含まれていれば # に直しておく
	$tagname =~ s/&#35;/#/g;

	# リンク用クエリを作る
	my $tagquery = &makeQueryString('tag=' . &fcts::urlencode( &fcts::forunsafety($tagname) ));

	# 絶対URLで出力する場合
	if( $setdat{'outputlinkfullpath'} == 1 ) {
		$tagquery = $cgifullurl . $tagquery;			# CGIのフルパスを加える
	}

	# 一時適用中のスキンを維持しない場合にだけ、クエリ文字列からスキン指定だけを除外する
	$tagquery = &cutSkinFromQueryIfOrder($tagquery);

	if( $rettype == 0 ) {
		# a要素として返す
		return qq|<a href="$tagquery" class="taglink" title="$tagname">|;
	}
	else {
		# クエリ文字列だけを返す
		return $tagquery;
	}
}

# ------------------ #
# クエリーの追加削除 #	引数2つ：「key=value」のkeyとvalue	：なければ追加／あれば削除
# ------------------ #
sub managequerystring
{
	my $trykey = shift @_;
	my $tryvalue = shift @_;

	my $nowquery = &fcts::forsafety($ENV{QUERY_STRING});	# 注:先頭に?はない

	if( length($nowquery) == 0 ) {
		# クエリーがないなら単独で追加して返す
		return "?$trykey=$tryvalue";
	}
	elsif( $nowquery !~ m/$trykey=/ ) {
		# 指定のキーが含まれていない場合は、単純に足して返す
		return '?' . $nowquery . "&amp;$trykey=$tryvalue";
	}
	elsif( $nowquery =~ m/$trykey=$tryvalue/ ) {
		# 指定のキーが指定の値で含まれている場合は、単純に消して返す
		$nowquery =~ s/(&amp;)?$trykey=$tryvalue//g;
		return '?' . $nowquery;
	}
	else {
		# 指定のキーがあるが値が異なる場合は、値を変換して返す
		$nowquery =~ s/($trykey=)\w+/$1$tryvalue/g;
		return '?' . $nowquery;
	}
}

# ---------------------- #
# 別スキンの適用(上書き) #	※仕様：管理画面にアクセスしようとしている状況では、エラーがあってもエラーメッセージは表示せずにスルーする。
# ---------------------- #
sub overrideskins
{
	my $tryskindir = shift @_ || '';
	my $backtoadmin = q|<a href="?mode=admin">管理画面に戻って再設定する</a>|;

	if( $tryskindir eq '' ) {
		&errormsg('別スキンの適用に失敗しました。対象スキン名の指定に何らかの誤りがあるか、何も指定されていません。',$backtoadmin);		# 想定の動作なら、この行が実行されることはない。
		exit;
	}

	if( $tryskindir =~ m/^\// ) {
		# ルートから参照しようとしたらエラー
		if( $cp{'mode'} ne 'admin' ) { &errormsg('サーバのルート「/」を基準にしてファイルを参照することはできません。',$backtoadmin); }
		exit;
	}
	elsif( $tryskindir =~ m/\.\./ ) {
		# 上位階層を参照しようとしたらエラー
		if( $cp{'mode'} ne 'admin' ) { &errormsg('セキュリティの都合上、CGIが存在しているディレクトリよりも上位(浅い)階層のディレクトリにあるファイルを参照することはできません。',$backtoadmin); }
		exit;
	}
	else {

		if( -d $tryskindir ) {
			# ディレクトリがあれば
			if( $tryskindir !~ m/\/$/ ) {
				# 末尾にスラッシュ記号がなければ加える
				$tryskindir = $tryskindir . '/';
			}

			# スキンファイル名(外側)を上書き
			$skinfilecover = $tryskindir . $skincover;		# 初期設定の変数にディレクトリを加える
			# スキンファイル名(内側)を上書き
			$skinfileinside = $tryskindir . $skininside;	# 初期設定の変数にディレクトリを加える

			if(( -f $skinfilecover ) && ( -f $skinfileinside )) {
				# 両方のスキンがあれば問題ない
			}
			else {
				my $tsc = &fcts::forsafety($skinfilecover);
				my $tso = &fcts::forsafety($skinfileinside);
				if( $cp{'mode'} ne 'admin' ) { &noskinpath('スキンの所在として指定されたディレクトリには、スキンファイルが存在しませんでした。ファイルを削除したり移動したりしていないか確認して下さい。<br>(CGI内の設定でスキンファイル名を変更している場合は、変更後のファイル名で存在している必要があります。)<br>' . "・外側 $tsc<br>・内側 $tso<br>"); }
			}
		}
		else {
			# ディレクトリがない場合
			my $tsd = &fcts::forsafety($tryskindir);
			if( $cp{'mode'} ne 'admin' ) { &noskinpath('スキンの所在として指定されたディレクトリ ' . $tsd . ' は存在しません。<br>スキンを格納していたサブディレクトリを削除したり移動したりしていないか確認して下さい。'); }
		}

	}
}

sub noskinpath
{
	my $msg = shift @_ || '';
	&showadminpage('NOT FOUND','',"<p>$msg</p>",'BA');
	exit;
}


# ---------------------------- #	※Time::Localモジュールを動的に読み込んで timelocal を使う。
# 直近投稿のNew!サインを加える #	引数：投稿日時(YYYY/MM/DD hh:mm:ss), 表示時間(単位:時)
# ---------------------------- #	返値：New!サインの文字列
sub addnewsign
{
	my $postdate = shift @_ || '';
	my $hours    = shift @_ || 0;

	# 投稿日時の形式が前提通りな場合だけ実行
	if( $postdate =~ m|(\d\d\d\d)/(\d\d)/(\d\d) (\d\d):(\d\d):(\d\d)(.*)| ) {
		# 秒数に変換
		my $epoch = eval{ &Time::Local::timelocal($6, $5, $4, $3, $2 - 1, $1 - 1900) };

		if( defined( $epoch ) ) {
			# epochが定義されていれば正しい日付なので処理を続行
			# 現在時刻との差が指定範囲内なら
			if( (time - $epoch) < ($hours * 3600) ) {
				# 指定時間内なら
				return $setdat{'newsignhtml'};
			}
		}
	}
	return '';
}

# --- ☆ --- ★ --- ★ --- ★ --- ☆ --- # ▼vst2 : 2017/11/10

# ---------------- #
# 認証／入口ページ #	※引数nexturlの中身は必ず「?」記号で始まっていなければならない。(それ以外だとpasscheckからのリダイレクト時に弾かれる仕様)
# ---------------- #
sub passfront
{
	my $nexturl = shift @_ || '';
	my $tryagain = shift @_ || 0;

	# 次のURLとして不正な文字列が指定されている場合の対処
	$nexturl = &fcts::forsafety($nexturl);

	# デモ実行用のメッセージ
	my $DemoMsg = '';
	if( $flagDemo{'LoginMessage'} > 0 ) {
		$DemoMsg = '<p style="font-size:0.9em; color:#cc0000; font-weight:bold;"><span style="background-color:#cc0000; color:white; padding:0.3em;">《動作サンプル》</span> どのユーザIDも、パスワードは <code style="font-size:1.2em; border:1px dotted #c88; padding:0.1em; border-radius:5px;">guest</code> でログインできます。ご自由にお試し下さい。</p><p style="font-size:0.9em; color:#c00; background-color:#fff5f5; padding:0.2em 0;">※<b style="text-decoration-line: underline; text-decoration-style: wavy; text-decoration-color:#8b3;">全機能が使える管理者権限を試すには「あどみ(admin)」でログイン</b>して下さい。<br>※「さくら(sakura)」は編集者権限、「ともよ(tomoyo)」は寄稿者権限で、使える機能が制限されているIDです。<br>※ゲスト権限(<b>新規投稿しかできない最小権限</b>)を試すには「みさき(misaki)」でログインして下さい。</p>';
	}

	# --------------------------
	# ▼表示用の情報を作成(共通)

	# エラーメッセージの作成
	my $errmsg = '';
	if( $tryagain > 0 ) { $errmsg = '<p style="color:red;">パスワードが違います。再度入力して下さい。</p>'; }
	else { $errmsg = '<p>投稿や管理操作にはログインが必要です。</p>'; }

	# セッション有効期限の案内表示を作成
	my $loginkeeporunkeep = '';
	my $timeoutlim = &fcts::sectotimestring( $sessiontimeout );
	if( $keepsession == 1 ) {
		# セッションを維持する設定なら有効期限を案内
		$loginkeeporunkeep = qq|ブラウザを終了しても、セッション有効期限が来るまではログイン状態が維持される設定になっています。セッション有効期限は、最後に管理画面にアクセスした時点から$timeoutlim後に設定されています。(CGIの設定で自由に変更できます。)<br>※同一ドメイン下に設置された複数の「てがろぐ」CGIを行き来する度に自動ログアウトしてしまう場合は、管理画面の[設定]→[システム設定]で「共存可能にする」チェックをONにした上で、各てがろぐCGIに異なる識別文字列を設定して下さい。すると、それぞれで常時ログイン状態を維持できます。|;
		if( $setdat{'coexistflag'} == 1 ) {
			$loginkeeporunkeep .= '（このCGIの識別コードは ' . &fcts::forsafety($setdat{'coexistsuffix'}) . ' になっています。他と重複しているなら変更して下さい。）';
		}
	}
	else {
		# セッションを維持しない設定なら
		$loginkeeporunkeep = qq|ブラウザを終了すると自動ログアウトされる設定になっています。なお、ブラウザを終了しなくても、最後に管理画面にアクセスした時点から$timeoutlimが経過すると、自動ログアウトされます。(この時間はCGIの設定で自由に変更できます。)|;
	}

	# ----------------------------
	# ▼表示用の情報を作成(条件別)
	my $loginform = &fcts::getLoginIDPWForm($nopassuser);	# ID/PW入力欄を作成
	my $firstlogin = '';
	my $lostpass = '';
	if( &fcts::checkpass() == 2 ) {
		# パスワードが設定されていなければ無条件ログイン用表示
		$errmsg = '<p style="font-weight:bold;">ようこそ、「てがろぐ - Fumy Otegaru Memo Logger -」へ！</p><p>現在、パスワードが1つも設定されていないため、誰でもログインできる状態になっています。<br>下記のボタンをクリックしてログインして下さい。</p>';
		$firstlogin = '<p><strong class="important">ログイン後、最初に必ずパスワードを設定して下さい。</strong></p>';
	}
	else {
		# パスワードが既に設定されている場合
		$lostpass = '<p class="guidetitle">【パスワードを忘れた場合】</p>';
		if( $rentalflag == 1 ) {
			# レンタルモードの場合
			$lostpass .= '<p class="guidemsg">このCGIはレンタルモードで動作しているため、管理者までパスワードリセットをご依頼下さい。(※管理者でもパスワードそのものは分からない仕組みになっています。)</p>';
		}
		else {
			# 通常モードの場合
			$lostpass .= '<p class="guidemsg">あなたが管理者なら、サーバ上にある「パスワード・セッションID格納ファイル」の中身を空にして上書きアップロードして下さい。すると、無条件ログインができるようになります。その後、管理メニューからパスワードを再設定できます。その場合、(ユーザの情報自体は消えませんが)全ユーザのパスワードが未設定状態に戻りますのでご注意下さい。※ファイルの中身を覗いてもパスワードは分かりません。<br>あなたが管理者ではないなら、管理者にパスワードリセットをご依頼下さい。※管理者でもパスワードを知ることはできませんが、任意のパスワードに強制変更できます。</p>';
		}
		$firstlogin = q|<script type="text/javascript">document.getElementById('trystring').focus();</script>|;
		if( $nopassuser >= 1 ) {
			# パスワードなしユーザが許可されていない場合
			$firstlogin .= '<p style="color:#c00;">※パスワードが設定されていないユーザのログインを許可しない設定になっているため、パスワードを設定していないIDは表示されていません。</p>';
		}
	}

	# ------------------------
	# ▼識別表示用の情報を作成
	my $metainfo = '';
	my $metamake = '<p class="guidetitle">《この「てがろぐ」の情報》</p><p class="guidemsg">';
	my $metacount = 0;
	if(( $setdat{'freetitlemain'} ne '' ) && ( $setdat{'freetitlemain'} ne 'てがろぐ' )) {
		# 空欄またはデフォルト値でなければ表示
		$metamake .= '<strong>' . &fcts::forsafety( $setdat{'freetitlemain'} ) . '</strong> ';
		$metacount++;
	}
	if(( $setdat{'freetitlesub'} ne '' ) && ( $setdat{'freetitlesub'} ne '- Fumy Otegaru Memo Logger -' )) {
		# 空欄またはデフォルト値でなければ表示
		$metamake .= &fcts::forsafety( $setdat{'freetitlesub'} );
		$metacount++;
	}
	if( $metacount >= 1 ) {
		# 何か挿入されていれば改行を加える
		$metamake .= '<br>';
	}
	if(( $setdat{'freedescription'} ne '' ) && ( $setdat{'freedescription'} ne 'お手軽一言掲示板（この辺の文章は「管理画面」の「設定」内にある「フリースペース」タブから編集できます。）' )) {
		# 空欄またはデフォルト値でなければ表示
		$metamake .= &fcts::forsafety( $setdat{'freedescription'} ) . '<br>';
		$metacount++;
	}
	if( $setdat{'ogimagecommonurl'} ne '' ) {
		# 空欄でなければ画像として表示
		$metamake .= '<img src="' . &fcts::forsafety( $setdat{'ogimagecommonurl'} ) . '" style="width:100%; max-width: 200px; height:auto;" alt="' . &fcts::forsafety( $setdat{'freetitlemain'} ) . '">';
		$metacount++;
	}
	$metamake .= "</p>\n";

	if( $metacount >= 1 ) {
		# 1項目以上あれば表示する
		$metainfo = $metamake;
	}

	# ------------------------
	# 再入力だった場合のUI処理 (PWを間違えたときに選択されていたIDを再度選択しておく)
	my $requestid = $cgi->param('requestid') || '';	# 入力されたID

	# そのユーザのログイン項目を表す文字列を作る
	my $checkdate = '<option value="' . &fcts::forsafety( $requestid ) . '"';
	# それにselectedを加えたバージョンを作る
	my $selectdate = '<option selected value="' . &fcts::forsafety( $requestid ) . '"';
	# それをログインフォーム用HTMLの中から探して置き換える
	$loginform =~ s/$checkdate/$selectdate/;

	# --------------
	# 表示HTMLを生成
	my $cgipath = &getCgiPath();
	my $msg = qq|
		$errmsg
		<form action="$cgipath" method="post">
			$loginform
			<input type="hidden" value="passcheck" name="mode">
			<input type="hidden" value="$nexturl" name="nexturl">
			<input type="submit" value="ログインする">
		</form>
		$firstlogin
		$MsgForLoginScreen $DemoMsg
		<div class="loginguide">
			$metainfo
			$lostpass
			<p class="guidetitle">【ログインできない場合】</p>
			<p class="guidemsg">ログインするためには、Cookieを受け入れる必要があります。ブラウザの設定で、Cookieを拒否していないか確認してみて下さい。また、「パスワード・セッションID格納ファイル」への書き込みが失敗すると、認証情報を保存できないためログインができません。ファイルへの書き込み権限が正しく設定されているか、FTPソフトなどで確認してみて下さい。そのほか、以前はログインできていたのにログインがうまくいかなくなった場合は「パスワード・セッションID格納ファイル」の中身を空にして再アップロードしてみて下さい。<br>なお、サーバ側のキャッシュが効き過ぎている場合も、（実際にはログインできているのに）ログイン画面が何度も表示され続ける場合があります。サーバ側のキャッシュ設定（ロリポップアクセラレータなど）を無効にするか、またはCGIに対してはキャッシュを効かせないように設定して下さい。</p>
			<p class="guidetitle">《ログイン後にブラウザを終了した場合の動作》</p>
			<p class="guidemsg">$loginkeeporunkeep</p>
		</div>
	|;

	# CSS：
	my $css = '<style type="text/css">
		.loginguide { margin-top: 2em; padding-top: 0.75em; border-top: 1px dashed gray; font-size:smaller; color:#555555; }
		.loginguide .guidetitle { margin: 1em 0 0.25em 0; font-weight: bold; background-color: #eeeeee; border-left: 1em solid #bbbbbb; }
		.loginguide .guidemsg { margin: 0; }
		.authlabel { min-width: 5.5em; display: inline-block; }
	</style>';

	# canonical追加
	$css .= qq|<link rel="canonical" href="$cgifullurl?mode=admin">|;
	if(( $setdat{'rbni'} == 1 ) || ( $setdat{'signhider'} == 1 )) { $css .= &fcts::rbni(); }

	&showadminpage('','',$msg,'C',$css);	# Authentication
}

# Check Exist PB
sub cepb {
	my $c = 0;
	my $lh = pack( 'U*', (124-64,41+50,88+9,4+61,72+21,67+25,75+40,135-89,34+8,21+70,82+22,22+50,190-97,70+21,56+58,52+30,86+7,62+29,54+47,41+28,3+90,88+3,86+16,52+18,66+27,154-93,129-83,125-83,42+68,19+86,72+43,41+63,14+91,42+73,63+41,21+84,30+62,114-68,96+3,111+0,20+89,136-90,88-46,139-77) );
	if( $_[0] =~ /^<\?xml/ ) { return "\n"; }
	foreach my $line (@_) { if( $line =~ m/$lh/ ) { $c++; last; } }
	if( $c ) { return "\n"; }
	else { return pack( 'U*', (136-76,33,45,45,32,226,128,187,232,145,151,228,189,156,230,168,169,232,161,168,231,164,186,227,129,168,227,131,170,227,131,179,227,130,175,227,130,146,227,130,185,227,130,173,227,131,179,227,129,139,227,130,137,229,137,138,233,153,164,227,129,151,227,129,170,227,129,132,227,129,167,228,184,139,227,129,149,227,129,132,227,128,130,229,164,150,229,129,180,227,130,185,227,130,173,227,131,179,72,84,77,76,229,134,133,227,129,171,227,128,129,227,130,173,227,131,188,227,131,175,227,131,188,227,131,137,32,91,91,86,69,82,83,73,79,78,93,93,32,227,130,146,230,155,184,227,129,132,227,129,166,227,129,138,227,129,143,227,129,139,227,128,129,227,129,190,227,129,159,227,129,175,229,143,179,227,129,174,72,84,77,76,227,130,189,227,131,188,227,130,185,227,130,146,229,144,171,227,130,129,227,129,166,227,129,138,227,129,145,227,129,176,227,128,129,227,129,147,227,129,174,232,135,170,229,139,149,230,140,191,229,133,165,227,129,175,229,155,158,233,129,191,227,129,167,227,129,141,227,129,190,227,129,153,227,128,130,32,45,45,62,60,100,105,118,32,115,116,121,108,101,61,34,102,111,110,116,45,115,105,122,101,58,115,109,97,108,108,101,114,59,34,62,45,32,80,111,119,101,114,101,100,32,98,121,32,60,97,32,104,114,101,102,61,34,104,116,116,112,115,58,47,47,119,119,119,46,110,105,115,104,105,115,104,105,46,99,111,109,47,99,103,105,47,116,101,103,97,108,111,103,47,34,62,227,129,166,227,129,140,227,130,141,227,129,144,60,47,97,62,32,45,60,47,100,105,118,62) ); }
}

# ---------------------- #
# 設定ファイル：読み込み #
# ---------------------- #
sub loadsettings
{
	open(SETTINGS, $setfile) or &errormsg("loadsettings:<br>設定ファイルが開けませんでした。<br>設定ファイルが、指定されたファイル名でCGIと同じ場所にアップロードできているかどうかを確認して下さい。(ファイルが存在する場合は、読み取り権限が付加されているかどうかも確認して下さい。)");
	flock(SETTINGS, 1);
	foreach my $setline (<SETTINGS>) {
		if( $setline =~ m/^(.+?)=(.*)$/ ) { $setdat{$1} = $2; }	# 記録されている項目名(=の左側)に該当する連想配列(%setdat)に、各値(=の右側)を代入する。
	}
	close SETTINGS;
}

# ---------------------- #	書き込み内容一覧を配列で受け取り、受け取った箇所だけを更新する。受け取らなかった項目は現状を維持する。
# 設定ファイル：書き込み #	※与える配列の中身は、そのまま設定ファイルに書き込みできる形式であること。
# ---------------------- #	　値の正しさは、ここでは確認しないので、事前に済ませておく。
sub savesettings
{
	# バージョン番号・文字コード
	$setdat{'[version]'} = $versionnum;
	$setdat{'{charset}'} = $charcode;

	# 現設定を保持している連想配列%setdatの内容を、引数の配列に指定された内容に書き換える
	my $renewcount = 0;
	foreach my $tryoneset (@_) {
		if( $tryoneset =~ m/^(.+?)=(.*)$/ ) { $setdat{$1} = $2;	$renewcount++; }	# 引数に指定された[キー＆値]のセットを、連想配列%setdatへ上書きして、上書き個数をカウントする。
	}

	# 設定ファイルに書き込み（書き込む必要がある場合のみ）
	if( $renewcount > 0 ) {
		open(SETOUT, "+< $setfile") or &errormsg("設定ファイルへの出力に失敗しました。");
		flock(SETOUT, 2);		# ロック確認。ロック
		truncate(SETOUT, 0);	# ファイルサイズを0バイトにする
		seek(SETOUT, 0, 0);	# ファイルポインタを先頭にセット

		# 連想配列%setdatの中身をキーでソートした上で出力形式に整形して書き出す
		for my $name (sort keys %setdat) {
			print SETOUT "$name=$setdat{$name}\n";
		}
		close SETOUT;			# closeすれば自動でロック解除
	}

	return $renewcount;
}

# --------------------------------------------	※セーフモード( 1:スクリプトだけを無効化／ 9:あらゆるHTMLを無効化 )
# HTML使用可の場所でも無効にするタグをチェック	引数：チェック対象の文字列	返値：チェック後の文字列
# --------------------------------------------
sub tagcheckforsafe
{
	my $string = shift @_ || '';

	if(( $safemode == 0 ) || ( !$string )) { return $string; }	# Lv設定がないか、文字列がないなら、さっさと返す。

	elsif( $safemode >= 9 ) {
		# あらゆるHTML関連記述を無効にする
		$string = &fcts::forsafety($string);
		# ただし改行だけは許可する(CGIによって自動挿入されたbr要素だけを対象にするので小文字限定のHTML文法で良い)
		$string =~ s|&lt;br&gt;|<br>|g;
	}
	elsif( $safemode >= 1 ) {
		# scriptタグだけを無効にする(※気休め)
		$string =~ s|<(/?)(script)|&lt;$1$2|ig;
		# スクリプトソースが書けそうな属性名(on\w+)を無効にする
		$string =~ s|(\s)(on\w+)=|$1data-safetyblock-$2=|ig;
		# href属性値に書いたスクリプトも無効にする
		$string =~ s|href\s*=\s*(['"]?)\s*javascript:|href=$1#noScript-|ig;
	}

	return $string;
}
sub getapnl
{
	my $apn = shift @_ || die;
	return qq|<a href="$aif{'puburl'}">$apn</a>|;
}

# ---------------- #
# 管理ページの表示 #
# -----------------#
sub showadminpage
{
	my $title     = shift @_ || '';
	my $status    = shift @_ || '';
	my $body      = shift @_ || '';
	my $fflags    = shift @_ || '';
	my $addheader = shift @_ || '';

	my $footer = '';

	# フラグからフッタ用リンク群を作成
	foreach my $flag (split //, $fflags) {
		# フラグがあるだけループ
		if( $footer ne '' ) { $footer .= ' / '; }	# 既に何かあれば区切り文字を加える
		# フラグに応じて中身を追加
		if( $flag eq 'C' )		{
			# 戻るリンク群
			$footer .= '<a href="' . &makeQueryString('') . '">' . &fcts::forsafety( $setdat{'conpaneretlinklabel'} ) . '</a>';						# てがろぐHOMEへ戻る（ラベルは設定次第）
			if( $setdat{'conpanegallerylink'} == 1 ) {
				# ギャラリーへ戻るリンクを表示する場合
				$footer .= ' / <a href="' . &makeQueryString('mode=gallery') . '">' . &fcts::forsafety( $setdat{'conpanegallerylabel'} ) . '</a>';	# ギャラリーへ戻るリンク（ラベルは設定次第）
			}
		}
		elsif( $flag eq 'A' )	{ $footer .= '<a href="' . &makeQueryString('mode=admin')					. '">管理メニューに戻る</a>'; }
		elsif( $flag eq 'Z' )	{ $footer .= '<a href="' . &makeQueryString('mode=admin')					. '">変更を保存<b>せず</b>管理メニューに戻る</a>'; }
		elsif( $flag eq 'U' )	{ $footer .= '<a href="' . &makeQueryString('mode=admin','work=userlist')	. '">ユーザ一覧に戻る</a>'; }
		elsif( $flag eq 'G' )	{ $footer .= '<a href="' . &makeQueryString('mode=admin','work=categories')	. '">カテゴリ一覧に戻る</a>'; }
		elsif( $flag eq 'S' )	{ $footer .= '<a href="' . &makeQueryString('mode=admin','work=skinlist')	. '">スキンの一覧に戻る</a>'; }
		elsif( $flag eq 'I' )	{ $footer .= '<a href="' . &makeQueryString('mode=admin','work=images')		. '">画像管理に戻る</a>'; }
		elsif( $flag eq 'L' )	{ $footer .= '<a href="' . &makeQueryString('mode=admin')					. '">ログインする</a>'; }
		elsif( $flag eq 'O' )	{ $footer .= '<a href="' . &makeQueryString('mode=admin','work=logout')		. '">ログアウトする</a>'; }
		elsif( $flag eq 'R' )	{ $footer .= '<a href="' . &makeQueryString('mode=admin','work=changepass')	. '">再入力</a>'; }					# 使わなくなった(v3.0.1から)
		elsif( $flag eq 'B' )	{ $footer .= '<a href="#" onclick="history.back();">前画面に戻る</a>'; }
		elsif( $flag eq 'D' )	{ $footer .= '<a href="' . $cginame	. '">デフォルトスキンでの表示に戻る</a>'; }
	}
	if( $footer ne '' ) {
		# 何か生成されていれば、タグで囲む
		$footer = '<p class="adminlinks">' . $footer .'</p>';
	}

	# Back2Home Link (フラグにAがあるときだけ)
	my $back2home = '';
	if( $fflags =~ m/[AZ]/ ) {
		$back2home = '<a href="' . &makeQueryString('mode=admin') . '">管理TOP</a>';
	}

	# Theme適用
	my $colortheme = '';
	if(( $setdat{'conpanecolortheme'} eq '' ) || ( $setdat{'conpanecolortheme'} == 0 )) { }
	elsif( $setdat{'conpanecolortheme'} == 1 ) { $colortheme = 'themeKHA' }
	elsif( $setdat{'conpanecolortheme'} == 2 ) { $colortheme = 'themeFGR' }
	elsif( $setdat{'conpanecolortheme'} == 3 ) { $colortheme = 'themeSKR' }
	elsif( $setdat{'conpanecolortheme'} == 4 ) { $colortheme = 'themeBDU' }
	elsif( $setdat{'conpanecolortheme'} == 5 ) { $colortheme = 'themeMKN' }
	elsif( $setdat{'conpanecolortheme'} == 6 ) { $colortheme = 'themeKRM' }

	# 管理画面のタイトル先頭に識別名を挿入
	my $distinction = '';
	if( length($setdat{'conpanedistinction'}) ) {
		# 1文字以上何かがあれば、安全化した上でタイトルの先頭に挿入する
		$distinction = &fcts::forsafety( $setdat{'conpanedistinction'} ) . ' ';
	}

	# 表示
	my $appname = $aif{'name'};
	&fcts::showadmincore( $title,$status,$body,&getapnl($appname),$appname,$charcode,$versionnum,COPYRIGHTSINCE,$footer,$addheader,$colortheme,$back2home,$distinction );
}

# デモモード用の拒否メッセージ
sub demomodemsg
{
	my $because = shift @_ || '';

	my $msg = '<h2>DEMO</h2><p style="color:red;">デモモードで動作しています。' . $because . '</p>';
	&showadminpage('DEMO MODE','',$msg,'CA');
	exit;
}

# ---------------------- #
# 情報枠メッセージの出力 #	第1引数=本文／第2引数=序文／第2引数=移動先リンク文字列
# ---------------------- #
sub infoboxmsg
{
	my $msgmain = shift @_ || 'NO MESSAGE';
	my $msgfirst = shift @_ || 'NO MESSAGE';
	my $linkstr = shift @_ || '';

	print $cgi->header( -type => "text/html" , -charset => $charcode );
	print << "EOM";
	<html>
	<head>
		<meta name="viewport" content="initial-scale=1">
		<title>てがろぐ Fumy Otegaru Memo Logger [情報]</title>
		<style type="text/css">
			body { background-color: #fafafa; font-family: "メイリオ",Meiryo,"Hiragino Kaku Gothic ProN","Hiragino Sans",sans-serif; }
			h1 { font-size: 1.2em; background-color:#080; padding: 3px; font-weight: bold; color: white; }
			#message { border: 1px green dotted; background-color: #efe; font-weight: bold; }
			#message p { margin: 1em 0.5em; }
			#link { text-align:center; }
			#foot { margin-top: 3em; font-size: 0.9em; text-align: right; }
		</style>
	</head>
	<body>
		<h1>てがろぐ <small>－Fumy Otegaru Memo Logger-</small> [情報]</h1>
		<p>$msgfirst</p>
		<div id="message">
			<p>$msgmain</p>
		</div>
		<p id="link">$linkstr</p>
		<p id="foot"><a href="https://www.nishishi.com/cgi/tegalog/">てがろぐ配布サイト</a></p>
	</body>
	</html>
EOM
	exit;
}

# タグ記号をエスケープ:安全用
sub cuttagmarks
{
	my $str = shift @_ || '';
	$str =~ s|&|&amp;|g;	# アンドを実体参照に
	$str =~ s|<|&lt;|g;		# 小なりを実体参照に
	$str =~ s|>|&gt;|g;		# 大なりを実体参照に
	$str =~ s|"|&quot;|g;	# 二重引用符を実体参照に
	$str =~ s|'|&apos;|g;	# 引用符を実体参照に
	return $str;
}

# ---------------------- #
# エラーメッセージの出力 #	第1引数=エラーメッセージ／第2引数=移動先リンク文字列
# ---------------------- #
sub errormsg
{
	my $msg = shift @_ || 'NO MESSAGE';
	my $linkstr = shift @_ || '';
	my $debugdetail = '';

	if( $flagDebug{'ShowDebugStrings'} == 1 ) {
		$debugdetail = '[PARAMS] ';
		my @params = $cgi->param();
		foreach my $op ( @params ) {
			$debugdetail .= "( $op = " . $cgi->param($op) . ' )';
		}
	}

	# 環境情報の取得
	my $envs = '';
	if ( !$setdat{'envlistonerror'} ) {
		$envs .= '<div id="envopen"><input type="button" value="環境情報を表示" onclick="showenv();"></div><div id="envbox"><p class="extrainfo">※なお、お問い合わせの際は、以下の枠内の情報も同時にお知らせ頂けると話が早いかもしれません。</p><ul class="envs">';
		$envs .= '<li>実行環境: Perl ' . $^V . ' on ' . $^O . '</li>';
		$envs .= '<li>Included:<ul>';
		foreach my $key (sort keys %INC) {
			$envs .= "<li>" . &cuttagmarks( $key .'： '. $INC{$key} ) . "</li>\n";
		}
		$envs .= '</ul></li><li>環境変数:<ul>';
		foreach my $key (sort keys %ENV) {
			$envs .= "<li>" . &cuttagmarks( $key .'： '. $ENV{$key} ) . "</li>\n";
		}
		$envs .= '</ul></li></ul></div>';
	}

	# 早い段階でエラーが出た場合のために独自に用意しておく
	my $cgi = new CGI;
	if( $charcode eq '' ) { $charcode = 'UTF-8'; }

	print $cgi->header( -type => "text/html" , -charset => $charcode );
	print << "EOM";
	<!DOCTYPE html>
	<html>
	<head>
		<meta name="viewport" content="initial-scale=1">
		<meta name="robots" content="noindex">
		<title>&#9940; てがろぐ 動作エラー</title>
		<style type="text/css">
			body { background-color: #fafafa; font-family: "メイリオ",Meiryo,"Hiragino Kaku Gothic ProN","Hiragino Sans",sans-serif; }
			h1 { font-size: 1.2em; background-color:#cc0000; padding: 3px; font-weight: bold; color: white; }
			.errorbox { padding:1em; margin:1em auto; border:1px solid #eee; background-color:white; border-radius:2em; width:75%; min-width:300px; box-sizing:border-box; }
			#message { border: 1px red dashed; background-color: #fff0f0; font-weight: bold; }
			#message p { margin: 1em 0.5em; }
			#link { text-align:center; }
			.afteralerts { margin: 3em 0 2em; }
			.contacttoauthor { margin:1em 0; padding:0 0 0 1.5em; }
			.extrainfo { margin: 2.5em 0 0 0; padding: 1.5em 0 0 0; }
			#envopen { text-align:right; }
			#envopen input { font-size:0.7em; }
			.envs { font-size:0.85em; height:10em; min-height:3em; border:1px solid green; overflow:auto; background-color:white; resize:vertical; }
			\@media (max-width: 999px) { .errorbox{ width:auto; } }
		</style>
	</head>
	<body>
		<h1>&#9940; てがろぐ 動作エラー</h1>
		<div class="errorbox">
			<p>CGIの動作中にエラーが発生しました。詳細は以下の通りです。</p>
			<div id="message">
				<p>$msg</p>
			</div>
			<p id="link">$linkstr</p>
			<p>$debugdetail</p>
			<p class="afteralerts">上記の赤枠内に表示されている内容を参考にして対処して下さい。(<a href="?mode=admin">管理画面を表示</a>)</p><ul class="contacttoauthor"><li>もし、作者に問い合わせたい場合は、(1)上記のメッセージ、(2)現在のURL、(3)もしCGIを修正したならその内容……の3点を併せて<a href="https://www.nishishi.com/">西村文宏/にしし</a>宛にお知らせ下さい。</li><li>なお、CGIは<a href="https://www.nishishi.com/cgi/tegalog/">てがろぐ(Tegalog)配布サイト</a>で公開されている最新のバージョンをお使い下さい。その際、CGI本体だけでなく、関連ファイル(.plファイル等)も含めて最新版をお使い頂くようお願いします。ただし、使用実績がある場合はデータファイルを上書きしてしまわないようご注意下さい。</li><li>現在、あなたがお使いのバージョンは、Ver<b> $versionnum </b>です。</li></ul>$envs
		</div>
		<script>
			document.getElementById('envbox').style.display = 'none';
			function showenv() {
				document.getElementById('envbox').style.display = 'block';
				document.getElementById('envopen').style.display = 'none';
			}
		</script>
	</body>
	</html>
EOM
	exit;
}

# ------------------------
# Built-inデータの読み込み		引数：対象タグ名
# ------------------------
sub loadbuiltin
{
	my $target = shift @_ || '';
	my $start = "<<<$target>>>";

	my @ret = ();

	# まだ<DATA>を読んでいなければ読む
	if( $#loadedDATA < 0 ) {
		@loadedDATA = <DATA>;
	}

	my $copyflag = 0;
	foreach my $line (@loadedDATA) {
		if( $line =~ /^$start/ ) {
			# 目的のタグを見つけたらフラグを立てて次の行から抽出開始
			$copyflag = 1;
			next;
		}
		elsif(( $copyflag == 1 ) && ( $line =~ /^<<</ )) {
			# フラグが立っているときに、Built-inタグが出てきたらループ終了
			last;
		}
		# フラグが立っていたらコピー
		if( $copyflag == 1 ) {
			push( @ret, $line);
		}
	}

	# 何も抽出しなかった場合
	if( $#ret < 0 ) {
		my $te = &fcts::forsafety($target);
		&errormsg("Built-inデータの読み込みに失敗しました。: $te",'');
	}

	# 抽出結果を返す
	return @ret;
}

exit;

__DATA__
<<<builtinskin-plaintext:outer>>>
<html><head><meta charset="[[CHARCODE]]"><meta name="viewport" content="initial-scale=1">
<title>EXPORT: [[SITUATION:TITLE]] [[FREE:TITLE:MAIN]] [[FREE:TITLE:SUB]] ]]</title>
<style>pre { border:1px solid #ccc; background-color: #fefefe; padding: 1em; overflow: auto; } .dateseparator{ background-color: #f0f0f0; padding:0.5em; font-size:0.8em; }</style>
</head><body>
<p style="background-color:crimson; color:white; padding:0.5em; font-weight:bold; line-height:1.1;">※注：以下の表示は、エクスポートモードでファイルに出力することを前提に作られているため、画面表示には向いていません。</p>
<p>Last Update: [[INFO:LASTUPDATE]]</p>
<pre>
[[TEGALOG]]
</pre>
<p>[[VERSION]] / <a href="[[ADMIN:URL]]">管理画面</a></p>
</body></html>
<<</builtinskin-plaintext:outer>>>

<<<builtinskin-plaintext:inner>>>
--- 
DATE: [[DATE]]
USER: [[USERNAME]] ([[USERID]])
CATEGORY: [[CATEGORYNAMES]]
LENGTH: [[LENGTH]]文字
[[COMMENT]]
[[PARMAURL:FULL]]

<<</builtinskin-plaintext:inner>>>

<<<builtinskin-rss:outer>>>
<?xml version="1.0" encoding="[[CHARCODE]]"?>
<rss version="2.0">
<channel>
	<title><![CDATA[ [[SITUATION:TITLE]] [[FREE:TITLE:MAIN]] [[FREE:TITLE:SUB]] ]]></title>
	<link>[[HOME:URL:FULL]]</link>
	<description><![CDATA[ [[FREE:DESCRIPTION]] ]]></description>
	<language>ja</language>
	<copyright>Copyright [[INFO:LASTUPDATE:Y]]</copyright>
	<lastBuildDate>[[INFO:LASTUPDATE:w, D e Y h:m:s +0900]]</lastBuildDate>
	<generator><![CDATA[ [[VERSION]] ]]></generator>
	<!-- BEGIN ENTRIES -->
	[[TEGALOG]]
	<!-- END ENTRIES -->
</channel>
</rss>
<<</builtinskin-rss:outer>>>

<<<builtinskin-rss:inner>>>
<!-- One Entry Data for RSS Feed -->
<item>
	<title><![CDATA[ [[COMMENT:TITLE:30]] ]]></title>
	<description><![CDATA[ [[COMMENT:BODY:120]] (全[[LENGTH]]文字) -- Posted by [[USERNAME]] ]]></description>
	<link>[[PARMAURL:PURE:FULL]]</link>
	<guid>[[PARMAURL:PURE:FULL]]</guid>
	<category>[[CATEGORYIDS:IFEMPTY:tegalog]]</category>
	<pubDate>[[DATE:w, D e Y h:m:s +0900]]</pubDate>
</item>
<<</builtinskin-rss:inner>>>

<<<builtinskin-rssfull:outer>>>
<?xml version="1.0" encoding="[[CHARCODE]]"?>
<rss version="2.0">
<channel>
	<title><![CDATA[ [[SITUATION:TITLE]] [[FREE:TITLE:MAIN]] [[FREE:TITLE:SUB]] ]]></title>
	<link>[[HOME:URL:FULL]]</link>
	<description><![CDATA[ [[FREE:DESCRIPTION]] ]]></description>
	<language>ja</language>
	<copyright>Copyright [[INFO:LASTUPDATE:Y]]</copyright>
	<lastBuildDate>[[INFO:LASTUPDATE:w, D e Y h:m:s +0900]]</lastBuildDate>
	<generator><![CDATA[ [[VERSION]] ]]></generator>
	<!-- BEGIN ENTRIES -->
	[[TEGALOG]]
	<!-- END ENTRIES -->
</channel>
</rss>
<<</builtinskin-rssfull:outer>>>

<<<builtinskin-rssfull:inner>>>
<!-- One Entry Data for RSS Feed -->
<item>
	<title><![CDATA[ [[COMMENT:TITLE:30]] ]]></title>
	<description><![CDATA[ [[COMMENT]] -- Posted by [[USERNAME]] 〔[[LENGTH]]文字〕 ]]></description>
	<link>[[PARMAURL:PURE:FULL]]</link>
	<guid>[[PARMAURL:PURE:FULL]]</guid>
	<category>[[CATEGORYIDS:IFEMPTY:tegalog]]</category>
	<pubDate>[[DATE:w, D e Y h:m:s +0900]]</pubDate>
</item>
<<</builtinskin-rssfull:inner>>>

<<<builtinskin-xmlsitemap:outer>>>
<?xml version="1.0" encoding="[[CHARCODE]]"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
	<url><loc>[[HOME:URL:FULL]]</loc></url>
[[TEGALOG]]
</urlset>
<<</builtinskin-xmlsitemap:outer>>>

<<<builtinskin-xmlsitemap:inner>>>
	<url><loc>[[PARMAURL:PURE:FULL]]</loc></url>
<<</builtinskin-xmlsitemap:inner>>>
