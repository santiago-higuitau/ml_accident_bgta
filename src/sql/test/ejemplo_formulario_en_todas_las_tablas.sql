SELECT * FROM historical_table_actor_vial --LIMIT 20
WHERE "FORMULARIO" = 'A000963247';

SELECT * FROM historical_table_vehiculo --LIMIT 20
WHERE "FORMULARIO" = 'A000963247';

SELECT * FROM historical_table_causa --LIMIT 20
WHERE "FORMULARIO" = 'A000963247';

SELECT * FROM historical_table_via --LIMIT 20
WHERE "FORMULARIO" = 'A000963247';

SELECT * FROM historical_table_accidente --LIMIT 20
WHERE "FORMULARIO" = 'A000963247';

SELECT * FROM historical_table_lesionado --LIMIT 20
WHERE "FORMULARIO" = 'A000963247';

SELECT * FROM historical_table_muerto --LIMIT 20
WHERE "FORMULARIO" = 'A000963247';

SELECT "ESTADO" as est_accidentado, COUNT(*) as nro_casos
FROM historical_table_actor_vial
GROUP BY 1
