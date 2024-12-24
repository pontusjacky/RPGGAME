# 地圖生成 - 適應度函數

## 概述

本專案使用演化演算法產生隨機地圖（包含水域、森林、山脈、平原）。

## 適應度函數

適應度函數綜合了以下幾個部分：

1. **多樣性**：必須包含4個地形。
2. **連續性**：地圖中座標類型的連續性，確保最大限度形成連接的區域。
3. **小區域懲罰**：對於小而孤立的區域進行懲罰。
4. **平原與森林的面積**：地圖中的平原面積必須大於森林面積。

### 適應度評分部分

1. **多樣性分數**：
 - 計算地圖中種類地形的多樣性（如水域、森林、山脈、平原）。

2. **連續性分數**：
 - 計算每個地形類型的連續性，。

3. **懲罰分數**：
 - 對於小型孤立區域（小於10、50、100個格子），給予高處罰，區域越大，處罰越小。

4. **平原與森林地帶**：
 - 平原的比例必須大於森林的比例。

###適應度計算公式
```
(0.5 * diversity_score + 0.5 * continuity_score - 2 * penalty_score)*rate
rate = 1 if plate > forest
else = 0.8
```


