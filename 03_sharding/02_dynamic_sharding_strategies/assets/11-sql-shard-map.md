```sql
CREATE TABLE shard_map (
    region      text PRIMARY KEY,
    dsn         text NOT NULL,
    is_readonly boolean NOT NULL DEFAULT false
);
```

