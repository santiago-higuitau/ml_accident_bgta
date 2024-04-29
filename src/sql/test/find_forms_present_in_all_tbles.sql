SELECT DISTINCT(a01."FORMULARIO") as formulario 
FROM historical_table_actor_vial a01
	JOIN historical_table_vehiculo a02
	ON a02."FORMULARIO" = a01."FORMULARIO"
	JOIN historical_table_causa a03
	ON a03."FORMULARIO" = a01."FORMULARIO"
	JOIN historical_table_via a04
	ON a04."FORMULARIO" = a01."FORMULARIO"
	JOIN historical_table_accidente a05
	ON a05."FORMULARIO" = a01."FORMULARIO"
	JOIN historical_table_lesionado a06
	ON a06."FORMULARIO" = a01."FORMULARIO"
	JOIN historical_table_muerto a07
	ON a07."FORMULARIO" = a01."FORMULARIO"
--WHERE a01."CODIGO_VEHICULO" IS NOT NULL
	
--A000035513: Múltiples muertes, PEATONES incluidos



SELECT DISTINCT(a01."FORMULARIO") as formulario 
FROM historical_table_actor_vial a01
WHERE a01."CODIGO_VEHICULO" IS NOT NULL
