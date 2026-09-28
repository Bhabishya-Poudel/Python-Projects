Internship Tracker

A small Python script that pulls current internship listings from a public JSON feed (SimplifyJobs/Summer2027-Internships), filters them down to active Summer 2026 postings, and exports the results to both CSV and Excel.

What it does: 
i)   Fetches the latest listings from the SimplifyJobs internship feed.
ii)  Filters for postings tagged Summer 2027 that are active.
iii) Writes the filtered results to internships.csv and internships.xlsx.
iv)  Users can export or use that file anywhere by accessing it from their storage.


Status:
 Work in progress. Current version covers the basic fetch → filter → export pipeline. Planned next steps include:
 
Letting users choose which internship category to filter for (software, hardware, economics, etc.)
A proper interface instead of running everything from the terminal
Auto-drafting/pre-filling applications for the user to review and submit themselves (Will be difficult I know, but I've kept it open for changes to the public so that anybody can add to it.)
