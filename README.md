# 🌾 UdyamSaathi: AI-Driven Rural Micro-Enterprise Platform

**UdyamSaathi** is an intelligent, offline-first ERP and credit-enablement platform tailored for rural micro-entrepreneurs in India. Built with Python, Streamlit, and SQLite, it bridges the gap between traditional bookkeeping and modern financial inclusion by offering multi-user enterprise isolation, automatic transaction history seeding, automated sales forecasting, and instant government credit application generation.

---

## 🌐 Live Demo

* **Web App**: [https://udyamsaathi-1.onrender.com](https://udyamsaathi-1.onrender.com)
* **Demo Shop ID**: `SHOP-9001`
* **Demo Password**: `password123`

---

## 🌟 Key Features

* **Multi-Tenant User Isolation**: Case-insensitive Shop ID authentication (`SHOP-XXXX`) that completely isolates transactions, ledgers, and credit records per business.
* **Instant 90-Day Transaction Seeding**: Automatically populates 90 days of structured sales and expense data for demo accounts and new registrations to enable immediate predictive analytics.
* **AI-Driven Sales & Inventory Forecasting**: Integrates trend analysis to predict 7-day revenue, calculate suggested stock re-order budgets, and highlight top-demand inventory items.
* **Government Scheme & Credit Matching**: Automatically matches business revenue metrics with eligible Ministry of Social Justice and Empowerment (MoSJE) concessional schemes.
* **Automated PDF Loan Report Generator**: Generates bank-ready financial summary reports formatted for credit application submissions.
* **Lock-Free Database Engine**: Built with batch-insertion pipelines and 10-second SQLite connection timeouts to ensure high concurrency without database locking.

---

## 🏗️ Tech Stack

* **Frontend / UI**: [Streamlit](https://streamlit.io/)
* **Backend Database**: SQLite3 (with custom batch insertion & timeout handling)
* **Data Processing**: Pandas, NumPy
* **Export Utilities**: ReportLab (PDF Generation)

---

## 🚀 Getting Started (Local Setup)

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/UdyamSaathi.in.git](https://github.com/Nandini776/UdyamSaathi.in.git)
   cd UdyamSaathi.in
