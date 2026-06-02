# Lieferspatz - DB Project Nov 2024

A comprehensive, full-stack food delivery application that connects customers with restaurants and enables real-time order management. Lieferspatz is built with Flask, SQLite, and WebSocket technology to provide a seamless ordering and delivery experience.

## 📋 Project Overview

Lieferspatz is a modern food delivery platform designed to facilitate transactions between customers and restaurants. The application implements a two-user-model architecture where customers can browse available restaurants, place orders, and complete payments, while restaurants can manage their menu items, view incoming orders, and update order statuses in real-time.

The platform emphasizes **real-time communication** between customers and restaurants through WebSocket integration, **secure authentication** using password hashing, and **location-based service discovery** using ZIP code filtering.

## ✨ Key Features

### Customer Features
- **User Registration & Authentication**: Secure sign-up with phone number validation and password hashing
- **Location-Based Restaurant Discovery**: Automatic filtering of available restaurants based on customer's ZIP code
- **Browse Menu**: View restaurant menus organized by category with item descriptions, prices, and images
- **Shopping Cart Management**: Add items to cart, maintain cart state across sessions, with single-restaurant restriction to simplify logistics
- **Place Orders**: Complete order placement with special delivery notes
- **Real-Time Order Tracking**: WebSocket integration for real-time communication with restaurant about order status
- **Payment Confirmation**: Receive order confirmation with payment details

### Restaurant Features
- **Restaurant Registration**: Register with business details, operating hours, and service areas (delivery ZIP codes)
- **Menu Management**: Full CRUD operations for menu items with image uploads
  - Add new items with name, price, description, and category
  - Edit existing items and update menu
  - Organize items by category for better customer experience
- **Order Management Dashboard**: Centralized view of incoming, in-progress, and completed orders
- **Real-Time Order Notifications**: Receive customer orders and payment notifications via WebSocket
- **Order Status Updates**: Update order status through workflow: In Process → In Delivery → Completed/Rejected
- **Order History**: View all completed and rejected orders with detailed order information
- **Dynamic Status Display**: Restaurant dashboard shows real-time operational status (OPEN/CLOSED) based on configured business hours

### Administrative Features
- **Two-Role Authentication System**: Distinct authentication flows for customers and restaurants
- **Session Management**: Secure session handling with role-based access control
- **Session Clearing on Logout**: Complete session data cleanup for security

## 🛠 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Flask (Python) |
| **Real-Time Communication** | Flask-SocketIO (WebSocket) |
| **Database** | SQLite |
| **Password Hashing** | Werkzeug Security |
| **File Uploads** | Werkzeug utilities |
| **Frontend** | HTML5, CSS3, Jinja2 Templates |
| **Client-Side Scripting** | Vanilla JavaScript |

## 📊 Application Flow

### Customer Order Flow
1. Customer registers with personal information and delivery ZIP code
2. Customer logs in and views available restaurants (filtered by ZIP code)
3. Customer selects a restaurant and browses menu items by category
4. Customer adds items to shopping cart
5. Customer reviews order and submits with delivery notes
6. Customer receives real-time order status updates
7. Order completion notification sent via WebSocket

### Restaurant Operations Flow
1. Restaurant registers with business details and service areas (multiple ZIP codes)
2. Restaurant adds menu items with images, categories, and prices
3. Restaurant monitors incoming orders on dashboard
4. Restaurant updates order status as it processes
5. Restaurant can reject orders if needed
6. Restaurant views order history and analytics

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Lieferspatz
```

2. Install dependencies:
```bash
pip install flask flask-socketio python-socketio python-engineio werkzeug
```

3. Run the application:
```bash
python app.py
```

4. Access the application:
- Open browser and navigate to `http://localhost:5000`
- Application runs with debug mode enabled

### Default Application Flow
- **Home Page**: `http://localhost:5000/`
- **Customer Registration**: `http://localhost:5000/register/customer`
- **Restaurant Registration**: `http://localhost:5000/register/restaurant`
- **Login**: `http://localhost:5000/login`