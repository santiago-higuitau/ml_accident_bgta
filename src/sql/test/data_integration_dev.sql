CREATE TABLE view_data_integration_3 as (
	-- Eliminando Duplicados En Causa y Construyendo Agg (CTE 1)
	WITH temp_agg_causa as (
		SELECT "FORMULARIO",
			   "CODIGO_ACCIDENTE",
			   "CODIGO_VEHICULO",
			   --"CODIGO_CAUSA",
			   --"NOMBRE",
			   --"TIPO",
			   "TIPO_CAUSA",
			   CASE
					WHEN "TIPO_CAUSA" = 'PEATON' THEN 0
					ELSE "CODIGO_VEHICULO"
			   END AS "CODIGO_VEHICULO_2",
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
	),
	--SELECT * FROM temp_agg_causa,
	--Add Cod-Accidente en Actor Vial (CTE 2)
	temp_tble_av as (
		SELECT *,
			  CAST(SPLIT_PART("CODIGO", '-', 1) as bigint) AS cod_accidente,
			  CASE 
				WHEN "CONDICION" = 'MOTOCICLISTA' THEN 'CONDUCTOR'
				WHEN "CONDICION" = 'CICLISTA' THEN 'CONDUCTOR'
				ELSE "CONDICION"
			  END AS "CONDICION_ACCIDENTADO_2",
			  --Assign 0 to CV for all PEATON
			  CASE
				WHEN "CONDICION" = 'PEATON' THEN 0
				ELSE "CODIGO_VEHICULO"
			  END AS "CODIGO_VEHICULO_2"
		FROM historical_table_actor_vial
	)
	SELECT --a01."FORMULARIO" as "FORMULARIO_ACC"
		  temp_tble_av."FORMULARIO"
		  --,a01."CODIGO_ACCIDENTE" as "CODIGO_ACCIDENTE_ACC"
		  ,temp_tble_av.cod_accidente as "CODIGO_ACCIDENTE"
		  ,a01."FECHA_OCURRENCIA_ACC"
		  ,a01."HORA_OCURRENCIA_ACC"
		  ,a01."ANO_OCURRENCIA_ACC"
		  ,a01."MES_OCURRENCIA_ACC"
		  ,a01."DIA_OCURRENCIA_ACC"
		  ,a01."FECHA_HORA_ACC"
		  ,a01."DIRECCION"
		  ,a01."GRAVEDAD"
		  ,a03."TIPO_CAUSA"
		  ,a03.nroInfracciones
		  --,a03."NOMBRE" as "NOMBRE_CAUSA"
		  ,a01."CLASE_ACC"
		  ,a01."LOCALIDAD"
		  ,a01."MUNICIPIO"
		  ,a01."LATITUD"
		  ,a01."LONGITUD"
		  ,temp_tble_av."CODIGO_ACCIDENTADO"
		--,temp_tble_av."CODIGO_VICTIMA"
		  ,temp_tble_av."CODIGO_VEHICULO"
		--,temp_tble_av."CODIGO_VEHICULO_2"
		  ,temp_tble_av."CONDICION" as "CONDICION_ACCIDENTADO"
		--,temp_tble_av."CONDICION_ACCIDENTADO_2"
		  ,temp_tble_av."ESTADO"
		  ,temp_tble_av."FECHA_NACIMIENTO"
		  ,temp_tble_av."EDAD"
		  ,temp_tble_av."GENERO"
		  ,CASE 
			   WHEN "ESTADO" IN ('HERIDO', 'ILESO') THEN 'N'
		       ELSE temp_tble_av."MUERTE_POSTERIOR"
		   END AS "MUERTE_POSTERIOR"
		  ,temp_tble_av."FECHA_POSTERIOR_MUERTE"
		  --,temo_tble_av."CONDICION_VEHICULO"
		  ,a02."CLASE" as "CLASE_DE_VEHICULO"
		  ,a02."SERVICIO" as "TIPO_DE_SERVICIO"
		  ,a02."MODALIDAD"
		  ,a02."ENFUGA"
	FROM temp_tble_av
	INNER join historical_table_accidente a01
		ON (a01."FORMULARIO" = temp_tble_av."FORMULARIO"
		AND a01."CODIGO_ACCIDENTE" = temp_tble_av.cod_accidente)
	LEFT join historical_table_vehiculo a02
		ON (a02."FORMULARIO" = temp_tble_av."FORMULARIO")
		AND a02."CODIGO_VEHICULO" = temp_tble_av."CODIGO_VEHICULO"
	LEFT join temp_agg_causa a03
		ON (a03."FORMULARIO" = temp_tble_av."FORMULARIO"
		AND a03."CODIGO_ACCIDENTE" = temp_tble_av.cod_accidente
		AND a03."CODIGO_VEHICULO_2" = temp_tble_av."CODIGO_VEHICULO_2"
		AND a03."TIPO_CAUSA" = temp_tble_av."CONDICION_ACCIDENTADO_2")
	WHERE temp_tble_av."ESTADO" is not NULL
);











