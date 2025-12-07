```mermaid
graph LR
Billing -->|event: MoneyWithdrawn| Inventory
Inventory -->|event: GoodsReserved| Orders
Orders -->|event: OrderCreated| Notifications
```

