--Testeo
SELECT * FROM historical_table_actor_vial
WHERE "FORMULARIO" = 'A001566898'

SELECT * FROM historical_table_causa
WHERE "FORMULARIO" = 'A001566898'

SELECT "FORMULARIO",
	   "CODIGO_ACCIDENTE",
	   "CODIGO_VEHICULO",
	   COUNT(*) as nro_causas
FROM (
	SELECT "FORMULARIO",
		   "CODIGO_ACCIDENTE",
		   "CODIGO_VEHICULO",
		   "TIPO_CAUSA",
		   COUNT(*) as nro_causas
	FROM historical_table_causa
	GROUP BY 1,2,3,4
	HAVING COUNT(*) > 1)
GROUP BY 1,2,3
HAVING COUNT(*) > 1
ORDER BY nro_causas desc


--Revisar Tble Data Integration
SELECT "FORMULARIO", 
	    "CODIGO_ACCIDENTE", 
		"CODIGO_VEHICULO",
		COUNT(*) as nro_rows
FROM view_data_integration
GROUP BY 1,2,3
HAVING COUNT(*) > 1
ORDER BY nro_rows desc;

SELECT * FROM view_data_integration
WHERE "FORMULARIO" = 'A001060001'

SELECT * 
FROM 
	(SELECT "FORMULARIO", 
			CAST(SPLIT_PART("CODIGO", '-', 1) as bigint) AS cod_accidente, 
			"CODIGO_VEHICULO",
			COUNT(*) as nro_rows
	FROM historical_table_actor_vial
	GROUP BY 1,2,3
	HAVING COUNT(*) > 1) temp_01
JOIN (
	SELECT "FORMULARIO", 
			"CODIGO_ACCIDENTE", 
			"CODIGO_VEHICULO",
			COUNT(*) as nro_rows
	FROM view_data_integration
	GROUP BY 1,2,3
	HAVING COUNT(*) > 1) temp_02
ON temp_01."FORMULARIO" = temp_02."FORMULARIO"
AND temp_01.cod_accidente = temp_02."CODIGO_ACCIDENTE"
AND temp_01."CODIGO_VEHICULO" = temp_02."CODIGO_VEHICULO"
AND temp_01.nro_rows <> temp_02.nro_rows




--Cruce Formularios Duplicados
SELECT b01.cod_formulario,
	   b02.cod_formulario,
	   b01.nro_rows as nro_rows_01,
	   b02.nro_rows as nro_rows_02,
	   (b01.nro_rows - b02.nro_rows) as diferencia
FROM (
	SELECT "FORMULARIO" as cod_formulario,
		   COUNT(*) as nro_rows
	FROM view_data_integration_3
	GROUP BY 1) b01
LEFT JOIN (
	SELECT "FORMULARIO" as cod_formulario,
	   	   COUNT(*) as nro_rows
    FROM view_data_integration_2
    GROUP BY 1
) b02
ON b01.cod_formulario = b02.cod_formulario
where (b01.nro_rows - b02.nro_rows) <> 0



--Testeo CASE when
--select *
--from view_data_integration LIMIT 100
--UNION ALL

WITH temp_agg_causa as (
	SELECT "FORMULARIO",
		   "CODIGO_ACCIDENTE",
		   "CODIGO_VEHICULO",
		   --"CODIGO_CAUSA",
		   --"NOMBRE",
		   --"TIPO",
		   "TIPO_CAUSA",
		   COUNT(*) as nroInfracciones
	FROM (
		SELECT ROW_NUMBER() OVER (PARTITION BY concat_causa ORDER BY "OBJECTID" desc) as row_number, *
		FROM (
			  SELECT CONCAT("FORMULARIO", '-', 
							"CODIGO_ACCIDENTE", '-', 
							"CODIGO_VEHICULO", '-',
							"CODIGO_CAUSA", '-',
							"TIPO", '-',
							"TIPO_CAUSA") as concat_causa,
					  *
			   FROM historical_table_causa) 
	) temp_causa_dup
	WHERE temp_causa_dup.row_number = 1
	GROUP BY 1,2,3,4
	--ORDER BY nroInfracciones desc
)
SELECT * FROM temp_agg_causa 
JOIN (
	SELECT DISTINCT "FORMULARIO", "CODIGO_ACCIDENTE", "CODIGO_VEHICULO", "CONDICION_ACCIDENTADO"
	FROM view_data_integration_3
	WHERE "TIPO_CAUSA" IS null
	  AND "CONDICION_ACCIDENTADO" IN ('MOTOCICLISTA', 'CICLISTA')
) b1
ON (b1."FORMULARIO" = temp_agg_causa."FORMULARIO"
AND b1."CODIGO_ACCIDENTE" = temp_agg_causa."CODIGO_ACCIDENTE"
AND b1."CODIGO_VEHICULO" = temp_agg_causa."CODIGO_VEHICULO")



SELECT COUNT(*) FROM view_data_integration_2

SELECT "TIPO_CAUSA",
	   COUNT(*) as nroTotal
FROM temp_agg_causa
GROUP BY 1

SELECT DISTINCT "CONDICION_VEHICULO" FROM historical_table_actor_vial

SELECT * FROM historical_table_actor_vial LIMIT 1000
WHERE "FORMULARIO" = '712171800'


SELECT "TIPO_CAUSA",
	   COUNT(*) as nroTotal
FROM view_data_integration_2
GROUP BY 1
UNION ALL
SELECT "TIPO_CAUSA",
	   COUNT(*) as nroTotal
FROM view_data_integration_3
GROUP BY 1


SELECT * FROM (
	SELECT DISTINCT "FORMULARIO", "CODIGO_ACCIDENTE", "CODIGO_VEHICULO", "CONDICION_ACCIDENTADO"
	FROM view_data_integration_2
	WHERE "TIPO_CAUSA" IS null
)
JOIN 




SELECT * FROM view_data_integration_2 --LIMIT 1000
WHERE "FORMULARIO" = '712450900'

SELECT * FROM historical_table_causa
WHERE "FORMULARIO" = '712450900'

SELECT DISTINCT "CONDICION_ACCIDENTADO" FROM view_data_integration_2
SELECT DISTINCT "TIPO_CAUSA" FROM historical_table_causa

SELECT DISTINCT "CONDICION_ACCIDENTADO_2", "CODIGO_VEHICULO"
FROM view_data_integration_2
WHERE "CONDICION_ACCIDENTADO_2" = 'PEATON'


SELECT DISTINCT "TIPO_CAUSA", "CODIGO_VEHICULO"
FROM historical_table_causa
WHERE "TIPO_CAUSA" = 'PEATON'

SELECT * FROM historical_table_actor_vial LIMIT 1000
WHERE "CONDICION_ACCIDENTADO_2" = 'PEATON'
