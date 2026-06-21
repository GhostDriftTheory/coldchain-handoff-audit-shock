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

st.markdown("""
<style>
.main .block-container {
    max-width: 700px;
    padding: 2.5rem 1.8rem 5rem;
    margin: 0 auto;
}
h1 {
    font-size: 1.5rem !important; font-weight: 900 !important;
    letter-spacing: -0.02em; color: #111;
    line-height: 1.3 !important; margin-bottom: 4px !important;
}
h2 {
    font-size: 0.72rem !important; font-weight: 700 !important;
    color: #aaa; letter-spacing: 0.14em; text-transform: uppercase;
    border-bottom: 1px solid #eee; padding-bottom: 8px;
    margin: 36px 0 16px !important;
}
.shock { border-left:5px solid #c53030; background:#fff5f5;
         padding:14px 18px; border-radius:0 6px 6px 0; margin:12px 0 18px; }
.shock p { margin:2px 0; color:#c53030; font-weight:700; font-size:1.05rem; }
.legacy-wrap { border:1px solid #eee; border-radius:8px; overflow:hidden; margin:12px 0; }
.legacy-row  { display:flex; border-bottom:1px solid #f5f5f5; font-size:0.9rem; }
.legacy-row:last-child { border-bottom:none; }
.legacy-key  { width:100px; flex-shrink:0; padding:8px 14px; color:#bbb; background:#fafafa; font-size:0.82rem; }
.legacy-val  { padding:8px 14px; color:#222; font-weight:500; flex:1; }
.status-complete { background:#f0fff4; border:2px solid #38a169; border-radius:6px;
    padding:12px 18px; margin:12px 0; text-align:center;
    font-size:1.05rem; font-weight:800; color:#276749; }
.pivot-note { background:#f7f7f7; border-radius:6px; padding:12px 16px;
    margin:14px 0; font-size:0.88rem; color:#555; line-height:1.65; }
.pivot-note strong { color:#111; }
.log-hdr { font-size:0.78rem; font-weight:700; color:#888;
    letter-spacing:0.06em; text-transform:uppercase; margin:18px 0 10px; }
.log-card { border:1px solid #eee; border-radius:8px; overflow:hidden; margin:8px 0; }
.log-card-title { background:#f7f7f7; padding:8px 14px;
    font-size:0.82rem; font-weight:700; color:#666; border-bottom:1px solid #eee; }
.log-row { display:flex; border-bottom:1px solid #f9f9f9; font-size:0.88rem; }
.log-row:last-child { border-bottom:none; }
.lk { width:110px; flex-shrink:0; padding:7px 14px; color:#bbb; font-size:0.8rem; background:#fafafa; }
.lv { padding:7px 14px; color:#222; font-weight:500; }
.log-row.ng .lk { background:#fff5f5; color:#e53e3e; }
.log-row.ng .lv { color:#e53e3e; }
.log-div { background:#fff5f5; padding:5px 14px; font-size:0.75rem;
    color:#e53e3e; font-weight:600;
    border-top:1px dashed #fca5a5; border-bottom:1px dashed #fca5a5; }
.proof-box { background:#fffbeb; border:1px solid #fcd34d;
    border-radius:8px; padding:14px 18px; margin:16px 0; }
.proof-title { font-size:0.75rem; font-weight:700; color:#d97706;
    letter-spacing:0.1em; text-transform:uppercase; margin-bottom:8px; }
.proof-box p { color:#78350f; font-size:0.92rem; line-height:1.65; margin:0; }
.verdict-box { background:#fff5f5; border:1px solid #fca5a5;
    border-radius:8px; padding:14px 18px; margin:10px 0; }
.verdict-item { color:#c53030; font-size:0.88rem; font-weight:600;
    padding:3px 0; border-bottom:1px solid #fee2e2; line-height:1.5; }
.verdict-item:last-of-type { border-bottom:none; }
.verdict-conclusion { margin-top:12px; font-size:0.88rem; color:#742a2a;
    line-height:1.7; padding-top:10px; border-top:1px solid #fca5a5; }
.gdp-note { background:#f0f4ff; border-left:5px solid #4361ee;
    border-radius:0 6px 6px 0; padding:14px 18px; margin:0 0 18px; }
.gdp-note .gn-label { font-size:0.75rem; font-weight:700; color:#4361ee;
    letter-spacing:0.1em; text-transform:uppercase; margin-bottom:8px; }
.gdp-note .gn-main { color:#1e3a8a; font-size:0.92rem; font-weight:600;
    margin-bottom:6px; line-height:1.5; }
.gdp-note .gn-sub { color:#1e40af; font-size:0.88rem; line-height:1.65; }
.q-box { border:2px solid #d97706; background:#fffbeb;
    border-radius:8px; padding:18px 22px; margin:14px 0; }
.q-label { font-size:0.72rem; font-weight:700; color:#d97706;
    letter-spacing:0.1em; text-transform:uppercase; margin-bottom:8px; }
.q-text  { font-size:1.05rem; font-weight:800; color:#78350f; line-height:1.55; }
.kinasashi { background:#c53030; color:#fff; border-radius:10px;
    padding:32px 24px; margin:16px 0; text-align:center; }
.km { font-size:2rem; font-weight:900; letter-spacing:-0.02em;
    margin-bottom:8px; line-height:1.2; }
.ks { font-size:0.85rem; opacity:0.85; line-height:1.75; }
.aq { border-left:3px solid #e53e3e; background:#fff5f5;
    border-radius:0 6px 6px 0; padding:10px 14px; margin:8px 0; }
.aq-l { font-size:0.7rem; font-weight:700; color:#e53e3e;
    text-transform:uppercase; letter-spacing:0.08em; margin-bottom:2px; }
.aq-premise { font-size:0.8rem; color:#aaa; margin-bottom:3px; }
.aq-q { font-weight:700; color:#742a2a; font-size:0.9rem; margin-bottom:4px; }
.aq-a { font-size:0.82rem; color:#e53e3e; }
.con-warn { background:#fffbeb; border-left:5px solid #d97706;
    border-radius:0 6px 6px 0; padding:14px 18px; margin:12px 0; }
.con-warn p { color:#92400e; font-weight:700; font-size:0.97rem; margin:0 0 4px; line-height:1.5; }
.con-warn p:last-child { margin:0; }
.con-box { background:#f7fafc; border-left:5px solid #4a5568;
    border-radius:0 6px 6px 0; padding:14px 18px; margin:12px 0; }
.con-box p { color:#2d3748; font-weight:500; margin:0 0 5px; line-height:1.65; font-size:0.9rem; }
.con-box p:last-child { margin:0; }
.pro-note { border:1px solid #e2e8f0; border-radius:6px;
    padding:12px 16px; margin:12px 0; font-size:0.82rem;
    color:#718096; line-height:1.75; }
.pro-note strong { color:#4a5568; }
/* glossary */
.gloss-term { border-left:3px solid #e2e8f0; padding:9px 16px; margin:8px 0; }
.gloss-word { font-weight:700; font-size:0.88rem; color:#4a5568; margin-bottom:4px; }
.gloss-desc { font-size:0.82rem; color:#718096; line-height:1.7; }
/* dark final section */
.dark-wrap { background:#0f172a; border-radius:12px; padding:28px 26px; margin:8px 0; }
.dark-wrap p, .dark-wrap div, .dark-wrap span { color:#cbd5e1; }
.dark-eyebrow { font-size:0.72rem !important; font-weight:700 !important; color:#64748b !important;
    letter-spacing:0.14em; text-transform:uppercase; margin:0 0 20px !important; }
.dark-sec-label-blue { font-size:0.72rem !important; font-weight:700 !important; color:#4361ee !important;
    letter-spacing:0.1em; text-transform:uppercase; margin:0 0 12px !important; }
.dark-sec-label-amber { font-size:0.72rem !important; font-weight:700 !important; color:#d97706 !important;
    letter-spacing:0.1em; text-transform:uppercase; margin:0 0 12px !important; }
.dark-body { font-size:0.92rem !important; color:#cbd5e1 !important; line-height:1.75; margin:0 0 12px !important; }
.dark-em { color:#e2e8f0 !important; font-weight:700; }
.dark-sub { font-size:0.88rem !important; color:#94a3b8 !important; line-height:1.7; margin:0 0 8px !important; }
.dark-headline { font-size:0.97rem !important; font-weight:700 !important; color:#f1f5f9 !important;
    margin:0 0 16px !important; line-height:1.5; }
.dark-closer { font-size:0.97rem !important; font-weight:700 !important; color:#f1f5f9 !important;
    margin:0 0 6px !important; line-height:1.5; }
.badge-row { display:flex; gap:8px; flex-wrap:wrap; margin:4px 0 0; }
.badge-g  { background:#166534; color:#bbf7d0; padding:4px 12px; border-radius:4px; font-size:0.8rem; font-weight:700; }
.badge-y  { background:#854d0e; color:#fef9c3; padding:4px 12px; border-radius:4px; font-size:0.8rem; font-weight:700; }
.badge-b  { background:#1d4ed8; color:#dbeafe; padding:4px 12px; border-radius:4px; font-size:0.8rem; font-weight:700; }
.badge-r  { background:#991b1b; color:#fee2e2; padding:4px 12px; border-radius:4px; font-size:0.8rem; font-weight:700; }
.dark-divider { border-top:1px solid #1e293b; margin:24px 0; }
.dark-cards { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:20px; }
.dark-card { background:#1e293b; border-radius:6px; padding:12px 14px; }
.dark-card-label { font-size:0.7rem; color:#64748b; font-weight:600;
    letter-spacing:0.06em; text-transform:uppercase; margin-bottom:5px; }
.dark-card-text { font-size:0.88rem; color:#e2e8f0; font-weight:600; line-height:1.5; }
.dark-quote-block { border-left:2px solid #334155; padding:8px 16px; margin:10px 0; }
.dark-quote-line { font-size:0.88rem !important; color:#64748b !important; margin:2px 0 !important; font-style:italic; }
.dark-proof-block { background:#1e293b; border-radius:6px; padding:14px 18px; margin:12px 0; }
.dark-proof-line { font-size:0.92rem !important; color:#e2e8f0 !important; font-weight:600; margin:2px 0 !important; line-height:1.6; }
.dark-check-list { margin:12px 0 14px; }
.dark-check-item { font-size:0.88rem; color:#94a3b8; padding:5px 0 5px 4px;
    border-bottom:1px solid #1e293b; line-height:1.5; }
.dark-check-item:last-child { border-bottom:none; }
.dark-closer-accent { font-size:1.05rem !important; font-weight:900 !important;
    color:#fff !important; margin:4px 0 !important; line-height:1.4; }
.dark-note { font-size:0.75rem; color:#475569; margin:16px 0 0;
    line-height:1.6; border-top:1px solid #1e293b; padding-top:14px; }
/* footer */
.adic-footer { margin-top:40px; padding-top:16px; border-top:1px solid #eee;
    color:#bbb; font-size:0.78rem; line-height:1.9; }
.adic-footer a { color:#bbb; text-decoration:underline; }
/* button */
div.stButton > button {
    width:100%; padding:13px; font-size:0.93rem; font-weight:700;
    border-radius:6px; margin-top:18px;
    background:#1a1a1a; color:#fff; border:none; cursor:pointer;
    transition:opacity .15s;
}
div.stButton > button:hover { opacity:0.82; background:#1a1a1a; color:#fff; }
div.stButton > button:focus { box-shadow:none; }
</style>
""", unsafe_allow_html=True)

# ── State ──────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 0
step = st.session_state.step
def advance(): st.session_state.step += 1

# ── Data ───────────────────────────────────────
AUDIT_4Q = [
    ("温度条件は、SOP（社内の作業手順）にあります。",
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

GLOSSARY = [
    ("SOP",
     "社内の作業手順書。誰が・どの条件で・どう作業するかを定めたルール。温度管理・積み替え手順・受領確認など、各工程ごとに存在する。"),
    ("GDP（Good Distribution Practice）",
     "医薬品を安全に保管・輸送するための品質管理基準。製造後、病院や患者に届くまでのサプライチェーン全体に適用される。EU・日本ともに外部委託先への管理責任・書面契約・監査を要求している。"),
    ("逸脱",
     "決められた温度・時間・手順などから外れること。逸脱が起きた場合は原因・影響・対応を記録し、品質判断を経る必要がある。"),
    ("証跡（しょうせき）",
     "あとから「何が起きたか」「誰が判断したか」「どの条件で進めたか」を確認できる記録。単に記録が存在するだけでなく、1件の出来事として結合されていることが重要。"),
    ("受け渡しID",
     "1回の受け渡しイベントに紐づく識別子。温度ログ・作業ログ・受領記録が同じIDを持つことで「この受け渡しの証跡」として結合できる。これがないと、記録はあっても別々のデータのまま。"),
    ("ADICが見ているもの",
     "記録の有無ではなく、それらの記録が「1件の受け渡し」として結合されているか。SOPも契約も温度ログも揃っていても、受け渡しIDでつながっていなければ、監査のたびに人が探してつなぎ直す必要が生じる。"),
]

# ── Title + shock (always visible) ─────────────
st.markdown("# 正常完了した配送を、荷主監査にかけます")
st.markdown(
    "<p style='color:#bbb;font-size:0.85rem;margin:2px 0 0'>"
    "温度ログあり。作業記録あり。逸脱警告ゼロ。それでも、説明できない配送があります。</p>",
    unsafe_allow_html=True,
)
st.markdown("""
<div class="shock">
  <p>事故は起きていません。</p>
  <p>温度も守られています。</p>
  <p>でも、荷主から一問聞かれたら答えられません。</p>
</div>
""", unsafe_allow_html=True)

if step == 0:
    st.button("確認する →", on_click=advance)
    st.stop()

# ── STEP 1 ─────────────────────────────────────
st.markdown("## STEP 1 ── この配送を見てください")
st.markdown("""
<div class="legacy-wrap">
  <div class="legacy-row"><div class="legacy-key">配送 ID</div><div class="legacy-val">DEL-2026-0501</div></div>
  <div class="legacy-row"><div class="legacy-key">貨物</div><div class="legacy-val">インスリン製剤（バイオ医薬品・冷蔵管理対象）</div></div>
  <div class="legacy-row"><div class="legacy-key">経路</div><div class="legacy-val">A製薬 → B物流 → 大阪DC → C病院グループ</div></div>
  <div class="legacy-row"><div class="legacy-key">温度ログ</div><div class="legacy-val">✓ あり（全区間記録）</div></div>
  <div class="legacy-row"><div class="legacy-key">積み替え</div><div class="legacy-val">✓ あり</div></div>
  <div class="legacy-row"><div class="legacy-key">作業記録</div><div class="legacy-val">✓ あり</div></div>
  <div class="legacy-row"><div class="legacy-key">逸脱警告</div><div class="legacy-val">✓ 0 件</div></div>
  <div class="legacy-row"><div class="legacy-key">到着時刻</div><div class="legacy-val">2026-05-10 16:10</div></div>
</div>
<div class="status-complete">✓ 配送完了 ── システム上、何も問題ありません。</div>
""", unsafe_allow_html=True)

if step == 1:
    st.button("荷主監査を開始する →", on_click=advance)
    st.stop()

# ── STEP 2 ─────────────────────────────────────
st.markdown("## STEP 2 ── 記録はある。でも、同じ受け渡しを証明していない")

st.markdown("""
<div class="gdp-note">
  <div class="gn-label">このデモの前提</div>
  <div class="gn-main">GDP対応していない現場を想定していません。<br>むしろ、SOP（作業手順）・契約・温度ログ・入出庫記録がすべて揃っている現場を想定しています。</div>
  <div class="gn-sub">問いは一つです。それらの記録を、後から人が探して説明するのではなく、この1件の受け渡し証跡として、機械的に結合できますか？</div>
</div>
<div class="pivot-note">
  B物流 → 大阪DC の受け渡しは、配送中の「温度を守る責任」から倉庫での「受け取り・保管・出荷可否を判断する責任」に<strong>切り替わる唯一の瞬間</strong>です。だからここだけは、誰がどんな条件で引き受けたかの証跡が必要です。
</div>
<div class="log-hdr">B物流 → 大阪DC ／ 2026-05-10 12:00 ／ 実際のログ</div>
<div class="log-card">
  <div class="log-card-title">📊 温度ログ</div>
  <div class="log-row"><div class="lk">時刻</div><div class="lv">12:00</div></div>
  <div class="log-row"><div class="lk">実測温度</div><div class="lv">5.2℃</div></div>
  <div class="log-row"><div class="lk">配送 ID</div><div class="lv">DEL-2026-0501</div></div>
  <div class="log-div">↓ ここから先が空欄</div>
  <div class="log-row ng"><div class="lk">受け渡し ID</div><div class="lv">── 別システム（手動確認が必要）</div></div>
  <div class="log-row ng"><div class="lk">受領者</div><div class="lv">── 承認記録あり / 本受け渡しに未結合</div></div>
  <div class="log-row ng"><div class="lk">受領条件</div><div class="lv">── SOP参照 / 自動結合なし</div></div>
</div>
<div class="log-card">
  <div class="log-card-title">📋 作業ログ</div>
  <div class="log-row"><div class="lk">時刻</div><div class="lv">12:00</div></div>
  <div class="log-row"><div class="lk">作業</div><div class="lv">B物流 → 大阪DC 引き渡し</div></div>
  <div class="log-row"><div class="lk">配送 ID</div><div class="lv">DEL-2026-0501</div></div>
  <div class="log-div">↓ ここから先が空欄</div>
  <div class="log-row ng"><div class="lk">受け渡し ID</div><div class="lv">── 別システム（手動確認が必要）</div></div>
  <div class="log-row ng"><div class="lk">受領条件</div><div class="lv">── 契約書参照 / 自動結合なし</div></div>
  <div class="log-row ng"><div class="lk">品質責任者</div><div class="lv">── 権限記録あり / 受け渡しに未結合</div></div>
</div>
<div class="proof-box">
  <div class="proof-title">荷主が証明を求めること</div>
  <p>大阪DCは、5.2℃の状態を確認し、2〜8℃条件の貨物として、品質責任を引き受けた。</p>
</div>
<div class="verdict-box">
  <div class="verdict-item">✗ 温度ログと作業ログをつなぐ受け渡しIDがない</div>
  <div class="verdict-item">✗ 大阪DCが温度条件を確認した記録がない</div>
  <div class="verdict-item">✗ 大阪DCが品質責任を引き受けた記録がない</div>
  <div class="verdict-conclusion">記録がないのではありません。<strong>記録はあります</strong>。しかし、監査のたびに<strong>人が探してつなぎ直している</strong>のであれば、それは証跡の結合ではなく、説明の再構成です。</div>
</div>
""", unsafe_allow_html=True)

if step == 2:
    st.button("荷主から一問きます →", on_click=advance)
    st.stop()

# ── STEP 3 ─────────────────────────────────────
st.markdown("## STEP 3 ── 荷主から、こんな問い合わせが来ました")
st.markdown("""
<div class="q-box">
  <div class="q-label">A製薬（荷主）からの問い合わせ ／ 2026-05-10 大阪DC受け渡し分</div>
  <div class="q-text">先日の配送ですが、大阪DCへの引き渡し時に<br>誰がどんな条件で受け取ったか確認したいので、<br>受け渡し時の記録を1枚送ってもらえますか。<br><br>
  具体的には——<br>
  ・受け取った担当者の名前<br>
  ・受け取った時の温度<br>
  ・2〜8℃の製品として受け取ったことの確認<br>
  ・問題があれば止める条件を確認したかどうか<br><br>
  よろしくお願いします。</div>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div class="proof-box" style="margin-top:12px">
  <div class="proof-title">本来なら即答できるべきこと</div>
  <p>「はい。2026-05-10 12:00、大阪DC 山田花子が、5.2℃を確認のうえ 2〜8℃条件の製品として受け取りました。停止条件は確認済み、受領承認番号は ACC-XXX です。」</p>
</div>
""", unsafe_allow_html=True)

if step == 3:
    st.button("実際に出せるものを確認する →", on_click=advance)
    st.stop()

# ── STEP 4: 記録なし ────────────────────────────
st.markdown("""
<div class="kinasashi">
  <div class="km">人が探して<br>つなぎ直す必要があります。</div>
  <div class="ks">温度ログはあります。作業ログもあります。SOPも契約もあります。しかし「12:00の受け渡しで大阪DCが何℃条件・誰の引受権限で受け取ったか」を機械的に1本の証跡として結合できていません。監査のたびに、誰かが記録を探してつなぎ直しています。</div>
</div>
""", unsafe_allow_html=True)

if step == 4:
    st.button("4つの問いに展開する →", on_click=advance)
    st.stop()

# ── STEP 4 続き: 4問 ────────────────────────────
st.markdown("## STEP 4 ── この一問は、4つの問いに展開されます")
st.markdown(
    "<p style='color:#888;font-size:0.85rem;margin:0 0 10px'>"
    "SOPも契約も記録もある。それでも「この受け渡し」で答えられない理由：</p>",
    unsafe_allow_html=True,
)
for i, (premise, question, answer) in enumerate(AUDIT_4Q, 1):
    st.markdown(f"""
<div class="aq">
  <div class="aq-l">✗ Q{i}</div>
  <div class="aq-premise">{premise}</div>
  <div class="aq-q">{question}</div>
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
  <p>それでも、荷主監査では<strong>説明不能</strong>です。</p>
</div>
""", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#444;line-height:1.75;margin:12px 0;font-size:0.9rem'>"
    "B物流 → 大阪DC の一点で、<strong>温度ログ・作業ログ・受領記録が同じ受け渡しイベントとして結合されていません</strong>。その後の保管・出荷・使用のすべてが、この一点を起点に宙に浮いています。</p>",
    unsafe_allow_html=True,
)
st.markdown("""
<div class="con-warn">
  <p>事故が起きていない日にも、説明不能な配送は完了扱いになっています。</p>
  <p>本当に危ない関門は少ない。でも、そこを外すと会社ごと説明不能になります。</p>
</div>
<div class="con-box">
  <p>温度が守られていたかだけでは、足りません。</p>
  <p>その温度条件のもとで、誰が品質責任を受け取り、どこで止められたかまで、<strong>1本の証跡として再構成できなければ</strong>、内部統制としては不十分です。</p>
</div>
<div class="pro-note">
  <strong>製薬物流・品質保証・GDP対応済みの現場の方へ：</strong><br>
  「うちはGDP・SOP・委託先監査・温度ロガー・WMSで対応しています」——それは正しいです。このデモはその対応を否定しません。問いはただ一つ：<strong>個別の受け渡し単位で、その記録を後から人が探すことなく機械的に1本の証跡として結合できますか？</strong><br>
  「はい」と答えられる現場には、このデモは刺さりません。そうでなければ、刺さります。
</div>
""", unsafe_allow_html=True)

# ── 用語解説 ────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='font-size:0.72rem;font-weight:700;color:#aaa;letter-spacing:0.14em;"
    "text-transform:uppercase;margin:0 0 14px'>このデモで出てくる言葉</p>",
    unsafe_allow_html=True,
)
for term, desc in GLOSSARY:
    st.markdown(
        f'<div class="gloss-term"><div class="gloss-word">{term}</div>'
        f'<div class="gloss-desc">{desc}</div></div>',
        unsafe_allow_html=True,
    )

# ── このデモの射程 ───────────────────────────────
st.markdown("---")
st.markdown("""
<div class="dark-wrap">
  <p class="dark-eyebrow">このデモの次にできること</p>

  <p class="dark-body">この受け渡しで、誰が・何℃条件で・どの責任を引き受けたかが特定できると、<span class="dark-em">荷主は物流会社や倉庫会社の管理を、より本格的に検査できるようになります。</span></p>

  <p class="dark-sub">なぜなら、これまでは</p>
  <div class="dark-quote-block">
    <p class="dark-quote-line">「温度ログはあります」</p>
    <p class="dark-quote-line">「作業記録はあります」</p>
    <p class="dark-quote-line">「契約上はこうなっています」</p>
  </div>
  <p class="dark-sub">という別々の説明に頼っていたものを、</p>
  <div class="dark-proof-block">
    <p class="dark-proof-line">「この1件の受け渡しで、</p>
    <p class="dark-proof-line">大阪DCが5.2℃を確認し、</p>
    <p class="dark-proof-line">2〜8℃条件の貨物として受け取り、</p>
    <p class="dark-proof-line">品質責任を引き受けた」</p>
  </div>
  <p class="dark-sub">という形で確認できるからです。</p>

  <div class="dark-divider"></div>

  <p class="dark-headline">さらにADICは、それが本当に成立していたかまで検査します。</p>
  <p class="dark-body">証跡がつながるだけでは足りません。荷主はさらに一段深く確認できます。</p>
  <div class="dark-check-list">
    <div class="dark-check-item">→ 確認した温度は有効な記録か</div>
    <div class="dark-check-item">→ 確認した人に受領権限はあったか</div>
    <div class="dark-check-item">→ 受領条件は契約・SOPと一致していたか</div>
    <div class="dark-check-item">→ その後の保管・出荷判断まで、同じ条件でつながっていたか</div>
  </div>
  <p class="dark-sub">ADICが見るのは、記録があるかどうかだけではありません。その記録によって、「この受け渡しで品質責任が成立していた」と言えるかまでを検査します。</p>

  <div class="dark-divider"></div>

  <div class="dark-cards">
    <div class="dark-card">
      <div class="dark-card-label">荷主にとって</div>
      <div class="dark-card-text">委託先の品質管理を、配送全体の報告ではなく受け渡し単位で検査できる</div>
    </div>
    <div class="dark-card">
      <div class="dark-card-label">物流会社にとって</div>
      <div class="dark-card-text">自社の管理品質を「言葉」ではなく「証跡」で示せる</div>
    </div>
  </div>

  <div class="dark-divider"></div>

  <p class="dark-closer">これからのコールドチェーンでは、温度を守るだけでは足りません。</p>
  <p class="dark-closer">荷主が委託先の品質管理を、受け渡し単位で検査できること。</p>
  <p class="dark-closer-accent">それが、選ばれる物流の条件になります。</p>

  <p class="dark-sub" style="margin-top:16px">さらに、AIが配車・在庫・出荷判断に入るほど、この検査可能性が必須になります。監査できない物流はブラックボックスになり、監査できる物流だけが荷主から選ばれ続けます。</p>

  <p class="dark-note">※内部的には、責任が切り替わる瞬間を切り出し、ADICで証跡を結合し、成立条件を検査する構成です。</p>
</div>
""", unsafe_allow_html=True)


# ── Footer ──────────────────────────────────────
st.markdown("""
<div class="adic-footer">
  ADIC（Advanced Data Integrity by Ledger of Computation）<br>
  GhostDrift数理研究所 ／ <a href="https://www.ghostdriftresearch.com">ghostdriftresearch.com</a><br>
  Lean 4 形式証明：<a href="https://github.com/GhostDriftTheory/adic-lean-proof-replay">github.com/GhostDriftTheory/adic-lean-proof-replay</a>
</div>
""", unsafe_allow_html=True)
