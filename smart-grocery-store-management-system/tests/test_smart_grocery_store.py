"""Repeatable, dependency-free console scenarios and fresh-process checks.

Each T-number starts with a fresh application. Inputs are echoed by the test
reader so recorded output shows precisely what was entered at every prompt.
"""

import contextlib
import io
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


APP_PATH = Path(__file__).resolve().parents[1] / "smart_grocery_store.py"


def product_inputs(product_id, name, category, price, stock):
    """Build menu inputs for one complete product registration."""
    return ["1", str(product_id), name, category, str(price), str(stock)]


MANGO = product_inputs(2, "Mango", "Fruit", 200, 20)
POTATO = product_inputs(4, "potato", "vegetable", 150, 9)
BASE = MANGO + POTATO
RECORDED_RESULTS = {}


def scenario(number, title, steps, expected, *, seed=True, **checks):
    """Keep executable inputs, readable expectations and assertions together."""
    return {
        "id": f"T{number:02d}",
        "title": title,
        "inputs": (BASE if seed else []) + steps + ["8"],
        "expected": expected,
        "seeded": seed,
        "steps": steps,
        **checks,
    }


SCENARIOS = [
    scenario(1, "Empty inventory", ["2"], "No products available.", seed=False,
             contains=["No products available."], product_count=0, sales_count=0),
    scenario(2, "Add a product", MANGO, "Mango saved: ID 2, price 200.00, stock 20.",
             seed=False, contains=["Product added successfully."], product_count=1,
             records={2: {"name": "Mango", "category": "Fruit", "price": 200.0, "stock": 20}}),
    scenario(3, "Duplicate ID", ["1", "2"], "Duplicate rejected; two products remain.",
             contains=["Product ID already exists. Product not added."], product_count=2,
             records={2: {"stock": 20}, 4: {"stock": 9}}, sales_count=0),
    scenario(4, "View all products", ["2"], "Both products display all five fields.",
             contains=["ID: 2 | Name: Mango | Category: Fruit | Price: 200.00 | Stock: 20",
                       "ID: 4 | Name: potato | Category: vegetable | Price: 150.00 | Stock: 9"]),
    scenario(5, "Search by ID", ["3", "2"], "Mango details display.",
             contains=["ID: 2 | Name: Mango"], product_count=2),
    scenario(6, "Search by mixed-case name", ["3", "mAnGo"], "Mango details display.",
             contains=["ID: 2 | Name: Mango"]),
    scenario(7, "Missing search result", ["3", "999"], "Product not found.",
             contains=["Product not found."], product_count=2),
    scenario(8, "Add stock", ["4", "2", "1", "5"], "Mango stock becomes 25.",
             contains=["Stock updated. Mango: 25"], records={2: {"stock": 25}}),
    scenario(9, "Replace stock", ["4", "4", "2", "3"], "Potato stock becomes 3.",
             contains=["Stock updated. potato: 3"], records={4: {"stock": 3}}),
    scenario(10, "Update unknown ID", ["4", "1"], "Product not found; stocks stay 20 and 9.",
             contains=["Product not found."], records={2: {"stock": 20}, 4: {"stock": 9}}),
    scenario(11, "Successful sale", ["5", "4", "3"], "Total 450.00; potato stock 6; one sale.",
             contains=["Sale completed.", "Quantity: 3 | Total: 450.00", "Remaining stock: 6"],
             records={4: {"stock": 6}}, sales_count=1, revenue=450.0),
    scenario(12, "Insufficient stock", ["5", "4", "10"], "Sale rejected; stock 9; no sales.",
             contains=["Insufficient stock. Available: 9. Sale not recorded."],
             records={4: {"stock": 9}}, sales_count=0),
    scenario(13, "Invalid sale quantities", ["5", "4", "0", "-2", "abc", "1"],
             "Three errors; quantity 1 sells for 150.00.", error_count=3,
             contains=["Quantity: 1 | Total: 150.00"], records={4: {"stock": 8}}, sales_count=1),
    scenario(14, "Sale with unknown ID", ["5", "1"], "Product not found; no sale.",
             contains=["Product not found."], sales_count=0, records={4: {"stock": 9}}),
    scenario(15, "Empty sales history", ["6"], "No sales recorded.", seed=False,
             contains=["No sales recorded."], sales_count=0),
    scenario(16, "View completed sales", ["5", "4", "3", "6"],
             "History shows ID 4, potato, quantity 3, total 450.00.",
             contains=["Product ID: 4 | Product: potato | Quantity: 3 | Total: 450.00"], sales_count=1),
    scenario(17, "Worked-example report", ["5", "4", "3", "7"],
             "2 products; 26 units; 1 transaction; revenue 450.00.",
             contains=["Total products: 2", "Total available stock: 26", "Total sales transactions: 1",
                       "Total revenue generated: 450.00", "Highest-priced product: Mango (200.00)",
                       "Lowest-priced product: potato (150.00)"], revenue=450.0),
    scenario(18, "Empty report", ["7"], "Zero totals; no low stock; price extrema N/A.",
             seed=False, contains=["Total products: 0", "Total available stock: 0",
                                   "Total sales transactions: 0", "Total revenue generated: 0.00",
                                   "Products below 5 units:\nNone.", "Highest-priced product: N/A",
                                   "Lowest-priced product: N/A"]),
    scenario(19, "Low-stock boundaries together", ["4", "2", "2", "0", "4", "4", "2", "4"]
             + product_inputs(6, "Water", "Drinks", 10, 5) + ["7"],
             "Stocks 0 and 4 appear as low stock; stock 5 is excluded.",
             contains=["ID: 2 | Name: Mango | Category: Fruit | Price: 200.00 | Stock: 0",
                       "ID: 4 | Name: potato | Category: vegetable | Price: 150.00 | Stock: 4"],
             excludes=["ID: 6 | Name: Water"], product_count=3),
    scenario(20, "Invalid IDs and initial stock", ["1", "abc", "2.5", "-1", "0", "2", "Mango",
             "Fruit", "200", "-1", "x", "1.5", "20"],
             "Seven numeric errors; valid Mango saved with stock 20.", seed=False,
             error_count=7, product_count=1, records={2: {"stock": 20}}),
    scenario(21, "Invalid prices", ["1", "2", "Mango", "Fruit", "-1", "abc", "nan", "inf",
             "1.2.3", "", "200", "20"], "Six price errors; price 200.00 accepted.",
             seed=False, price_error_count=6, records={2: {"price": 200.0}}),
    scenario(22, "Zero price and stock", product_inputs(2, "Mango", "Fruit", 0, 0),
             "Zero price and zero stock accepted.", seed=False, product_count=1,
             records={2: {"price": 0.0, "stock": 0}}),
    scenario(23, "Blank product fields together", ["1", "2", "", "1", "2", "Mango", "   "],
             "Both attempts rejected; no products saved.", seed=False, product_count=0,
             contains=["Product name cannot be blank.", "Product category cannot be blank."]),
    scenario(24, "Invalid menu choices", ["0", "9", "abc"],
             "Three invalid-choice messages; menu continues.", seed=False, menu_error_count=3),
    scenario(25, "Invalid stock action", ["4", "2", "9"],
             "Invalid action; both stocks unchanged.", contains=["Invalid stock action. Stock unchanged."],
             records={2: {"stock": 20}, 4: {"stock": 9}}),
    scenario(26, "Price rounding", product_inputs(2, "Mango", "Fruit", "12.346", 1) + ["2"],
             "Price stored and displayed as 12.35.", seed=False,
             contains=["Price: 12.35 | Stock: 1"], records={2: {"price": 12.35}}),
    scenario(27, "No low-stock products", ["7"], "Low-stock section says None.",
             contains=["Products below 5 units:\nNone."]),
    scenario(28, "Equal product prices", MANGO + product_inputs(4, "potato", "vegetable", 200, 9) + ["7"],
             "First-added Mango is both highest and lowest.", seed=False,
             contains=["Highest-priced product: Mango (200.00)", "Lowest-priced product: Mango (200.00)"]),
    scenario(29, "Exit", [], "Goodbye prints once and the menu stops.", seed=False,
             goodbye_count=1, menu_count=1),
    {**scenario(30, "Restart clears records", ["2", "6"],
              "Second session starts with empty products and sales.", seed=False,
              contains=["No products available.", "No sales recorded."], product_count=0, sales_count=0),
     "prior_session": BASE + ["5", "4", "3", "8"]},
    scenario(31, "Minimum product ID", product_inputs(1, "Rice", "Grain", 10, 1),
             "ID 1 is accepted.", seed=False, product_count=1, records={1: {"stock": 1}}),
    scenario(32, "Sell all available stock", ["5", "4", "9", "7"],
             "Sale 1350.00 succeeds; stock becomes 0 and is low.",
             contains=["Remaining stock: 0", "Total revenue generated: 1350.00"],
             records={4: {"stock": 0}}, sales_count=1, revenue=1350.0),
    scenario(33, "Zero-price sale", product_inputs(1, "Water", "Drinks", 0, 2) + ["5", "1", "1"],
             "One free sale recorded; stock 1; revenue 0.00.", seed=False,
             contains=["Quantity: 1 | Total: 0.00"], sales_count=1, records={1: {"stock": 1}}, revenue=0.0),
    scenario(34, "Repeated sales", ["5", "4", "3", "5", "4", "2", "7"],
             "Two sales; revenue 750.00; potato stock 4.",
             sales_count=2, revenue=750.0, records={4: {"stock": 4}},
             contains=["Total sales transactions: 2", "Total revenue generated: 750.00"]),
    scenario(35, "Invalid stock additions", ["4", "2", "1", "0", "-1", "abc", "1.5", "1"],
             "Four errors; only valid addition 1 changes stock to 21.",
             error_count=4, records={2: {"stock": 21}}),
    scenario(36, "Invalid replacement counts", ["4", "4", "2", "-1", "abc", "1.5", "0"],
             "Three errors; valid replacement 0 is accepted.", error_count=3, records={4: {"stock": 0}}),
    scenario(37, "Spaces-only product name", ["1", "2", "   "],
             "Name rejected; no record saved.", seed=False, product_count=0,
             contains=["Product name cannot be blank."]),
    scenario(38, "Empty category", ["1", "2", "Mango", ""],
             "Category rejected; no record saved.", seed=False, product_count=0,
             contains=["Product category cannot be blank."]),
    scenario(39, "Invalid ID during sale", ["5", "0", "abc", "-1", "4", "1"],
             "Three ID errors; valid potato sale records 150.00.",
             error_count=3, sales_count=1, revenue=150.0, records={4: {"stock": 8}}),
    scenario(40, "Invalid ID during update", ["4", "0", "x", "4", "1", "1"],
             "Two ID errors; potato stock becomes 10.", error_count=2, records={4: {"stock": 10}}),
    scenario(41, "Blank search", ["3", "   "], "Search cannot be blank.",
             contains=["Search cannot be blank."], product_count=2),
    scenario(42, "Partial name is not a match", ["3", "Man"], "Product not found.",
             contains=["Product not found."], excludes=["ID: 2 | Name: Mango"]),
    scenario(43, "Duplicate names with distinct IDs", product_inputs(9, "Mango", "Other", 10, 1)
             + ["3", "MANGO"], "Both exact-name matches display.", product_count=3,
             contains=["ID: 2 | Name: Mango", "ID: 9 | Name: Mango"]),
    scenario(44, "Stock exactly five", product_inputs(1, "Boundary", "Test", 10, 5) + ["7"],
             "Stock 5 is not low.", seed=False, contains=["Products below 5 units:\nNone."],
             excludes=["ID: 1 | Name: Boundary"]),
    scenario(45, "Stock exactly four", product_inputs(1, "Boundary", "Test", 10, 4) + ["7"],
             "Stock 4 is listed as low.", seed=False,
             contains=["ID: 1 | Name: Boundary | Category: Test | Price: 10.00 | Stock: 4"]),
    scenario(46, "Stock exactly zero", product_inputs(1, "Boundary", "Test", 10, 0) + ["7"],
             "Stock 0 is listed as low.", seed=False,
             contains=["ID: 1 | Name: Boundary | Category: Test | Price: 10.00 | Stock: 0"]),
    scenario(47, "One-product extrema", MANGO + ["7"],
             "Mango appears as both highest and lowest.", seed=False,
             contains=["Highest-priced product: Mango (200.00)", "Lowest-priced product: Mango (200.00)"]),
    scenario(48, "Leading decimal point", product_inputs(1, "Sample", "Test", ".50", 1),
             "Price .50 is accepted as 0.50.", seed=False, records={1: {"price": 0.5}}),
    scenario(49, "Trailing decimal point", product_inputs(1, "Sample", "Test", "12.", 1),
             "Price 12. is accepted as 12.00.", seed=False, records={1: {"price": 12.0}}),
    scenario(50, "Non-ASCII prices", ["1", "2", "Mango", "Fruit", "١٢", "²", "１２", "200", "20"],
             "Three non-ASCII prices rejected; 200 accepted.", seed=False,
             price_error_count=3, records={2: {"price": 200.0}}),
    scenario(51, "Non-ASCII integer digits", ["1", "٢", "²", "２", "2", "Mango", "Fruit", "200", "20"],
             "Three non-ASCII IDs rejected; ID 2 accepted.", seed=False,
             error_count=3, records={2: {"stock": 20}}),
    scenario(52, "Oversized integer", ["1", "9" * 19, "2", "Mango", "Fruit", "200", "20"],
             "19 significant digits rejected; ID 2 accepted.", seed=False,
             error_count=1, product_count=1),
    scenario(53, "Leading zeros", product_inputs("0" * 25 + "2", "Mango", "Fruit", 200, "00020"),
             "Leading zeros normalize to ID 2 and stock 20.", seed=False,
             records={2: {"stock": 20}}),
    scenario(54, "Price overflow", ["1", "2", "Mango", "Fruit", "9" * 400, "200", "20"],
             "Non-finite price rejected; 200 accepted.", seed=False,
             price_error_count=1, records={2: {"price": 200.0}}),
    scenario(55, "Sale amount overflow", product_inputs(1, "Large", "Test", "1" + "0" * 308, 2)
             + ["5", "1", "2"], "Unrepresentable sale rejected; stock 2; no sales.",
             seed=False, contains=["Sale amount is too large. Stock unchanged; sale not recorded."],
             records={1: {"stock": 2}}, sales_count=0),
    scenario(56, "Accumulated revenue overflow", product_inputs(1, "Large", "Test", "1" + "0" * 308, 2)
             + ["5", "1", "1", "5", "1", "1"],
             "First sale succeeds; second rejected; stock 1; one finite sale.", seed=False,
             contains=["Sale completed.", "Sale amount is too large."], records={1: {"stock": 1}},
             sales_count=1, revenue=1e308),
    scenario(57, "Several invalid fields in one session", ["1", "abc", "0", "3", "Rice", "Grain",
             "-1", "nan", "10", "-1", "x", "2", "5", "3", "0", "bad", "2", "7"],
             "Six integer and two price errors; valid sale totals 20.00; stock 0.", seed=False,
             error_count=6, price_error_count=2, sales_count=1, revenue=20.0, records={3: {"stock": 0}}),
    scenario(58, "Non-numeric stock action", ["4", "2", "abc"],
             "Action rejected; Mango stock remains 20.", contains=["Invalid stock action."],
             records={2: {"stock": 20}}),
    scenario(59, "Empty menu choice", [""], "Invalid choice shown once before exit.",
             seed=False, menu_error_count=1, goodbye_count=1),
    scenario(60, "Rejected sale after a successful sale", ["5", "4", "3", "5", "4", "7"],
             "First sale retained; second rejected; stock 6; revenue 450.00.",
             records={4: {"stock": 6}}, sales_count=1, revenue=450.0,
             contains=["Insufficient stock. Available: 6. Sale not recorded."]),
    scenario(61, "Numeric full product name", product_inputs(7, "123", "Test", 10, 1) + ["3", "123"],
             "Full name 123 finds product ID 7.", seed=False, contains=["ID: 7 | Name: 123"]),
    scenario(62, "Trim surrounding whitespace", [" 1 ", " 2 ", " Mango ", " Fruit ", " 200 ", " 20 "],
             "Whitespace stripped; clean values saved.", seed=False,
             records={2: {"name": "Mango", "category": "Fruit", "price": 200.0, "stock": 20}}),
    scenario(63, "Sales history survives restocking", ["5", "4", "3", "4", "4", "2", "50", "6"],
             "History still shows quantity 3 and 450.00 after stock is set to 50.",
             contains=["Product ID: 4 | Product: potato | Quantity: 3 | Total: 450.00"],
             records={4: {"stock": 50}}, sales_count=1, revenue=450.0),
    scenario(64, "Report across different products", ["5", "2", "2", "5", "4", "3", "7"],
             "2 products; 24 units; 2 transactions; revenue 850.00.", sales_count=2, revenue=850.0,
             contains=["Total products: 2", "Total available stock: 24", "Total sales transactions: 2",
                       "Total revenue generated: 850.00"]),
    scenario(65, "Multiword exact name", product_inputs(1, "Brown Rice", "Dry Goods", 10, 1)
             + ["3", "brown rice"], "Exact multiword name matches ignoring case.", seed=False,
             contains=["ID: 1 | Name: Brown Rice | Category: Dry Goods"]),
    scenario(66, "Menu continues after report", ["7", "2"],
             "Report returns to the menu; inventory can still be viewed.",
             contains=["--- Store Report ---", "--- Products ---"], menu_count=5, product_count=2),
    scenario(67, "Sale in empty inventory", ["5", "1"], "Product not found; no sale.",
             seed=False, contains=["Product not found."], sales_count=0, product_count=0),
    scenario(68, "Update in empty inventory", ["4", "1"], "Product not found; no products.",
             seed=False, contains=["Product not found."], product_count=0),
    scenario(69, "Search in empty inventory", ["3", "Mango"], "Product not found.",
             seed=False, contains=["Product not found."], product_count=0),
    scenario(70, "Zero-stock sale", product_inputs(1, "Water", "Drinks", 0, 0) + ["5", "1", "1"],
             "Sale rejected even at zero price; stock remains 0.", seed=False,
             contains=["Insufficient stock. Available: 0. Sale not recorded."],
             records={1: {"stock": 0}}, sales_count=0),
]


def run_session(inputs):
    """Run the real application entry point using a fully consumed input list."""
    values = iter(inputs)
    output = io.StringIO()

    def read_input(prompt=""):
        try:
            value = next(values)
        except StopIteration as error:
            raise AssertionError(f"Application requested unexpected input: {prompt}") from error
        print(prompt + value)
        return value

    with contextlib.redirect_stdout(output), patch("builtins.input", read_input):
        state = runpy.run_path(str(APP_PATH), run_name="__main__")
    remaining = list(values)
    if remaining:
        raise AssertionError(f"Application did not consume input: {remaining}")
    return {"stdout": output.getvalue(), "products": state["products"], "sales": state["sales"]}


def execute_scenario(case):
    """Run an optional previous session, then the scenario's fresh session."""
    previous = run_session(case["prior_session"]) if "prior_session" in case else None
    result = run_session(case["inputs"])
    if previous is not None:
        result["prior_session"] = previous
    return result


class GroceryScenarios(unittest.TestCase):
    """One independently named test for each of the 70 console scenarios."""


def make_test(case):
    """Turn each scenario into a normal discoverable unittest test method."""
    def test(self):
        result = execute_scenario(case)
        output = result["stdout"]
        for text in case.get("contains", []):
            self.assertIn(text, output)
        for text in case.get("excludes", []):
            self.assertNotIn(text, output)
        for field, text in [("error_count", "Invalid input."),
                            ("price_error_count", "Invalid price."),
                            ("menu_error_count", "Invalid choice."),
                            ("goodbye_count", "Goodbye!"),
                            ("menu_count", "=== Smart Grocery Store Management System ===")]:
            if field in case:
                self.assertEqual(output.count(text), case[field])
        if "product_count" in case:
            self.assertEqual(len(result["products"]), case["product_count"])
        if "sales_count" in case:
            self.assertEqual(len(result["sales"]), case["sales_count"])
        if "revenue" in case:
            self.assertAlmostEqual(sum(sale["total_amount"] for sale in result["sales"]), case["revenue"])
        by_id = {product["id"]: product for product in result["products"]}
        for product_id, fields in case.get("records", {}).items():
            self.assertIn(product_id, by_id)
            for field, value in fields.items():
                self.assertEqual(by_id[product_id][field], value)
        if "prior_session" in case:
            self.assertEqual(len(result["prior_session"]["products"]), 2)
            self.assertEqual(len(result["prior_session"]["sales"]), 1)
        RECORDED_RESULTS[case["id"]] = result
    return test


for case in SCENARIOS:
    setattr(GroceryScenarios, f"test_{case['id']}", make_test(case))


class ProcessChecks(unittest.TestCase):
    """Check genuine separate processes, import behaviour and disk isolation."""

    def test_import_has_no_menu_side_effect(self):
        result = subprocess.run(
            [sys.executable, "-c", "import smart_grocery_store; print('Import completed.')"],
            cwd=APP_PATH.parent, text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Import completed.\n")

    def test_subprocess_restart_and_no_data_files(self):
        with tempfile.TemporaryDirectory() as directory:
            first = subprocess.run(
                [sys.executable, str(APP_PATH)], input="\n".join(BASE + ["5", "4", "3", "8"]) + "\n",
                cwd=directory, text=True, capture_output=True, check=False,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertIn("Quantity: 3 | Total: 450.00", first.stdout)
            second = subprocess.run(
                [sys.executable, str(APP_PATH)], input="2\n6\n8\n", cwd=directory,
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("No products available.", second.stdout)
            self.assertIn("No sales recorded.", second.stdout)
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
