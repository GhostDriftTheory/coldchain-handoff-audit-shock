# coldchain-handoff-audit-shock

**正常完了した配送を、荷主監査にかけます。**

温度ログあり。作業記録あり。逸脱警告ゼロ。  
それでも、説明できない配送があります。

---

## これは何か

製薬品の冷蔵配送を1件取り上げ、荷主監査で崩れる瞬間を見せるデモです。

既存の配送管理システム上は「正常完了」に見える配送が、  
荷主から一問聞かれただけで「説明不能」に反転する——その構造を体感するためのツールです。

> **事故は起きていません。温度も守られています。  
> でも、荷主から一問聞かれたら答えられません。**

---

## デモの流れ（5ステップ）

| ステップ | 内容 |
|---|---|
| STEP 1 | 配送ステータス確認 ── 温度ログあり・逸脱警告ゼロ・配送完了 |
| STEP 2 | プレーヤーごとの「事故後に聞かれること」── 倉庫で切り替わる責任変数 |
| STEP 3 | 荷主からの一問 ── 大阪DCは何℃条件で、誰の責任として受け取りましたか？ |
| STEP 4 | 記録なし → 4問に展開される |
| STEP 5 | 結論 ── 事故が起きていない日にも、説明不能な配送は完了扱いになっている |

**核心：** ログの「有無」ではなく、「ログ体系が品質責任の移転を証明できるか」が問われます。

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
├── coldchain_adic_poc.py    ← CLI 版（ターミナルで実行可）
├── requirements.txt         ← streamlit のみ
└── README.md
```

### CLI 版の実行

```bash
python3 coldchain_adic_poc.py
```

Python 3.7+ のみ。外部ライブラリ不要。

---

## コアメッセージ

```
コールドチェーンでは、温度が守られていたかだけでは足りない。

その温度条件のもとで、
誰が品質責任を受け取り、
どこで止められたかまで記録されていなければ、
内部統制としては不十分である。
```

---

## 背景：ADIC と GhostDrift

- **ADIC**（Advanced Data Integrity by Ledger of Computation）  
  AI・自動化システムの判断過程を、第三者が後から再検証できる証拠として残す技術

- **Lean 4 形式証明**：https://github.com/GhostDriftTheory/adic-lean-proof-replay
- **プレスリリース**：https://prtimes.jp/main/html/rd/p/000000001.000182721.html
- **和算2.0**：https://www.ghostdriftresearch.com/wasan20
- **GhostDrift数理研究所**：https://www.ghostdriftresearch.com

---

## ライセンス

MIT
