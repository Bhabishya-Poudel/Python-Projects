import requests
import csv
from openpyxl import Workbook
URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2027-Internships/dev/.github/scripts/listings.json"


def fetch_internships(url):
    data = requests.get(url).json()
    return data

def filter_internships(data):
    filtered = [item for item in data if 'Summer 2026' in item["terms"] and item["active"]]
    return filtered

def write_csv(filtered):
    Headings = ["Company Name", "Job Type", "Title" , "Job ID", "Link"]
    with open("internships.csv", "w", newline="")as line:
        writer = csv.DictWriter(line, fieldnames=Headings)
        writer.writeheader()
        for item in filtered:
          writer.writerow({
            "Company Name" : item["company_name"],
            "Job Type": item["category"],
            "Title" : item["title"],
            "Link" : item["url"],
            "Job ID" : item["id"]
        })
          
def write_excel(filtered, file_name = "internships.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.append(["Company Name", "Job Type", "Job Title" , "Job ID", "Link"])
    for item in filtered:
        ws.append([item["company_name"], item["category"], item["title"], item["id"], item["url"]])
    wb.save(file_name)
          
def main():
    data = fetch_internships(URL)
    filtered = filter_internships(data)
    write_csv(filtered)
    write_excel(filtered)
    print(f"Wrote {len(filtered) + 1} internships to CSV and Excel.")

if __name__ == "__main__":
    main()
    

