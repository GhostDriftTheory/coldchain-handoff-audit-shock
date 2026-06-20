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
/* ── Base ── */
[data-testid="stAppViewContainer"] { background: #fff; }
[data-testid="stMainBlockContainer"] { max-width: 740px; padding-top: 2rem; }
[data-testid="stVerticalBlock"] { gap: 0; }

/* ── Typography ── */
h1 { font-size: 1.7rem !important; font-weight: 800 !important;
     letter-spacing: -0.02em; color: #111; line-height: 1.2 !important; }
h2 { font-size: 1.05rem !important; font-weight: 700 !important;
     color: #444; letter-spacing: 0.04em; text-transform: uppercase;
     border-bottom: 1px solid #e5e5e5; padding-bottom: 8px; margin-bottom: 0 !important; }

/* ── Opening shock ── */
.shock {
    border-left: 5px solid #c53030;
    background: #fff5f5;
    padding: 18px 22px;
    border-radius: 0 6px 6px 0;
    margin: 16px 0 24px;
}
.shock p { margin: 0 0 4px; color: #c53030; font-weight: 700; font-size: 1.15rem; }
.shock p:last-child { margin: 0; }

/* ── Legacy system view ── */
.legacy-table { width: 100%; border-collapse: collapse; margin: 16px 0; }
.legacy-table td { padding: 9px 12px; border-bottom: 1px solid #f0f0f0;
                   font-size: 0.95rem; }
.legacy-table td:first-child { color: #888; width: 120px; white-space: nowrap; }
.legacy-table td:last-child { color: #222; font-weight: 500; }
.status-complete {
    background: #f0fff4; border: 2px solid #38a169;
    border-radius: 6px; padding: 14px 20px; margin: 16px 0;
    text-align: center; font-size: 1.2rem; font-weight: 800; color: #276749;
}

/* ── Player cards ── */
.player-dim {
    background: #f8f8f8; border-radius: 6px; padding: 12px 16px;
    margin: 8px 0; color: #aaa;
}
.player-dim .ptitle { font-weight: 600; color: #bbb; margin-bottom: 4px; }
.player-dim ul { margin: 0; padding-left: 18px; }
.player-dim li { font-size: 0.88rem; line-height: 1.6; }

.player-key {
    background: #fffbeb; border-left: 5px solid #d97706;
    border-radius: 0 8px 8px 0; padding: 18px 22px; margin: 12px 0;
}
.player-key .ptitle { font-weight: 800; color: #92400e; font-size: 1.05rem; margin-bottom: 6px; }
.player-key .prole  { color: #78350f; font-size: 0.9rem; margin-bottom: 10px; }
.player-key .pswitch{ font-weight: 600; color: #b45309; margin: 8px 0 4px; font-size: 0.9rem; }
.player-key ul { margin: 0; padding-left: 18px; }
.player-key li { color: #92400e; font-size: 0.9rem; line-height: 1.7; }

.pivot-note {
    background: #1a1a1a; color: #fff;
    border-radius: 6px; padding: 16px 20px; margin: 20px 0;
    font-weight: 700; font-size: 1rem; line-height: 1.6;
}

/* ── Question ── */
.question-box {
    border: 2px solid #d97706; background: #fffbeb;
    border-radius: 8px; padding: 22px 26px; margin: 16px 0;
}
.q-label { font-size: 0.8rem; font-weight: 700; color: #d97706;
           letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 10px; }
.q-text  { font-size: 1.15rem; font-weight: 800; color: #78350f; line-height: 1.5; }

/* ── 記録なし ── */
.kinasashi {
    background: #c53030; color: #fff;
    border-radius: 10px; padding: 40px 30px; margin: 20px 0;
    text-align: center;
}
.kinasashi .knmain { font-size: 2.6rem; font-weight: 900; letter-spacing: -0.02em;
                      margin-bottom: 8px; }
.kinasashi .knsub  { font-size: 0.95rem; opacity: 0.85; line-height: 1.6; }

/* ── Audit Q's ── */
.audit-q {
    border-left: 3px solid #e53e3e; background: #fff5f5;
    border-radius: 0 6px 6px 0; padding: 12px 16px; margin: 10px 0;
}
.audit-q .aq-label { font-size: 0.8rem; font-weight: 700; color: #e53e3e;
                      text-transform: uppercase; letter-spacing: 0.08em; }
.audit-q .aq-q { font-weight: 600; color: #742a2a; margin: 4px 0 6px; }
.audit-q .aq-ans{ font-size: 0.88rem; color: #e53e3e; }

/* ── Conclusion ── */
.conclusion-warn {
    background: #fffbeb; border-left: 5px solid #d97706;
    border-radius: 0 6px 6px 0; padding: 20px 24px; margin: 20px 0;
}
.conclusion-warn p { color: #92400e; font-weight: 700; font-size: 1.05rem;
                      margin: 0 0 6px; }
.conclusion-warn p:last-child { margin: 0; }

.conclusion-final {
    background: #f7fafc; border-left: 5px solid #4a5568;
    border-radius: 0 6px 6px 0; padding: 20px 24px; margin: 20px 0;
}
.conclusion-final p { color: #2d3748; font-weight: 600; margin: 0 0 6px;
                       line-height: 1.6; }
.conclusion-final p:last-child { margin: 0; }

.adic-footer {
    margin-top: 48px; padding-top: 20px; border-top: 1px solid #e5e5e5;
    color: #aaa; font-size: 0.82rem; line-height: 1.8;
}

/* ── Buttons ── */
div.stButton > button {
    width: 100%; padding: 14px; font-size: 1rem; font-weight: 700;
    border-radius: 6px; margin-top: 24px;
    border: none; cursor: pointer;
    background: #1a1a1a; color: #fff;
    transition: opacity .15s;
}
div.stButton > button:hover { opacity: 0.85; }
div[data-testid="stVerticalBlock"] > div { padding: 0; }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
#  Session state
# ────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 0

step = st.session_state.step

def advance():
    st.session_state.step += 1

# ────────────────────────────────────────────────
#  データ
# ────────────────────────────────────────────────
DELIVERY = {
    "id":      "DEL-2026-0501",
    "cargo":   "インスリン製剤（バイオ医薬品・冷蔵管理対象）",
    "shipper": "田辺製薬株式会社",
    "route":   "田辺製薬 → B物流 → 大阪DC → 中国地区病院群",
    "arrival": "2026-05-10 16:10",
}

AUDIT_4Q = [
    "大阪DCは、何℃条件の貨物として受け取りましたか？",
    "何℃・何分なら止める約束でしたか？",
    "受け渡し時点でその条件を誰が確認しましたか？",
    "大阪DCは品質責任を引き受けた記録を残していますか？",
]

# ────────────────────────────────────────────────
#  タイトル（常時表示）
# ────────────────────────────────────────────────
st.markdown("# 正常完了した配送を、荷主監査にかけます")
st.markdown(
    "<p style='color:#999;font-size:0.95rem;margin:0 0 4px'>温度ログあり。作業記録あり。逸脱警告ゼロ。それでも、説明できない配送があります。</p>",
    unsafe_allow_html=True,
)

st.markdown("""
<div class="shock">
  <p>事故は起きていません。</p>
  <p>温度も守られています。</p>
  <p>でも、荷主から一問聞かれたら答えられません。</p>
</div>
""", unsafe_allow_html=True)

# ── Step 0: opener ──────────────────────────────
if step == 0:
    st.button("確認する →", on_click=advance)
    st.stop()

# ── Step 1: 正常完了画面 ────────────────────────
st.markdown("## STEP 1 ── この配送を見てください")
st.markdown(f"""
<table class="legacy-table">
  <tr><td>配送ID</td>    <td>{DELIVERY['id']}</td></tr>
  <tr><td>貨物</td>      <td>{DELIVERY['cargo']}</td></tr>
  <tr><td>経路</td>      <td>{DELIVERY['route']}</td></tr>
  <tr><td>温度ログ</td>  <td>✓ あり（全区間記録）</td></tr>
  <tr><td>積み替え</td>  <td>✓ あり</td></tr>
  <tr><td>作業記録</td>  <td>✓ あり</td></tr>
  <tr><td>逸脱警告</td>  <td>✓ 0 件</td></tr>
  <tr><td>到着時刻</td>  <td>{DELIVERY['arrival']}</td></tr>
</table>
<div class="status-complete">✓ 配送完了 ── システム上、何も問題ありません。</div>
""", unsafe_allow_html=True)

if step == 1:
    st.button("荷主監査を開始する →", on_click=advance)
    st.stop()

# ── Step 2: プレーヤーと「事故後に聞かれること」 ─
st.markdown("## STEP 2 ── プレーヤーが変わると、事故後に聞かれることが変わる")
st.markdown(
    "<p style='color:#888;font-size:0.9rem;margin:12px 0'>事故や品質問題が起きたとき、荷主・行政・法務から聞かれることはプレーヤーによって違います。</p>",
    unsafe_allow_html=True,
)

st.markdown("""
<div class="player-dim">
  <div class="ptitle">🚛 配送会社（B物流） ── 移動中の温度・時間を守る</div>
  <ul>
    <li>移動中に温度は逸脱しなかったか</li>
    <li>積み替え時に一時逸脱はなかったか</li>
    <li>遅延による時間超過はなかったか</li>
  </ul>
</div>

<div class="player-key">
  <div class="ptitle">🏭 中継倉庫（大阪DC）</div>
  <div class="prole">在庫として受け取り、保管し、出荷する</div>
  <div class="pswitch">
    ここで「誰が何を管理するか」が切り替わります。<br>
    運んでいる間の「温度・時間を守る」から、<br>
    倉庫に入った瞬間から「受け取り・保管・出荷許可の判断」へ。
  </div>
  <ul>
    <li>保管温度・保管時間は管理されていたか</li>
    <li>ロット番号・期限は把握されていたか</li>
    <li>先入先出は守られていたか</li>
    <li>逸脱疑い品の出荷保留判断は誰が行ったか</li>
    <li>出荷可否を誰が承認したか</li>
  </ul>
</div>

<div class="player-dim">
  <div class="ptitle">🏥 納品先（中国地区病院群） ── 受け入れ可否を判断し、使用許可を出す</div>
  <ul>
    <li>受入可否の判断（薬剤師確認）はあったか</li>
    <li>使用可否・品質保証の最終承認は誰が行ったか</li>
    <li>受入拒否時の隔離・連絡フローは踏まれたか</li>
  </ul>
</div>

<div class="pivot-note">
  B物流（配送会社）→ 大阪DC（中継倉庫）の受け渡しは、単なる「荷物の引き渡し」ではありません。<br>
  「誰が・何を・どんな条件で」引き受けたかが問われる、唯一の関門です。
</div>
""", unsafe_allow_html=True)

if step == 2:
    st.button("次へ ── 荷主から一問きます →", on_click=advance)
    st.stop()

# ── Step 3: 一問 ────────────────────────────────
st.markdown("## STEP 3 ── 荷主から、一問だけ来ます")
st.markdown(
    "<p style='color:#888;font-size:0.9rem;margin:12px 0'>受け渡し：B物流（配送会社） → 大阪DC（中継倉庫） ／ 2026-05-10 12:00</p>",
    unsafe_allow_html=True,
)
st.markdown("""
<div class="question-box">
  <div class="q-label">荷主（田辺製薬）からの質問</div>
  <div class="q-text">大阪DCは、この貨物を何℃条件で、<br>誰の責任として受け取りましたか？</div>
</div>
""", unsafe_allow_html=True)

if step == 3:
    st.button("回答を確認する →", on_click=advance)
    st.stop()

# ── Step 4: 記録なし ────────────────────────────
st.markdown("""
<div class="kinasashi">
  <div class="knmain">記録なし。</div>
  <div class="knsub">
    この受け渡しには、温度ログがあります。作業ログもあります。<br>
    しかし「何℃条件で」「誰の責任として」という記録がありません。
  </div>
</div>
""", unsafe_allow_html=True)

if step == 4:
    st.button("4つの問いに展開する →", on_click=advance)
    st.stop()

# ── Step 5: 4問 ─────────────────────────────────
st.markdown("## STEP 4 ── この一問は、4つの問いに展開されます")
st.markdown(
    "<p style='color:#888;font-size:0.9rem;margin:12px 0'>「誰が引き受けたか」は最初の一問に過ぎません。答えられなければ、続く4問がすべて崩れます。</p>",
    unsafe_allow_html=True,
)

for i, q in enumerate(AUDIT_4Q, 1):
    st.markdown(f"""
<div class="audit-q">
  <div class="aq-label">✗ Q{i}</div>
  <div class="aq-q">{q}</div>
  <div class="aq-ans">→ 記録なし</div>
</div>
""", unsafe_allow_html=True)

if step == 5:
    st.button("結論を見る →", on_click=advance)
    st.stop()

# ── Step 6: 結論 ────────────────────────────────
st.markdown("## STEP 5 ── この配送の「完了」は何を意味するか")

st.markdown("""
<div class="conclusion-warn">
  <p>この配送は、温度が守られていました。</p>
  <p>事故は起きていません。</p>
  <p style="margin-top:12px">それでも、荷主監査では<strong>説明不能</strong>です。</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="color:#444;line-height:1.7;margin:16px 0">
B物流 → 大阪DC の一点で、<strong>「誰が、何℃条件で、どんな責任として引き受けたか」</strong>が記録されていなかった。<br>
その後の保管・出荷・使用のすべてが、この一点を起点に宙に浮いています。
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="conclusion-warn">
  <p>事故が起きていない日にも、説明不能な配送は完了扱いになっています。</p>
  <p>本当に危ない関門は少ない。</p>
  <p>でも、その少ない関門を外すと、会社ごと説明不能になります。</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="conclusion-final">
  <p>温度が守られていたかだけでは、足りません。</p>
  <p>その温度条件のもとで、誰が品質責任を受け取り、どこで止められたかまで記録されていなければ、内部統制としては不十分です。</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="adic-footer">
  この「責任消失点」を機械的に検出する内部統制レイヤー：<strong>ADIC</strong>（Advanced Data Integrity by Ledger of Computation）<br>
  GhostDrift数理研究所 ／ <a href="https://www.ghostdriftresearch.com" style="color:#aaa">ghostdriftresearch.com</a><br>
  Lean 4 形式証明：<a href="https://github.com/GhostDriftTheory/adic-lean-proof-replay" style="color:#aaa">github.com/GhostDriftTheory/adic-lean-proof-replay</a>
</div>
""", unsafe_allow_html=True)
