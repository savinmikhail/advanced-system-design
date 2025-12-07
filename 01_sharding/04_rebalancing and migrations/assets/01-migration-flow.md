```mermaid
flowchart LR
    App --> Router
    Router --> OldShard
    Router --> NewShard

    OldShard -- CDC/changes --> Migrator
    Migrator --> NewShard

    Router -. switch .-> NewShard
```

