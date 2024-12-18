import streamlit as st
import pandas as pd
 
# Pages that contain the stats
people_page = st.Page("people.py", title="People")
promotions_page =  st.Page("promotions.py", title="Promotions")
transactions_page = st.Page("transactions.py", title="Transactions")
transfer_page = st.Page("transfers.py", title="Transfer")
statistics_page = st.Page("statistics.py", title="Statistics")


pg = st.navigation([people_page,
                    promotions_page,
                    transactions_page,
                    transfer_page,
                    statistics_page
                    ])

st.set_page_config(page_title="Dashboard")
pg.run()