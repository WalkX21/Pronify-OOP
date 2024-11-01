from lib.auth import AUTH
import streamlit as st
from lib.html_parsing import inspect_html_sections




def main():
    # Step 1: Log in and fetch the HTML (update the file each time)
    auth = AUTH()
    auth.bot_log()
    page_source = auth.login_and_fetch_html()

    # Step 2: Inspect the HTML and create the .ics calendar
    inspect_html_sections(page_source)

    # Step 3: Automatically open the .ics file in Apple Calendar



if __name__ == "__main__":
    main()

