#%%
import duckdb
import pandas as pd
from datetime import date
#%%
def create_duck_db_products(duckdb_file_path,products_data):
    try:
        conn = duckdb.connect(duckdb_file_path, read_only=False)
        tables = conn.execute("SHOW TABLES;").fetchall()
        if ("products",) not in tables:
            conn.execute(
            """
            CREATE TABLE products (
                title VARCHAR,
                price VARCHAR,
                rating VARCHAR,
                review_number VARCHAR,
                url VARCHAR,
                fecha DATE
            );
            """
            )
            
        conn.execute("INSERT INTO products SELECT * FROM products_data;")  
        conn.close()
        print("Datos Cargados")
    except Exception as e:
        print(e)
        

# SELECT CAST('5999.00' as float)
# SELECT * FROM products WHERE title LIKE '%A54%'

# with duckdb.connect(database="products.db") as write_conn:
#     write_conn.execute("SHOW TABLES;").fetchall()
    
    
# amazon_df["price"]=amazon_df["price"].str.replace('$','').str.replace(',', '')




# """
# INSERT INTO history
# WITH base_table AS (
# SELECT 
#     UPPER(title) AS title,
#     TRY_CAST(price AS FLOAT) AS price,
#     TRY_CAST(left(rating,3) AS FLOAT) AS rating,
#     fecha
# FROM amazon_df 
# WHERE fecha = '2024-04-22'
# AND title LIKE '%A54%'
# ), 
# calculation AS (
#     SELECT 
#     title,
#     price,
#     AVG(rating) OVER (PARTITION BY "fecha") AS avg_rating,
#     fecha,
#     row_number() OVER (ORDER BY price) AS row_num
# FROM base_table
# )
# SELECT 
#     title,
#     price,
#     round(avg_rating,2) AS avg_rating,
#     fecha,
# FROM calculation
# WHERE row_num=1
# """

# WINDOW raiting_partition AS (
#     PARTITION BY "fecha"
#     ORDER BY "price"
# )


# GROUP BY title,fecha
# row_number() OVER (ORDER BY price) 

def create_duck_db_history(duckdb_file_path,today):
    try:
        conn = duckdb.connect(duckdb_file_path, read_only=False)
        tables = conn.execute("SHOW TABLES;").fetchall()
        if ("history",) not in tables:
            conn.execute(
            """
            CREATE TABLE history (
                title VARCHAR,
                price FLOAT,
                avg_rating FLOAT,
                fecha DATE
            );
            """
            )

        conn.execute(f"DELETE FROM history WHERE fecha = '{today}'")
        
        conn.execute(f"""
            INSERT INTO history
            WITH base_table AS (
            SELECT 
                UPPER(title) AS title,
                TRY_CAST(price AS FLOAT) AS price,
                TRY_CAST(left(rating,3) AS FLOAT) AS rating,
                fecha
            FROM products 
            WHERE fecha = '{today}'
            AND title LIKE '%A54%'
            ), 
            calculation AS (
                SELECT 
                title,
                price,
                AVG(rating) OVER (PARTITION BY "fecha") AS avg_rating,
                fecha,
                row_number() OVER +9o'´'0'(ORDER BY price) AS row_num
            FROM base_table
            )
            SELECT 
                title,
                price,
                round(avg_rating,2) AS avg_rating,
                fecha,
            FROM calculation
            WHERE row_num=1;
            """
            )  
        conn.close()
        print("Datos Cargados al historico")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    today = date.today()
    amazon_df=pd.read_csv("amazon_data.csv")
    duckdb_file_path = "products_base.duckdb"
    create_duck_db_products(duckdb_file_path,amazon_df)
    create_duck_db_history(duckdb_file_path,today)