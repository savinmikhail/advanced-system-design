```sql
CREATE TABLE users (
  id bigint NOT NULL,
  ...
) PARTITION BY HASH (id);

ALTER TABLE users
  ADD CONSTRAINT users_pkey PRIMARY KEY (id);
```

