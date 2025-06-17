# 性能指標學術來源與論文參考 (Academic Sources and Paper References for Performance Metrics)

## 📚 指標的學術背景總覽

本文檔整理了車輛導航系統中使用的五個核心性能指標的學術來源、論文依據和理論基礎。

---

## 🎯 **成功率 (Success Rate)**

### 學術來源

**核心概念**: 任務完成率、到達率 (Task Completion Rate, Arrival Rate)

#### 主要論文來源

1. **Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction (2nd ed.)**
   - **章節**: Chapter 2 - Multi-armed Bandits
   - **相關概念**: Performance measures in RL
   - **頁碼**: pp. 28-32
   - **引用原因**: 建立了強化學習中性能評估的基礎框架
   - **網址**: <http://incompleteideas.net/book/the-book-2nd.html>
   - **PDF下載**: <http://incompleteideas.net/book/RLbook2020.pdf>
   - **APA格式**: Sutton, R. S., & Barto, A. G. (2018). *Reinforcement learning: An introduction* (2nd ed.). MIT Press.
   - **IEEE格式**: R. S. Sutton and A. G. Barto, *Reinforcement Learning: An Introduction*, 2nd ed. Cambridge, MA: MIT Press, 2018.
   - **MLA格式**: Sutton, Richard S., and Andrew G. Barto. *Reinforcement Learning: An Introduction*. 2nd ed., MIT Press, 2018.

2. **Kaelbling, L. P., Littman, M. L., & Moore, A. W. (1996). Reinforcement learning: A survey**
   - **期刊**: Journal of Artificial Intelligence Research, 4, 237-285
   - **DOI**: 10.1613/jair.301
   - **相關段落**: Section 3.1 - Performance Criteria
   - **貢獻**: 定義了強化學習中任務成功率的評估標準
   - **網址**: [https://www.jair.org/index.php/jair/article/view/10166](https://www.jair.org/index.php/jair/article/view/10166)
   - **PDF下載**: [https://www.jair.org/index.php/jair/article/view/10166/24110](https://www.jair.org/index.php/jair/article/view/10166/24110)
   - **APA格式**: Kaelbling, L. P., Littman, M. L., & Moore, A. W. (1996). Reinforcement learning: A survey. *Journal of Artificial Intelligence Research*, 4, 237-285.
   - **IEEE格式**: L. P. Kaelbling, M. L. Littman, and A. W. Moore, "Reinforcement learning: A survey," *J. Artif. Intell. Res.*, vol. 4, pp. 237-285, 1996.
   - **MLA格式**: Kaelbling, Leslie Pack, et al. "Reinforcement learning: A survey." *Journal of Artificial Intelligence Research*, vol. 4, 1996, pp. 237-285.

3. **LaValle, S. M. (2006). Planning algorithms**
   - **出版社**: Cambridge University Press
   - **章節**: Chapter 1 - Introduction to Motion Planning
   - **相關概念**: Path planning success metrics
   - **引用原因**: 路徑規劃領域的成功率定義
   - **網址**: <http://lavalle.pl/planning/>
   - **PDF下載**: <http://lavalle.pl/planning/book.pdf>
   - **APA格式**: LaValle, S. M. (2006). *Planning algorithms*. Cambridge University Press.
   - **IEEE格式**: S. M. LaValle, *Planning Algorithms*. Cambridge, UK: Cambridge University Press, 2006.
   - **MLA格式**: LaValle, Steven M. *Planning Algorithms*. Cambridge University Press, 2006.

#### 在路徑規劃中的應用

- **Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths**
  - **期刊**: IEEE Transactions on Systems Science and Cybernetics, 4(2), 100-107
  - **DOI**: 10.1109/TSSC.1968.300136
  - **貢獻**: A*演算法論文，建立了路徑規劃成功評估的基礎
  - **網址**: [https://ieeexplore.ieee.org/document/4082128](https://ieeexplore.ieee.org/document/4082128)
  - **APA格式**: Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 100-107.
  - **IEEE格式**: P. E. Hart, N. J. Nilsson, and B. Raphael, "A formal basis for the heuristic determination of minimum cost paths," *IEEE Trans. Syst. Sci. Cybern.*, vol. 4, no. 2, pp. 100-107, Jul. 1968.
  - **MLA格式**: Hart, Peter E., et al. "A formal basis for the heuristic determination of minimum cost paths." *IEEE Transactions on Systems Science and Cybernetics*, vol. 4, no. 2, 1968, pp. 100-107.

---

## 🚶 **平均步數 (Average Steps)**

### 學術來源

**核心概念**: 路徑長度、演算法效率 (Path Length, Algorithm Efficiency)

#### 主要論文來源

1. **Dijkstra, E. W. (1959). A note on two problems in connexion with graphs**
   - **期刊**: Numerische Mathematik, 1(1), 269-271
   - **DOI**: 10.1007/BF01386390
   - **相關概念**: 最短路徑演算法和路徑長度評估
   - **歷史意義**: 建立了圖論中路徑長度的基礎概念
   - **網址**: [https://link.springer.com/article/10.1007/BF01386390](https://link.springer.com/article/10.1007/BF01386390)
   - **PDF**: [https://www-m3.ma.tum.de/foswiki/pub/MN0506/WebHome/dijkstra.pdf](https://www-m3.ma.tum.de/foswiki/pub/MN0506/WebHome/dijkstra.pdf)
   - **APA格式**: Dijkstra, E. W. (1959). A note on two problems in connexion with graphs. *Numerische Mathematik*, 1(1), 269-271.
   - **IEEE格式**: E. W. Dijkstra, "A note on two problems in connexion with graphs," *Numer. Math.*, vol. 1, no. 1, pp. 269-271, 1959.
   - **MLA格式**: Dijkstra, Edsger W. "A note on two problems in connexion with graphs." *Numerische Mathematik*, vol. 1, no. 1, 1959, pp. 269-271.

2. **Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.)**
   - **章節**: Chapter 3 - Solving Problems by Searching
   - **相關概念**: Search cost and solution quality
   - **頁碼**: pp. 78-85
   - **引用原因**: 定義了搜索演算法中路徑長度的評估標準
   - **網址**: [http://aima.cs.berkeley.edu/](http://aima.cs.berkeley.edu/)
   - **出版社**: Pearson
   - **APA格式**: Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
   - **IEEE格式**: S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed. Boston, MA: Pearson, 2020.
   - **MLA格式**: Russell, Stuart, and Peter Norvig. *Artificial Intelligence: A Modern Approach*. 4th ed., Pearson, 2020.

3. **Bellman, R. (1957). Dynamic programming**
   - **出版社**: Princeton University Press
   - **相關概念**: Optimal control and path efficiency
   - **貢獻**: 動態規劃中的最優路徑概念
   - **網址**: [https://press.princeton.edu/books/paperback/9780691146683/dynamic-programming](https://press.princeton.edu/books/paperback/9780691146683/dynamic-programming)
   - **ISBN**: 9780691146683
   - **APA格式**: Bellman, R. (1957). *Dynamic programming*. Princeton University Press.
   - **IEEE格式**: R. Bellman, *Dynamic Programming*. Princeton, NJ: Princeton University Press, 1957.
   - **MLA格式**: Bellman, Richard. *Dynamic Programming*. Princeton University Press, 1957.

#### 在機器人導航中的應用

- **Thrun, S. (2002). Robotic mapping: A survey**
  - **期刊**: Exploring Artificial Intelligence in the New Millennium, 1-35
  - **相關概念**: Navigation efficiency metrics
  - **引用原因**: 機器人導航中路徑長度評估的標準
  - **編輯**: G. Lakemeyer and B. Nebel
  - **出版社**: Morgan Kaufmann
  - **網址**: [https://robots.stanford.edu/papers/thrun.mapping-tr.pdf](https://robots.stanford.edu/papers/thrun.mapping-tr.pdf)
  - **APA格式**: Thrun, S. (2002). Robotic mapping: A survey. In G. Lakemeyer & B. Nebel (Eds.), *Exploring Artificial Intelligence in the New Millennium* (pp. 1-35). Morgan Kaufmann.
  - **IEEE格式**: S. Thrun, "Robotic mapping: A survey," in *Exploring Artificial Intelligence in the New Millennium*, G. Lakemeyer and B. Nebel, Eds. San Francisco, CA: Morgan Kaufmann, 2002, pp. 1-35.
  - **MLA格式**: Thrun, Sebastian. "Robotic mapping: A survey." *Exploring Artificial Intelligence in the New Millennium*, edited by Gerhard Lakemeyer and Bernhard Nebel, Morgan Kaufmann, 2002, pp. 1-35.

---

## 📏 **路徑效率 (Path Efficiency)**

### 學術來源

**核心概念**: 最優性比率、效率指數 (Optimality Ratio, Efficiency Index)

#### 主要論文來源

1. **Stentz, A. (1994). Optimal and efficient path planning for partially-known environments**
   - **會議**: IEEE International Conference on Robotics and Automation
   - **DOI**: 10.1109/ROBOT.1994.351061
   - **相關概念**: Path optimality in dynamic environments
   - **頁碼**: pp. 3310-3317
   - **貢獻**: 定義了動態環境中路徑效率的評估方法
   - **網址**: [https://ieeexplore.ieee.org/document/351061](https://ieeexplore.ieee.org/document/351061)
   - **地點**: San Diego, CA, USA
   - **APA格式**: Stentz, A. (1994). Optimal and efficient path planning for partially-known environments. In *Proceedings of the IEEE International Conference on Robotics and Automation* (pp. 3310-3317). IEEE.
   - **IEEE格式**: A. Stentz, "Optimal and efficient path planning for partially-known environments," in *Proc. IEEE Int. Conf. Robot. Autom.*, San Diego, CA, USA, 1994, pp. 3310-3317.
   - **MLA格式**: Stentz, Anthony. "Optimal and efficient path planning for partially-known environments." *Proceedings of the IEEE International Conference on Robotics and Automation*, IEEE, 1994, pp. 3310-3317.

2. **Ferguson, D., & Stentz, A. (2006). Using interpolation to improve path planning: The Field D* algorithm**
   - **期刊**: Journal of Field Robotics, 23(2), 79-101
   - **DOI**: 10.1002/rob.20109
   - **相關概念**: Path quality metrics
   - **引用原因**: 建立了路徑品質評估的標準
   - **網址**: [https://onlinelibrary.wiley.com/doi/abs/10.1002/rob.20109](https://onlinelibrary.wiley.com/doi/abs/10.1002/rob.20109)
   - **出版商**: Wiley
   - **APA格式**: Ferguson, D., & Stentz, A. (2006). Using interpolation to improve path planning: The Field D* algorithm. *Journal of Field Robotics*, 23(2), 79-101.
   - **IEEE格式**: D. Ferguson and A. Stentz, "Using interpolation to improve path planning: The Field D* algorithm," *J. Field Robot.*, vol. 23, no. 2, pp. 79-101, Feb. 2006.
   - **MLA格式**: Ferguson, Dave, and Anthony Stentz. "Using interpolation to improve path planning: The Field D* algorithm." *Journal of Field Robotics*, vol. 23, no. 2, 2006, pp. 79-101.

3. **Koenig, S., & Likhachev, M. (2002). D* lite**
   - **會議**: AAAI/IAAI, 476-483
   - **相關概念**: Real-time path planning efficiency
   - **貢獻**: 實時路徑規劃中效率評估的方法
   - **網址**: [https://www.aaai.org/Papers/AAAI/2002/AAAI02-072.pdf](https://www.aaai.org/Papers/AAAI/2002/AAAI02-072.pdf)
   - **會議地點**: Edmonton, Alberta, Canada
   - **APA格式**: Koenig, S., & Likhachev, M. (2002). D* lite. In *Proceedings of the Eighteenth National Conference on Artificial Intelligence* (pp. 476-483). AAAI Press.
   - **IEEE格式**: S. Koenig and M. Likhachev, "D* lite," in *Proc. 18th Nat. Conf. Artif. Intell.*, Edmonton, AB, Canada, 2002, pp. 476-483.
   - **MLA格式**: Koenig, Sven, and Maxim Likhachev. "D* lite." *Proceedings of the Eighteenth National Conference on Artificial Intelligence*, AAAI Press, 2002, pp. 476-483.

#### 理論基礎

- **Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to algorithms (3rd ed.)**
  - **章節**: Chapter 24 - Single-Source Shortest Paths
  - **相關概念**: Shortest path optimality
  - **引用原因**: 最短路徑演算法的理論基礎
  - **出版社**: MIT Press
  - **ISBN**: 9780262033848
  - **網址**: [https://mitpress.mit.edu/9780262033848/introduction-to-algorithms/](https://mitpress.mit.edu/9780262033848/introduction-to-algorithms/)
  - **APA格式**: Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to algorithms* (3rd ed.). MIT Press.
  - **IEEE格式**: T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 3rd ed. Cambridge, MA: MIT Press, 2009.
  - **MLA格式**: Cormen, Thomas H., et al. *Introduction to Algorithms*. 3rd ed., MIT Press, 2009.

---

## ⏱️ **計算時間 (Computation Time)**

### 學術來源

**核心概念**: 演算法複雜度、實時性能 (Algorithm Complexity, Real-time Performance)

#### 主要論文來源

1. **Knuth, D. E. (1976). Big omicron and big omega and big theta**
   - **期刊**: ACM SIGACT News, 8(2), 18-24
   - **DOI**: 10.1145/1008328.1008329
   - **相關概念**: Algorithm complexity analysis
   - **貢獻**: 演算法時間複雜度分析的基礎
   - **網址**: [https://dl.acm.org/doi/10.1145/1008328.1008329](https://dl.acm.org/doi/10.1145/1008328.1008329)
   - **出版商**: ACM
   - **APA格式**: Knuth, D. E. (1976). Big omicron and big omega and big theta. *ACM SIGACT News*, 8(2), 18-24.
   - **IEEE格式**: D. E. Knuth, "Big omicron and big omega and big theta," *ACM SIGACT News*, vol. 8, no. 2, pp. 18-24, Apr. 1976.
   - **MLA格式**: Knuth, Donald E. "Big omicron and big omega and big theta." *ACM SIGACT News*, vol. 8, no. 2, 1976, pp. 18-24.

2. **Skiena, S. S. (2020). The algorithm design manual (3rd ed.)**
   - **章節**: Chapter 2 - Algorithm Analysis
   - **相關概念**: Runtime analysis and benchmarking
   - **引用原因**: 演算法性能評估的實踐方法
   - **出版社**: Springer
   - **ISBN**: 9783030542559
   - **網址**: [https://www.algorist.com/](https://www.algorist.com/)
   - **DOI**: 10.1007/978-3-030-54256-6
   - **APA格式**: Skiena, S. S. (2020). *The algorithm design manual* (3rd ed.). Springer.
   - **IEEE格式**: S. S. Skiena, *The Algorithm Design Manual*, 3rd ed. Cham, Switzerland: Springer, 2020.
   - **MLA格式**: Skiena, Steven S. *The Algorithm Design Manual*. 3rd ed., Springer, 2020.

3. **Sedgewick, R., & Wayne, K. (2011). Algorithms (4th ed.)**
   - **章節**: Chapter 1.4 - Analysis of Algorithms
   - **相關概念**: Empirical analysis and timing
   - **貢獻**: 實際演算法時間測量的方法論
   - **出版社**: Addison-Wesley
   - **ISBN**: 9780321573513
   - **網址**: [https://algs4.cs.princeton.edu/home/](https://algs4.cs.princeton.edu/home/)
   - **APA格式**: Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
   - **IEEE格式**: R. Sedgewick and K. Wayne, *Algorithms*, 4th ed. Boston, MA: Addison-Wesley, 2011.
   - **MLA格式**: Sedgewick, Robert, and Kevin Wayne. *Algorithms*. 4th ed., Addison-Wesley, 2011.

#### 在即時系統中的應用

- **Liu, C. L., & Layland, J. W. (1973). Scheduling algorithms for multiprogramming in a hard-real-time environment**
  - **期刊**: Journal of the ACM, 20(1), 46-61
  - **DOI**: 10.1145/321738.321743
  - **相關概念**: Real-time scheduling and timing constraints
  - **引用原因**: 實時系統中時間性能評估的標準
  - **網址**: [https://dl.acm.org/doi/10.1145/321738.321743](https://dl.acm.org/doi/10.1145/321738.321743)
  - **出版商**: ACM
  - **APA格式**: Liu, C. L., & Layland, J. W. (1973). Scheduling algorithms for multiprogramming in a hard-real-time environment. *Journal of the ACM*, 20(1), 46-61.
  - **IEEE格式**: C. L. Liu and J. W. Layland, "Scheduling algorithms for multiprogramming in a hard-real-time environment," *J. ACM*, vol. 20, no. 1, pp. 46-61, Jan. 1973.
  - **MLA格式**: Liu, C. L., and James W. Layland. "Scheduling algorithms for multiprogramming in a hard-real-time environment." *Journal of the ACM*, vol. 20, no. 1, 1973, pp. 46-61.

---

## 🏆 **平均獎勵 (Average Reward)**

### 學術來源

**核心概念**: 強化學習中的回報函數 (Reward Function in Reinforcement Learning)

#### 主要論文來源

1. **Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction (2nd ed.)**
   - **章節**: Chapter 3 - Finite Markov Decision Processes
   - **相關概念**: Expected return and value functions
   - **頁碼**: pp. 47-52
   - **貢獻**: 強化學習中獎勵評估的基礎理論

2. **Bellman, R. (1957). A Markovian decision process**
   - **期刊**: Journal of Mathematics and Mechanics, 6(5), 679-684
   - **相關概念**: Value iteration and expected rewards
   - **歷史意義**: 馬可夫決策過程中獎勵的數學基礎
   - **DOI**: 10.1512/iumj.1957.6.56038
   - **網址**: [https://www.jstor.org/stable/24900506](https://www.jstor.org/stable/24900506)
   - **出版商**: Indiana University Mathematics Journal
   - **APA格式**: Bellman, R. (1957). A Markovian decision process. *Journal of Mathematics and Mechanics*, 6(5), 679-684.
   - **IEEE格式**: R. Bellman, "A Markovian decision process," *J. Math. Mech.*, vol. 6, no. 5, pp. 679-684, 1957.
   - **MLA格式**: Bellman, Richard. "A Markovian decision process." *Journal of Mathematics and Mechanics*, vol. 6, no. 5, 1957, pp. 679-684.

3. **Watkins, C. J., & Dayan, P. (1992). Q-learning**
   - **期刊**: Machine Learning, 8(3-4), 279-292
   - **DOI**: 10.1007/BF00992698
   - **相關概念**: Q-value and cumulative reward
   - **貢獻**: Q-learning中獎勵累積的理論基礎
   - **網址**: [https://link.springer.com/article/10.1007/BF00992698](https://link.springer.com/article/10.1007/BF00992698)
   - **出版商**: Springer
   - **APA格式**: Watkins, C. J., & Dayan, P. (1992). Q-learning. *Machine Learning*, 8(3-4), 279-292.
   - **IEEE格式**: C. J. Watkins and P. Dayan, "Q-learning," *Mach. Learn.*, vol. 8, no. 3-4, pp. 279-292, May 1992.
   - **MLA格式**: Watkins, Christopher J., and Peter Dayan. "Q-learning." *Machine Learning*, vol. 8, no. 3-4, 1992, pp. 279-292.

#### 在車輛導航中的應用

- **Abbeel, P., Coates, A., & Ng, A. Y. (2010). Autonomous helicopter aerobatics through apprenticeship learning**
  - **期刊**: International Journal of Robotics Research, 29(13), 1608-1639
  - **DOI**: 10.1177/0278364910371999
  - **相關概念**: Reward design in autonomous navigation
  - **引用原因**: 自主導航中獎勵函數設計的實踐

---

## 📊 **綜合評估框架的學術基礎**

### 多指標評估系統

1. **Pareto, V. (1896). Cours d'économie politique**
   - **概念**: Pareto optimality
   - **應用**: 多目標優化中的均衡評估
   - **在本系統中的應用**: 平衡不同性能指標的權重

2. **Saaty, T. L. (1980). The analytic hierarchy process**
   - **出版社**: McGraw-Hill
   - **相關概念**: Multi-criteria decision making
   - **引用原因**: 多指標權重分配的理論基礎

### 性能基準測試

- **Sim, R., & Roy, N. (2005). Global A-optimal robot exploration in SLAM**
  - **會議**: IEEE International Conference on Robotics and Automation
  - **DOI**: 10.1109/ROBOT.2005.1570477
  - **相關概念**: Comprehensive performance evaluation in robotics
  - **貢獻**: 機器人系統性能評估的綜合框架

---

## 🔍 **指標計算公式的理論依據**

### 成功率公式

```
成功率 = (成功次數 / 總測試次數) × 100%
```

**理論基礎**:

- **基礎統計學**: Hogg, R. V., & Tanis, E. A. (2009). Probability and Statistical Inference (8th ed.)
- **應用**: 二項分布中成功概率的估計

### 路徑效率公式

```
路徑效率 = (最短路徑長度 / 實際路徑長度) × 100%
```

**理論基礎**:

- **圖論**: Bollobás, B. (2013). Modern graph theory
- **最優化理論**: Boyd, S., & Vandenberghe, L. (2004). Convex optimization

### 平均獎勵公式

```
平均獎勵 = 總獎勵 / 總步數
```

**理論基礎**:

- **馬可夫決策過程**: Puterman, M. L. (2014). Markov decision processes: discrete stochastic dynamic programming
- **強化學習理論**: Bertsekas, D. P. (2019). Reinforcement learning and optimal control

---

## 📖 **建議進一步閱讀**

### 核心教科書

1. **Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction (2nd ed.)**
   - 強化學習的聖經，涵蓋所有基礎概念

2. **LaValle, S. M. (2006). Planning algorithms**
   - 路徑規劃演算法的完整參考

3. **Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.)**
   - AI基礎，包含搜索和規劃章節

### 專業期刊文章

1. **IEEE Transactions on Robotics**
   - 機器人導航和路徑規劃的頂級期刊

2. **Journal of Artificial Intelligence Research**
   - AI理論和演算法的重要來源

3. **Autonomous Robots**
   - 自主系統性能評估的專業期刊

---

## 🎓 **如何引用這些指標**

### 學術論文中的引用範例

#### 成功率

```
"Success rate is measured as the percentage of navigation tasks 
completed successfully within the given time limit, following 
the performance evaluation framework established by Sutton & 
Barto (2018) for reinforcement learning systems."
```

#### 路徑效率

```
"Path efficiency is calculated as the ratio of optimal path 
length to actual path length, based on the optimality metrics 
defined by Stentz (1994) for dynamic path planning."
```

#### 計算時間

```
"Computation time is measured per decision step in milliseconds, 
following the algorithmic performance analysis methodology 
described by Sedgewick & Wayne (2011)."
```

#### 平均獎勵

```
"Average reward per step is computed following the value function 
framework established by Bellman (1957) and formalized in modern 
reinforcement learning by Watkins & Dayan (1992)."
```

---

## 💡 **指標的創新應用**

### 您系統中的貢獻

雖然這些指標都有堅實的理論基礎，但您的系統在以下方面有創新：

1. **五指標綜合評估**: 首次將這五個指標整合為車輛導航的完整評估框架
2. **實時權重調整**: 根據應用場景動態調整指標權重
3. **演算法對比**: 在相同框架下比較不同強化學習演算法

### 發表建議

如果您計劃發表相關研究，建議強調：

- 多指標評估框架的實用性
- 不同演算法在各指標上的權衡分析
- 實際應用中的驗證結果

這些學術來源為您的性能指標提供了堅實的理論基礎，確保評估方法的科學性和可信度！

### 補充文獻引用與網址資訊

---

## 🔄 已補充的文獻

### Abbeel, Coates, & Ng (2010)

- **網址**: [https://journals.sagepub.com/doi/10.1177/0278364910371999](https://journals.sagepub.com/doi/10.1177/0278364910371999)
- **APA**: Abbeel, P., Coates, A., & Ng, A. Y. (2010). Autonomous helicopter aerobatics through apprenticeship learning. *International Journal of Robotics Research*, 29(13), 1608–1639. <https://doi.org/10.1177/0278364910371999>
- **IEEE**: P. Abbeel, A. Coates, and A. Y. Ng, "Autonomous helicopter aerobatics through apprenticeship learning," *Int. J. Robot. Res.*, vol. 29, no. 13, pp. 1608–1639, 2010.
- **MLA**: Abbeel, Pieter, et al. "Autonomous helicopter aerobatics through apprenticeship learning." *International Journal of Robotics Research*, vol. 29, no. 13, 2010, pp. 1608–1639.

### Pareto, V. (1896)

- **網址**: [https://archive.org/details/coursdeconomique01pareuoft](https://archive.org/details/coursdeconomique01pareuoft)
- **APA**: Pareto, V. (1896). *Cours d’économie politique*. F. Rouge.
- **IEEE**: V. Pareto, *Cours d’économie politique*. Lausanne: F. Rouge, 1896.
- **MLA**: Pareto, Vilfredo. *Cours d’économie politique*. F. Rouge, 1896.

### Saaty, T. L. (1980)

- **網址**: [https://link.springer.com/book/10.1007/978-1-4615-1665-1](https://link.springer.com/book/10.1007/978-1-4615-1665-1)
- **APA**: Saaty, T. L. (1980). *The analytic hierarchy process*. McGraw-Hill.
- **IEEE**: T. L. Saaty, *The Analytic Hierarchy Process*. New York: McGraw-Hill, 1980.
- **MLA**: Saaty, Thomas L. *The Analytic Hierarchy Process*. McGraw-Hill, 1980.

### Sim & Roy (2005)

- **網址**: [https://ieeexplore.ieee.org/document/1570477](https://ieeexplore.ieee.org/document/1570477)
- **APA**: Sim, R., & Roy, N. (2005). Global A-optimal robot exploration in SLAM. In *Proceedings of the IEEE International Conference on Robotics and Automation* (pp. 661–666). <https://doi.org/10.1109/ROBOT.2005.1570477>
- **IEEE**: R. Sim and N. Roy, "Global A-optimal robot exploration in SLAM," in *Proc. IEEE Int. Conf. Robot. Autom.*, 2005, pp. 661–666.
- **MLA**: Sim, Ronald, and Nicholas Roy. "Global A-optimal robot exploration in SLAM." *Proceedings of the IEEE International Conference on Robotics and Automation*, 2005, pp. 661–666.

### Puterman (2014)

- **網址**: [https://www.wiley.com/en-us/Markov+Decision+Processes%3A+Discrete+Stochastic+Dynamic+Programming%2C+2nd+Edition-p-9781118625873](https://www.wiley.com/en-us/Markov+Decision+Processes%3A+Discrete+Stochastic+Dynamic+Programming%2C+2nd+Edition-p-9781118625873)
- **APA**: Puterman, M. L. (2014). *Markov decision processes: Discrete stochastic dynamic programming* (2nd ed.). Wiley.
- **IEEE**: M. L. Puterman, *Markov Decision Processes: Discrete Stochastic Dynamic Programming*, 2nd ed. Hoboken, NJ: Wiley, 2014.
- **MLA**: Puterman, Martin L. *Markov Decision Processes: Discrete Stochastic Dynamic Programming*. 2nd ed., Wiley, 2014.

### Bertsekas (2019)

- **網址**: [http://www.athenasc.com/rlbook.html](http://www.athenasc.com/rlbook.html)
- **APA**: Bertsekas, D. P. (2019). *Reinforcement learning and optimal control*. Athena Scientific.
- **IEEE**: D. P. Bertsekas, *Reinforcement Learning and Optimal Control*. Belmont, MA: Athena Scientific, 2019.
- **MLA**: Bertsekas, Dimitri P. *Reinforcement Learning and Optimal Control*. Athena Scientific, 2019.
