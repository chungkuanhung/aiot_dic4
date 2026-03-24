# AIoT 儀表板開發對話紀錄與歷程

本文件紀錄了開發 `aiot_dic4` 專案期間的對話與開發流程。

## 1. 環境初始化
**👩‍💻 使用者：**
請先架設 uv 虛擬環境

**🤖 AI 助手：**
使用命令列在專案目錄下執行了 `uv venv` 建立虛擬環境，並告知可以透過 `.venv\Scripts\activate` 啟動。

---

## 2. 建立專案主體 (資料產生器與儀表板)
**👩‍💻 使用者：**
請幫我完成可達到以下目標的專案：
1. insert into SQLite3 aiotdb.db, sensors table
2. random generate temperature and humidity data every 2 sec
3. query data in the aiotdb.db streamlit 劃出 (dynamic)

**🤖 AI 助手：**
* 建立了 `generate_data.py`：使用 Python 在背景執行，建立資料庫並每兩秒寫入亂數溫濕度。
* 建立了 `app.py`：使用 Streamlit 動態讀取最新 60 筆數據，利用 `time.sleep(2)` 與 `st.empty` 建立即時動態刷新的儀表板。
* 建立了一個快捷的 `run_demo.bat` 同時啟動兩支程式。
* 安裝了 `streamlit` 與 `pandas` 套件。

---

## 3. 解決資料表載入順序與 Error 問題
**👩‍💻 使用者：**
執行 `app.py` 時發生了 `pandas.errors.DatabaseError: no such table: sensors` 錯誤。

**🤖 AI 助手：**
解釋了由於 Streamlit 搶先在資料產生腳本建表前執行查詢所導致的錯誤。修正了 `app.py` 的例外處理機制（改為攔截 `Exception`），讓網頁在資料表建立前安全地等待，不會直接崩潰。

---

## 4. 客製化圖表：雙 Y 軸設定
**👩‍💻 使用者：**
請幫我分成兩個縱軸，左邊的縱軸顯示溫度 (℃)，右邊的縱軸顯示濕度 (%)。

**🤖 AI 助手：**
將原本單純的 `st.line_chart` 替換為 `Altair` 繪圖函式庫，自訂了左邊為紅色的溫度 Y 軸，右邊為藍色的濕度 Y 軸，並透過 `resolve_scale(y='independent')` 疊加兩個圖層完美達成雙 Y 軸顯示。

---

## 5. 汰換 Bat 腳本並撰寫 README
**👩‍💻 使用者：**
將 `run_demo.bat` 刪除，並寫一個 `README.md`，將環境及指令寫在 `README.md`。

**🤖 AI 助手：**
刪除了 `run_demo.bat`，並撰寫了一份完整的 `README.md`，包含環境建置 (`uv venv` / `uv pip install`) 以及個別開啟兩個終端機執行兩支 Python 腳本的啟動說明。

---

## 6. 將專案改為正式 uv 專案
**👩‍💻 使用者：**
我已經新增成 uv 專案了，請修改 `README.md`。

**🤖 AI 助手：**
配合專案中新增的 `pyproject.toml`，將 `README.md` 中的安裝依賴指令簡化並更新為 `uv sync` 的標準做法。

---

## 7. 專案版本控制與開源 (GitHub)
**👩‍💻 使用者：**
幫我 push to github，名稱：`aiot_dic4`，權限：public。

**🤖 AI 助手：**
* 將 `.gitignore` 更新，明確排除了執行期間產生的本機資料庫 `aiotdb.db`。
* 透過終端機腳本執行 `git init`、`git add .`、`git commit`。
* 使用 GitHub 官方命令列工具 `gh repo create aiot_dic4 --public --source=. --remote=origin --push` 將專案上傳至 GitHub。
