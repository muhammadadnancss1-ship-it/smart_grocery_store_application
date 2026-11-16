# Used to check that a price is a finite number.
from math import isfinite

# Named limits for input safety, price rounding and the store report.
MAX_INTEGER_DIGITS = 18
PRICE_DECIMAL_PLACES = 2
LOW_STOCK_THRESHOLD = 5

# Keep product details and completed sales in separate lists.
products = []
sales = []


def read_integer(prompt, minimum=0):
    # Read the input as text first so we can check it before using int().
    while True:
        number = input(prompt).strip()

        # Only convert the input when it contains digits.
        if (number.isdecimal()
                and len(number.lstrip("0") or "0") <= MAX_INTEGER_DIGITS):
            number = int(number.lstrip("0") or "0")

            # Stock can be zero, but IDs and sale quantities must start at 1.
            if number >= minimum:
                return number

        print(
            f"Enter a whole number of {minimum} or more "
            f"with at most {MAX_INTEGER_DIGITS} significant digits."
        )


def read_price():
    while True:
        price = input("Enter price: ").strip()

        # Remove one dot to check that the rest of the price is digits.
        if price.replace(".", "", 1).isdecimal():
            price = float(price)

            # Very large numbers can become infinity, so check before saving.
            if isfinite(price):
                return round(price, PRICE_DECIMAL_PLACES)

        print("Enter a valid price of 0 or more.")


def find_product(product_id):
    # Look through the list and return the product with this ID.
    for product in products:
        if product["id"] == product_id:
            return product

    # None means the ID was not found.
    return None


def display_product(product):
    # .2f shows the price with two digits after the decimal point.
    print(
        f"ID: {product['id']} | Name: {product['name']} | "
        f"Category: {product['category']} | "
        f"Price: {product['price']:.2f} | Stock: {product['stock']}"
    )


# Keep showing the menu until the user chooses to exit.
while True:
    print("""
====================================
SMART GROCERY STORE SYSTEM
====================================
1. Add New Product
2. View All Products
3. Search Product
4. Update Product Stock
5. Process Customer Sale
6. View Sales Records
7. Generate Store Report
8. Exit
""")

    # strip() removes any spaces at the start or end of the input.
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        # Check the ID before asking for the rest of the product details.
        product_id = read_integer("Enter product ID: ", 1)

        if find_product(product_id) is not None:
            print("This product ID already exists.")

            # Go back to the menu without adding a duplicate product.
            continue

        name = input("Enter product name: ").strip()
        category = input("Enter category: ").strip()

        # Don't save a product if its name or category is blank.
        if not name or not category:
            print("Product name and category cannot be empty.")
            continue

        price = read_price()
        stock = read_integer("Enter available stock: ")

        # append() adds all these details as one dictionary in the list.
        products.append({
            "id": product_id,
            "name": name,
            "category": category,
            "price": price,
            "stock": stock
        })

        print("Product added successfully.")

    elif choice == "2":
        if not products:
            print("No products available.")

        # Show each product using the same display function.
        for product in products:
            display_product(product)

    elif choice == "3":
        search = input("Enter product name or ID: ").strip()

        # Remember whether anything matched the search.
        found = False

        for product in products:
            # Compare IDs as text and ignore capital letters in names.
            if (search == str(product["id"])
                    or search.lower() == product["name"].lower()):
                display_product(product)
                found = True

        if not found:
            print("Product not found.")

    elif choice == "4":
        product_id = read_integer("Enter product ID: ", 1)
        product = find_product(product_id)

        if product is None:
            print("Product not found.")
            continue

        print("1. Add stock\n2. Set available stock")
        stock_choice = input("Enter your choice: ").strip()

        # This is the dictionary in products, so the stock change stays in the list.
        if stock_choice == "1":
            # Add this quantity to the stock already available.
            product["stock"] += read_integer("Enter stock to add: ", 1)

        elif stock_choice == "2":
            # Replace the old stock with the quantity entered here.
            product["stock"] = read_integer("Enter new stock quantity: ")

        else:
            print("Invalid choice.")
            continue

        display_product(product)

    elif choice == "5":
        product_id = read_integer("Enter product ID: ", 1)
        product = find_product(product_id)

        if product is None:
            print("Product not found.")
            continue

        # A sale needs at least one unit and cannot exceed the available stock.
        quantity = read_integer("Enter purchase quantity: ", 1)

        if quantity > product["stock"]:
            print(f"Insufficient stock. Available: {product['stock']}")
            continue

        # Calculate and validate the amount before changing any records.
        total_amount = round(product["price"] * quantity, PRICE_DECIMAL_PLACES)
        current_revenue = 0
        for previous_sale in sales:
            current_revenue += previous_sale["total_amount"]

        if (not isfinite(total_amount)
                or not isfinite(current_revenue + total_amount)):
            print("Sale amount is too large. Stock unchanged; sale not recorded.")
            continue

        product["stock"] -= quantity

        # Keep a separate record of this completed sale.
        sales.append({
            "product_id": product["id"],
            "product_name": product["name"],
            "quantity_sold": quantity,
            "total_amount": total_amount
        })

        print(f"Product: {product['name']} | ID: {product['id']}")
        print(f"Quantity: {quantity} | Total: {total_amount:.2f}")
        print(f"Remaining stock: {product['stock']}")

    elif choice == "6":
        if not sales:
            print("No sales recorded.")

        # Read the details of each sale from the sales list.
        for sale in sales:
            print(
                f"ID: {sale['product_id']} | Name: {sale['product_name']} | "
                f"Quantity sold: {sale['quantity_sold']} | "
                f"Total amount: {sale['total_amount']:.2f}"
            )

    elif choice == "7":
        # Start at zero and add up the stock and completed sales.
        total_stock = 0
        total_revenue = 0

        for product in products:
            total_stock += product["stock"]

        for sale in sales:
            total_revenue += sale["total_amount"]

        print("\nSTORE REPORT")

        # len() counts the products and the completed sales transactions.
        print(f"Total products: {len(products)}")
        print(f"Total available stock: {total_stock}")
        print(f"Total sales transactions: {len(sales)}")
        print(f"Total revenue generated: {total_revenue:.2f}")

        # Skip the price comparisons when there are no products.
        if not products:
            print(f"Products below {LOW_STOCK_THRESHOLD} units: None")
            print("Highest-priced product: N/A")
            print("Lowest-priced product: N/A")
            continue

        # Use the first product as the starting point for both comparisons.
        highest_price_product = products[0]
        lowest_price_product = products[0]
        low_stock_found = False

        print(f"\nProducts below {LOW_STOCK_THRESHOLD} units:")

        for product in products:
            # Zero stock also counts as low stock.
            if product["stock"] < LOW_STOCK_THRESHOLD:
                display_product(product)
                low_stock_found = True

            # Keep the most expensive and cheapest products found so far.
            if product["price"] > highest_price_product["price"]:
                highest_price_product = product

            if product["price"] < lowest_price_product["price"]:
                lowest_price_product = product

        if not low_stock_found:
            print("None")

        print("\nHighest-priced product:")
        display_product(highest_price_product)

        print("Lowest-priced product:")
        display_product(lowest_price_product)

    elif choice == "8":
        print("Goodbye!")

        # break ends the menu loop and stops the program.
        break

    else:
        print("Invalid choice. Enter a number from 1 to 8.")