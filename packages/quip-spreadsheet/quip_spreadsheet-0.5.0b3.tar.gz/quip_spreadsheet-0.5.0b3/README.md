# Quip Spreadsheet

[![PyPI Latest Release](https://img.shields.io/pypi/v/quip-spreadsheet.svg)](https://pypi.org/project/quip-spreadsheet/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An opinionated client to search, retrieve, and parse Quip spreadsheets using the [Quip Automation API](https://quip.com/dev/automation/documentation).

It provides a client to pull data from the Quip API as well as classes to interact with folders, spreadsheets, pages, and rows.

## Install

```sh
pip install quip-spreadsheet
```

## Usage

```py
# Import
from quip_spreadsheet.quip import QuipPage
# Initialize Client
quip = QuipClient(QUIP_ACCESS_TOKEN, QUIP_BASE_URL)
# Search by term
threads = quip.search_threads("My Spreadsheet", count=1)
# Load the content of a spreadsheet
spreadsheet = threads.spreadsheets[0]
spreadsheet.load_content()
# Get a specific page of a spreadsheet
page = spreadsheet.get_named_page("Sheet1")
# Get a specific row from a page
row = page.get_nth_row(pointer)
# Get cells content from a row
cells = row.get_row_cells_content(include_index=False)
```

## License

[MIT](https://github.com/dreamorosi/quip-spreadsheet/blob/main/LICENSE)

## Contributing & Developing

PRs are welcome as long as documented, accompained by passing unit tests and in scope with the project.

To setup the development environment run:

```sh
pipenv install --dev
```

or manually install all the development dependencies found in the [Pipfile](https://github.com/dreamorosi/quip-spreadsheet/blob/main/Pipfile).
