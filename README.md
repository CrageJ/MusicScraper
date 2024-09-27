# Music Scraper CLI

This is a command-line interface for scraping and retrieving music album data from various websites.

Features:
- Scrapes the top x rated albums for any year from 4 different music rating websites



## Prerequisites

- Python 3.10+
- Poetry

## Installation

1. Clone this repository
2. Navigate to the project directory
3. Run `poetry install` to install dependencies
4. Change `.env.template` to .env. Add spotify api credentials if you choose.

## Usage

Use the following command structure to run the Music Scraper CLI:

```
poetry run python CLI.py <appname> <command> <from_year> <to_year> <top_x> [options]
```

### Parameters:

- `<appname>`: Name of the application database (stored in root directory in /db)
- `<command>`: One of `scrape`, `get_content`, or `get_aggregated_content`
- `<from_year>`: Start year for the data range
- `<to_year>`: End year for the data range
- `<top_x>`: Number of top entries to retrieve

### Options:

- `--aoty`: Include Album of the Year
- `--bea`: Include Best Ever Albums (currently disabled)
- `--rym`: Include Rate Your Music (currently disabled)
- `--meta`: Include Metacritic (currently disabled)

### Examples:

1. Scrape data:
   ```
   poetry run python CLI.py myapp scrape 2020 2023 100 --aoty
   ```
   This scrapes the top 100 albums from Album of the Year for the years 2020 to 2023.

2. Get content:
   ```
   poetry run python CLI.py myapp get_content 2020 2023 50 --aoty
   ```
   This retrieves the top 50 albums from Album of the Year for the years 2020 to 2023.

3. Get aggregated content:
   ```
   poetry run python CLI.py myapp get_aggregated_content 2020 2023 25 --aoty
   ```
   This retrieves the top 25 aggregated albums from Album of the Year for the years 2020 to 2023.

Note: Currently, only the Album of the Year (`--aoty`) option is functional. The other website options (`--bea`, `--rym`, `--meta`) are disabled in the current implementation.

## Output

The `get_content` and `get_aggregated_content` commands will print the retrieved data as JSON to the console.

## Logging

The application logs its start and end in the console.

```

This README provides a clear explanation of how to use the Music Scraper CLI with Poetry, including the command structure, parameters, options, and example commands. It also notes the current limitations (only AOTY being functional) and describes the expected output. You can adjust or expand this README as needed to fit your project's specific requirements or to add more detailed information.
