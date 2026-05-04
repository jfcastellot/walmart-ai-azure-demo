# Glosario de Métricas — Walmart Retail Intelligence

## Variables del Modelo

**CPI (Consumer Price Index)**
Índice de Precios al Consumidor. Mide el cambio promedio en los precios 
que los consumidores pagan por bienes y servicios. Un CPI alto indica 
inflación — cuando sube, los consumidores tienden a reducir gastos 
discrecionales, lo que impacta las ventas de ciertos departamentos.

**Unemployment (Desempleo)**
Porcentaje de la población activa que no tiene empleo. Un desempleo alto 
se correlaciona con menor poder adquisitivo y por lo tanto menores ventas 
en categorías no esenciales.

**Fuel Price (Precio del Combustible)**
Precio promedio del galón de gasolina en la región de la tienda. Impacta 
directamente el tráfico a la tienda — precios altos reducen visitas de 
clientes que recorren largas distancias.

**Temperature (Temperatura)**
Temperatura promedio semanal en grados Fahrenheit en la región de la tienda.
Influye en la demanda de categorías estacionales como ropa, climatización 
y alimentos.

**MarkDowns (Descuentos Promocionales)**
Reducciones de precio aplicadas a productos específicos. Walmart registra 
5 tipos de MarkDown (MD1 a MD5) que representan diferentes tipos de 
promociones. Tienen impacto significativo en las ventas semanales.

**IsHoliday (Día Festivo)**
Indica si la semana contiene un día festivo importante como Super Bowl, 
Thanksgiving, Christmas o Labor Day. Las semanas con festivos tienen 
ventas significativamente más altas.

## Métricas de Evaluación del Modelo

**R² (Coeficiente de Determinación)**
Mide qué tan bien el modelo explica la variación en las ventas. 
Va de 0 a 1 — nuestro modelo tiene R²=0.9735, lo que significa que 
explica el 97.35% de la variación en ventas semanales.

**MAE (Mean Absolute Error)**
Error promedio absoluto entre la predicción y el valor real en dólares.

**RMSE (Root Mean Square Error)**
Similar al MAE pero penaliza más los errores grandes. Útil para detectar 
predicciones muy alejadas de la realidad.