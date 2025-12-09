#!/bin/bash
# Le volume app_logs sera monté sur /logs
LOG_FILE="/logs/api.log"

while true
do
    echo "--- $(date) : Rapport de Monitoring ---"

    if [ -f "$LOG_FILE" ]; then
        # Compte le nombre total de requêtes
        TOTAL_REQUESTS=$(wc -l < "$LOG_FILE")
        echo "Requêtes totales : $TOTAL_REQUESTS"

        # Compte le nombre d'erreurs (codes 4xx ou 5xx)
        ERROR_COUNT=$(grep -c ' 4[0-9][0-9]\| 5[0-9][0-9]' "$LOG_FILE")
        echo "Erreurs (4xx/5xx) : $ERROR_COUNT"
        
        if [ "$ERROR_COUNT" -gt 0 ]; then
            echo "Dernière erreur enregistrée :"
            grep ' 4[0-9][0-9]\| 5[0-9][0-9]' "$LOG_FILE" | tail -n 1
        fi
    else
        echo "Fichier de logs non trouvé : $LOG_FILE"
    fi

    echo "-----------------------------------"
    sleep 10
done
