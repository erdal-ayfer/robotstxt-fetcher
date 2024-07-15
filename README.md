# Robots.txt Fetcher

This script is designed to fetch the `robots.txt` files for a list of URLs provided in a CSV file. It processes each URL, fetches the `robots.txt` file, and saves it to a specified directory. Additionally, it generates a new CSV file with paths to the fetched `robots.txt` files.

## Installation

1. Clone the repository or download the script files to your local machine.
2. Navigate to the directory containing the script files.
3. Install the required Python packages using pip:

   ```sh
   pip install requests pandas

## Directory Structure

```
project_directory/
│
├── stats/
│   └── url_stats/
│       └── test.csv    # csv file to fetch
│
├── robots/
│
├── output_download/
│
└── fetch_robots.py
```

* `stats/url_stats/test.csv`: The input CSV file containing the URLs to process.
* `robots/`: The directory where fetched robots.txt files will be saved.
* `output_download/`: The directory where the output CSV files will be saved.
* `fetch_robots.py`: The script file.

## Example test.csv
````
fqdn,docs,freq
example.com,example documentation,weekly
anotherexample.com,another documentation,daily
````

## Usage
1. Ensure the directory structure and input CSV file are correctly set up.
2. Run the script
3. The script will process the URLs in the input CSV file, fetch the robots.txt files, and save them to the `robots/` directory. It will also generate a new CSV file in the `output_download/` directory with paths to the fetched robots.txt files.

