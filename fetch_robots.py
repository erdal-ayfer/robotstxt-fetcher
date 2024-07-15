import warnings
import requests
import pandas as pd
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="http.cookiejar")

# Function to sanitize URL
def sanitize_url(url):
    return url.replace('..', '.').strip()

# Function to fetch robots.txt
def fetch_robots_txt(url):
    full_url = f"http://{sanitize_url(url)}/robots.txt"
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MyBot/1.0)'}
    try:
        response = requests.get(full_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return url, response.status_code, response.text
        else:
            return url, response.status_code, ""
    except requests.RequestException:
        return url, None, ""

# Function to save robots.txt content to a file
def save_robots_txt(url, content, csv_filename):
    sanitized_url = sanitize_url(url)
    dir_path = os.path.join("robots", csv_filename)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, f"{sanitized_url}.robots.txt")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to file {file_path} for URL {url}: {e}")
        return None
    return file_path

# Function to process a single CSV file
def process_csv(file_path):
    csv_filename = os.path.splitext(os.path.basename(file_path))[0]
    df = pd.read_csv(file_path)
    results = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_url = {executor.submit(fetch_robots_txt, row['fqdn']): row for _, row in df.iterrows()}
        for future in as_completed(future_to_url):
            row = future_to_url[future]
            try:
                url, status_code, robots_txt_content = future.result()
                if status_code == 200:
                    file_path = save_robots_txt(url, robots_txt_content, csv_filename)
                    if file_path:
                        results.append({'fqdn': url, 'docs': row['docs'], 'freq': row['freq'], 'Robots': file_path})
                        print(f"Fetched successfully for {url} to {file_path}")
                    else:
                        results.append({'fqdn': url, 'docs': row['docs'], 'freq': row['freq'], 'Robots': "Error Writing File"})
                else:
                    results.append({'fqdn': url, 'docs': row['docs'], 'freq': row['freq'], 'Robots': "Not Reachable"})
                    print(f"Couldn't fetch {url}")
            except Exception as e:
                print(f"Error processing URL {url}: {e}")
                results.append({'fqdn': url, 'docs': row['docs'], 'freq': row['freq'], 'Robots': "Error"})

    results_df = pd.DataFrame(results)

    # Save the results to a new CSV file
    output_path = os.path.join("output_download", f"robots_paths_{csv_filename}.csv")
    results_df.to_csv(output_path, index=False)

    print(f"robots.txt paths have been saved to {output_path}")

# Paths to the directories and file
directory_path = "stats/url_stats"
file_path = os.path.join(directory_path, "test.csv")

# Create output directories if they don't exist
if not os.path.exists("output_download"):
    os.makedirs("output_download")
if not os.path.exists("robots"):
    os.makedirs("robots")

# Start the timer
start_time = time.time()

# Process the specific CSV file
if os.path.exists(file_path):
    output_file_path = os.path.join("output_download", "robots_paths_output-fineweb-edu.csv")

    # Check if the output file already exists
    if os.path.exists(output_file_path):
        print(f"Skipping {file_path}, output file already exists.")
    else:
        process_csv(file_path)
else:
    print(f"File {file_path} does not exist.")

# End the timer
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time:.2f} seconds")