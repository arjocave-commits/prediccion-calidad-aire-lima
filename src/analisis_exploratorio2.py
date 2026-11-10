# Seleccionar únicamente las columnas que necesitamos
sjl_modelo = sjl_unico[["FECHA_HORA", "PM2_5"]].copy()

# Ordenar los registros por fecha
sjl_modelo = sjl_modelo.sort_values("FECHA_HORA").reset_index(drop=True)

# Mostrar información general
print("Total de registros:", len(sjl_modelo))
print("Primera fecha:", sjl_modelo["FECHA_HORA"].min())
print("Última fecha:", sjl_modelo["FECHA_HORA"].max())

# Mostrar los primeros registros
print(sjl_modelo.head())