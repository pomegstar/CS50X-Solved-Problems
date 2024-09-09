# FinAid

#### Video Demo: https://youtu.be/M38GECGi2BE?si=r80RaaeuftY6CljX

## Overview

The FinAid is a Django-based web application designed to facilitate the purchase of expensive products through installment payments. Users can set their desired price and monthly installment rate, and once the admin approves the order, users can make payments in installments. The application also allows users to track their payments, view the due amount that have to pay. This system simplifies the process of buying high-value items by offering flexible payment options and a transparent tracking mechanism.


## Project Structure

### 1. `models.py`

This file defines the core data structures of the application:
- `User`: Represents all users, including their name, username, email and password.
- `Order`: Stores user orders, including the product name, desired price, and installment terms.
- `Deal_officer`: Stores the Dealer of the order, user buy products by the reference of them.
- `Installment` : It includes the installment that has been paid.

### 2. `views.py`

This file contains the business logic for handling user interactions:
- Handles the submission of new orders by users, including order status and saving order details.
- Allows users to view the installments of their orders, including installment history and the due installments.
- Enables admins to review and approve or reject user orders. And many more.

### 3. `urls.py`

This file maps URLs to the corresponding view functions, ensuring proper routing of requests:
- Route for creating new orders.
- Route for viewing the installment lists of a specific order.
- Route for admin approval of orders. And many more.

### 4. `templates/`

This directory contains HTML templates used for rendering views:
- Form for users to create a new order.
- Page for users to view their orders and the installment lists of a specific order.
- Interface for admins to review and approve orders. And many more.

### 5. `static/`

This directory holds static files such as CSS that enhance the user interface:
- `styles.css`: Custom styles for the application.

### 6. `requirements.txt`

Lists all Python packages required for the project, ensuring that all dependencies are properly managed and installed.

## Running the Application

1. **Install Dependencies**: Run `pip install -r requirements.txt` to install the necessary Python packages.
2. **Database Setup**: Run `python manage.py migrate` to apply database migrations.
3. **Create Superuser**: Use `python manage.py createsuperuser` to create an admin user for managing the application.
4. **Run Server**: Start the development server with `python manage.py runserver`.
5. **Access the App**: Open your web browser and navigate to `http://127.0.0.1:8000/` to use the application.

## Additional Information

- **User Guide**:
    - A user can't pay installment until the order is accepted by the admin.
    - The value of a Order's due field won't be changed until the installment is accepted by the admin.
    - When a orders due will be zero, that means user has paid all the installments of that order and become the owner of that product.

## Conclusion

The FinAid is a comprehensive solution for handling high-value product purchases through installment payments. It combines user-friendly interfaces with robust backend logic to manage orders and payments effectively. The integration of Django's powerful features and real-time updates ensures a smooth and interactive experience for both users and admins.
