```mermaid
graph LR
A[Сервис] -->|TX: INSERT/UPDATE| B[(БД)]
B --> C[Outbox]
C -->|CDC| D[Kafka]
```

