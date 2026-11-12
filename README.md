# Smart Grocery Store Management System

A Python console application for managing a grocery store's products, stock and sales. It uses lists of dictionaries, reusable functions, loops and input checks to support the store's daily tasks.

**Products and sales are kept in memory for the current session. Closing or restarting the program clears the records.**

## Features and menu

| Choice | Operation | What it does |
| --- | --- | --- |
| `1` | Add New Product | Collects product details, prevents duplicate IDs and saves the dictionary with `.append()`. |
| `2` | View All Products | Displays each product's ID, name, category, price and stock. |
| `3` | Search Product | Finds products by ID or full name, ignoring capitalization in names. |
| `4` | Update Product Stock | Adds to the current stock or replaces it with a new quantity. |
| `5` | Process Customer Sale | Checks the product and quantity, calculates the total, reduces stock and records the sale. |
| `6` | View Sales Records | Displays the details of completed sales. |
| `7` | Generate Store Report | Shows product, stock, transaction and revenue totals, low stock, and the highest- and lowest-priced products. |
| `8` | Exit | Ends the program. |

## Requirements and setup

- Python 3 installed and available through the `python` command.
- A terminal, such as Windows PowerShell.
- No external packages are required; `math` is part of Python's standard library.

1. Save `smart_grocery_store.py` in your project folder.
2. Open a terminal in that folder.
3. Run the application:

   ```bash
   python smart_grocery_store.py
   ```

Enter a menu number and press **Enter**. Follow the prompts, entering one value at a time. The menu returns after each operation.

| File | Purpose |
| --- | --- |
| `smart_grocery_store.py` | Application code and explanatory comments. |
| `README.md` | Setup, usage, implementation notes and test cases. |

## Use cases and worked example

### 1. Register products and check inventory

The owner wants to record the stock available at the start of the session. Choose `1` once for each product and enter these details:

| Product ID | Name | Category | Price | Starting stock |
| --- | --- | --- | --- | --- |
| `2` | Mango | Fruit | `200` | `20` |
| `4` | potato | vegetable | `150` | `9` |

Then choose `2` to view both products. Choose `3` and enter `Mango`, `mango` or `2` to find Mango.

Product IDs are the values you assign when adding products. In this example, the valid IDs are `2` and `4`; entering ID `1` returns `Product not found.`

### 2. Complete a customer sale

A customer buys three potatoes. Starting with the inventory above, enter:

```text
Enter your choice: 5
Enter product ID: 4
Enter purchase quantity: 3
```

The application prints:

```text
Product: potato | ID: 4
Quantity: 3 | Total: 450.00
Remaining stock: 6
```

The calculation is `150 × 3 = 450`. Potato stock decreases from `9` to `6`, and one sale is added to `sales`. Choose `6` to view that record.

### 3. Review the store report

After the sale above, choose `7`. The report should contain:

| Report field | Expected result |
| --- | --- |
| Total products | `2` |
| Total available stock | `26` (`20 + 6`) |
| Total sales transactions | `1` |
| Total revenue generated | `450.00` |
| Products below 5 units | None |
| Highest-priced product | Mango, `200.00` |
| Lowest-priced product | potato, `150.00` |

### 4. Restock or correct a stock count

Use option `4` when a delivery arrives or a physical count changes the available quantity:

| Task | Inputs after choosing `4` | Result |
| --- | --- | --- |
| Add five mangoes | ID `2`, action `1`, quantity `5` | Mango stock changes from `20` to `25`. |
| Set the potato count to four | ID `4`, action `2`, quantity `4` | Potato stock becomes `4` and appears in the next low-stock report. |

## Data and functions

`products` is a list of dictionaries. Each dictionary contains `id`, `name`, `category`, `price` and `stock`:

```python
{"id": 2, "name": "Mango", "category": "Fruit", "price": 200.0, "stock": 20}
```

`sales` is a separate list of dictionaries. A completed sale contains:

```python
{"product_id": 4, "product_name": "potato", "quantity_sold": 3, "total_amount": 450.0}
```

| Custom function | Purpose |
| --- | --- |
| `read_integer(prompt, minimum=0)` | Repeats the prompt until the input is a whole number at or above the minimum. |
| `read_price()` | Accepts a non-negative, finite price and rounds it to two decimal places. |
| `find_product(product_id)` | Returns the matching product dictionary, or `None` when the ID is absent. |
| `display_product(product)` | Prints all product fields and formats the price to two decimal places. |

The program uses `while` loops for the menu and repeated prompts, `for` loops to process records, dictionary keys to access fields, and `if`/`elif`/`else` statements for decisions. Input is checked before conversion; there are no `try`/`except` blocks.

## Input and reporting rules

| Field or operation | Rule |
| --- | --- |
| Product ID | A unique whole number of `1` or more. |
| Name and category | Cannot be empty or contain only spaces. Category wording is stored as entered. |
| Price | Zero or a positive decimal number, such as `200` or `200.50`. Negative numbers, letters, `nan` and `inf` are rejected. |
| Available stock | A whole number of `0` or more. |
| Stock addition | A whole number of `1` or more. |
| Purchase quantity | A whole number of `1` or more, no greater than available stock. |
| Search | An exact ID or full name; name matching ignores capitalization. |
| Low stock | Stock strictly below `5`, including `0`. Stock of exactly `5` is excluded. |

Invalid numeric inputs prompt again. Duplicate IDs, blank product details, missing products and insufficient stock return to the menu without saving the rejected operation.

Each successful sale covers one product and counts as one transaction. Revenue is the sum of recorded sale amounts, while the highest and lowest prices refer to product unit prices. If prices tie, the first-added matching product is shown. Prices use Python floating-point numbers and are rounded/formatted to two decimal places.

## Test cases

**Verification result: 30 scenarios passed.** Checks used scripted input, captured console output and the resulting product and sales records.

Each case is independent. Unless a case says **Fresh run** or describes a restart, begin a new session and add both products from use case 1 with their original stocks (`20` and `9`). For product-entry tests, use the Mango example for fields not specified. Enter consecutive values one at a time when the program prompts.

| ID | Scenario | Input / steps | Expected result |
| --- | --- | --- | --- |
| T01 | Empty inventory | Fresh run: option 2 | No products available. |
| T02 | Add a product | Fresh run: option 1; Mango example | One product saved with ID 2, price 200.00 and stock 20. |
| T03 | Duplicate ID | Option 1; ID 2 | Duplicate rejected; product count stays 2. |
| T04 | View all products | Option 2 | Both products display all five fields. |
| T05 | Search by ID | Option 3; 2 | Mango details display. |
| T06 | Search by name | Option 3; mAnGo | Mango details display despite different capitalization. |
| T07 | Missing search result | Option 3; 999 | Product not found. |
| T08 | Add stock | Option 4; ID 2; add 5 | Mango stock becomes 25. |
| T09 | Replace stock | Option 4; ID 4; set to 3 | Potato stock becomes 3. |
| T10 | Update unknown ID | Option 4; ID 1 | Product not found; stock stays 20 and 9. |
| T11 | Successful sale | Option 5; ID 4; quantity 3 | Total 450.00; potato stock 6; one sale saved. |
| T12 | Insufficient stock | Option 5; ID 4; quantity 10 | Sale rejected; potato stock remains 9; no sale saved. |
| T13 | Invalid sale quantities | Option 5; ID 4; enter 0, -2, abc, then 1 | Invalid values prompt again; only quantity 1 sells for 150.00. |
| T14 | Sale with unknown ID | Option 5; ID 1 | Product not found; no sale saved. |
| T15 | Empty sales history | Fresh run: option 6 | No sales recorded. |
| T16 | View completed sales | Sell 3 potatoes, then option 6 | History shows ID 4, potato, quantity 3 and total 450.00. |
| T17 | Worked-example report | Sell 3 potatoes, then option 7 | 2 products; 26 units; 1 transaction; revenue 450.00. |
| T18 | Empty report | Fresh run: option 7 | All totals 0; no low-stock products; highest/lowest N/A. |
| T19 | Low-stock boundary | Set stocks to 0 and 4; add Water (ID 6, price 10, stock 5); option 7 | Stocks 0 and 4 are listed as low; stock 5 is excluded. |
| T20 | Invalid IDs and stock | Fresh run: ID abc, 2.5, -1, 0, then 2; stock -1, x, 1.5, then 20 | Invalid inputs prompt again; valid Mango product saved. |
| T21 | Invalid prices | Fresh run: price -1, abc, nan, inf, 1.2.3, blank, then 200 | Invalid prices prompt again; 200 is accepted. |
| T22 | Zero price and stock | Fresh run: add ID 2 with price 0 and stock 0 | Product is accepted with zero price and zero stock. |
| T23 | Blank name or category | Fresh run: blank name; retry with a spaces-only category | Both attempts rejected; no product saved. |
| T24 | Invalid main-menu choice | Fresh run: 0, 9, abc | Invalid-choice message each time; menu continues. |
| T25 | Invalid stock action | Option 4; ID 2; action 9 | Invalid choice; stock stays 20 and 9. |
| T26 | Price rounding and display | Fresh run: price 12.346, stock 1; then option 2 | Price is stored and displayed as 12.35. |
| T27 | No low-stock products | Option 7 with original example stocks | Low-stock section says None. |
| T28 | Equal product prices | Fresh run: add both examples priced at 200; option 7 | First-added product appears as both highest and lowest. |
| T29 | Exit | Fresh run: option 8 | Goodbye! prints and the menu stops. |
| T30 | Restart behavior | Add products and a sale; exit; start again; choose 2 and 6 | New session starts with empty product and sales lists. |

The restart test confirms the intended session-only storage: records from the previous run are not loaded when the application starts again.
