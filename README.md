# 🛒 CloudCart — Full-Stack E-Commerce Application

A modern, full-stack e-commerce application built with **Python, Flask, PostgreSQL, HTML, CSS, and JavaScript**, featuring customer authentication, product management, shopping cart, order processing, and an administrative dashboard.

CloudCart is designed as a practical cloud-native application and DevOps portfolio project, with a roadmap toward containerization, automated CI/CD, AWS infrastructure, Infrastructure as Code, and Kubernetes deployment.

---

## 📌 Table of Contents

* [Project Overview](#-project-overview)
* [Project Objectives](#-project-objectives)
* [Key Features](#-key-features)
* [Technology Stack](#-technology-stack)
* [Application Architecture](#-application-architecture)
* [Project Structure](#-project-structure)
* [Application Modules](#-application-modules)
* [Database Design](#-database-design)
* [API Documentation](#-api-documentation)
* [Installation and Setup](#-installation-and-setup)
* [Environment Configuration](#-environment-configuration)
* [Running the Application](#-running-the-application)
* [Admin Dashboard](#-admin-dashboard)
* [Security Considerations](#-security-considerations)
* [Testing](#-testing)
* [Deployment](#-deployment)
* [DevOps Roadmap](#-devops-roadmap)
* [Future Enhancements](#-future-enhancements)
* [Author](#-author)

---

## 📖 Project Overview

CloudCart is a three-tier-style e-commerce application developed to demonstrate practical full-stack development and cloud engineering concepts.

The application provides two primary interfaces:

### Customer Storefront

Customers can:

* Browse available products.
* View product information and pricing.
* Register and log in.
* Add products to their shopping cart.
* Update cart quantities.
* Remove items from their cart.
* Place orders.
* View their order history.

### Administrative Dashboard

Administrators can:

* Access a protected admin dashboard.
* View business statistics.
* Manage products.
* View registered customers.
* Monitor customer orders.
* Update order statuses.
* Track product inventory.

The backend exposes REST-style APIs that connect the frontend and administrative dashboard to a shared PostgreSQL database.

---

## 🎯 Project Objectives

The primary objective of CloudCart is to build a practical application that can be progressively enhanced using industry-standard DevOps tools.

The project focuses on:

* Full-stack application development.
* REST API development.
* Database integration.
* Authentication and authorization.
* Application deployment on AWS EC2.
* Linux server administration.
* Docker containerization.
* CI/CD automation.
* Infrastructure as Code.
* Kubernetes orchestration.
* Monitoring and observability.

---

## ✨ Key Features

### Customer Features

| Feature              | Description                              |
| -------------------- | ---------------------------------------- |
| User Registration    | Create a customer account                |
| Authentication       | Secure password-based login              |
| Product Catalogue    | Retrieve available products              |
| Shopping Cart        | Add, update, and remove cart items       |
| Checkout             | Create orders from cart items            |
| Order History        | View customer-specific orders            |
| Inventory Management | Product stock validation during checkout |

### Admin Features

| Feature              | Description                               |
| -------------------- | ----------------------------------------- |
| Admin Authentication | Restricted dashboard access               |
| Dashboard Statistics | Products, customers, orders, revenue      |
| Product Management   | Create, read, update, and delete products |
| Customer Management  | View registered customers                 |
| Order Management     | View all customer orders                  |
| Order Status         | Update order lifecycle status             |
| Low Stock Monitoring | Identify products with low inventory      |

---

## 🛠️ Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap (where used)

### Backend

* Python
* Flask
* Flask-Login
* SQLAlchemy
* Flask-Migrate
* Werkzeug

### Database

* PostgreSQL

### Development and Deployment

* Ubuntu Linux
* AWS EC2
* Git
* GitHub

### Planned DevOps Technologies

* Docker
* Docker Compose
* GitHub Actions
* AWS ECR
* AWS EKS
* Terraform
* AWS CloudWatch
* Prometheus
* Grafana

*The planned technologies are part of the project roadmap and should not be considered implemented until their deployment is completed.*

---

## 🏗️ Application Architecture

CloudCart follows a three-tier-style architecture.

```mermaid
flowchart TD
    A[Customer Browser]
    B[Admin Browser]
    C[Frontend HTML CSS JavaScript]
    D[Flask Backend / REST APIs]
    E[Authentication and Authorization]
    F[Business Logic]
    G[(PostgreSQL Database)]

    A --> C
    B --> C
    C --> D
    D --> E
    D --> F
    F --> G
```

### Architecture Components

**Presentation Layer**

Provides the customer storefront and admin dashboard through browser-based interfaces.

**Application Layer**

Flask handles API requests, authentication, product operations, shopping cart management, checkout, and order processing.

**Data Layer**

PostgreSQL stores application data, including users, products, cart items, and orders.

---

## 📂 Project Structure

```text
CloudCart/
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── product.py
│   │   │   ├── cart.py
│   │   │   └── order.py
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── products.py
│   │   │   ├── cart.py
│   │   │   ├── orders.py
│   │   │   └── admin.py
│   │   │
│   │   ├── templates/
│   │   │   ├── index.html
│   │   │   ├── admin.html
│   │   │   └── login.html
│   │   │
│   │   └── static/
│   │       ├── css/
│   │       │   ├── style.css
│   │       │   └── admin.css
│   │       │
│   │       └── js/
│   │           ├── app.js
│   │           └── admin.js
│   │
│   ├── migrations/
│   ├── venv/
│   ├── .env
│   ├── requirements.txt
│   └── run.py
│
├── .gitignore
└── README.md
```

> The virtual environment and `.env` file are local configuration and should not be committed to Git.

---

## 🧩 Application Modules

### 1. Authentication Module

Responsible for:

* Customer registration.
* User login and logout.
* Password hashing.
* Session management.
* User identity verification.
* Role-based access control.

User roles include:

* `customer`
* `admin`

### 2. Product Module

Handles:

* Product listing.
* Product details.
* Product creation.
* Product updates.
* Product deletion.
* Inventory information.

Administrative product operations require authentication and administrator authorization.

### 3. Shopping Cart Module

Provides:

* Add product to cart.
* Retrieve cart items.
* Update item quantity.
* Remove cart items.
* Calculate item subtotals.

### 4. Order Module

The checkout process:

1. Retrieves the authenticated customer's cart.
2. Validates product availability.
3. Checks stock quantities.
4. Creates an order.
5. Creates order items.
6. Decreases product inventory.
7. Clears the customer's cart.

### 5. Admin Module

Provides administrative endpoints for:

* Dashboard statistics.
* Customer listing.
* All-order listing.
* Order status management.

---

## 🗄️ Database Design

CloudCart uses PostgreSQL as its relational database.

### Main Tables

| Table       | Purpose                             |
| ----------- | ----------------------------------- |
| users       | Customer and administrator accounts |
| products    | Product catalogue and stock         |
| cart_items  | Customer shopping cart              |
| orders      | Customer order records              |
| order_items | Products included in orders         |

### Relationship Overview

```mermaid
erDiagram
    USERS ||--o{ CART_ITEMS : owns
    PRODUCTS ||--o{ CART_ITEMS : contains
    USERS ||--o{ ORDERS : places
    ORDERS ||--o{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : references

    USERS {
        int id
        string username
        string email
        string password_hash
        string role
    }

    PRODUCTS {
        int id
        string name
        decimal price
        int stock
    }

    CART_ITEMS {
        int id
        int user_id
        int product_id
        int quantity
    }

    ORDERS {
        int id
        int user_id
        decimal total_amount
        string status
    }

    ORDER_ITEMS {
        int id
        int order_id
        int product_id
        string product_name
        decimal unit_price
        int quantity
    }
```

---

## 🔌 API Documentation

Base URL:

```text
http://localhost:5000
```

### Authentication APIs

| Method | Endpoint             | Description           |
| ------ | -------------------- | --------------------- |
| POST   | `/api/auth/register` | Register a customer   |
| POST   | `/api/auth/login`    | Authenticate a user   |
| GET    | `/api/auth/me`       | Retrieve current user |
| POST   | `/api/auth/logout`   | Logout                |

### Product APIs

| Method | Endpoint             | Description            |
| ------ | -------------------- | ---------------------- |
| GET    | `/api/products/`     | List products          |
| GET    | `/api/products/<id>` | Get product details    |
| POST   | `/api/products/`     | Create product (admin) |
| PUT    | `/api/products/<id>` | Update product (admin) |
| DELETE | `/api/products/<id>` | Delete product (admin) |

### Cart APIs

| Method | Endpoint         | Description     |
| ------ | ---------------- | --------------- |
| GET    | `/api/cart/`     | Retrieve cart   |
| POST   | `/api/cart/`     | Add item        |
| PUT    | `/api/cart/<id>` | Update quantity |
| DELETE | `/api/cart/<id>` | Remove item     |

### Order APIs

| Method | Endpoint               | Description                    |
| ------ | ---------------------- | ------------------------------ |
| POST   | `/api/orders/checkout` | Place an order                 |
| GET    | `/api/orders/`         | Retrieve current user's orders |

### Admin APIs

| Method | Endpoint                        | Description          |
| ------ | ------------------------------- | -------------------- |
| GET    | `/api/admin/dashboard`          | Dashboard statistics |
| GET    | `/api/admin/customers`          | List customers       |
| GET    | `/api/admin/orders`             | List all orders      |
| PATCH  | `/api/admin/orders/<id>/status` | Update order status  |

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "application": "CloudCart",
  "version": "1.0.0"
}
```

---

## ⚙️ Installation and Setup

### Prerequisites

Install the following:

* Python 3.10+
* PostgreSQL
* Git
* pip
* Linux, macOS, or Windows with a compatible Python environment

### Step 1: Clone the repository

```bash
git clone https://github.com/drblack2/CloudCart.git
cd CloudCart
```

### Step 2: Navigate to backend

```bash
cd backend
```

### Step 3: Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on Linux:

```bash
source venv/bin/activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure PostgreSQL

Create a database and database user using PostgreSQL administration tools.

Example:

```sql
CREATE DATABASE cloudcart_db;
```

Configure the database connection through environment variables.

### Step 6: Configure environment variables

Create a `.env` file in the backend directory.

Example configuration:

```env
SECRET_KEY=replace_with_a_secure_random_secret
DATABASE_URL=postgresql://cloudcart_user:YOUR_PASSWORD@localhost:5432/cloudcart_db
```

Use your own database credentials. Never commit `.env` to GitHub.

### Step 7: Initialize database migrations

If migrations are already included:

```bash
flask db upgrade
```

If setting up migrations for the first time:

```bash
flask db init
flask db migrate -m "Initial database migration"
flask db upgrade
```

Do not run `flask db init` again if the migrations directory already exists.

### Step 8: Start the application

```bash
python run.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

---

## 🖥️ Application URLs

| Page                | URL               |
| ------------------- | ----------------- |
| Customer Storefront | `/`               |
| Admin Login         | `/api/auth/login` |
| Admin Dashboard     | `/admin`          |
| Health Check        | `/health`         |

The login page uses a browser GET route, while the authentication API accepts POST requests.

---

## 🔐 Security Considerations

CloudCart incorporates several foundational security practices:

* Password hashing.
* Login-required routes.
* Administrator role checks.
* Environment-based configuration.
* Database-backed user authentication.
* Server-side product stock validation.
* Git exclusion of sensitive environment files.

### Production Security Roadmap

Before production deployment, implement or verify:

* HTTPS/TLS.
* Secure session cookie settings.
* CSRF protection for state-changing browser requests.
* Rate limiting on authentication endpoints.
* Strong production secrets.
* Restricted database network access.
* Production-grade WSGI server.
* Secure database backups.
* Centralized logging and monitoring.

---

## 🧪 Testing

Basic application checks:

### Health endpoint

```bash
curl http://127.0.0.1:5000/health
```

### Product API

```bash
curl http://127.0.0.1:5000/api/products/
```

### Application syntax validation

```bash
python -m compileall -q app
```

### Recommended Functional Test Cases

* Customer registration.
* Valid and invalid login.
* Product listing.
* Admin product creation.
* Cart quantity update.
* Checkout with available stock.
* Checkout with insufficient stock.
* Order history.
* Admin order status update.
* Unauthorized admin access.

---

## ☁️ Deployment

### Current Development Deployment

CloudCart has been run on an Ubuntu-based AWS EC2 instance.

The current application uses Flask on port `5000` for development and testing.

### Production Deployment Direction

The planned architecture is:

```mermaid
flowchart TD
    A[Internet]
    B[Route 53]
    C[Application Load Balancer]
    D[Containerized CloudCart]
    E[(Amazon RDS PostgreSQL)]
    F[Amazon ECR]
    G[GitHub Actions]
    H[Amazon EKS]

    A --> B
    B --> C
    C --> H
    H --> D
    D --> E
    G --> F
    F --> H
```

This diagram represents the target deployment architecture, not the current deployed infrastructure.

---

## 🚀 DevOps Roadmap

| Phase | Technology           | Planned Work                       |
| ----- | -------------------- | ---------------------------------- |
| 1     | Flask + PostgreSQL   | Application development            |
| 2     | Git + GitHub         | Version control                    |
| 3     | Docker               | Containerization                   |
| 4     | Docker Compose       | Multi-container local environment  |
| 5     | GitHub Actions       | CI/CD pipeline                     |
| 6     | AWS ECR              | Container image registry           |
| 7     | AWS EC2 / ALB        | Cloud deployment                   |
| 8     | Terraform            | Infrastructure as Code             |
| 9     | AWS EKS              | Kubernetes orchestration           |
| 10    | Prometheus + Grafana | Monitoring and observability       |
| 11    | AWS CloudWatch       | Logs and infrastructure monitoring |

---

## 🔮 Future Enhancements

Potential future improvements include:

* Product categories and search.
* Product image uploads.
* Pagination and filtering.
* Customer profile management.
* Order tracking.
* Email notifications.
* Payment gateway integration.
* Product reviews and ratings.
* Automated test coverage.
* Docker-based deployment.
* CI/CD pipeline.
* Kubernetes deployment.
* Infrastructure provisioning using Terraform.
* Monitoring, alerting, and centralized logs.

---

## 👨‍💻 Author

**Chirag Singhal**

DevOps Engineer | AWS | Docker | Kubernetes | Terraform | CI/CD

GitHub: [@drblack2](https://github.com/drblack2)

LinkedIn: [Chirag Singhal](https://linkedin.com/in/chirag-singhal-755756233)

---

## 📄 License

This project is developed for educational, portfolio, and demonstration purposes.

A formal open-source license can be added when the project is ready for public distribution.

---

⭐ If you find this project useful, feel free to explore the repository and follow its development.
