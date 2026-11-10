
import pandas as pd

# 1. Cargar el archivo original
df = pd.read_csv("senahmi.csv", low_memory=False)



for estacion in df["ESTACION"].unique():

    datos = df[df["ESTACION"] == estacion].copy()

    datos["FECHA_DT"] = pd.to_datetime(
        datos["FECHA"].astype(str),
        format="%Y%m%d"
    )

    datos = datos.sort_values("ID")

    print(f"\nESTACIÓN: {estacion}")
    print(datos[["ID", "FECHA", "HORA"]].head(5))
    print(datos[["ID", "FECHA", "HORA"]].tail(5))