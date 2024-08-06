import psycopg2
import streamlit as st
import pandas as pd

# Database connection setup
def get_connection():
    conn = psycopg2.connect(database="k9_db",
                            host="localhost",
                            user="airflow",
                            password="airflow",
                            port="5432")
    return conn

# Fetch facts from the database based on category
def fetch_facts(category=None):
    conn = get_connection()
    cursor = conn.cursor()
    if category and category != "All":
        query = "SELECT fact, category FROM facts WHERE category = %s"
        cursor.execute(query, (category,))
    else:
        query = "SELECT fact, category FROM facts"
        cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# Streamlit app
def main():
    st.title("K9 Facts Viewer")

    # Select category type
    category_type = st.selectbox("Select Category Type", ["All", "with_numbers", "without_numbers"])

    # Fetch facts based on selected category type
    data_tuples = fetch_facts(category_type)
    df = pd.DataFrame(data_tuples, columns=['fact', 'category'])

    # Display facts under each category
    if not df.empty:
        if category_type == "All":
            categories = df['category'].unique()
            for category in categories:
                st.header(f"Category: {category}")
                category_facts = df[df['category'] == category]['fact'].tolist()
                for fact in category_facts:
                    st.write(f"- {fact}")
        else:
            st.header(f"Category: {category_type}")
            category_facts = df['fact'].tolist()
            for fact in category_facts:
                st.write(f"- {fact}")
    else:
        st.write("No facts found for the selected category.")

if __name__ == "__main__":
    main()
