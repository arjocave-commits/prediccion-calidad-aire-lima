import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy
import pyodbc


from sklearn import linear_model
from sklearn.metrics import mean_absolute_error,mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor



import numpy as np

df = pd.read_csv("senahmi.csv")

df["FECHA_DT"] = pd.to_datetime(df["FECHA"].astype(str),format="%Y%m%d")

df["anio"]=df["FECHA_DT"].dt.year
df["mes"]=df["FECHA_DT"].dt.month

df["HORA_NUM"]=pd.to_numeric(df["HORA"],errors="coerce")

df["HORA_DIA"]=df["HORA_NUM"]//10000


print(df.head())
print(df.info())


contaminacion= df.groupby("ESTACION")["PM2_5"].agg(["count","mean","median","max"])

contaminacion=contaminacion.sort_values(by="mean",ascending=False)

print(contaminacion)

contaminacion["mean"].plot(kind="bar", figsize= (10,5))


plt.title("Promedio de PM2_5 por estacion")
plt.xlabel("Estacion")
plt.ylabel("PM2_5")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


contaminacion_anual = df.groupby("anio")["PM2_5"].agg(["count","mean","median","max"])

print("Contaminación por años")
print(contaminacion_anual)

plt.figure(figsize=(10,5))

plt.plot(contaminacion_anual.index,contaminacion_anual["mean"],marker="o")

plt.title("Evolución anual del PM2.5 (2015-2024)")
plt.xlabel("Año")
plt.ylabel("Concentración promedio de PM2.5 (µg/m³)")
plt.xticks(contaminacion_anual.index)
plt.grid(True)

plt.tight_layout()
plt.show()


contaminacion_mensual = df.groupby("mes")["PM2_5"].agg(["count","mean","median"])

contaminacion_mensual = contaminacion_mensual.sort_index()

print("\nCONTAMINACIÓN POR MES:")
print(contaminacion_mensual)

plt.figure(figsize=(10,5))

plt.bar(contaminacion_mensual.index,contaminacion_mensual["mean"],color="blue")

plt.title("Promedio de PM2.5 por mes (2015-2024)")
plt.xlabel("Mes")
plt.ylabel("PM2.5 (µg/m³)")
plt.xticks(
    range(1, 13),
    ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
     "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
)

plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()


contaminacion_horaria = df.groupby("HORA_DIA")["PM2_5"].agg(["count","mean","median",])

print("\nCONTAMINACIÓN POR HORA:")
print(contaminacion_horaria)

plt.figure(figsize=(10,5))

plt.plot(contaminacion_horaria.index,contaminacion_horaria["mean"],marker="o")

plt.title("Promedio de PM2.5 por hora del día")
plt.xlabel("Hora")
plt.ylabel("PM2.5 (µg/m³)")
plt.xticks(range(24))
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

contaminacion_estacion_anual = df.groupby(["ESTACION","anio"])["PM2_5"].agg(["count","mean","median"])

print("\nCONTAMINACIÓN POR ESTACIÓN Y AÑO:")
print(contaminacion_estacion_anual)


# Crear tabla para el gráfico
tabla_grafico = df.pivot_table(
    index="anio",
    columns="ESTACION",
    values="PM2_5",
    aggfunc="mean"
)

# Graficar
tabla_grafico.plot(
    kind="line",
    marker="o",
    figsize=(12, 6)
)

plt.title("Evolución anual del PM2.5 por estación")
plt.xlabel("Año")
plt.ylabel("PM2.5 (µg/m³)")
plt.grid(True, alpha=0.3)
plt.legend(title="Estación")
plt.tight_layout()
plt.show()


# Cantidad de mediciones válidas por estación y año
cobertura = df.groupby(
    ["ESTACION", "anio"]
)["PM2_5"].count().reset_index()

# Horas esperadas por año
horas_esperadas = {
    anio: (8784 if pd.Timestamp(f"{anio}-12-31").is_leap_year else 8760)
    for anio in range(2015, 2024)
}

# 2024 solo tiene datos de enero a mayo
horas_esperadas[2024] = 152 * 24

# Calcular porcentaje de cobertura
cobertura["HORAS_ESPERADAS"] = cobertura["anio"].map(horas_esperadas)

cobertura["COBERTURA_%"] = (
    cobertura["PM2_5"] / cobertura["HORAS_ESPERADAS"]
) * 100

# Ordenar resultados
cobertura = cobertura.sort_values(
    ["ESTACION", "anio"]
)

print("\nCOBERTURA POR ESTACIÓN Y AÑO:")
print(cobertura.to_string(index=False))


sjl = df[(df["ESTACION"] == "SAN_JUAN_DE_LURIGANCHO") & (df["PM2_5"].notna())].copy()

sjl["FECHA_HORA"]=(sjl["FECHA_DT"] + pd.to_timedelta(sjl["HORA_DIA"],unit = "h"))

sjl = sjl.sort_values("FECHA_HORA")

sjl_unico=sjl.drop_duplicates(subset="FECHA_HORA")


horas_completas = pd.date_range(start=sjl_unico["FECHA_DT"].min(),end=sjl_unico["FECHA_DT"].max(),freq="h")

horas_registradas = sjl_unico["FECHA_HORA"].nunique()

horas_esperadas = len(horas_completas)

horas_faltantes = horas_esperadas - horas_registradas


continuidad = (horas_registradas / horas_esperadas) * 100


print("\nCONTINUIDAD TEMPORAL - SAN JUAN DE LURIGANCHO")
print("Registros válidos:", len(sjl))
print("Horas únicas registradas:", horas_registradas)
print("Horas esperadas:", horas_esperadas)
print("Horas faltantes:", horas_faltantes)
print("Continuidad temporal:", round(continuidad, 2), "%")


sjl_unico["DIF_HORAS"]= (sjl_unico["FECHA_HORA"].diff().dt.total_seconds())

huecos = sjl_unico[sjl_unico["DIF_HORAS"]>1]

print("\nANÁLISIS DE HUECOS TEMPORALES")

print("Cantidad de huecos:", len(huecos))

print("Mayor intervalo sin mediciones:",
      huecos["DIF_HORAS"].max(), "horas")

print("\nHUECOS MÁS GRANDES:")
print(
    huecos[["FECHA_HORA", "DIF_HORAS"]]
    .sort_values("DIF_HORAS", ascending=False)
    .head(10)
)

print("FECHA MÁS ANTIGUA:")
print(sjl_unico["FECHA_HORA"].min())

print("\nFECHA MÁS RECIENTE:")
print(sjl_unico["FECHA_HORA"].max())

# Mostrar las primeras y últimas fechas
print("\nPRIMEROS REGISTROS:")
print(sjl_unico["FECHA_HORA"].head(5))

print("\nÚLTIMOS REGISTROS:")
print(sjl_unico["FECHA_HORA"].tail(5))

# Calcular nuevamente las diferencias
sjl_unico["DIF_HORAS"] = (
    sjl_unico["FECHA_HORA"].diff().dt.total_seconds() / 3600
)

print("\nMAYOR DIFERENCIA:")
print(sjl_unico["DIF_HORAS"].max())



# Ordenar cronológicamente y reiniciar los índices
sjl_unico = sjl_unico.sort_values("FECHA_HORA").reset_index(drop=True)

# Calcular la diferencia entre cada registro y el anterior
sjl_unico["DIF_HORAS"] = (
    sjl_unico["FECHA_HORA"].diff().dt.total_seconds() / 3600
)

# Mostrar los intervalos más grandes
print(sjl_unico.nlargest(10, "DIF_HORAS")[
    ["FECHA_HORA", "DIF_HORAS"]
])

print("HUECOS POR DURACIÓN")

print("Más de 24 horas:", (sjl_unico["DIF_HORAS"] > 24).sum())
print("Más de 7 días:", (sjl_unico["DIF_HORAS"] > 168).sum())
print("Más de 30 días:", (sjl_unico["DIF_HORAS"] > 720).sum())
print("Más de 90 días:", (sjl_unico["DIF_HORAS"] > 2160).sum())


sjl_modelo = sjl_unico[["FECHA_HORA", "PM2_5"]].copy()

sjl_modelo = sjl_modelo.sort_values("FECHA_HORA").reset_index(drop=True)

print("Total de registros:", len(sjl_modelo))
print("Primera fecha:",sjl_modelo["FECHA_HORA"].min())
print("Ultima fecha:" , sjl_modelo["FECHA_HORA"].max())

print(sjl_modelo.head())

sjl_modelo["PM25_LAG_1"] = sjl_modelo["PM2_5"].shift(1)
sjl_modelo["PM25_LAG2"] = sjl_modelo["PM2_5"].shift(2)
sjl_modelo["PM25_LAG3"] = sjl_modelo["PM2_5"].shift(3)
sjl_modelo["PM25_LAG_24"] = sjl_modelo["PM2_5"].shift(24)

print(sjl_modelo.head(30))

sjl_modelo["PM25_MEDIA_3H"]= (sjl_modelo["PM2_5"].shift(1).rolling(window=3).mean())

sjl_modelo["PM25_MEDIA_24H"] = (sjl_modelo["PM2_5"].shift(1).rolling(window=24).mean())

print (sjl_modelo.head(30))


sjl_modelo["HORA"] = sjl_modelo["FECHA_HORA"].dt.hour

sjl_modelo["DIA_SEMANA"] = sjl_modelo["FECHA_HORA"].dt.day_of_week

sjl_modelo["MES"] = sjl_modelo["FECHA_HORA"].dt.month

sjl_modelo["ANIO"] = sjl_modelo["FECHA_HORA"].dt.year

print(sjl_modelo[[
    "FECHA_HORA",
    "HORA",
    "DIA_SEMANA",
    "MES",
    "ANIO"
]].head(15))

sjl_modelo["DIF_HORAS"]= (sjl_modelo["FECHA_HORA"].diff().dt.total_seconds()/3600)

sjl_modelo["NUEVA SECUENCIA"] = (sjl_modelo["DIF_HORAS"] != 1)| (sjl_modelo["DIF_HORAS"].isna())

sjl_modelo["SECUENCIA"] = sjl_modelo["NUEVA SECUENCIA"].cumsum()

print("Cantidad de secuencias:", sjl_modelo["SECUENCIA"].nunique())

print(sjl_modelo[["FECHA_HORA","PM2_5","DIF_HORAS","SECUENCIA"]].head(10))


grupo = sjl_modelo.groupby("SECUENCIA")["PM2_5"]

sjl_modelo["PM25_LAG_1"] = grupo.shift(1)
sjl_modelo["PM25_LAG_2"] = grupo.shift(2)
sjl_modelo["PM25_LAG_3"] = grupo.shift(3)
sjl_modelo["PM25_LAG_24"] = grupo.shift(24)

sjl_modelo["PM25_MEDIA_3H"] = grupo.transform(
    lambda x: x.shift(1).rolling(window=3).mean()
)

sjl_modelo["PM25_MEDIA_24H"] = grupo.transform(
    lambda x: x.shift(1).rolling(window=24).mean()
)

print(sjl_modelo.head(30))

variables = [
    "PM25_LAG_1",
    "PM25_LAG_2",
    "PM25_LAG_3",
    "PM25_LAG_24",
    "PM25_MEDIA_3H",
    "PM25_MEDIA_24H",
    "HORA",
    "DIA_SEMANA",
    "MES",
    "ANIO"
]


print("Valores faltantes:")
print(sjl_modelo[variables].isna().sum())

sjl_modelo_limpio= sjl_modelo.dropna(subset=variables + ["PM2_5"]).copy()

print("\nREGISTROS ORIGINALES:", len(sjl_modelo))
print("REGISTROS UTILIZABLES:", len(sjl_modelo_limpio))
print("REGISTROS ELIMINADOS:", len(sjl_modelo) - len(sjl_modelo_limpio))

sjl_modelo_limpio["PM25_OBJETIVO"] = (sjl_modelo_limpio.groupby("SECUENCIA")["PM2_5"].shift(-1))

sjl_modelo_limpio = sjl_modelo_limpio.dropna(subset=["PM25_OBJETIVO"]).copy()

print(sjl_modelo_limpio[[
    "FECHA_HORA",
    "PM2_5",
    "PM25_LAG_1",
    "PM25_MEDIA_3H",
    "PM25_OBJETIVO"
]].head(10))


sjl_modelo_limpio=sjl_modelo_limpio.sort_values("FECHA_HORA").reset_index(drop=True)

punto_corte = int(len(sjl_modelo_limpio)*0.80)

print("Total de registros: ",len(sjl_modelo_limpio))

print("Punto de corte:" , punto_corte)

print("Ultima fecha de entrenamiento" , sjl_modelo_limpio.loc[punto_corte - 1 ,"FECHA_HORA"])

print(sjl_modelo_limpio.loc[
    punto_corte - 2:punto_corte + 2,
    ["FECHA_HORA", "PM2_5", "PM25_OBJETIVO"]
])

entrenamiento = sjl_modelo_limpio.iloc[:punto_corte].copy()

prueba = sjl_modelo_limpio.iloc[punto_corte:].copy()

print("Registros de entrenamiento:" , len(entrenamiento))

print("Registros de prueba:" , len(prueba))

variables = [
    "PM2_5",
    "PM25_LAG_1",
    "PM25_LAG_2",
    "PM25_LAG_3",
    "PM25_LAG_24",
    "PM25_MEDIA_3H",
    "PM25_MEDIA_24H",
    "HORA",
    "DIA_SEMANA",
    "MES",
    "ANIO"
]

x_train = entrenamiento[variables]
x_test = prueba[variables]

y_train = entrenamiento["PM25_OBJETIVO"]
y_test = prueba["PM25_OBJETIVO"]

print("X_train:", x_train.shape)
print("X_test:", x_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)

print("\nValores faltantes:")
print(x_train.isna().sum().sum())
print(x_test.isna().sum().sum())

predicciones_baseline = x_test["PM2_5"]

mae_baseline = mean_absolute_error(y_test, predicciones_baseline)

rmse_baseline = np.sqrt(mean_squared_error(y_test, predicciones_baseline))

print("RESULTADOS DE BASELINE")
print("MAE:", round(mae_baseline,2))
print("RMSE:", round(rmse_baseline,2))

modelo_lineal = LinearRegression()

modelo_lineal.fit(x_train, y_train)

prediccion_lineal=modelo_lineal.predict(x_test)

mae_lineal = mean_absolute_error(y_test, prediccion_lineal)

rmse_lineal = np.sqrt(mean_squared_error(y_test, prediccion_lineal))

print("RESULTADOS REGRESIÓN LINEAL")
print("MAE:", round(mae_lineal,2))
print("RMSE:", round(rmse_lineal,2))

modelo_rf = RandomForestRegressor(
    n_estimators= 100,
    max_depth= 15,
    min_samples_leaf=5,
    random_state= 2,
    n_jobs= -1
)

modelo_rf.fit(x_train, y_train)

predicciones_rf = modelo_rf.predict(x_test)
mae_rf = mean_absolute_error(y_test, predicciones_rf)
rmse_rf = np.sqrt(mean_squared_error(y_test, predicciones_rf))
print("RESULTADOS RANDOM FOREST")
print("MAE:", round(mae_rf, 2))
print("RMSE:", round(rmse_rf, 2))

print("\nCOMPARACIÓN DE MODELOS")
print("---------------------------")
print("Baseline:")
print("MAE:", round(mae_baseline, 2))
print("RMSE:", round(rmse_baseline, 2))

print("\nRegresión Lineal:")
print("MAE:", round(mae_lineal, 2))
print("RMSE:", round(rmse_lineal, 2))

print("\nRandom Forest:")
print("MAE:", round(mae_rf, 2))
print("RMSE:", round(rmse_rf, 2))

comparacion = pd.DataFrame({"FECHA_HORA":prueba["FECHA_HORA"].values,
        "VALOR_REAL":y_test.values,"PREDICCION_RF":predicciones_rf,"PREDICCION_LINEAL":prediccion_lineal})

comparacion["FECHA_OBJETIVO"] = (
    comparacion["FECHA_HORA"] + pd.Timedelta(hours=1)
)


comparacion["ERROR_ABSOLUTO"] = abs(comparacion["VALOR_REAL"] - comparacion["PREDICCION_RF"])

mayores_errores = comparacion.sort_values(by="ERROR_ABSOLUTO", ascending=False)


print(comparacion.head(10))

datos_grafico = comparacion.head(168)

plt.figure(figsize=(15,6))
plt.plot(
    datos_grafico["FECHA_OBJETIVO"],
    datos_grafico["VALOR_REAL"],
    label="Valores reales",
    alpha=0.8
)

plt.plot(
    datos_grafico["FECHA_OBJETIVO"],
    datos_grafico["PREDICCION_RF"],
    label="Random Forest",
    alpha=0.8
)

plt.plot(
    datos_grafico["FECHA_OBJETIVO"],
    datos_grafico["PREDICCION_LINEAL"],
    label="Prediccion lineal",
    alpha=0.8
)

plt.title("PM2.5 real vs. predicciones HORA OBJETIVO")
plt.xlabel("Fecha y hora")
plt.ylabel("PM2.5 (µg/m³)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print(
    mayores_errores[
        ["FECHA_OBJETIVO", "VALOR_REAL",
         "PREDICCION_RF", "ERROR_ABSOLUTO"]
    ].head(10)
)

detalle_errores = prueba.iloc[mayores_errores.head(10).index][
    ["FECHA_HORA", "PM2_5", "PM25_LAG_1", "PM25_LAG_2", "PM25_LAG_3", "PM25_LAG_24", "PM25_OBJETIVO"]]

print(detalle_errores)

# Obtener importancia de cada variable
importancias = pd.DataFrame({
    "VARIABLE": x_train.columns,
    "IMPORTANCIA": modelo_rf.feature_importances_
})

# Ordenar de mayor a menor importancia
importancias = importancias.sort_values(
    "IMPORTANCIA",
    ascending=False
)

print(importancias)


variables_sin_actual = [
    variable for variable in variables
    if variable != "PM2_5"
]

x_train_sin_actual = x_train[variables_sin_actual]
x_test_sin_actual = x_test[variables_sin_actual]

modelo_rf_sin_actual = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

modelo_rf_sin_actual.fit(
    x_train_sin_actual,
    y_train
)

predicciones_rf_sin_actual = modelo_rf_sin_actual.predict(
    x_test_sin_actual
)
mae_rf_sin_actual = mean_absolute_error(
    y_test,
    predicciones_rf_sin_actual
)

rmse_rf_sin_actual = np.sqrt(
    mean_squared_error(
        y_test,
        predicciones_rf_sin_actual
    )
)

print("RANDOM FOREST SIN PM2.5 ACTUAL")
print("MAE:", round(mae_rf_sin_actual, 2))
print("RMSE:", round(rmse_rf_sin_actual, 2))

resultados = pd.DataFrame({
    "MODELO": [
        "Baseline",
        "Regresion Lineal",
        "Random Forest",
        "Random Forest sin PM2.5 actual"
    ],
    "MAE": [
        mae_baseline,
        mae_lineal,
        mae_rf,
        mae_rf_sin_actual
    ],
    "RMSE": [
        rmse_baseline,
        rmse_lineal,
        rmse_rf,
        rmse_rf_sin_actual
    ]
})

print(resultados.sort_values("MAE"))


sjl_modelo_limpio.to_csv(
    "sjl_modelo_limpio.csv",
    index=False
)

comparacion.to_csv(
    "comparacion.csv",
    index=False
)

print("DataFrames exportados correctamente")