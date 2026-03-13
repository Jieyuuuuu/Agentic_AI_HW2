# Report Outline 

本檔案是給使用者參考的報告撰寫方向，你需要把以下內容整理後轉成 `report.pdf` 提交。

## Section 1: Implementation Logic
**System Prompt Strategy:**  
(請將 `agent.py` 中的 `SYSTEM_PROMPT` 貼上，包含 Few-Shot 範例)
*為什麼這很重要？*  
One-Shot 範例幫助 LLM 具體了解我們期望輸出的語法規格：明確分出 Thought 與 Action，且 Action 的格式必須是 `Search[關鍵字]`。這有助於 `google-genai` 更穩定地生成我們可以利用的正則表達式解析格式，且減少幻覺（Hallucination）。

**The Loop Mechanism:**  
我實作了一個 `while step < 5` 的迴圈。在每一次迴圈中，LLM 會收到過去累積的對話歷史 (history) 進行生成。
最關鍵的是 **Stop Sequence**，我設定當抓到要輸出 `Observation:` 字眼時，LLM 會強迫停止輸出（因為這部分應由程式執行 Search API 回傳）。
隨後，Python 用 Regex 抓取 `Action: Search[...]` 中的關鍵字，送給 DuckDuckGo 進行真實網路搜尋，最後把得到的字串拼裝成 `Observation: [真實搜尋結果]` 塞回 history 中，再讓迴圈繼續，讓 LLM 根據真實搜尋結果去思考（Reflection / Planning）下一步。

## Section 2: Benchmark Traces (The Evidence)

*(請將你在執行 `main.py` 時終端機 (Console) 的 Trace 貼在相對應的任務分析底下)*

**Task 1: Planning & Quantitative Reasoning**
*   **Analysis:** (請貼上 Trace) 分析它有沒有先查日本人口，再查台灣人口。並說明它是如何在不瞎猜的情況下，得到兩個數字才進行數學計算。（展示出 Planning 任務拆解能力）。

**Task 2: Technical Specificity**
*   **Analysis:** (請貼上 Trace) 查看它從 DuckDuckGo 得到的 Observation 裡，有沒有明確抓到 "120Hz"（S24）與 "60Hz"（iPhone 15）螢幕更新率的關鍵字，並最終整理出該有的技術規格。

**Task 3: Resilience & Reflection Test**
*   **Analysis:** (請貼上 Trace) 如果查 "Morphic AI CEO" 沒結果，分析 Agent 有沒有輸出類似 "Thought: 剛剛搜尋不到 Morphic 的資訊，或許我該改查 Morphic AI startup founder..." 這樣的重新修正行為？這是展示 Agentic Reflection 的關鍵。
