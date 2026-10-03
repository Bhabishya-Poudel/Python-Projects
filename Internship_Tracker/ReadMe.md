Internship Tracker

A small Python script that pulls current internship listings from a public JSON feed (SimplifyJobs/Summer2027-Internships), filters them down to active postings for terms you choose (2026 and later), and exports the results to both CSV and Excel.

What it does: 
i)   Fetches the latest listings from the SimplifyJobs internship feed
ii)  Prompts you to pick which term(s) you want (e.g. Summer 2027, Spring 2026) from a list of current/future terms, then filters for active postings matching your picks
iii) Writes the filtered results to internships.csv and internships.xlsx
iv)  Users can export or use that file anywhere by accessing it from their storage.


Status:
🚧 Work in progress. Current version covers fetch → interactive term filter → export. Planned next steps (Future Development):

- Letting users choose which internship category/field to filter for (software, hardware, economics, etc.), not just the term (done)
- A dropdown/checkbox-style filter UI (web page, or a richer terminal menu) instead of typing comma-separated terms by hand
- A proper interface instead of running everything from the terminal
- Auto-drafting/pre-filling applications for the user to review and submit themselves (Will be difficult I know, but I've kept it open for changes to the public so that anybody can add to it.)

Next step:
Build a interactive interface with it. 
