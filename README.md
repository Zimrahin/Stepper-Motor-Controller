TODO:

- GUI
    Viernes
        - implementar envío automático de parametros una vez se conecta
        (para que sea coherente con lo que se muestra en la GUI y tenga sentido enviar un ángulo)
            - o hacer que el enviar ángulo se desbloquee solo después de aplicar "apply" por primera vez
        - averiguar cómo acceder a variables de otros Widget
            - se debe imprimir en puerto serial (decidido en connectionWidget)
            - se debe convertir ángulo a steps (en angleWidget) por factor de conversión definido en paramWidget



baja prioridad
- guardar datos en la tarjeta SD sin necesidad de comunicación con el computador
- experimentar con baudrates más altos
