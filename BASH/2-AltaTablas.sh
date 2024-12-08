cd  ~/Documents/TP-FINAL-CEIA/Recursos/pinot-recipes/ingest-json-files-kafka
docker exec -it pinot-controller-json bin/pinot-admin.sh AddTable     -tableConfigFile /config/table.json     -schemaFile /config/schema.json   -exec

