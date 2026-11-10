-- 1. Evolución anual
SELECT ANIO,
       COUNT(*) AS REGISTROS,
       AVG(PM2_5) AS PROMEDIO_PM25
FROM dbo.[Modelo de datos]
GROUP BY ANIO
ORDER BY ANIO;

-- 2. Contaminación por hora
SELECT HORA,
       AVG(PM2_5) AS PROMEDIO_PM25
FROM dbo.[Modelo de datos]
GROUP BY HORA
ORDER BY HORA;

-- 3. Clasificación descriptiva
SELECT
    CASE
        WHEN PM2_5 < 15 THEN 'Bajo'
        WHEN PM2_5 < 30 THEN 'Moderado'
        ELSE 'Alto'
    END AS NIVEL,
    COUNT(*) AS REGISTROS
FROM dbo.[Modelo de datos]
GROUP BY
    CASE
        WHEN PM2_5 < 15 THEN 'Bajo'
        WHEN PM2_5 < 30 THEN 'Moderado'
        ELSE 'Alto'
    END;

-- 4. Evaluación de modelos
SELECT
    AVG(ABS(VALOR_REAL - PREDICCION_RF)) AS MAE_RF,
    SQRT(AVG(POWER(VALOR_REAL - PREDICCION_RF, 2))) AS RMSE_RF,
    AVG(ABS(VALOR_REAL - PREDICCION_LINEAL)) AS MAE_LINEAL,
    SQRT(AVG(POWER(VALOR_REAL - PREDICCION_LINEAL, 2))) AS RMSE_LINEAL
FROM dbo.Prediciones;