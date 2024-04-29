WITH tble_temp as (
		SELECT 'tble_accidente' as tble_selected, count(*) as nro_registros
		from historical_table_accidente
		UNION ALL
		SELECT 'tble_actorVial' as tble_selected, count(*) as nro_registros
		from historical_table_actor_vial
		UNION ALL
		SELECT 'tble_causa' as tble_selected, count(*) as nro_registros
		from historical_table_causa
		UNION ALL
		SELECT 'tble_lesionado' as tble_selected, count(*) as nro_registros
		from historical_table_lesionado
		UNION ALL
		SELECT 'tble_muerto' as tble_selected, count(*) as nro_registros
		from historical_table_muerto
		UNION ALL
		SELECT 'tble_vehiculo' as tble_selected, count(*) as nro_registros
		from historical_table_vehiculo
		UNION ALL
		SELECT 'tble_via' as tble_selected, count(*) as nro_registros
		from historical_table_via
	)
select * from tble_temp
order by nro_registros desc