```sql
CREATE TABLE events (
    id         bigserial PRIMARY KEY,
    user_id    bigint      NOT NULL,
    created_at timestamptz NOT NULL,
    payload    jsonb       NOT NULL
) PARTITION BY RANGE (created_at);
```

