SELECT "TIPO_CAUSA" as tipo_causa,
count(*) as nro_causa FROM historical_table_causa
GROUP BY 1


SELECT * FROM historical_table_causa
WHERE "FORMULARIO" = 'A001572786'

SELECT * FROM historical_table_actor_vial
WHERE "FORMULARIO" = 'A001572786'