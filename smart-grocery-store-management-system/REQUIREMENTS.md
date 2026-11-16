# Requirements and Assumptions

## Specification reviewed

The user supplied `README(2).md`, describing the Smart Grocery Store Management System. The assessment-brief field in the request is still `[paste the assessment instructions here]`. This submission uses the attached README as its available functional specification. No separate assessment sheet, required repository name, author identity, GitHub username, deadline, marking weights or grading rubric was supplied. Alignment with an unseen assessment rubric cannot be confirmed.

## Required application deliverables

| Requirement | Delivery |
| --- | --- |
| Language and interface | Python console application with a repeating eight-choice menu. |
| Exact application filename from the source | `smart_grocery_store.py` at the repository root. |
| Documentation filename | `README.md` at the repository root. |
| Program structure | One application file, matching the source README; each menu operation has a reusable function. |
| Runtime dependencies | Standard library only. |
| Product storage | A list of dictionaries with `id`, `name`, `category`, `price`, `stock`. |
| Sale storage | A separate list with `product_id`, `product_name`, `quantity_sold`, `total_amount`. |
| Session lifetime | Lists start empty; exiting or restarting clears records; no persistence is added. |
| 1 — Add New Product | Unique positive ID; non-blank name/category; non-negative finite price and whole-number stock; append only a complete valid record. |
| 2 — View All Products | Print all five fields for every product; handle an empty list. |
| 3 — Search Product | Exact ID or full name; ignore name capitalization; print a not-found message when needed. |
| 4 — Update Product Stock | Add a positive whole number or replace with a non-negative whole number; reject missing products and invalid actions. |
| 5 — Process Customer Sale | Existing product; positive whole-number quantity within stock; calculate total; reduce stock and append one sale. |
| 6 — View Sales Records | Print completed transactions or an empty-history message. |
| 7 — Generate Store Report | Product count, stock total, transaction count, revenue, products below 5 units and highest/lowest unit prices. |
| Price ties | First-added product wins; empty inventory shows N/A. |
| 8 — Exit | Print Goodbye and end the loop. |
| Repeated validation | Invalid numeric input repeats; rejected duplicates, blanks, missing products or insufficient stock return to the menu. |
| Implementation topics | Lists, dictionaries, functions, while/for loops, if/elif/else, formatted output and validation before conversion. |
| Original verification scenarios | T01–T30 retained and executed; T31–T70 plus P01–P02 extend verification. |

## User delivery requirements

| Request | Included result |
| --- | --- |
| Review all requirements before documentation | This file, functional tests and the captured test log. |
| Clear names, small reusable functions, useful comments and constants | Application functions and named limits/menu constants. |
| Independent solution for the supplied topic | Application written for this submission from the documented behaviour; no classroom sample code supplied or copied. |
| Test normal, boundary, isolated failure, combined failure and invalid input cases | 70 console scenarios and 2 process checks with output/state assertions. |
| Use actual output only | README samples extracted verbatim from the passing runs; complete captures in `tests/recorded_runs.json`. |
| Banner around 1000×260 | `assets/banner.svg` at exactly 1000×260; white canvas with an inset gradient, title, subtitle, chips and highlighted code window. |
| Overview card for every task | `assets/overview.svg`, eight cards with file, topic, input, rule, output and concepts. |
| Flowchart per task | Eight `*_flow.svg` files with relevant input, validation, branching, traversal/retry and return/end paths. |
| Suitable UML | `assets/uml_diagram.svg`; a module diagram for the procedural application. |
| Self-contained SVGs and consistent colours | White canvases, local sans-serif fallback, no linked fonts/images; blue input, purple decision, green success, red error, amber warning. |
| PNG render and visual check | PNG copy of each of the eleven SVGs; rendered previews inspected for legibility, clipping and arrows. |
| README structure | Banner; overview; folder structure; eight task sections; UML; concepts; run instructions; real samples; test tables; author footer. |
| Per-task documentation | Summary, rules, flow image, methods table, input validation and expected results. |
| Real filenames/functions and relative image paths | All referenced files, helpers and operations exist; images use `assets/...`. |
| GitHub-ready extras | `.gitignore` plus a standard-library test workflow in `.github/workflows/tests.yml`. |
| Complete folder and ZIP | Repository folder plus a complete delivery archive. |
| Light/dark rendered README previews outside repo | Offline `previews/README-light.html` and `previews/README-dark.html` in the delivery archive. |
| Syntax and SVG validation | Python compilation, XML/asset checks and visual review completed before packaging. |
| Upload checklist | `UPLOAD_CHECKLIST.md` alongside, outside the repository folder. |

## Assumptions and additions

- **Repository/folder:** `smart-grocery-store-management-system` is a descriptive assumption; no official name was supplied.
- **Identity:** `YOUR_NAME` and `YOUR_USERNAME` are explicit fields to replace, not claimed author information.
- **Python:** the delivery targets Python 3.10+; local execution used Python 3.12.14. The CI matrix is configured for 3.10, 3.12 and 3.13 but has not been executed remotely.
- **Task boundaries:** the source specifies one console application, so its eight menu operations are documented as tasks within one Python file.
- **Numeric safety additions:** ASCII numeric input, at most 18 significant digits for each integer input, and finite-sale/revenue checks prevent conversion failures and overflow. Leading zeros do not count toward the limit. Stock additions can accumulate beyond the per-input limit.
- **Prices:** preserve Python float storage and two-decimal rounding/display. This is a learning application and does not implement exact-decimal accounting, taxes, discounts or multi-product baskets.
- **Search detail:** matching is exact after trimming; all duplicate full-name matches display. Names made entirely of digits can also match as names.
- **Additional folders:** `assets/`, `tests/` and `.github/workflows/` support the user's diagrams, verification and GitHub-readiness requirements. The HTML previews and upload checklist stay outside the repo.
- **Additional root file:** `REQUIREMENTS.md` makes the source review, additions and missing rubric explicit.
- **Publishing:** a complete upload-ready repository is supplied; no GitHub repository has been created or published.
- **Brief overrides:** none could be identified because no separate assessment brief was supplied. The source README's one-file layout takes priority over the generic one-file-per-task preference.
