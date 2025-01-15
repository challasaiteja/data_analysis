import uuid
import random
import csv
from datetime import datetime, timedelta

CATEGORIES = ["Electronics", "Books", "Clothing", "Home", "Toys"]
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 50
NUM_PURCHASES = 5000

def generate_customers():
    """
    Generate a list of unique customer IDs.

    The customer IDs are just the first 8 characters of a UUID4.
    """
    customers = []
    for _ in range(NUM_CUSTOMERS):
        customer_id = str(uuid.uuid4())[:8]  # short unique ID
        customers.append(customer_id)
    return customers

def generate_products():
    """
    Generate a list of products with unique IDs and random categories.

    The product IDs are formatted as 'PXXX', where XXX represents a three-digit number.
    Each product is randomly assigned to a category from the predefined CATEGORIES list.

    Returns:
        list: A list of tuples, each containing a product ID and its category.
    """
    products = []
    for i in range(NUM_PRODUCTS):
        product_id = f"P{i:03d}"  # Create a unique product ID
        category = random.choice(CATEGORIES)  # Randomly select a category
        products.append((product_id, category))  # Add the product to the list
    return products

def generate_purchases(customers, products):
    """
    Generate a list of purchases, where each purchase is a tuple representing the customer ID,
    product ID, category, purchase amount, and purchase date.

    The purchases are randomly distributed across the customers and products, with random
    purchase amounts and dates within the last year.

    Args:
        customers: A list of unique customer IDs.
        products: A list of tuples, each containing a product ID and its category.

    Returns:
        list: A list of tuples, each containing the customer ID, product ID, category,
        purchase amount, and purchase date.
    """
    purchases = []
    today = datetime.now()
    for _ in range(NUM_PURCHASES):
        customer_id = random.choice(customers)
        product_id, category = random.choice(products)
        purchase_amount = round(random.uniform(5, 500), 2)
        days_offset = random.randint(0, 365)
        purchase_date = today - timedelta(days=days_offset)
        purchases.append((customer_id, product_id, category, purchase_amount, purchase_date))
    return purchases

def save_to_csv(customers, products, purchases):
    # Save customers
    with open('data/customers.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["CustomerID"])
        for c in customers:
            writer.writerow([c])

    # Save products
    with open('data/products.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ProductID", "Category"])
        for p in products:
            writer.writerow(list(p))

    # Save purchases
    with open('data/purchases.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["CustomerID", "ProductID", "Category", "PurchaseAmount", "PurchaseDate"])
        for pur in purchases:
            writer.writerow([pur[0], pur[1], pur[2], pur[3], pur[4].strftime("%Y-%m-%d")])

def main():
    customers = generate_customers()
    products = generate_products()
    purchases = generate_purchases(customers, products)
    save_to_csv(customers, products, purchases)
    print("Synthetic data generated successfully!")

if __name__ == "__main__":
    main()
