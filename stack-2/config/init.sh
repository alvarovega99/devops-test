#!/bin/bash

if [ -f .env ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

if [ -z "$GRAYLOG_API_URL" ] || [ -z "$GRAYLOG_AUTH_USERNAME" ] || [ -z "$GRAYLOG_AUTH_PASSWORD" ]; then
    echo "Error: Faltan algunas variables de entorno."
    exit 1
fi

headers="Content-Type: application/json"
configure_gelf_udp_input() {
    echo 'Configurando entrada GELF UDP...'
    curl -X POST \
         -H "Content-Type: application/json" \
         -H "X-Requested-By: curl" \
         -d '{"title":"GELF UDP Input","global":true,"type":"org.graylog2.inputs.gelf.udp.GELFUDPInput","configuration":{"bind_address":"0.0.0.0","port":12201,"recv_buffer_size":262144}}' \
         -u "$GRAYLOG_AUTH_USERNAME:$GRAYLOG_AUTH_PASSWORD" \
         "$GRAYLOG_API_URL/api/system/inputs"
    if [ $? -eq 0 ]; then
        echo "¡Entrada GELF UDP configurada correctamente!"
    else
        echo "Error al configurar la entrada GELF UDP."
    fi
}

configure_gelf_udp_input
