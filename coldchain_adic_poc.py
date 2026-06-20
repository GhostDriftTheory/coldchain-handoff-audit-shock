#!/usr/bin/env python3
"""
正常完了した配送を、荷主監査にかけます。

温度ログあり。作業記録あり。逸脱警告ゼロ。
それでも、説明できない配送があります。
"""

# ──────────────────────────────────────────────
#  ANSI カラー
# ──────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

def B(s):    return f"{BOLD}{s}{RESET}"
def G(s):    return f"{GREEN}{s}{RESET}"
def R(s):    return f"{RED}{s}{RESET}"
def Y(s):    return f"{YELLOW}{s}{RESET}"
def C(s):    return f"{CYAN}{s}{RESET}"
def D(s):    return f"{DIM}{s}{RESET}"
def ok(s):   return f"{GREEN}✓  {s}{RESET}"
def ng(s):   return f"{RED}✗  {s}{RESET}"

W = 70

def rule(c="─"): print(D(c * W))
def blank():     print()
def pause(msg="  [Enter] で続ける..."): input(D(msg))

# ──────────────────────────────────────────────
#  データ
# ──────────────────────────────────────────────

# 各プレーヤーが本来管理すべき「致命変数」
FATAL_VARIABLES = [
    {
        "player": "配送会社（B物流）",
        "role":   "移動中の温度・時間を守る",
        "fatal":  [
            "移動中の温度逸脱",
            "積み替え時の一時逸脱",
            "遅延による時間超過",
        ],
        "icon": "🚛",
    },
    {
        "player": "中継倉庫（大阪DC）",
        "role":   "在庫として受け取り、管理し、出荷する",
        "fatal":  [
            "保管温度・保管時間の管理",
            "ロット番号・期限の把握",
            "先入先出の遵守",
            "逸脱疑い品の出荷保留判断",
            "出荷可否を誰が承認したか",
        ],
        "icon": "🏭",
        "key": True,   # ← ここが変数切替点
    },
    {
        "player": "納品先（C病院グループ）",
        "role":   "受け入れ可否を判断し、使用許可を出す",
        "fatal":  [
            "受入可否の判断（薬剤師確認）",
            "使用可否・品質保証の最終承認",
            "受入拒否時の隔離・連絡フロー",
        ],
        "icon": "🏥",
    },
]

# 監査対象の配送
DELIVERY = {
    "id":      "DEL-2026-0501",
    "cargo":   "インスリン製剤（バイオ医薬品・冷蔵管理対象）",
    "shipper": "A製薬株式会社",
    "route":   ["A製薬", "B物流", "大阪DC", "C病院グループ"],
    "arrival": "2026-05-10 16:10",
    # 既存システムの表示
    "legacy": {
        "temp_log":  "あり（全区間記録）",
        "transfer":  "あり",
        "workers":   "あり",
        "alerts":    "0 件",
        "status":    "配送完了",
    },
    # 問題の受け渡し（B物流→大阪DC）
    "collapse_handoff": {
        "from": "B物流（配送会社）",
        "to":   "大阪DC（中継倉庫）",
        "time": "2026-05-10 12:00",
        # 4問への展開
        "audit_4": [
            ("大阪DCは、何℃条件の貨物として受け取りましたか？",    False, None),
            ("何℃・何分なら止める約束でしたか？",                  False, None),
            ("受け渡し時点でその条件を誰が確認しましたか？",         False, None),
            ("大阪DCは品質責任を引き受けた記録を残していますか？",   False, None),
        ],
    },
}

# ──────────────────────────────────────────────
#  メイン
# ──────────────────────────────────────────────

def main():

    # ──────────────────
    # タイトル
    # ──────────────────
    blank()
    print(B("╔" + "═"*(W-2) + "╗"))
    print(B("║") + f"{'正常完了した配送を、荷主監査にかけます':^{W-4}}  " + B("║"))
    print(B("╠" + "═"*(W-2) + "╣"))
    print(B("║") + D(f"{'温度ログあり。作業記録あり。逸脱警告ゼロ。':^{W-3}} ") + B("║"))
    print(B("║") + D(f"{'それでも、説明できない配送があります。':^{W-2}}") + B("║"))
    print(B("╚" + "═"*(W-2) + "╝"))
    blank()

    blank()
    print(R(B("  事故は起きていません。")))
    print(R(B("  温度も守られています。")))
    print(R(B("  でも、荷主から一問聞かれたら答えられません。")))
    blank()
    pause("  [Enter] で確認する...")

    # ──────────────────
    # STEP 1: 正常完了画面
    # ──────────────────
    blank()
    print(B(C(f"  STEP 1  ──  この配送を見てください")))
    rule("━")
    blank()

    leg = DELIVERY["legacy"]
    print(f"  {B('配送ID    :')} {DELIVERY['id']}")
    print(f"  {B('貨物      :')} {DELIVERY['cargo']}")
    print(f"  {B('経路      :')} {' → '.join(DELIVERY['route'])}")
    print(f"  {B('温度ログ  :')} {leg['temp_log']}")
    print(f"  {B('積み替え  :')} {leg['transfer']}")
    print(f"  {B('作業記録  :')} {leg['workers']}")
    print(f"  {B('逸脱警告  :')} {leg['alerts']}")
    print(f"  {B('到着時刻  :')} {DELIVERY['arrival']}")
    blank()
    print(f"  {B('ステータス:')}  {G(B('✓  配送完了  ──  システム上、何も問題ありません。'))}")
    blank()

    pause()

    # ──────────────────
    # STEP 2: プレーヤーごとの致命変数
    # ──────────────────
    blank()
    print(B(C(f"  STEP 2  ──  プレーヤーが変わると、事故後に聞かれることが変わる")))
    rule("━")
    blank()
    print(D("  事故や品質問題が起きたとき、荷主・行政・法務から聞かれることは"))
    print(D("  プレーヤーによって違います。"))
    blank()

    for p in FATAL_VARIABLES:
        is_key = p.get("key", False)
        if is_key:
            blank()
            print(Y(B(f"  {p['icon']}  {p['player']}")))
            print(Y(f"     役割：{p['role']}"))
            print(Y(f"     ここで「誰が何を管理するか」が切り替わります。"))
            print(Y(f"     運んでいる間に守ること（温度・時間）ではなく、"))
            print(Y(f"     倉庫に入った瞬間から、受け取り・保管・出荷許可の判断へ。"))
            blank()
            print(Y(f"     事故後に必ず聞かれること："))
            for v in p["fatal"]:
                print(Y(f"       ・{v}"))
            blank()
        else:
            print(D(f"  {p['icon']}  {p['player']}  ──  {p['role']}"))
            for v in p["fatal"]:
                print(D(f"       ・{v}"))
            blank()

    rule()
    blank()
    print(B("  つまり B物流（配送会社）→ 大阪DC（中継倉庫）の受け渡しは、"))
    print(B("  単なる「貨物の受け渡し」ではありません。"))
    blank()
    print(B(Y("  「誰が・何を・どんな条件で」引き受けたかが問われる、唯一の関門です。")))
    blank()
    print(D("  ここで「誰が、何を、どんな条件で引き受けたか」が記録されていなければ、"))
    print(D("  その後の保管・出荷・使用のすべてが宙に浮きます。"))
    blank()

    pause()

    # ──────────────────
    # STEP 3: 荷主から一問
    # ──────────────────
    blank()
    print(B(C(f"  STEP 3  ──  荷主から、一問だけ来ます")))
    rule("━")
    blank()
    blank()

    h = DELIVERY["collapse_handoff"]
    hfrom, hto, htime = h["from"], h["to"], h["time"]
    print(f"  {D(f'受け渡し：{hfrom} → {hto}  {htime}')}")
    blank()
    print(B(Y("  荷主（A製薬）からの質問：")))
    blank()
    print(B(f"  「 大阪DCは、この貨物を何℃条件で、"))
    print(B(f"      誰の責任として受け取りましたか？ 」"))
    blank()
    blank()

    pause("  [Enter] で回答を確認...")

    blank()
    print(R(B("  " + "─"*60)))
    print(R(B("  記録なし。")))
    print(R(B("  " + "─"*60)))
    blank()
    print(R("  この受け渡しには、温度ログがあります。"))
    print(R("  作業ログもあります。"))
    print(R("  しかし「何℃条件で」「誰の責任として」という記録がありません。"))
    blank()

    pause()

    # ──────────────────
    # STEP 4: 一問 → 4問に展開
    # ──────────────────
    blank()
    print(B(C(f"  STEP 4  ──  この一問は、4つの問いに展開されます")))
    rule("━")
    blank()
    print(D("  荷主監査では、「誰が引き受けたか」は最初の一問に過ぎません。"))
    print(D("  答えられなければ、続きの4問がすべて崩れます。"))
    blank()

    hfrom2, hto2 = h["from"], h["to"]
    print(f"  {R(B(f'受け渡し：{hfrom2} → {hto2}'))}")
    blank()

    for i, (question, answered, answer) in enumerate(h["audit_4"], 1):
        if answered:
            print(f"    {ok(f'Q{i}. {question}')}")
            if answer:
                print(D(f"         → {answer}"))
        else:
            print(f"    {ng(f'Q{i}. {question}')}")
            print(R(f"         → 記録なし"))
        blank()

    pause()

    # ──────────────────
    # STEP 5: 結論
    # ──────────────────
    blank()
    print(B(C(f"  STEP 5  ──  この配送の「完了」は何を意味するか")))
    rule("━")
    blank()
    print("  この配送は、温度が守られていました。")
    print("  事故は起きていません。")
    blank()
    rule()
    blank()
    print(R(B("  それでも、荷主監査では説明不能です。")))
    blank()
    print(R("  なぜか。"))
    blank()
    print(R("  B物流 → 大阪DC の一点で、"))
    print(R("  「誰が、何℃条件で、どんな責任として引き受けたか」"))
    print(R("  が記録されていないからです。"))
    blank()
    print(R("  その後の保管・出荷・使用のすべてが、"))
    print(R("  この一点を起点に宙に浮いています。"))
    blank()
    rule()
    blank()
    print(Y(B("  事故が起きていない日にも、")))
    print(Y(B("  説明不能な配送は完了扱いになっています。")))
    blank()
    print(Y(B("  そして、本当に危ない関門は少ない。")))
    print(Y(B("  でも、その少ない関門を外すと、")))
    print(Y(B("  会社ごと説明不能になります。")))
    blank()
    rule("━")
    blank()
    print("  温度が守られていたかだけでは、足りません。")
    blank()
    print(B("  その温度条件のもとで、"))
    print(B("  誰が品質責任を受け取り、"))
    print(B("  どこで止められたかまで記録されていなければ、"))
    print(B("  内部統制としては不十分です。"))
    blank()
    rule("━")
    blank()
    print(D("  この「責任消失点」を機械的に検出する内部統制レイヤー：ADIC"))
    print(D("  GhostDrift数理研究所  /  https://www.ghostdriftresearch.com"))
    blank()


if __name__ == "__main__":
    main()
