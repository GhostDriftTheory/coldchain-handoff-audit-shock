"""
coldchain-handoff-audit-shock
正常完了した配送を、荷主監査にかけます。

GhostDrift数理研究所 — https://www.ghostdriftresearch.com
"""

import streamlit as st

st.set_page_config(
    page_title="荷主監査シミュレーション",
    page_icon="🚛",
    layout="centered",
)

# ────────────────────────────────────────────────
#  CSS
# ────────────────────────────────────────────────
st.markdown("""
<style>
/* layout */
.main .block-container {
    max-width: 720px;
    padding: 2.5rem 2rem 4rem;
    margin: 0 auto;
}
/* headings */
h1 {
    font-size: 1.55rem !important;
    font-weight: 900 !important;
    letter-spacing: -0.02em;
    color: #111;
    line-height: 1.3 !important;
    margin-bottom: 4px !important;
}
h2 {
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    color: #999;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border-bottom: 1px solid #eee;
    padding-bottom: 8px;
    margin: 32px 0 16px !important;
}
/* shock strip */
.shock {
    border-left: 5px solid #c53030;
    background: #fff5f5;
    padding: 16px 20px;
    border-radius: 0 6px 6px 0;
    margin: 14px 0 20px;
}
.shock p { margin: 2px 0; color: #c53030; font-weight: 700; font-size: 1.1rem; }
/* legacy table */
.legacy-wrap {
    border: 1px solid #eee;
    border-radius: 8px;
    overflow: hidden;
    margin: 12px 0;
}
.legacy-row {
    display: flex;
    border-bottom: 1px solid #f5f5f5;
    font-size: 0.92rem;
}
.legacy-row:last-child { border-bottom: none; }
.legacy-key {
    width: 110px;
    flex-shrink: 0;
    padding: 9px 14px;
    color: #aaa;
    background: #fafafa;
    font-size: 0.85rem;
}
.legacy-val {
    padding: 9px 14px;
    color: #222;
    font-weight: 500;
    flex: 1;
}
.status-complete {
    background: #f0fff4;
    border: 2px solid #38a169;
    border-radius: 6px;
    padding: 13px 18px;
    margin: 12px 0;
    text-align: center;
    font-size: 1.1rem;
    font-weight: 800;
    color: #276749;
}
/* player cards */
.player-dim {
    background: #f8f8f8;
    border-radius: 6px;
    padding: 11px 15px;
    margin: 7px 0;
    color: #bbb;
    font-size: 0.88rem;
}
.player-dim .pt { font-weight: 600; color: #ccc; margin-bottom: 5px; }
.player-dim ul { margin: 0; padding-left: 16px; line-height: 1.7; }
.player-key {
    background: #fffbeb;
    border-left: 5px solid #d97706;
    border-radius: 0 8px 8px 0;
    padding: 16px 20px;
    margin: 10px 0;
}
.player-key .pt  { font-weight: 800; color: #92400e; font-size: 1rem; margin-bottom: 5px; }
.player-key .ps  { color: #78350f; font-size: 0.88rem; margin-bottom: 9px; }
.player-key .pw  { font-weight: 600; color: #b45309; margin: 7px 0 4px; font-size: 0.87rem; }
.player-key ul   { margin: 0; padding-left: 16px; }
.player-key li   { color: #92400e; font-size: 0.88rem; line-height: 1.7; }
/* records-exist table */
.rec-table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 0.9rem;
}
.rec-table th {
    text-align: left;
    padding: 7px 12px;
    background: #f5f5f5;
    color: #888;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.rec-table td { padding: 8px 12px; border-bottom: 1px solid #f0f0f0; }
.rec-table td:last-child { text-align: center; color: #38a169; font-weight: 700; }
.rec-gap {
    background: #fff5f5;
    border-left: 5px solid #e53e3e;
    border-radius: 0 6px 6px 0;
    padding: 14px 18px;
    margin: 14px 0;
    font-size: 0.93rem;
    color: #742a2a;
    line-height: 1.7;
}
.rec-gap strong { font-weight: 800; }
/* pivot note */
.pivot-note {
    background: #1a1a1a;
    color: #fff;
    border-radius: 6px;
    padding: 14px 18px;
    margin: 16px 0;
    font-weight: 700;
    font-size: 0.95rem;
    line-height: 1.6;
}
/* question box */
.q-box {
    border: 2px solid #d97706;
    background: #fffbeb;
    border-radius: 8px;
    padding: 20px 24px;
    margin: 14px 0;
}
.q-label { font-size: 0.75rem; font-weight: 700; color: #d97706; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 9px; }
.q-text  { font-size: 1.1rem; font-weight: 800; color: #78350f; line-height: 1.5; }
/* 記録なし */
.kinasashi {
    background: #c53030;
    color: #fff;
    border-radius: 10px;
    padding: 36px 28px;
    margin: 16px 0;
    text-align: center;
}
.kinasashi .km { font-size: 2.4rem; font-weight: 900; letter-spacing: -0.02em; margin-bottom: 8px; }
.kinasashi .ks { font-size: 0.88rem; opacity: 0.85; line-height: 1.7; }
/* audit questions */
.aq {
    border-left: 3px solid #e53e3e;
    background: #fff5f5;
    border-radius: 0 6px 6px 0;
    padding: 11px 15px;
    margin: 9px 0;
}
.aq .aq-l { font-size: 0.72rem; font-weight: 700; color: #e53e3e; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 3px; }
.aq .aq-q { font-weight: 600; color: #742a2a; font-size: 0.93rem; margin-bottom: 5px; }
.aq .aq-a { font-size: 0.85rem; color: #e53e3e; }
/* conclusion */
.con-warn {
    background: #fffbeb;
    border-left: 5px solid #d97706;
    border-radius: 0 6px 6px 0;
    padding: 16px 20px;
    margin: 14px 0;
}
.con-warn p { color: #92400e; font-weight: 700; font-size: 1rem; margin: 0 0 5px; line-height: 1.5; }
.con-warn p:last-child { margin: 0; }
.con-box {
    background: #f7fafc;
    border-left: 5px solid #4a5568;
    border-radius: 0 6px 6px 0;
    padding: 16px 20px;
    margin: 14px 0;
}
.con-box p { color: #2d3748; font-weight: 500; margin: 0 0 6px; line-height: 1.65; font-size: 0.93rem; }
.con-box p:last-child { margin: 0; }
.pro-note {
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 14px 18px;
    margin: 14px 0;
    font-size: 0.85rem;
    color: #718096;
    line-height: 1.7;
}
.pro-note strong { color: #4a5568; }
/* footer */
.adic-footer {
    margin-top: 40px;
    padding-top: 18px;
    border-top: 1px solid #eee;
    color: #bbb;
    font-size: 0.8rem;
    line-height: 1.9;
}
.adic-footer a { color: #bbb; text-decoration: underline; }
/* button */
div.stButton > button {
    width: 100%;
    padding: 13px;
    font-size: 0.95rem;
    font-weight: 700;
    border-radius: 6px;
    margin-top: 20px;
    background: #1a1a1a;
    color: #fff;
    border: none;
    cursor: pointer;
    transition: opacity .15s;
}
div.stButton > button:hover { opacity: 0.82; background: #1a1a1a; color: #fff; }
div.stButton > button:focus { box-shadow: none; }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
#  State
# ────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 0

step = st.session_state.step

def advance():
    st.session_state.step += 1

# ────────────────────────────────────────────────
#  データ（架空名）
# ────────────────────────────────────────────────
DELIVERY = {
    "id":      "DEL-2026-0501",
    "cargo":   "インスリン製剤（バイオ医薬品・冷蔵管理対象）",
    "shipper": "A製薬株式会社",
    "route":   "A製薬 → B物流 → 大阪DC → C病院グループ",
    "arrival": "2026-05-10 16:10",
}

RECORDS_EXIST = [
    ("荷主との基本契約",     "あり"),
    ("SOP（温度管理手順書）", "あり"),
    ("温度ログ",            "あり（全区間）"),
    ("WMS 入庫記録",        "あり"),
    ("作業者記録",           "あり"),
    ("出荷記録",             "あり"),
]

AUDIT_4Q = [
    ("温度条件はSOPにあります。",
     "この受け渡し記録に紐づいていますか？",
     "SOPと個別配送記録が別システム。この受け渡し時点での紐づけが確認できません。"),
    ("停止条件は契約にあります。",
     "大阪DCの受領時点で評価されていますか？",
     "評価記録なし。契約に書かれた条件がこの受け渡しで履行されたかを示す証跡がありません。"),
    ("作業者記録はあります。",
     "その人に品質責任の引受権限がありますか？",
     "権限付与記録と受領記録が別管理。品質責任として引き受けた証跡がありません。"),
    ("入庫記録はあります。",
     "出荷可否判断まで責任が連続していますか？",
     "入庫から出荷判断への責任連鎖を一つながりで再構成できません。"),
]

# ────────────────────────────────────────────────
#  常時表示：タイトル + ショック
# ────────────────────────────────────────────────
st.markdown("# 正常完了した配送を、荷主監査にかけます")
st.markdown(
    "<p style='color:#aaa;font-size:0.88rem;margin:2px 0 0'>温度ログあり。作業記録あり。逸脱警告ゼロ。それでも、説明できない配送があります。</p>",
    unsafe_allow_html=True,
)
st.markdown("""
<div class="shock">
  <p>事故は起きていません。</p>
  <p>温度も守られています。</p>
  <p>でも、荷主から一問聞かれたら答えられません。</p>
</div>
""", unsafe_allow_html=True)

# ── Step 0 ──────────────────────────────────────
if step == 0:
    st.button("確認する →", on_click=advance)
    st.stop()

# ── STEP 1: 正常完了画面 ────────────────────────
st.markdown("## STEP 1 ── この配送を見てください")
st.markdown(f"""
<div class="legacy-wrap">
  <div class="legacy-row"><div class="legacy-key">配送 ID</div><div class="legacy-val">{DELIVERY['id']}</div></div>
  <div class="legacy-row"><div class="legacy-key">貨物</div><div class="legacy-val">{DELIVERY['cargo']}</div></div>
  <div class="legacy-row"><div class="legacy-key">経路</div><div class="legacy-val">{DELIVERY['route']}</div></div>
  <div class="legacy-row"><div class="legacy-key">温度ログ</div><div class="legacy-val">✓ あり（全区間記録）</div></div>
  <div class="legacy-row"><div class="legacy-key">積み替え</div><div class="legacy-val">✓ あり</div></div>
  <div class="legacy-row"><div class="legacy-key">作業記録</div><div class="legacy-val">✓ あり</div></div>
  <div class="legacy-row"><div class="legacy-key">逸脱警告</div><div class="legacy-val">✓ 0 件</div></div>
  <div class="legacy-row"><div class="legacy-key">到着時刻</div><div class="legacy-val">{DELIVERY['arrival']}</div></div>
</div>
<div class="status-complete">✓ 配送完了 ── システム上、何も問題ありません。</div>
""", unsafe_allow_html=True)

if step == 1:
    st.button("荷主監査を開始する →", on_click=advance)
    st.stop()

# ── STEP 2: プレーヤー + 既存記録の罠 ──────────
st.markdown("## STEP 2 ── 記録はあります。でも、別々の記録です。")
st.markdown(
    "<p style='color:#888;font-size:0.88rem;margin:0 0 12px'>事故や品質問題が起きたとき、荷主・行政・法務から聞かれることはプレーヤーによって違います。</p>",
    unsafe_allow_html=True,
)

st.markdown("""
<div class="player-dim">
  <div class="pt">🚛 B物流（配送会社） ── 移動中の温度・時間を守る</div>
  <ul>
    <li>移動中に温度は逸脱しなかったか</li>
    <li>積み替え時に一時逸脱はなかったか</li>
    <li>遅延による時間超過はなかったか</li>
  </ul>
</div>

<div class="player-key">
  <div class="pt">🏭 大阪DC（中継倉庫）</div>
  <div class="ps">在庫として受け取り、保管し、出荷する ── ここで管理対象が切り替わります</div>
  <div class="pw">運んでいる間の「温度・時間を守る」から、<br>倉庫に入った瞬間から「受け取り・保管・出荷可否の判断」へ。</div>
  <ul>
    <li>事故後に必ず聞かれること：保管温度・保管時間・ロット・先入先出・出荷保留判断・出荷承認者</li>
  </ul>
</div>

<div class="player-dim">
  <div class="pt">🏥 C病院グループ（納品先） ── 受け入れ可否を判断し、使用許可を出す</div>
  <ul>
    <li>受入可否の判断（薬剤師確認）・使用可否の最終承認・拒否時の隔離フロー</li>
  </ul>
</div>
""", unsafe_allow_html=True)

# 既存記録の罠
rows_html = "".join(
    f'<tr><td>{label}</td><td>{val}</td></tr>'
    for label, val in RECORDS_EXIST
)
st.markdown(f"""
<p style="color:#444;font-weight:600;margin:20px 0 8px">この配送に関係する記録：</p>
<table class="rec-table">
  <thead><tr><th>記録の種類</th><th>状態</th></tr></thead>
  <tbody>{rows_html}</tbody>
</table>
<div class="rec-gap">
  <strong>しかし、これらは別々の記録です。</strong><br>
  荷主が知りたいのは「記録があるか」ではありません。<br>
  <strong>この受け渡し時点で、誰がどの条件を引き受けたかを一つながりで説明できるか</strong>です。
</div>

<div class="pivot-note">
  B物流 → 大阪DC の受け渡しは、この配送で最大の責任切替点です。<br>
  「誰が・何℃条件で・どの停止条件で引き受けたか」が、ここだけ一つながりの証跡として結合されていません。
</div>
""", unsafe_allow_html=True)

if step == 2:
    st.button("荷主から一問きます →", on_click=advance)
    st.stop()

# ── STEP 3: 一問 ────────────────────────────────
st.markdown("## STEP 3 ── 荷主から、一問だけ来ます")
st.markdown(
    "<p style='color:#aaa;font-size:0.85rem;margin:4px 0 14px'>受け渡し：B物流（配送会社） → 大阪DC（中継倉庫） ／ 2026-05-10 12:00</p>",
    unsafe_allow_html=True,
)
st.markdown("""
<div class="q-box">
  <div class="q-label">A製薬（荷主）からの質問</div>
  <div class="q-text">大阪DCは、この配送について<br>何℃条件で、誰の責任として受け取りましたか？<br>その証跡を出してもらえますか？</div>
</div>
""", unsafe_allow_html=True)

if step == 3:
    st.button("回答を確認する →", on_click=advance)
    st.stop()

# ── STEP 4: 記録なし（再構成不能）──────────────
st.markdown("""
<div class="kinasashi">
  <div class="km">一つながりの証跡として<br>再構成できません。</div>
  <div class="ks">
    温度ログはあります。入庫記録もあります。SOPも契約もあります。<br>
    しかし「この受け渡し時点でB物流から大阪DCへ、何℃条件・どの停止条件・誰の引受権限で渡ったか」を<br>
    一本の証跡として示すことができません。
  </div>
</div>
""", unsafe_allow_html=True)

if step == 4:
    st.button("4つの問いに展開する →", on_click=advance)
    st.stop()

# ── STEP 4 続き: 4問（プロ向け）──────────────────
st.markdown("## STEP 4 ── この一問は、4つの問いに展開されます")
st.markdown(
    "<p style='color:#888;font-size:0.88rem;margin:0 0 12px'>SOPも契約も記録もある。それでも「この受け渡し」で答えられない理由：</p>",
    unsafe_allow_html=True,
)

for i, (premise, question, answer) in enumerate(AUDIT_4Q, 1):
    st.markdown(f"""
<div class="aq">
  <div class="aq-l">✗ Q{i}</div>
  <div class="aq-q"><span style="color:#aaa">{premise}</span><br>{question}</div>
  <div class="aq-a">→ {answer}</div>
</div>
""", unsafe_allow_html=True)

if step == 5:
    st.button("結論を見る →", on_click=advance)
    st.stop()

# ── STEP 5: 結論 ────────────────────────────────
st.markdown("## STEP 5 ── この配送の「完了」は何を意味するか")

st.markdown("""
<div class="con-warn">
  <p>この配送は、温度が守られていました。</p>
  <p>事故は起きていません。SOPも契約もあります。</p>
  <p style="margin-top:10px">それでも、荷主監査では<strong>説明不能</strong>です。</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="color:#444;line-height:1.75;margin:14px 0;font-size:0.93rem">
B物流 → 大阪DC の一点で、<strong>「誰が、何℃条件で、どの権限として、どの停止条件で引き受けたか」</strong>が<br>
一つながりの証跡として結合されていません。<br>
その後の保管・出荷・使用のすべてが、この一点を起点に宙に浮いています。
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="con-warn">
  <p>事故が起きていない日にも、説明不能な配送は完了扱いになっています。</p>
  <p>本当に危ない関門は少ない。</p>
  <p>でも、その関門を外すと、会社ごと説明不能になります。</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="con-box">
  <p>温度が守られていたかだけでは、足りません。</p>
  <p>その温度条件のもとで、誰が品質責任を受け取り、どこで止められたかまで、<strong>一本の証跡として再構成できなければ</strong>、内部統制としては不十分です。</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="pro-note">
  <strong>製薬物流の専門家の方へ：</strong><br>
  これは「現場がずさんだ」というデモではありません。<br>
  契約・SOP・温度ログ・WMS記録があっても、<strong>個別の受け渡し単位で責任移転の証跡が結合されていなければ、
  荷主監査では答えられない</strong>、という構造の問題です。<br>
  GDPが求める「各当事者の義務・責任の明確化」と「追跡可能性」は、記録の存在だけでは満たされません。
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="adic-footer">
  この「責任消失点」を機械的に検出する内部統制レイヤー：<strong>ADIC</strong>（Advanced Data Integrity by Ledger of Computation）<br>
  GhostDrift数理研究所 ／ <a href="https://www.ghostdriftresearch.com">ghostdriftresearch.com</a><br>
  Lean 4 形式証明：<a href="https://github.com/GhostDriftTheory/adic-lean-proof-replay">github.com/GhostDriftTheory/adic-lean-proof-relay</a>
</div>
""", unsafe_allow_html=True)
