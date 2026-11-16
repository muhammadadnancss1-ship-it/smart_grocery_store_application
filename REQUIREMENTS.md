# Requirements, Source Review and Assumptions

## Available assessment information

The functional reference is the supplied `smart_grocery_store.py`, supported by the earlier grocery-store README. The assessment-brief field still contains `[paste the assessment instructions here]`. No official repository name, folder layout beyond the application filename, author identity, username, marking weights, deadline or submission portal was supplied. Alignment with an unseen rubric cannot be confirmed.

## Application requirements

| Requirement | Implementation / evidence |
| --- | --- |
| Exact application filename | `smart_grocery_store.py` at the repository root. |
| Single application | All eight menu tasks remain in that one file, matching the supplied code. |
| Data structures | `products` and `sales`, each a list of dictionaries with the original field names. |
| Four helpers | `read_integer`, `read_price`, `find_product`, `display_product`; no invented operation functions. |
| 1: add product | Positive unique ID, non-blank name/category, finite non-negative price, non-negative stock, append a full dictionary. |
| 2: view products | Display all five fields and handle empty inventory. |
| 3: search | Exact ID string or full name using `lower()`; show every match or `Product not found.`. |
| 4: update stock | Add at least 1, or set a value of at least 0; missing ID/invalid action cannot change stock. |
| 5: customer sale | Existing product, positive quantity within stock, rounded total, reduce stock, append one transaction. |
| 6: sales history | Display product ID, name, quantity sold and total amount; handle an empty list. |
| 7: report | Product count, stock total, transaction count, revenue, stock below 5, highest/lowest product records. |
| Ties and empty data | First-added price ties; empty report uses zero totals and N/A extrema. |
| 8: exit | Print Goodbye and break the top-level loop. |
| Session storage | No database or saved data files; restart clears both lists. |
| Topic | Conditions, loops, functions, lists, dictionaries, validation, arithmetic and formatted output. |

## Complete prompt compliance

| Requested item | Delivered item |
| --- | --- |
| A: full requirements review | This document, including missing brief/rubric information and assumptions. |
| A: exact names and no unexplained folders | Original program filename retained; chosen repository name disclosed; all extra folders explained in README. |
| B: clear reusable code, comments, constants, input validation | Supplied four-helper structure retained; named constants and two numeric guards added; no unrelated application rewrite. |
| B: independent work | Documentation and test harness built for the supplied program; no classroom/textbook sample copied. |
| B: one file per task unless specified otherwise | All eight tasks stay in one application file because the source explicitly uses a single menu program. |
| C: run programs with real input | 80 console scenarios and 2 subprocess checks; real captures in `tests/recorded_runs.json`. |
| C: normal, boundary, individual/combined failure and invalid inputs | Original T01–T30 plus T31–T80; stocks 0/4/5, exact-stock sales, text errors, numeric errors, missing IDs, repeated failures, integer/range limits. |
| C: fix found bugs, check syntax | Long-integer crash and sale/revenue overflow fixed; source compiles; regression evidence compares original/corrected runs. |
| C: actual README output only | Examples extracted verbatim from the passing run output; no invented console text. |
| D: banner SVG ~1000×260 | `assets/banner.svg`, exactly 1000×260: title, subtitle, chips, highlighted code, inset gradient on a white canvas. |
| D: overview per task | `assets/overview.svg`, eight cards with filename, topic, input, rules, output and concepts. |
| D: flow per task | Eight `*_flow.svg` assets with relevant start/input/decisions/loops/outputs/return or end. |
| D: fitting UML | Module diagram showing the four helpers, constants, lists and inline menu branches with call arrows. |
| D: white/self-contained/consistent SVGs | Sans-serif local fallback, no linked fonts/images; blue input, purple decision, green output, red error, amber warning. |
| D: render PNG and visually check | PNG counterpart for all 11 SVGs, with visual review before packaging. |
| E: exact README order | Banner, overview table + image, real folder tree, eight task sections, UML, concepts, run instructions, actual samples, test tables, author footer. |
| E: each task's content | Topic summary, rules, flow, code-method/section table, input validation and expected results. |
| E: names and links match files/code | Only the actual four helper functions and real inline branches are described; images use relative `assets/...` paths. |
| F: complete folder + ZIP | GitHub-ready repository and all companion deliverables in one archive. |
| F: light/dark HTML outside repo | Two standalone offline previews in the outer `previews/` folder. |
| F: compilation and SVG checks | Actual syntax checks, XML/reference validation, PNG rendering and visual review. |
| F: upload checklist | Outer `UPLOAD_CHECKLIST.md`: create repo, upload contents/assets, commit, public visibility, copy URL and official submission method. |
| GitHub extras | `.gitignore` and a standard-library CI workflow; no external runtime dependencies. |

## Changes to the uploaded code

The supplied program was used as the starting file, preserving its four functions, eight inline branches, dictionary fields and normal menu behaviour.

1. Added `MAX_INTEGER_DIGITS = 18`, `PRICE_DECIMAL_PLACES = 2` and `LOW_STOCK_THRESHOLD = 5`, replacing repeated business values where relevant.
2. Guarded and normalized integer conversion. A 5,000-digit input previously raised Python's conversion-limit `ValueError`; it now prints a validation error and retries. Leading ASCII zeros are removed before conversion.
3. Checked a sale total and new accumulated revenue with `isfinite()` before reducing stock or appending a sale. The original file could record an infinite amount or produce an infinite revenue report.
4. Corrected the indentation of one search comment and normalized the working copy's line endings. These changes do not alter ordinary behaviour.

The original upload is preserved byte for byte as `source/smart_grocery_store_original.py` outside the repository; `source/submission_changes.patch` shows the exact text changes. `tests/regression_evidence.json` contains actual before/after runs for the numeric defects.

- Original upload SHA-256: `978b7921c793f7f6fa39ef5e597a276628c3050173e9ef8c536535cd3dee91b6`
- Submitted application SHA-256: `527c0d6bc1ce875a07b6d8931067f3b453113faa5a6cca66162d182741695728`

## Assumptions and deliberate limits

- Repository/folder name: `smart-grocery-store-management-system`, assumed because no official name was supplied.
- Identity: `YOUR_NAME` and `YOUR_USERNAME` must be replaced; no identity has been guessed.
- Python target: 3.10+; local tests used 3.12.14. CI is configured for 3.10/3.12/3.13 and has not run remotely.
- Source structure wins over generic task separation: the source is one menu-driven file, so no extra operation functions or main guard were introduced. Importing it starts the menu; run it directly.
- Each integer input has at most 18 digits after removing leading ASCII zeros. Unicode decimal digits are accepted as in the supplied `isdecimal()` checks; non-ASCII leading zeros count toward that length.
- Search compares IDs as strings. `02` does not find ID `2`; names use `lower()`, which is not Unicode case folding. Blank/partial queries produce the normal not-found message.
- Prices retain float rounding/display; exact-decimal accounting, taxes, discounts, multi-product baskets and persistent storage are outside the supplied scope.
- Extra repo folders: `assets/`, `tests/`, `.github/workflows/`. Outer `previews/` and `source/` are delivery companions. `REQUIREMENTS.md` is the only added root documentation file.
- No remote repository was created, published or made public; the upload checklist explains those final steps.
- No additional brief-specific submission steps can be asserted without the official brief. No other brief override was identified.
