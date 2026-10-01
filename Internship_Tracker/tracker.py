import re
import requests
import csv
from openpyxl import Workbook
URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2027-Internships/dev/.github/scripts/listings.json"
minimum_year = 2026


def fetch_internships(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def get_available_terms(data):
    terms = set()
    for item in data:
        if isinstance(item, dict):
            terms.update(item.get("terms") or [])
    current_or_future = {t for t in terms if (_term_year(t) or 0) >= minimum_year}
    return sorted(current_or_future)

def _term_year(term):
    match = re.search(r"\d{4}", term)
    return int(match.group()) if match else None

def prompt_for_terms(available_terms):
    print("Available terms:")
    for i, term in enumerate(available_terms, 1):
        print(f"  {i}. {term}")
    raw = input("Enter the terms you want (comma-separated numbers or names): ").strip()

    selected = []
    for part in (p.strip() for p in raw.split(",")):
        if not part:
            continue
        if part.isdigit() and 1 <= int(part) <= len(available_terms):
            selected.append(available_terms[int(part) - 1])
            continue
        match = next((t for t in available_terms if t.lower() == part.lower()), None)
        if match:
            selected.append(match)
        else:
            print(f"  (ignoring unrecognized term: {part})")

    if not selected:
        raise ValueError("No valid terms selected.")
    return list(dict.fromkeys(selected))

def filter_internships(data, terms):
    filtered = [
        item for item in data
        if isinstance(item, dict)
        and item.get("active")
        and any(term in (item.get("terms") or []) for term in terms)
    ]
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
    try:
        data = fetch_internships(URL)
    except requests.RequestException as e:
        print(f"Could not fetch internship data: {e}")
        return
    except ValueError as e:
        print(f"Internship source returned invalid data: {e}")
        return

    if not isinstance(data, list):
        print("Unexpected response format from internship source; aborting.")
        return

    available_terms = get_available_terms(data)
    if not available_terms:
        print("No terms found in the fetched data; aborting.")
        return

    while True:
        try:
            selected_terms = prompt_for_terms(available_terms)
            break
        except ValueError as e:
            print(f"{e} Please try again.")
        except (EOFError, KeyboardInterrupt):
            print("\nNo input received; exiting.")
            return

    filtered = filter_internships(data, selected_terms)
    write_csv(filtered)
    write_excel(filtered)
    print(f"Wrote {len(filtered)} internships to CSV and Excel.")

if __name__ == "__main__":
    main()