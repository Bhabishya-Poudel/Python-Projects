import html
import random
import re
from pathlib import Path

import streamlit as st
import pandas as pd
import requests
import tracker

# --- Apply page --------------------------------------------------------------
# The "Apply" link in the table points back at this app (?job=<id>) and opens in
# a new browser tab, which renders that job's page inside this website.
# set_page_config must be the first Streamlit command, so it runs before anything else.
APPLY_JOB_ID = st.query_params.get("job")
st.set_page_config(
    page_title = "Link" if APPLY_JOB_ID else "Internship Finder",
    page_icon = ":material/work:",
    layout = "wide",
)


@st.cache_data(ttl = 3600)
def load_listings():
    return tracker.fetch_internships(tracker.URL)


def get_listings():
    try:
        listings = load_listings()
    except (requests.RequestException, ValueError) as e:
        st.error(f"Could not load internship data: {e}")
        st.stop()

    if not isinstance(listings, list):
        st.error("Unexpected response format from the internship source.")
        st.stop()
    return listings


@st.cache_data(ttl = 3600, show_spinner = False)
def can_embed(url):
    """True/False if the site allows/forbids being shown inside another page
    (X-Frame-Options / CSP frame-ancestors); None if the server did not tell us."""
    try:
        with requests.get(url, timeout = 8, stream = True,
                          headers = {"User-Agent": "Mozilla/5.0"}) as response:
            headers = response.headers
            status = response.status_code
    except requests.RequestException:
        return None

    if headers.get("X-Frame-Options"):
        return False
    ancestors = re.search(r"frame-ancestors([^;]*)", headers.get("Content-Security-Policy", ""))
    if ancestors and "*" not in ancestors.group(1):
        return False
    # An error page (e.g. a bot-blocking 403) says nothing about the real page's headers.
    return True if status < 400 else None


if APPLY_JOB_ID:
    job = next(
        (item for item in get_listings()
         if isinstance(item, dict) and item.get("id") == APPLY_JOB_ID),
        None,
    )
    if job is None:
        st.error("That internship could not be found. It may have been removed.")
        st.stop()

    url = job.get("url") or ""
    if not url.startswith(("http://", "https://")):
        st.error("This internship has no valid application link.")
        st.stop()

    st.subheader(f"{job['company_name']} - {job['title']}")
    st.link_button("Open original site", url)

    embeddable = can_embed(url)
    if embeddable is False:
        st.warning(
            f"{job['company_name']} does not allow its application page to be shown "
            "inside another website. Use the \"Open original site\" button above."
        )
    else:
        st.iframe(url, height = 900)
        if embeddable is None:
            st.caption(
                "If the page above is blank, this company blocks being shown inside "
                "another website. Use the \"Open original site\" button."
            )
    st.stop()

# --- Main page ---------------------------------------------------------------
PAGE_CSS = """
<style>
.block-container { max-width: 1180px; }
.intro { max-width: 760px; margin: 2.2rem 0 1.4rem; animation: rise .8s ease both; }
.intro .kicker { color: #5eead4; letter-spacing: .18em; text-transform: uppercase;
                 font-size: .8rem; margin: 0 0 .6rem; }
.intro h2 { font-size: clamp(1.9rem, 4vw, 2.8rem); line-height: 1.1; margin: 0 0 1rem; font-weight: 700; }
.intro p { color: #aab2c5; font-size: 1.08rem; line-height: 1.65; margin: 0; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
         gap: 16px; margin: 2rem 0 3rem; }
.card { border: 1px solid #232a3a; background: #10141d; border-radius: 16px; padding: 22px;
        transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
        animation: rise .8s ease both; }
.card:nth-child(2) { animation-delay: .1s; }
.card:nth-child(3) { animation-delay: .2s; }
.card:hover { transform: translateY(-6px); border-color: #5eead4;
              box-shadow: 0 12px 32px rgba(94, 234, 212, .12); }
.card .num { color: #5eead4; font-weight: 700; font-size: .85rem; letter-spacing: .12em; }
.card h3 { margin: .5rem 0 .5rem; font-size: 1.15rem; }
.card p { margin: 0; color: #aab2c5; line-height: 1.55; font-size: .96rem; }
.hype { display: inline-block; margin: 0 0 .9rem; padding: .5rem 1rem; border-radius: 999px;
         background: rgba(94, 234, 212, .12); border: 1px solid rgba(94, 234, 212, .45);
         color: #5eead4; font-weight: 600; animation: pop .5s cubic-bezier(.2, 1.6, .4, 1) both; }
@keyframes pop { from { opacity: 0; transform: scale(.7) translateY(8px); } to { opacity: 1; transform: none; } }
@keyframes rise { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
@media (prefers-reduced-motion: reduce) { .intro, .card, .hype { animation: none; transition: none; } }
</style>
"""

INTRO_HTML = """
<section class="intro">
  <p class="kicker">Welcome</p>
  <h2>Find the internship that fits your season.</h2>
  <p>An internship is a short, structured stint at a company, a chance to work on real
  projects, learn how a team operates and find out whether a field is right for you.
  Browse live listings below, filtered by the year and season you are available.</p>
</section>
<div class="cards">
  <div class="card">
    <span class="num">01</span>
    <h3>What is an internship?</h3>
    <p>Typically a few months of hands-on work alongside a team, often paid, and a common
    first step into a full-time role.</p>
  </div>
  <div class="card">
    <span class="num">02</span>
    <h3>When should I apply?</h3>
    <p>Summer is the most common season, and many roles open months ahead, so apply early.
    Fall, Winter and Spring internships exist as well.</p>
  </div>
  <div class="card">
    <span class="num">03</span>
    <h3>How does this site work?</h3>
    <p>Pick a year and a season, browse the list, select a row and hit Apply, right here
    or on the company's own site.</p>
  </div>
</div>
"""

st.html(PAGE_CSS)
st.iframe(Path(__file__).parent / "hero.html", height = 400)
st.html(INTRO_HTML)

SEASON_ORDER = ["Spring", "Summer", "Fall", "Winter"]

listings = get_listings()

# {year: {season: original term string}}, e.g. {2027: {"Summer": "Summer 2027"}}
terms_by_year = {}
for term in tracker.get_available_terms(listings):
    year = tracker._term_year(term)
    season = term.replace(str(year), "").strip()
    terms_by_year.setdefault(year, {})[season] = term

if not terms_by_year:
    st.error("No internship terms were found in the data.")
    st.stop()

st.subheader("Find internships", anchor = "find-internships")

year = st.segmented_control("Year", sorted(terms_by_year), key = "year")

if year is None:
    st.info("Pick a year to continue.")
    st.stop()

seasons = sorted(
    terms_by_year[year],
    key = lambda s: SEASON_ORDER.index(s) if s in SEASON_ORDER else len(SEASON_ORDER),
)
season = st.pills("Season", seasons, key = f"season_{year}")

if season is None:
    st.info("Pick a season to see internships.")
    st.stop()

filtered = tracker.filter_internships(listings, [terms_by_year[year][season]])

# The Apply cell's real value is "?job=<id>", not the company's URL. The dataframe
# search matches the underlying value, so a URL like tesla.com/... would count as
# an extra "Tesla" match; this value never contains the company name.
df = pd.DataFrame(
    {
        "Company Name": [item["company_name"] for item in filtered],
        "Job Type": [item["category"] for item in filtered],
        "Title": [item["title"] for item in filtered],
        "Link": [f"?job={item['id']}" for item in filtered],
    }
)

# Hide the built-in column "Statistics" entry (Values / Empty / Distinct / ...).
# Streamlit has no option for this; it is the only column-menu item with
# aria-haspopup="true" (the "Format" item uses "menu").
st.markdown(
    """
    <style>
    [data-testid="stDataFrameColumnMenu"] [role="menuitem"][aria-haspopup="true"],
    [data-testid="stDataFrameStatisticsMenu"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html = True,
)

st.caption(f"{len(df)} internships for {season} {year}")

event = st.dataframe(
    df,
    column_config = {
        "Link": st.column_config.LinkColumn(
            "Link",
            display_text = "Apply",
        ),
    },
    hide_index = True,
    on_select = "rerun",
    selection_mode = "single-row",
    key = f"internships_{year}_{season}",
)

HYPE_LINES = [
    "Woah! All the best! \U0001F64C",
    "Woohoo! \U0001F389",
    "You go, champ! \U0001F3C6",
    "Have that resume ready \U0001F4C4",
    "Go get 'em! \U0001F680",
    "Manifesting that offer \u2728",
    "Update LinkedIn first. Trust me. \U0001F60E",
    "Bold pick. I respect it \U0001FAE1",
    "Future intern energy \U0001F525",
    "Coffee, resume, confidence. You're set \u2615",
]
COMPANY_LINES = [
    "{company}, you sure? \U0001FAE9",
    "{company}? Aim high, champ \U0001F3AF",
    "{company} won't know what hit them \U0001F4A5",
    "Ooh, {company}. Spicy choice \U0001F336\uFE0F",
    "{company} is about to get a great applicant \U0001F4EC",
]


def random_hype(company):
    pool = HYPE_LINES + [line.format(company = company) for line in COMPANY_LINES]
    return random.choice(pool)


# Apply panel for the selected row. Selected positions refer to the original
# (unsorted) df, so they index `filtered`.
selected_rows = event.selection.rows
if selected_rows:
    job = filtered[selected_rows[0]]

    # A new random message each time a different row is picked, but not on every rerun.
    picked = (year, season, job["id"])
    if st.session_state.get("hype_for") != picked:
        st.session_state["hype_for"] = picked
        st.session_state["hype_msg"] = random_hype(job["company_name"])
        st.toast(st.session_state["hype_msg"])
        if st.session_state["hype_msg"].startswith("Woohoo"):
            st.balloons()

    with st.container(border = True):
        st.html(f'<div class="hype">{html.escape(st.session_state["hype_msg"])}</div>')
        st.caption(f"{job['category']}  |  {season} {year}")
        st.subheader(job["company_name"])
        st.write(job["title"])

        apply_col, original_col = st.columns(2)
        # "?job=<id>" opens this website's Apply page in a new tab (see the top of this file).
        apply_col.link_button(
            "Apply",
            f"?job={job['id']}",
            type = "primary",
            icon = ":material/open_in_new:",
            width = "stretch",
        )
        original_col.link_button(
            "Open original site",
            job["url"],
            icon = ":material/link:",
            width = "stretch",
        )
else:
    st.caption("Select a row to apply.")

st.caption("Listings come from the community-maintained SimplifyJobs internship list and refresh hourly.")
