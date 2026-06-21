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
    font-size: 1.5rem !important;
    font-weight: 900 !important;
    letter-spacing: -0.02em;
    color: #111;
    line-height: 1.3 !important;
    margin-bottom: 4px !important;
}
h2 {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    color: #aaa;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    border-bottom: 1px solid #eee;
    padding-bottom: 8px;
    margin: 36px 0 16px !important;
}
/* shock */
.shock {
    border-left: 5px solid #c53030;
    background: #fff5f5;
    padding: 14px 18px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0 18px;
}
.shock p { margin: 2px 0; color: #c53030; font-weight: 700; font-size: 1.05rem; }
/* legacy */
.legacy-wrap { border: 1px solid #eee; border-radius: 8px; overflow: hidden; margin: 12px 0; }
.legacy-row  { display: flex; border-bottom: 1px solid #f5f5f5; font-size: 0.9rem; }
.legacy-row:last-child { border-bottom: none; }
.legacy-key  { width: 100px; flex-shrink:0; padding: 8px 14px; color:#bbb; background:#fafafa; font-size:0.82rem; }
.legacy-val  { padding: 8px 14px; color:#222; font-weight:500; flex:1; }
.status-complete {
    background:#f0fff4; border:2px solid #38a169; border-radius:6px;
    padding:12px 18px; margin:12px 0; text-align:center;
    font-size:1.05rem; font-weight:800; color:#276749;
}
/* pivot note */
.pivot-note {
    background:#f7f7f7; border-radius:6px; padding:12px 16px;
    margin:14px 0; font-size:0.88rem; color:#555; line-height:1.65;
}
.pivot-note strong { color:#111; }
/* log section */
.log-header {
    font-size:0.78rem; font-weight:700; color:#888;
    letter-spacing:0.06em; text-transform:uppercase;
    margin: 18px 0 10px;
}
.log-card {
    border:1px solid #eee; border-radius:8px;
    overflow:hidden; margin:8px 0;
}
.log-card-title {
    background:#f7f7f7; padding:8px 14px;
    font-size:0.82rem; font-weight:700; color:#666;
    border-bottom:1px solid #eee;
}
.log-row {
    display:flex; border-bottom:1px solid #f9f9f9;
    font-size:0.88rem;
}
.log-row:last-child { border-bottom:none; }
.lk { width:110px; flex-shrink:0; padding:7px 14px; color:#bbb; font-size:0.8rem; background:#fafafa; }
.lv { padding:7px 14px; color:#222; font-weight:500; }
.log-row.ng .lk { background:#fff5f5; color:#e53e3e; }
.log-row.ng .lv { color:#e53e3e; }
.log-divider {
    background:#fff5f5; padding:5px 14px;
    font-size:0.75rem; color:#e53e3e; font-weight:600;
    border-top:1px dashed #fca5a5; border-bottom:1px dashed #fca5a5;
}
/* proof / verdict */
.proof-box {
    background:#fffbeb; border:1px solid #fcd34d;
    border-radius:8px; padding:14px 18px; margin:16px 0;
}
.proof-title { font-size:0.75rem; font-weight:700; color:#d97706;
               letter-spacing:0.1em; text-transform:uppercase; margin-bottom:8px; }
.proof-box p { color:#78350f; font-size:0.92rem; line-height:1.65; margin:0; }
.verdict-box {
    background:#fff5f5; border:1px solid #fca5a5;
    border-radius:8px; padding:14px 18px; margin:10px 0;
}
.verdict-item {
    color:#c53030; font-size:0.88rem; font-weight:600;
    padding:3px 0; border-bottom:1px solid #fee2e2; line-height:1.5;
}
.verdict-item:last-of-type { border-bottom:none; }
.verdict-conclusion {
    margin-top:12px; font-size:0.88rem; color:#742a2a; line-height:1.7;
    padding-top:10px; border-top:1px solid #fca5a5;
}
/* question */
.q-box {
    border:2px solid #d97706; background:#fffbeb;
    border-radius:8px; padding:18px 22px; margin:14px 0;
}
.q-label { font-size:0.72rem; font-weight:700; color:#d97706;
           letter-spacing:0.1em; text-transform:uppercase; margin-bottom:8px; }
.q-text  { font-size:1.05rem; font-weight:800; color:#78350f; line-height:1.55; }
/* kinasashi */
.kinasashi {
    background:#c53030; color:#fff; border-radius:10px;
    padding:32px 24px; margin:16px 0; text-align:center;
}
.km { font-size:2rem; font-weight:900; letter-spacing:-0.02em; margin-bottom:8px; line-height:1.2; }
.ks { font-size:0.85rem; opacity:0.85; line-height:1.75; }
/* audit q */
.aq {
    border-left:3px solid #e53e3e; background:#fff5f5;
    border-radius:0 6px 6px 0; padding:10px 14px; margin:8px 0;
}
.aq-l { font-size:0.7rem; font-weight:700; color:#e53e3e;
         text-transform:uppercase; letter-spacing:0.08em; margin-bottom:2px; }
.aq-premise { font-size:0.8rem; color:#aaa; margin-bottom:3px; }
.aq-q { font-weight:700; color:#742a2a; font-size:0.9rem; margin-bottom:4px; }
.aq-a { font-size:0.82rem; color:#e53e3e; }
/* conclusion */
.con-warn {
    background:#fffbeb; border-left:5px solid #d97706;
    border-radius:0 6px 6px 0; padding:14px 18px; margin:12px 0;
}
.con-warn p { color:#92400e; font-weight:700; font-size:0.97rem; margin:0 0 4px; line-height:1.5; }
.con-warn p:last-child { margin:0; }
.con-box {
    background:#f7fafc; border-left:5px solid #4a5568;
    border-radius:0 6px 6px 0; padding:14px 18px; margin:12px 0;
}
.con-box p { color:#2d3748; font-weight:500; margin:0 0 5px; line-height:1.65; font-size:0.9rem; }
.con-box p:last-child { margin:0; }
.pro-note {
    border:1px solid #e2e8f0; border-radius:6px;
    padding:12px 16px; margin:12px 0; font-size:0.82rem;
    color:#718096; line-height:1.75;
}
.pro-note strong { color:#4a5568; }
/* footer */
.adic-footer {
    margin-top:40px; padding-top:16px; border-top:1px solid #eee;
    color:#bbb; font-size:0.78rem; line-height:1.9;
}
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
<div style="background:#f0f4ff;border-left:5px solid #4361ee;border-radius:0 6px 6px 0;padding:14px 18px;margin:0 0 18px">
  <p style="font-size:0.75rem;font-weight:700;color:#4361ee;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 8px">このデモの前提</p>
  <p style="color:#1e3a8a;font-size:0.92rem;margin:0 0 6px;font-weight:600">
    GDP対応していない現場を想定していません。<br>
    むしろ、SOP・契約・温度ログ・入出庫記録が<strong>すべて揃っている現場</strong>を想定しています。
  </p>
  <p style="color:#1e40af;font-size:0.88rem;margin:0;line-height:1.65">
    問いは一つです。<br>
    それらの記録を、<strong>後から人が探して説明するのではなく</strong>、<br>
    この1件の受け渡し証跡として、機械的に結合できますか？
  </p>
</div>

<div class="pivot-note">
  B物流 → 大阪DC の受け渡しは、配送中の「温度を守る責任」から<br>
  倉庫での「受け取り・保管・出荷可否を判断する責任」に<strong>切り替わる唯一の瞬間</strong>です。<br>
  だからここだけは、誰がどんな条件で引き受けたかの証跡が必要です。
</div>
<div class="log-header">B物流 → 大阪DC ／ 2026-05-10 12:00 ／ 実際のログ</div>

<div class="log-card">
  <div class="log-card-title">📊 温度ログ</div>
  <div class="log-row"><div class="lk">時刻</div><div class="lv">12:00</div></div>
  <div class="log-row"><div class="lk">実測温度</div><div class="lv">5.2℃</div></div>
  <div class="log-row"><div class="lk">配送 ID</div><div class="lv">DEL-2026-0501</div></div>
  <div class="log-divider">↓ ここから先が空欄</div>
  <div class="log-row ng"><div class="lk">受け渡し ID</div><div class="lv">── 別システム（手動確認が必要）</div></div>
  <div class="log-row ng"><div class="lk">受領者</div><div class="lv">── 承認記録あり / 本受け渡しに未結合</div></div>
  <div class="log-row ng"><div class="lk">受領条件</div><div class="lv">── SOP参照 / 自動結合なし</div></div>
</div>

<div class="log-card">
  <div class="log-card-title">📋 作業ログ</div>
  <div class="log-row"><div class="lk">時刻</div><div class="lv">12:00</div></div>
  <div class="log-row"><div class="lk">作業</div><div class="lv">B物流 → 大阪DC 引き渡し</div></div>
  <div class="log-row"><div class="lk">配送 ID</div><div class="lv">DEL-2026-0501</div></div>
  <div class="log-divider">↓ ここから先が空欄</div>
  <div class="log-row ng"><div class="lk">受け渡し ID</div><div class="lv">── 別システム（手動確認が必要）</div></div>
  <div class="log-row ng"><div class="lk">受領条件</div><div class="lv">── 契約書参照 / 自動結合なし</div></div>
  <div class="log-row ng"><div class="lk">品質責任者</div><div class="lv">── 権限記録あり / 受け渡しに未結合</div></div>
</div>

<div class="proof-box">
  <div class="proof-title">荷主が証明を求めること</div>
  <p>大阪DCは、5.2℃の状態を確認し、<br>
     2〜8℃条件の貨物として、品質責任を引き受けた。</p>
</div>

<div class="verdict-box">
  <div class="verdict-item">✗ 温度ログと作業ログをつなぐ受け渡しIDがない</div>
  <div class="verdict-item">✗ 大阪DCが温度条件を確認した記録がない</div>
  <div class="verdict-item">✗ 大阪DCが品質責任を引き受けた記録がない</div>
  <div class="verdict-conclusion">
    記録がないのではありません。<strong>記録はあります</strong>。<br>
    しかし、監査のたびに<strong>人が探してつなぎ直している</strong>のであれば、<br>
    それは証跡の結合ではなく、説明の再構成です。
  </div>
</div>
""", unsafe_allow_html=True)

if step == 2:
    st.button("荷主から一問きます →", on_click=advance)
    st.stop()

# ── STEP 3 ─────────────────────────────────────
st.markdown("## STEP 3 ── 荷主から、一問だけ来ます")
st.markdown(
    "<p style='color:#bbb;font-size:0.82rem;margin:4px 0 12px'>"
    "受け渡し：B物流 → 大阪DC ／ 2026-05-10 12:00</p>",
    unsafe_allow_html=True,
)
st.markdown("""
<div class="q-box">
  <div class="q-label">A製薬（荷主）からの質問</div>
  <div class="q-text">
    この配送 DEL-2026-0501 の 12:00 の受け渡しについて——<br>
    契約上の温度条件、実測温度、受領者、受領承認が、<br>
    同じ受け渡し証跡として出せますか？
  </div>
</div>
""", unsafe_allow_html=True)

if step == 3:
    st.button("回答を確認する →", on_click=advance)
    st.stop()

# ── STEP 4 : 記録なし ───────────────────────────
st.markdown("""
<div class="kinasashi">
  <div class="km">人が探して<br>つなぎ直す必要があります。</div>
  <div class="ks">
    温度ログはあります。作業ログもあります。SOPも契約もあります。<br>
    しかし「12:00 の受け渡しで大阪DCが何℃条件・誰の引受権限で受け取ったか」を<br>
    機械的に1本の証跡として結合できていません。<br>
    監査のたびに、誰かが記録を探してつなぎ直しています。
  </div>
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
  <p style="margin-top:8px">それでも、荷主監査では<strong>説明不能</strong>です。</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="color:#444;line-height:1.75;margin:12px 0;font-size:0.9rem">
B物流 → 大阪DC の一点で、<strong>温度ログ・作業ログ・受領記録が同じ受け渡しイベントとして結合されていません</strong>。<br>
その後の保管・出荷・使用のすべてが、この一点を起点に宙に浮いています。
</p>
""", unsafe_allow_html=True)

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
  「うちはGDP・SOP・委託先監査・温度ロガー・WMSで対応しています」——それは正しいです。<br>
  このデモはその対応を否定しません。<br>
  問いはただ一つ：<strong>個別の受け渡し単位で、その記録を後から人が探すことなく機械的に1本の証跡として結合できますか？</strong><br>
  「はい」と答えられる現場には、このデモは刺さりません。そうでなければ、刺さります。
</div>

<div class="adic-footer">
  この「記録はあるが結合されていない」状態を機械的に検出し、受け渡し単位で証跡を自動結合する内部統制レイヤー：<strong>ADIC</strong>（Advanced Data Integrity by Ledger of Computation）<br>
  GhostDrift数理研究所 ／ <a href="https://www.ghostdriftresearch.com">ghostdriftresearch.com</a><br>
  Lean 4 形式証明：<a href="https://github.com/GhostDriftTheory/adic-lean-proof-replay">github.com/GhostDriftTheory/adic-lean-proof-replay</a>
</div>
""", unsafe_allow_html=True)
