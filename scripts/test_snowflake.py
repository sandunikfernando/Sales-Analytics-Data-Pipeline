import snowflake.connector

conn = snowflake.connector.connect(
    user="sandunifernando",
    password="REMOVED",
    account="REMOVED",
    warehouse="SALES_WH",
    database="SALES_ANALYTICS",
    schema="RAW"
)

cur = conn.cursor()

cur.execute("SELECT CURRENT_VERSION()")

print(cur.fetchone())

cur.close()
conn.close()