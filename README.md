# 💰 Django Expense Tracker

A modern, full-stack Expense Tracker web application built with **Django**, **Python**, **SQLite**, **HTML**, **CSS**, **Bootstrap**, and **Matplotlib**.

This application helps users securely manage daily expenses, visualize spending habits through analytics, filter expenses by multiple criteria, and generate professional PDF reports.

---

## 📸 Screenshots

### Dashboard

> Add your dashboard screenshot here

```
screenshots/dashboard.png
```

### Analytics Dashboard

> Add analytics screenshot here

```
screenshots/analytics.png
```

### PDF Report

> Add PDF report screenshot here

```
screenshots/pdf-report.png
```

---

# ✨ Features

## 🔐 Authentication

- User Registration
- User Login
- User Logout
- Secure Password Hashing
- User-specific Expense Records

---

## 💵 Expense Management

- Add Expense
- Edit Expense
- Delete Expense
- View Expense History
- Search Expenses
- Category-wise Organization

---

## 📊 Analytics Dashboard

- Total Expenses
- Total Transactions
- Top Spending Category
- Biggest Expense
- Average Daily Spending
- Last 30 Days Summary

---

## 🔍 Smart Filters

Filter expenses using:

- Search
- Category
- Month
- Year

Supports combining multiple filters simultaneously.

Example:

- July 2026
- Food Expenses
- Search "Laptop"

---

## 📈 Data Visualization

Interactive Pie Chart showing:

- Category-wise Spending
- Filtered Chart based on Search
- Monthly Analytics
- Yearly Analytics

---

## 📄 PDF Report Generation

Generate beautiful PDF reports including:

- Applied Filters
- Expense Table
- Total Expenses
- Expense Distribution Pie Chart
- Dynamic Report Title
- Timestamp

Reports automatically reflect current filters.

Example:

- July 2026 Report
- Food Expenses Report
- Search Results Report

---

# 🛠️ Built With

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Django | Web Framework |
| SQLite | Database |
| HTML5 | Frontend |
| CSS3 | Styling |
| Bootstrap 5 | Responsive UI |
| JavaScript | Dynamic UI |
| Matplotlib | Pie Chart Generation |
| ReportLab | PDF Generation |

---

# 📂 Project Structure

```
expense_tracker/
│
├── accounts/
│
├── expense_tracker/
│
├── expenses/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── add_expense.html
│   ├── edit_expense.html
│
├── requirements.txt
├── manage.py
└── README.md
```

---

# 🚀 Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/mdjaheerashraf/python-expense-tracker-django.git
```

---

## 2️⃣ Move into Project

```bash
cd python-expense-tracker-django
```

---

## 3️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5️⃣ Apply Migrations

```bash
python manage.py migrate
```

---

## 6️⃣ Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

## 7️⃣ Run Server

```bash
python manage.py runserver
```

Open

```
http://127.0.0.1:8000
```

---

# 📋 Dependencies

Major packages used:

- Django
- Matplotlib
- ReportLab
- Pillow

Install everything using

```bash
pip install -r requirements.txt
```

---

# 🔒 Security Features

- CSRF Protection
- Django Authentication
- Login Required Decorators
- User-specific Data Access
- Password Hashing

---

# 🎯 Future Improvements

- Email Verification
- Monthly Budget Alerts
- Expense Export to Excel
- Dark Mode
- Income Tracking
- Recurring Expenses
- AI Spending Insights
- REST API
- Mobile Responsive Improvements

---

# 👨‍💻 Author

## MD Jaheer Ashraf

**GitHub**

https://github.com/mdjaheerashraf

**LinkedIn**

https://www.linkedin.com/in/mdjaheerashraf/

---

# ⭐ Support

If you found this project useful,

⭐ Star this repository on GitHub.

---

# 📜 License

This project is licensed under the MIT License.
