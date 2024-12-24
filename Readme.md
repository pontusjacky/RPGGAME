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
 ```
  diversity_score = 1    #所有區域都有出現
  diversity_score = 0    #否則
 ```
2. **連續性分數**：
 - 計算每個地形類型的連續性。
 ```
  continuity_score = 每個像素的鄰居地形一盪的數量/8 * 所有像素   
 ```

3. **懲罰分數**：
 - 對於小型孤立區域（小於10、50、100個格子），給予高處罰，區域越大，處罰越小。
 ```
  penalty_score < 10     #懲罰1倍
  penalty_score < 50     #懲罰25倍
  penalty_score < 10     #懲罰50倍
 ```
4. **平原與森林地帶**：
 - 平原的比例必須大於森林的比例。
 ```
  rate = 1     if plate > forest
  rate = 0.8   if plate < forest
 ```
###適應度計算公式
```
fitness score = (0.5 * diversity_score + 0.5 * continuity_score - 2 * penalty_score)*rate
rate = 1     if plate > forest
rate = 0.8   if plate < forest
```

## 測試
使用參數：population_size = 1000
genrations = 200
範例:
![image](https://github.com/pontusjacky/RPGGAME/blob/main/output1/generation_1000_1.png)


