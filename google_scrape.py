import csv
from googlesearch import search

# File to read horse names from
input_file = "google_Horse_result.csv"
# File to save the results
output_file = "google_Horse_results.csv"

# Read horse names from the input CSV file
try:
    with open(input_file, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        headers = next(reader, None)  # Get header, if exists
        if headers is None:
            print(f"❌ The file '{input_file}' is empty or missing headers!")
            exit()

        horse_names = [row[0] for row in reader if row]  # Get all horse names, excluding empty rows

        if not horse_names:
            print(f"❌ No horse names found in the file '{input_file}'!")
            exit()
except FileNotFoundError:
    print(f"❌ The file '{input_file}' was not found!")
    exit()

# Prepare the output file and write headers
try:
    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Horse Name", "Search Result URL"])  # Add header row
        
        # Iterate over each horse name
        for horse_name in horse_names:
            query = f"{horse_name} horse results site:https://www.racingpost.com/"  # Search query
            
            try:
                # Perform the Google search and get the results as a list
                search_results = list(search(query, num_results=1))
                if search_results:
                    result_url = search_results[0]  # Get the first link
                    print(f"✅ Found: {horse_name} -> {result_url}")
                    writer.writerow([horse_name, result_url])  # Write the result to the CSV
                else:
                    print(f"⚠️ No result found for: {horse_name}")
                    writer.writerow([horse_name, "No result found"])
            
            except Exception as e:
                print(f"❌ Error searching for {horse_name}: {e}")
                writer.writerow([horse_name, "Error"])
            
except Exception as e:
    print(f"❌ An error occurred while writing the results: {e}")
    exit()

print(f"✅ All results have been saved to '{output_file}'")
