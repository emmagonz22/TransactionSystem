import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

# API URLs
TRANSACTION_API_URL = "http://127.0.0.1:5000/transaction"
PEOPLE_API_URL = "http://127.0.0.1:5000/people"
PROMOTION_API_URL = "http://127.0.0.1:5000/promotion"
TRANSFER_API_URL = "http://127.0.0.1:5000/transfers"

st.title("Stadistics")

# Operation selector
operation = st.sidebar.selectbox("Choose an stadistic to display", ["Top 5 sold items",
                                                                    "Top 5 stores with most sales (quantity)",
                                                                    "Top 5 stores with most profits",
                                                                    "Transfer amount ($) over time",
                                                                    "Quantity of transfers over time by year",
                                                                    "Top 5 senders"])

plt.style.use('dark_background')

if operation == "Top 5 sold items":
    st.header("Top 5 Sold Items")

    # Fetch the data for the top 5 sold items
    response = requests.get(f"{TRANSACTION_API_URL}/top-sold-items")
    if response.status_code == 200:
        top_items = response.json()

        item_names = [item["item_name"] for item in top_items]
        quantities = [item["total_quantity"] for item in top_items]

        fig, ax = plt.subplots(figsize=(10, 6)) 
        ax.bar(item_names, quantities, color='green')
        ax.set_xlabel("Item Name")
        ax.set_ylabel("Total Quantity Sold")
        ax.set_title("Top 5 Sold Items")

        st.pyplot(fig)      # show graph

    else:
        st.error("Failed to fetch top sold items from the API.")
        
elif operation == "Top 5 stores with most sales (quantity)":
    st.header("Top 5 Stores with the Most Sales")

    # Fetch data 
    response = requests.get(f"{TRANSACTION_API_URL}/top-five-stores-by-amount")
    if response.status_code == 200:
        top_stores = response.json()

        store_names = [store["store"] for store in top_stores]
        total_sales = [store["total_sales"] for store in top_stores]

        # plot 
        fig, ax = plt.subplots(figsize=(10, 6)) 
        ax.bar(store_names, total_sales,color='green')
        ax.set_xlabel("Store")
        ax.set_ylabel("Total Sales")
        ax.set_title("Top 5 Stores with Most Sales")
        print(store_names, total_sales)
       
        plt.tight_layout()  # fit layout
      
        st.pyplot(fig) # show graph
    else:
        st.error("Failed to fetch top stores data.")
        
elif operation == "Top 5 stores with most profits":
    st.header("Top 5 Stores with the Most Profits")

    # Fetch data 
    response = requests.get(f"{TRANSACTION_API_URL}/top-five-stores-by-profit")
    if response.status_code == 200:
        
        top_stores = response.json()

        store_names = [store["store"] for store in top_stores]
        total_profit = [float(store["total_profit"]) for store in top_stores]
        print(store_names, total_profit)
        # plot 
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(store_names, total_profit, color="green")
        ax.set_xlabel("Store")
        ax.set_ylabel("Total Profit")
        ax.set_title("Top 5 Stores by Total Profit")

        ax.set_ylim(0, max(total_profit) * 1.1)
        
        st.pyplot(fig) # show graph
    else:
        st.error("Failed to fetch top stores data.")

elif operation == "Transfer amount ($) over time":
    st.title("Transfer Amount ($) Over Time")

    # Get data
    response = requests.get(f"{TRANSFER_API_URL}/amount-over-time")
    if response.status_code == 200:
        data = response.json()
        
        # Format data in pandas df
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year

        # Ensure "total_amount" is numeric and handle any non-numeric data
        df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)

        # Resample to monthly frequency and calculate the sum for each month
        monthly_df = df.resample("M", on="date").sum().reset_index()

        # Plotting
        fig, ax = plt.subplots(figsize=(12, 6))

        # Calculate cumulative transferred amount for each year
        for year, yearly_data in monthly_df.groupby(monthly_df["date"].dt.year):
            yearly_data = yearly_data.sort_values("date")
            yearly_data["cumulative_amount"] = yearly_data["total_amount"].cumsum()
            ax.plot(yearly_data["date"], yearly_data["cumulative_amount"], label=f"Year {year}", marker="o")


        # Total over all the years
        monthly_df["total_cumulative_amount"] = monthly_df["total_amount"].cumsum()
        ax.plot(
            monthly_df["date"], 
            monthly_df["total_cumulative_amount"], 
            label="Total Cumulative Amount", 
            color="red", 
            linestyle="--", 
            linewidth=2
        )
        # Formatting
        ax.set_xlabel("Date")
        ax.set_ylabel("Cumulative Transfer Amount ($)")
        ax.set_title("Cumulative Transfer Amount Over Time by Year")
        ax.legend(title="Year")

        # Display plot in Streamlit
        st.pyplot(fig)

        
    else:
        st.error("Failed to fetch transfer amount data.")
        
elif operation == "Quantity of transfers over time by year":
    st.title("Quantity of Transfers Over Time by Year")

    response = requests.get(f"{TRANSFER_API_URL}/quantity-over-time")
    if response.status_code == 200:
        data = response.json()
        
        # Put data in a pandas df
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
       
   
        # Resample data to monthly frequency
        df.set_index("date", inplace=True)
        monthly_counts = df.resample("M").sum().reset_index()
        #print(monthly_counts.groupby(monthly_counts["date"].dt.year).head())
        #print(df)
        # create plot 
        fig, ax = plt.subplots(figsize=(12, 6))

        # group the data by year
        for year, yearly_data in monthly_counts.groupby(monthly_counts["date"].dt.year):
            yearly_data = yearly_data.sort_values("date")
            # Interpolation to make the lines more smooth
            smoothed_counts = yearly_data["transfer_count"].rolling(window=3, center=True).mean()
         
            ax.plot(yearly_data["date"], smoothed_counts, label=str(year), marker='o', linestyle='-')

        # Line with the total amount of transfers
        total_smoothed_counts = monthly_counts["transfer_count"].rolling(window=5, center=True).mean()
        ax.plot(monthly_counts["date"], total_smoothed_counts, color="red", linewidth=2, linestyle='--', label="Total")

        ax.set_xlabel("Date")
        ax.set_ylabel("Transfer Quantity")
        ax.set_title("Quantity of Transfers Over Time by Year (Monthly Aggregation)")
        ax.legend(title="Year")

        st.pyplot(fig)
    else:
        st.error("Failed to fetch transfer quantity data.")
elif operation == "Top 5 senders":
    st.title("Top 5 senders")
    response = requests.get(f"{TRANSFER_API_URL}/top-senders")
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        st.dataframe(df, width=700)
    else:
        print("Failed to retrieve data")
