# Coupon System Implementation Documentation

## Overview
This document outlines the implementation of the Coupon Logic within the E-commerce API. The system allows users to validate coupons before purchase and applies them securely during the checkout process.

## 1. Database Models
The system relies on two primary models in `ecommerce/models.py`.

### A. Coupon Model
Stores the rules for discounts.
- **code**: Unique string (e.g., "SAVE20").
- **discount_type**: `flat` (Fixed Amount) or `percent` (Percentage of total).
- **min_purchase_amount**: Minimum cart total required to apply.
- **usage_limit**: Total times the coupon can be used globally.
- **valid_from / valid_to**: Date range for validity.
- **active**: Boolean switch to enable/disable.

### B. CouponUsage Model
Tracks individual usage to prevent abuse.
- **user**: The user who used the coupon.
- **coupon**: The specific coupon used.
- **order**: The order ID where it was applied.
- **used_at**: Timestamp.

---

## 2. API Endpoints

### API 1: Validate & Apply Coupon
Use this API on the **Cart Page** when the user clicks "Apply Coupon". It checks validity without creating an order.

**Endpoint:** `POST /api/coupon/apply/`  
**Auth:** Header `Authorization: Bearer <access_token>`

#### Request Body
```json
{
    "code": "WELCOME50",
    "cart_total": 1500
}
```

#### Response (Success)
```json
{
    "valid": true,
    "message": "Coupon applied successfully",
    "code": "WELCOME50",
    "discount_amount": 500.0,
    "discount_type": "flat",
    "new_total": 1000.0,
    "coupon_id": 12
}
```

#### Response (Error)
```json
{
    "valid": false,
    "error": "Minimum purchase amount of ₹2000 required"
}
```

---

### API 2: Checkout (Place Order with Coupon)
Use this API on the **Checkout Page** when the user clicks "Place Order". This finalizes the discount and records the usage.

**Endpoint:** `POST /api/checkout/`  
**Auth:** Header `Authorization: Bearer <access_token>`

#### Request Body
```json
{
    "address_id": 5,
    "items": [
        {
            "product_id": 101,
            "quantity": 2,
            "variation_id": 3 
        }
    ],
    "coupon_code": "WELCOME50" 
}
```

*Note: `variation_id` and `coupon_code` are optional.*

#### Implementation Logic (Backend)
1.  **Re-Validation**: The backend re-validates the coupon code during order creation to ensure rules haven't changed since the user last checked.
2.  **Calculation**: Calculates the final discount based on the implementation in `Coupon.calculate_discount()`.
3.  **Order Record**: 
    - Saves `coupon_id` in the `Order` table.
    - Saves `discount_total` in the `Order` table.
4.  **Usage Record**:
    - Creates a record in `CouponUsage` table linked to the User and Order.
    - Increments the `used_count` on the Coupon model.

#### Response (Success)
```json
{
    "message": "Order created successfully",
    "order_id": 455
}
```

#### Response (Error - Invalid Coupon)
If the coupon becomes invalid (e.g., expires right before clicking), the order will **fail** to prevent monetary loss.
```json
{
    "coupon_code": [
        "Coupon usage limit reached"
    ]
}
```

---

## 3. Frontend Integration Flow

1.  **Cart Screen**:
    - User enters code in a text input.
    - Call `POST /api/coupon/apply/`.
    - If `valid: true`, show the discount amount and the "New Total" in the UI. Save the `code` in the component state.
    - If `valid: false`, show the error message (e.g., "Expired").

2.  **Checkout Screen**:
    - When sending the payload to create the order, include the valid `coupon_code` from the state in the `POST /api/checkout/` body.
    - Handle 400 Bad Request errors in case the coupon became invalid during the process.
