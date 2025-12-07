```sql
CREATE TABLE events (
  id         bigint NOT NULL,
  created_at timestamptz NOT NULL,
  ...
) PARTITION BY RANGE (created_at);

ALTER TABLE events
  ADD CONSTRAINT events_pkey PRIMARY KEY (id, created_at);
```

