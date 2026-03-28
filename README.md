# GroceryMate Automation Project



## Description

GroceryMate Automation Project is a robust quality assurance framework specifically engineered to streamline the testing lifecycle of the GroceryMate platform. This initiative focuses on the implementation of automated testing suites to validate critical end-to-end user workflows, including **age verification for alcoholic products**, **product rating system**, and **shipping cost changes**. By leveraging advanced automation techniques, the project ensures high software reliability, reduces manual regression efforts, and facilitates continuous integration and delivery for a superior grocery shopping experience.

## Features

- :test_tube: Testing


## Project Structure

```
.
├── pages
│   ├── __init__.py
│   ├── age_verification_page.py
│   ├── base_page.py
│   ├── checkout_page.py
│   ├── login_page.py
│   ├── product_page.py
│   └── shop_page.py
├── tests
│   ├── conftest.py
│   ├── test_age_verification.py
│   ├── test_free_shipping.py
│   ├── test_login.py
│   ├── test_product_review.py
│   ├── test_registration.py
│   ├── test_review_suite.py
│   └── test_shop.py
└── utils
    ├── __init__.py
    ├── constants.py
    └── helpers.py
```