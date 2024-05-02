
import duckdb
import pandas as pd
from datetime import date

def create_duck_db_products(duckdb_file_path,products_data):
    """
    Crea una base de datos o en su defecto, agrega datos a una base 
    de datos existente llamda products la cual contendra informacion
    de varios articulos.

    Parametros
    -----------
    duckdb_file_path: ruta al archivo duckdb
    products_data: datos recopilados de la extraccion
    """
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
        
def create_duck_db_history(duckdb_file_path,today):
    """
    Crea una base de datos o en su defecto, agrega datos a una base 
    de datos existente llamada history, la cual guardara la informacion
    historica del producto.

    Parametros
    -----------
    duckdb_file_path: ruta al archivo duckdb
    today: fecha del dia de hoy 
    """
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
                row_number() OVER (ORDER BY price) AS row_num
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
    duckdb_file_path = "./scripts/products_base.duckdb"
    create_duck_db_products(duckdb_file_path,amazon_df)
    create_duck_db_history(duckdb_file_path,today)

