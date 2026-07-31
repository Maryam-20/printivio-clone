# Printivo-Style E-Commerce Platform

A Django-based e-commerce web application for a print-on-demand business, supporting product catalog browsing, category filtering, custom design file uploads, session and account-based cart management, user account management, and a reseller/affiliate program.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=flat&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=flat&logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat&logo=bootstrap&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat)
![License](https://img.shields.io/badge/License-Unlicensed-lightgrey?style=flat)

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Applications](#applications)
  - [productApp](#productapp)
  - [orderApp](#orderapp)
  - [authApp](#authapp)
- [Data Models](#data-models)
- [URL Routes](#url-routes)
- [Key Workflows](#key-workflows)
  - [Cart Merge on Login](#cart-merge-on-login)
  - [Anonymous Design File Upload](#anonymous-design-file-upload)
  - [Category & Product Filtering](#category--product-filtering)
- [Setup & Installation](#setup--installation)
- [Environment Configuration](#environment-configuration)
- [Frontend Notes](#frontend-notes)
- [Known Limitations & Open Items](#known-limitations--open-items)
- [Contributing](#contributing)

---

## Overview

This project replicates the core functionality of a print-on-demand e-commerce storefront (modeled on Printivo). It allows anonymous and authenticated users to browse a product catalog organized by category, view individual product details with configurable quantity tiers, upload custom print designs, manage a shopping cart, and maintain a personal account profile. A reseller/affiliate sign-up flow is also included.

The codebase is split into three Django apps, each owning a distinct domain of the application (product catalog, ordering/cart, and authentication/account management).

## Tech Stack

| Layer | Technology |
|---|---|
| Backend framework | Django (Python) |
| Database | MySQL |
| Frontend | Django Templates, Bootstrap 5.3, custom CSS |
| Forms | `django-crispy-forms` |
| Rate limiting | `django-ratelimit` |
| Authentication | Django's built-in `django.contrib.auth`, including the built-in password reset flow |
| Media storage | Django `FileField` / `ImageField`, served via `MEDIA_URL` / `MEDIA_ROOT` in development |
| Icons | Inline SVG (Material Design Icons paths) |

## Project Structure

```
ecommerce/
├── ecommerce/              # Project-level settings, root urls.py
├── productApp/              # Product catalog, categories, product admin forms
├── orderApp/                 # Cart, checkout, design file uploads
├── authApp/                # User signup, profile, account management
├── static/
│   └── css/style.css       # Shared stylesheet across all apps
    └── js/index.js
├── media/                  # User-uploaded files (product images, design files, avatars)
└── templates/
    ├── common.html          # Base template (footer, trusted-companies, reviews, scripts)
    └── lightHeroNav.html    # Secondary base template (breadcrumb-style nav) used by
                              # inner pages (cart, checkout, profile, all-products, etc.)
```

## Applications

### productApp

Owns the product catalog: categories, products, and the quantity/pricing tier structure for each product.

**Responsibilities:**
- Homepage product and category showcase (randomized selection)
- "All Products" page with category-based filtering
- Single product detail page
- Category browsing by name (`?category_name=`)
- Staff-only forms for adding categories and products

**Key views (`productApp/views.py`):**

| View | Purpose |
|---|---|
| `homePageView` | Renders the homepage with a random sample of products and populated categories |
| `allProductView` | Lists all products, optionally filtered by `?category=` query param |
| `singleProductView` | Displays a single product's full detail page |
| `addCategory` | Staff-only form to create a new `Category` |
| `addProduct` | Staff-only form to create a new `Product` (supports image upload) |
| `browseProducts_inCategory` | Displays all products under one category, matched by `?category_name=` |

### orderApp

Owns the shopping cart, checkout process, custom design file uploads, and per-product quantity/price calculation.

**Responsibilities:**
- Custom design file upload per product (supports both authenticated and anonymous users)
- Add-to-cart logic (session-based for anonymous users, database-backed for authenticated users)
- Cart viewing, with automatic session→database cart merge on login
- Dynamic price calculation as quantity selection changes (AJAX endpoint)
- Checkout (in progress — see [Known Limitations](#known-limitations--open-items))

**Key views (`orderApp/views.py`):**

| View | Purpose |
|---|---|
| `designRequestOptions` | Handles the "design request" page and file upload (rate-limited, validated by file type/size) |
| `add_to_cart` | Adds a product (with selected quantity) to the cart — session dict for anonymous users, `CartItems` row for authenticated users |
| `view_cart` | Displays cart contents; merges any pending session cart into the database cart for authenticated users |
| `calculate_price` | AJAX endpoint returning a computed price (unit price × quantity, less a 5% discount) as the quantity selector changes |
| `checkout` | Placeholder — intended to convert cart contents into a confirmed `Order` |

### authApp

Owns user account creation, authentication-adjacent pages, and profile management.

**Responsibilities:**
- Custom sign-up form (extends Django's `UserCreationForm`)
- Post-signup "verify your email" interstitial page
- Profile viewing and editing (split across `User` and `UserProfile`)
- Integrates with Django's built-in password reset views (`django.contrib.auth.urls`)

**Key views (`authApp/views.py`):**

| View | Purpose |
|---|---|
| `createAccountView` | Handles account registration |
| `verifyEmailInfoView` | Static confirmation page shown after signup |
| `ProfileView` | Displays the logged-in user's profile |
| `editProfileView` | Handles editing both `User` fields and `UserProfile` fields via two combined forms |

## Data Models

> The tables below summarize the core models referenced throughout the codebase. Refer to each app's `models.py` for full field definitions, constraints, and `Meta` options.

**productApp**
- `Category` — product category (`name`, and related products via `related_name="prod"`)
- `Product` — core product record (title, image, description, material, finishing, stock status, base pricing fields)
- `ProductQuantityOrderOptions` — per-product selectable quantity tiers (`quantity_per_order`, `price_per_quantity_order`), related to `Product` via `related_name="quantity_options"`

**orderApp**
- `DesignFile` — an uploaded design file, associated with either an authenticated `User` or an anonymous browser `session_key`, scoped to a specific `Product`
- `Cart` — one cart per authenticated user
- `CartItems` — line items within a cart (`product`, `quantity`), related to `Cart` via `related_name="items"`
- `Order` / `OrderItems` — order records and their line items (created at checkout)

**authApp**
- `UserProfile` — extends Django's built-in `User` model with e-commerce-specific fields: profile image, date of birth, phone numbers, shipping address, account type (buyer/reseller/seller), referral code, and verification flags

## URL Routes

### Project root (`ecommerce/urls.py`)

| Path | Include |
|---|---|
| `/admin/` | Django admin |
| `/` | `productApp.homePageView` (site homepage) |
| `/accounts/` | Django's built-in auth URLs (login, logout, password reset flow) |
| `/products/` | `productApp.urls` |
| `/products/` | `orderApp.urls` *(shares the same prefix as productApp — see note below)* |
| `/auth/` | `authApp.urls` |

> **Note:** Both `productApp.urls` and `orderApp.urls` are mounted under the same `/products/` prefix. This works because their internal path patterns don't collide, but it means the two apps' URL namespaces are visually interleaved under one prefix — worth keeping in mind when adding new routes to avoid accidental collisions.

### productApp

| Path | Name |
|---|---|
| `/products/all-products/` | `allProducts` |
| `/products/product-detail/<id>/` | `productDetails` |
| `/products/add-category/` | `add-category` |
| `/products/add-product/` | `add-products` |
| `/products/category/` | `browse-products` |
| `/products/reseller/` | `reseller` |

### orderApp

| Path | Name |
|---|---|
| `/products/<product_title>/design_options/` | `design-request` |
| `/products/cart/<product_id>/` | `add-to-cart` |
| `/products/view-cart/` | `view-cart` |
| `/products/calculate-price/<product_id>/` | `calculate_price` |
| `/products/checkout/` | `checkout` |

### authApp

| Path | Name |
|---|---|
| `/auth/my-profile/` | `myProfile` |
| `/auth/members/sign-up/` | `signup` |
| `/auth/members/verify_email/` | `verify-email` |
| `/auth/members/edit-profile/` | `edit-profile` |

## Key Workflows

### Cart Merge on Login

Anonymous visitors add items to a cart stored in `request.session["cart"]` as a `{product_id: quantity}` dictionary. On visiting the cart page while authenticated (`view_cart`), any pending session cart is merged into the user's persistent `Cart`/`CartItems` records, and the session cart is then cleared to prevent re-merging on subsequent visits.

### Anonymous Design File Upload

Users can upload a custom design file before creating an account. For anonymous visitors, the uploaded file is associated with the current Django session key (`session_key` field on `DesignFile`) rather than a `User`. This upload is protected by:
- File extension allow-list (PNG, JPEG, PSD, AI)
- Maximum file size (2MB)
- IP-based rate limiting (5 uploads/hour) via `django-ratelimit`

### Category & Product Filtering

The "All Products" page and category-specific browsing pages (`browseProducts_inCategory`) filter the product catalog by category name passed via query string, allowing a single reusable template and view per filtering context rather than one view per category.

## Setup & Installation

```bash
# 1. Clone the repository and create a virtual environment
git clone <repository-url>
cd ecommerce
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your database in settings.py (MySQL) and apply migrations
python manage.py makemigrations
python manage.py migrate

# 4. Create a superuser for admin access
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

## Environment Configuration

The following should be defined via environment variables or `settings.py` before running in any shared or production environment:

| Setting | Purpose |
|---|---|
| `SECRET_KEY` | Django cryptographic signing key |
| `DEBUG` | Should be `False` outside local development |
| Database credentials | MySQL host, name, user, password |
| `MEDIA_URL` / `MEDIA_ROOT` | Location for user-uploaded files (product images, design files, avatars) |
| `EMAIL_BACKEND` | Console/file backend for local development; a real SMTP backend for production password-reset emails |
| `LOGIN_URL` | Where unauthenticated users are redirected by `@login_required` |

## Frontend Notes

- `common.html` is the primary base template, providing the footer, "trusted companies," and customer review sections shared across the site.
- `lightHeroNav.html` is a secondary base template used by inner pages (cart, checkout, profile, all-products, design request, signup) that need a breadcrumb-style navigation header rather than the full homepage hero section.
- Styling lives in a single shared `static/css/style.css`, using plain CSS (BEM-adjacent class naming) alongside Bootstrap 5 utility classes and components (modals, dropdowns).
- Responsive breakpoints are implemented at `max-width: 992px` (tablet) and `max-width: 768px` (mobile) via `@media` queries at the end of `style.css`.

## Known Limitations & Open Items

- **Checkout is not yet implemented** (`orderApp.views.checkout` is a placeholder). Converting cart contents into a persisted `Order`/`OrderItems` record, along with payment integration, remains outstanding.
- **Cart quantity updates**: the cart page's quantity dropdown is wired to update the displayed price via an AJAX call (`calculate_price`), but the endpoint that persists a changed quantity back to the cart (session or `CartItems`) needs to be finalized and confirmed end-to-end.
- **Pricing field consistency**: some views reference `product.price_moq`, others reference `product.price_per_unit` or the `ProductQuantityOrderOptions` tier table. These should be reconciled to a single source of truth for "current cart price" to avoid inconsistent totals.
- **Anonymous `DesignFile` cleanup**: uploaded files tied to a `session_key` (rather than a `User`) that are never claimed (user never logs in or completes an order) will accumulate over time. A periodic cleanup task is recommended.
- **URL namespace overlap**: `productApp` and `orderApp` are both mounted at `/products/`; consider distinct prefixes if the route list grows further, to reduce the risk of future path collisions.

## Contributing

This is currently a solo learning/development project. When adding new features:
1. Keep model changes and their corresponding migrations in the same commit.
2. Favor database-level constraints (e.g. `unique_together`, `UniqueConstraint`) over relying on application logic alone to prevent duplicate records.
3. Follow the existing session-for-anonymous / database-for-authenticated pattern when extending cart- or upload-related features, to keep anonymous and authenticated user experiences consistent.