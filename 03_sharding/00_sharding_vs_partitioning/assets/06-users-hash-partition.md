```sql
CREATE TABLE users (
    id    bigint PRIMARY KEY,
    email text NOT NULL
) PARTITION BY HASH (id);

CREATE TABLE users_p0
    PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE users_p1
    PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);
-- и так далее
```

