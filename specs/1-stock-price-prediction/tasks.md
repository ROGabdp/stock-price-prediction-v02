# 任務：股價漲跌機率預測系統

**輸入**: 設計文件來自 `/specs/1-stock-price-prediction/`
**Prerequisites**: plan.md (必要), spec.md (使用者故事為必要), research.md, data-model.md, contracts/

**Tests**: 專案章程強調可測試性，因此將包含測試任務。

**Organization**: 任務按使用者故事分組，以實現每個故事的獨立實作與測試。

## 格式: `[ID] [P?] [Story] Description`

- **[P]**: 可並行執行 (不同檔案，無依賴關係)
- **[Story]**: 此任務所屬的使用者故事 (例如：US1, US2, US3)
- 在描述中包含確切的檔案路徑

## 路徑慣例

- **單一專案**: `src/`, `tests/` 在儲存庫根目錄

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 建立專案根目錄下的 `src/` 和 `tests/` 目錄
- [X] T002 在 `src/` 下建立 `data/`, `models/`, `services/`, `ui/`, `utils/` 目錄
- [X] T003 在 `tests/` 下建立 `unit/`, `integration/`, `e2e/` 目錄
- [X] T004 初始化 Python 虛擬環境並安裝核心依賴 (Flask, Dash, TensorFlow/PyTorch, Pandas, Plotly)
- [X] T005 [P] 設定程式碼風格檢查 (例如 Flake8, Black) 和格式化工具 (例如 Black)
- [X] T006 建立 `requirements.txt` 檔案並記錄所有依賴

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 實作 `src/utils/data_loader.py` 用於載入 CSV 歷史資料
- [X] T008 實作 `src/utils/model_manager.py` 用於儲存和載入機器學習模型檔案
- [X] T009 實作 `src/utils/metadata_manager.py` 用於管理模型元資料 (JSON 檔案)
- [X] T010 設定 Flask 應用程式的基本結構在 `src/app.py`
- [X] T011 設定 Dash 應用程式的基本結構在 `src/ui/dashboard.py`
- [X] T012 實作 `src/services/data_service.py` 提供資料相關的業務邏輯
- [X] T013 實作 `src/services/model_service.py` 提供模型相關的業務邏輯

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - 模型訓練與預測 (優先級: P1) 🎯 MVP

**Goal**: 作為使用者，我想要上傳或選擇一個歷史股價資料集，並啟動模型訓練，系統應自動調整參數並進行多次訓練，以生成對未來 N 天股價的預測結果。

**Independent Test**: 使用者可以成功上傳一個 CSV 檔案，點擊「訓練」按鈕，系統會產生一個模型檔案，並在介面上顯示未來 N 天的漲跌機率與幅度預測表格。

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T014 [P] [US1] 單元測試 `src/data/preprocessor.py` 中的資料預處理邏輯，在 `tests/unit/test_preprocessor.py`
- [X] T015 [P] [US1] 單元測試 `src/models/trainer.py` 中的模型訓練和自動參數調整邏輯，在 `tests/unit/test_trainer.py`
- [X] T016 [P] [US1] 單元測試 `src/services/model_service.py` 中的模型儲存和載入功能，在 `tests/unit/test_model_service.py`
- [X] T017 [P] [US1] 整合測試 `/api/model/train` 端點，在 `tests/integration/test_api_train.py`

### Implementation for User Story 1

- [X] T018 [US1] 實作 `src/data/preprocessor.py` 用於歷史資料的預處理
- [X] T019 [US1] 實作 `src/models/trainer.py` 包含機器學習模型定義、訓練邏輯和自動參數調整
- [X] T020 [US1] 實作 `src/models/predictor.py` 用於使用訓練好的模型進行預測
- [X] T021 [US1] 實作 `/api/model/train` API 端點在 `src/app.py`，用於啟動模型訓練
- [X] T022 [US1] 實作 `/api/model/train/status/<task_id>` API 端點在 `src/app.py`，用於查詢訓練任務狀態
- [ ] T023 [US1] 更新 `src/services/model_service.py` 以整合自動參數調整和模型元資料管理

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - 視覺化圖表 (優先級: P2)

**Goal**: 作為使用者，我想要在一個圖表上同時看到歷史股價和我所選模型的預測結果，以便直觀地評估預測的趨勢。

**Independent Test**: 當模型訓練完成或被選中後，介面會顯示一個包含兩條線的圖表：一條代表歷史收盤價，另一條代表模型預測的未來價格趨勢。

### Tests for User Story 2 ⚠️

- [ ] T024 [P] [US2] 單元測試 `src/ui/components/chart_generator.py` 中的圖表生成邏輯，在 `tests/unit/test_chart_generator.py`
- [ ] T025 [P] [US2] 端到端測試 Dash 介面是否正確顯示歷史和預測圖表，在 `tests/e2e/test_dashboard_chart.py`

### Implementation for User Story 2

- [ ] T026 [US2] 實作 `src/ui/components/chart_generator.py` 使用 Plotly 根據歷史和預測數據生成圖表
- [ ] T027 [US2] 更新 `src/ui/dashboard.py` 以整合圖表顯示功能
- [ ] T028 [US2] 實作 `/api/data/history` API 端點在 `src/app.py`，用於取得歷史數據
- [ ] T029 [US2] 實作 `/api/model/predict` API 端點在 `src/app.py`，用於取得模型預測結果

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - 模型與資料選擇 (優先級: P3)

**Goal**: 作為使用者，我想要能夠從一個列表中輕鬆選擇不同的訓練資料集和之前已訓練好的模型，以便進行比較和重新預測。

**Independent Test**: 介面上有兩個下拉式選單。一個用於選擇不同的資料檔案，另一個用於選擇已儲存的模型檔案。選擇後，系統會使用所選項目更新預測結果和圖表。

### Tests for User Story 3 ⚠️

- [ ] T030 [P] [US3] 單元測試 `src/ui/components/data_selector.py` 和 `src/ui/components/model_selector.py`，在 `tests/unit/test_selectors.py`
- [ ] T031 [P] [US3] 整合測試 `/api/model/list` 和 `/api/data/upload` 端點，在 `tests/integration/test_api_selectors.py`
- [ ] T032 [P] [US3] 端到端測試 Dash 介面中的資料和模型選擇功能，在 `tests/e2e/test_dashboard_selectors.py`

### Implementation for User Story 3

- [ ] T033 [US3] 實作 `src/ui/components/data_selector.py` 用於資料集選擇介面
- [ ] T034 [US3] 實作 `src/ui/components/model_selector.py` 用於已訓練模型選擇介面
- [ ] T035 [US3] 更新 `src/ui/dashboard.py` 以整合資料和模型選擇功能，並處理選擇事件
- [ ] T036 [US3] 實作 `/api/model/list` API 端點在 `src/app.py`，用於取得已訓練模型列表
- [ ] T037 [US3] 實作 `/api/data/upload` API 端點在 `src/app.py`，用於上傳新的歷史資料

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T038 [P] 完善錯誤處理和日誌記錄機制
- [ ] T039 [P] 撰寫專案 README.md 和使用說明文件
- [ ] T040 [P] 程式碼清理、重構和註釋
- [ ] T041 [P] 效能優化 (例如：資料載入、模型預測速度)
- [ ] T042 [P] 安全性強化 (例如：輸入驗證、API 認證)
- [ ] T043 [P] 執行 `quickstart.md` 驗證

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "單元測試 src/data/preprocessor.py 中的資料預處理邏輯，在 tests/unit/test_preprocessor.py"
Task: "單元測試 src/models/trainer.py 中的模型訓練和自動參數調整邏輯，在 tests/unit/test_trainer.py"
Task: "單元測試 src/services/model_service.py 中的模型儲存和載入功能，在 tests/unit/test_model_service.py"
Task: "整合測試 /api/model/train 端點，在 tests/integration/test_api_train.py"

# Launch all models for User Story 1 together:
Task: "實作 src/data/preprocessor.py 用於歷史資料的預處理"
Task: "實作 src/models/trainer.py 包含機器學習模型定義、訓練邏輯和自動參數調整"
Task: "實作 src/models/predictor.py 用於使用訓練好的模型進行預測"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
