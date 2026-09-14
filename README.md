# Identity System (身分認證與管理系統)

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=flat-square&logo=vuedotjs&logoColor=4FC08D)
![TiDB](https://img.shields.io/badge/TiDB-MySQL_Compatible-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat-square)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=flat-square&logo=github-actions&logoColor=white)

本專案為職前訓練期間的實作成果，主要用於實作前後端分離架構、RESTful API、資料庫操作與 Web Application 開發流程。

專案採用前後端分離架構，包含基礎的使用者註冊、登入驗證與狀態管理功能，後續並實作自動化部署與雲端資料庫串接。

## 🌟 專案功能

* **身分證字號驗證**
  * 身分證字號格式與檢核規則驗證
* **個人資料管理**
  * 新增個人資料
  * 查詢個人資料
  * 修改個人資料
*   **後端設計**
    *   使用 DAO (Data Access Object) 處理資料庫存取
    *   使用 VO (Value Object) 作為資料傳遞格式
    *   API 統一回應格式
*   **雲端部署**
    *   使用 TiDB Cloud 作為資料庫
    *   使用 Render 部署後端 API
    *   使用 GitHub Actions (`.github/workflows/deploy.yml`) 執行 CI/CD

## 🛠️ 技術棧

* **前端**：Vue.js, Vite, HTML, CSS, JavaScript
* **後端**：Python 3.x, RESTful API
* **資料庫**：TiDB Cloud (MySQL-Compatible)
* **部署**：Render
* **自動化部署**：GitHub Actions


## 📁 專案結構

```text
identity-system/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions 部署流程
│
├── backend/
│   ├── app.py                  # 後端主程式入口
│   ├── db.py                   # TiDB 資料庫連線設定
│   ├── Dao.py                  # 資料庫存取
│   ├── Vo.py                   # 資料傳遞結構
│   ├── response.py             # API 統一回應格式
│   └── requirements.txt        # Python 依賴套件
│
└── vue-project/
    ├── src/
    │   ├── App.vue
    │   └── main.js
    ├── public/
    │   └── zh-HANT.json        # 繁體中文語系
    ├── package.json
    ├── vite.config.js
    ├── .env.development        # 開發環境設定
    └── .env.production         # 正式環境設定
```

## 🚀 本地開發

請先確認已安裝 **Python 3.x** 與 **Node.js**。

**Frontend**
```bash
cd vue-project
npm install
npm run dev
```

**Backend**
請先設定資料庫連線相關環境變數：
```bash
cd backend
pip install -r requirements.txt
python app.py
```

## ☁️ 部署

本專案後續加入雲端環境與自動化部署：

```text
GitHub
   │
   │ Push
   ▼
GitHub Actions
   │
   │ Build / Deploy
   ▼
Render
   │
   │ API
   ▼
TiDB Cloud
```

*   **Backend**：Render
*   **Database**：TiDB Cloud
*   **CI/CD**：GitHub Actions
*   **Environment**：Development / Production
