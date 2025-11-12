# 實作計畫：[功能名稱]

**分支**: `[###-feature-name]` | **日期**: [DATE] | **規格書**: [link]
**輸入**: 功能規格書來自 `/specs/[###-feature-name]/spec.md`

**注意**: 此模板由 `/speckit.plan` 命令填寫。執行流程請參閱 `.specify/templates/commands/plan.md`。

## 總結

[從功能規格書中提取：主要需求 + 來自研究的技術方法]

## 技術背景

<!--
  需要處理：請將本節內容替換為專案的技術細節。
  此處的結構僅為指導迭代過程的建議。
-->

**語言/版本**: [例如：Python 3.11, Swift 5.9, Rust 1.75 或 需釐清]  
**主要依賴套件**: [例如：FastAPI, UIKit, LLVM 或 需釐清]  
**儲存**: [如適用，例如：PostgreSQL, CoreData, 檔案系統 或 不適用]  
**測試**: [例如：pytest, XCTest, cargo test 或 需釐清]  
**目標平台**: [例如：Linux 伺服器, iOS 15+, WASM 或 需釐清]
**專案類型**: [單一/網站/行動應用 - 這將決定原始碼結構]  
**效能目標**: [領域相關，例如：1000 req/s, 10k lines/sec, 60 fps 或 需釐清]  
**限制**: [領域相關，例如：p95 < 200ms, 記憶體 < 100MB, 可離線使用 或 需釐清]  
**規模/範圍**: [領域相關，例如：1萬使用者, 1百萬行程式碼, 50個畫面 或 需釐清]

## 章程檢查

*閘門：必須在第 0 階段研究前通過。在第 1 階段設計後重新檢查。*

[閘門根據章程檔案決定]

## 專案結構

### 文件 (此功能)

```text
specs/[###-feature]/
├── plan.md              # 本檔案 (/speckit.plan 命令的輸出)
├── research.md          # 第 0 階段輸出 (/speckit.plan 命令)
├── data-model.md        # 第 1 階段輸出 (/speckit.plan 命令)
├── quickstart.md        # 第 1 階段輸出 (/speckit.plan 命令)
├── contracts/           # 第 1 階段輸出 (/speckit.plan 命令)
└── tasks.md             # 第 2 階段輸出 (/speckit.tasks 命令 - 非由 /speckit.plan 建立)
```

### 原始碼 (儲存庫根目錄)
<!--
  需要處理：請將下方的預留位置樹狀結構替換為此功能的具體佈局。
  刪除未使用的選項，並用真實路徑擴展所選結構（例如：apps/admin, packages/something）。
  交付的計畫中不得包含「選項」標籤。
-->

```text
# [若未使用請移除] 選項 1：單一專案 (預設)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [若未使用請移除] 選項 2：Web 應用程式 (當偵測到 "frontend" + "backend")
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [若未使用請移除] 選項 3：行動應用 + API (當偵測到 "iOS/Android")
api/
└── [同上述 backend]

ios/ 或 android/
└── [平台特定結構：功能模組、UI 流程、平台測試]
```

**結構決策**: [記錄所選的結構，並引用上方捕獲的真實目錄]

## 複雜度追蹤

> **僅在「章程檢查」有違規且必須說明理由時填寫**

| 違規項目 | 為何需要 | 為何拒絕更簡單的替代方案 |
|-----------|------------|-------------------------------------|
| [例如：第四個專案] | [目前的需求] | [為何三個專案不足夠] |
| [例如：儲存庫模式] | [具體問題] | [為何直接存取資料庫不足夠] |