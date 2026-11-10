import sqlalchemy
import pandas as pd
import pyodbc
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.types import DateTime, Float, Integer, Boolean


print(pyodbc.drivers())

sjl_modelo_limpio = pd.read_csv("sjl_modelo_limpio.csv")
comparacion=pd.read_csv("comparacion.csv")

conexion = URL.create(
    "mssql+pyodbc",
    query={
        "odbc_connect": (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=LAPTOP-5FPIF11N\\SQLEXPRESS;"
            "DATABASE=Proyecto_Calidad_Aire;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    }
)

engine = create_engine(
    conexion,
    fast_executemany=True
)

with engine.connect() as conn:
    resultado = conn.execute(
        text("SELECT DB_NAME()")
    )
    print("Conectado a:", resultado.scalar())


sjl_modelo_limpio["FECHA_HORA"] = pd.to_datetime(sjl_modelo_limpio["FECHA_HORA"])

comparacion["FECHA_HORA"] = pd.to_datetime(comparacion["FECHA_HORA"])

comparacion["FECHA_OBJETIVO"] = pd.to_datetime(comparacion["FECHA_OBJETIVO"])

sjl_modelo_limpio = sjl_modelo_limpio.rename(
    columns={"NUEVA SECUENCIA": "NUEVA_SECUENCIA"})

sjl_modelo_limpio.to_sql(
    name = "Modelo de datos",
    con = engine,
    if_exists = "replace",
    index = False,
    chunksize = 5000,
)

print("Tabla Modelo_Datos importada")

comparacion.to_sql(
    name = "Prediciones",
    con = engine,
    if_exists = "replace",
    index = False,
    chunksize = 5000,
)

print("Tabla Predicciones importada")
