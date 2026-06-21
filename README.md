# coldchain-handoff-audit-shock

**正常完了した配送を、荷主監査にかけます。**

温度ログあり。作業記録あり。逸脱警告ゼロ。  
それでも、説明できない配送があります。

---

## これは何か

製薬品の冷蔵配送を1件取り上げ、荷主監査で崩れる瞬間を体感するデモです。

> **事故は起きていません。温度も守られています。**  
> **でも、荷主から一問聞かれたら答えられません。**

「記録がないから怖い」ではありません。  
**記録はある。でも、別々の記録が1件の受け渡し証跡としてつながっていない。**

それが怖い。

---

## このデモが想定する現場

GDP未対応の、ずさんな物流現場を想定していません。

**SOP・契約・温度ログ・入出庫記録がすべて揃っている現場を想定しています。**

問いはただ一つです。

> それらの記録を、後から人が探して説明するのではなく、  
> この1件の受け渡し証跡として、機械的に結合できますか？

---

## デモの流れ（5ステップ）

| ステップ | 内容 |
|---|---|
| STEP 1 | 配送ステータス確認 ── 温度ログ・作業記録・逸脱警告ゼロ・配送完了。すべて正常に見える |
| STEP 2 | 温度ログと作業ログを実際に表示 ── 記録はある。でも、受け渡しIDが両方とも空欄 |
| STEP 3 | 荷主からの一問 ── 契約上の温度条件・実測温度・受領者・受領承認を同じ証跡として出せますか？ |
| STEP 4 | 人が探してつなぎ直す必要があります → 4問に展開される |
| STEP 5 | 結論 ── 事故が起きていない日にも、説明不能な配送は完了扱いになっている |

STEP 2 の核心：

```
📊 温度ログ          📋 作業ログ
時刻: 12:00          時刻: 12:00
実測温度: 5.2℃       作業: B物流→大阪DC
配送ID: DEL-2026     配送ID: DEL-2026
↓ ここから先が空欄   ↓ ここから先が空欄
受け渡しID: ── 別システム（手動確認が必要）
受領条件:   ── SOP参照 / 自動結合なし
品質責任者: ── 権限記録あり / 受け渡しに未結合
```

---

## このデモの次にできること

この受け渡しで、誰が・何℃条件で・どの責任を引き受けたかが特定できると、  
**荷主は物流会社や倉庫会社の管理を、受け渡し単位で検査できるようになります。**

さらに ADIC は、「証跡がつながっているか」だけでなく、  
**「その受け渡しで品質責任が本当に成立していたか」まで検査します。**

- 確認した温度は有効な記録か
- 確認した人に受領権限はあったか
- 受領条件は契約・SOP と一致していたか
- その後の保管・出荷判断まで、同じ条件でつながっていたか

その先では、この貨物を出荷してよいか・一時保留か・品質確認か・出荷不可かまで  
記録に基づいて判断できるようになります（RELEASE / HOLD / QA_REVIEW / REJECT）。

---

## コアメッセージ

```
コールドチェーンでは、温度が守られていたかだけでは足りない。

荷主が委託先の品質管理を、
受け渡し単位で検査できること。

それが、選ばれる物流の条件になる。
```

---

## 起動方法

```bash
git clone https://github.com/GhostDriftTheory/coldchain-handoff-audit-shock
cd coldchain-handoff-audit-shock
pip install -r requirements.txt
streamlit run app.py
```

ブラウザで `http://localhost:8501` が開きます。

---

## ファイル構成

```
coldchain-handoff-audit-shock/
├── app.py                   ← Streamlit デモ（メイン）
├── coldchain_adic_poc.py    ← CLI 版（ターミナルのみで動く）
├── requirements.txt         ← streamlit のみ
└── README.md
```

**CLI 版**（外部ライブラリ不要、Python 3.7+）:

```bash
python3 coldchain_adic_poc.py
```

---

## 背景：ADIC と GhostDrift

- **ADIC**（Advanced Data Integrity by Ledger of Computation）  
  記録の「有無」ではなく、記録が1件の受け渡し証跡として結合され、  
  その責任が本当に成立していたかを機械的に検査する内部統制レイヤー

- **Lean 4 形式証明**：[github.com/GhostDriftTheory/adic-lean-proof-replay](https://github.com/GhostDriftTheory/adic-lean-proof-replay)
- **プレスリリース**：[prtimes.jp/main/html/rd/p/000000001.000182721.html](https://prtimes.jp/main/html/rd/p/000000001.000182721.html)
- **和算2.0**：[ghostdriftresearch.com/wasan20](https://www.ghostdriftresearch.com/wasan20)
- **GhostDrift数理研究所**：[ghostdriftresearch.com](https://www.ghostdriftresearch.com)


