```sql
-- свежие события на SSD
CREATE TABLE events_2026_01
  PARTITION OF events
  FOR VALUES FROM ('2026-01-01') TO ('2026-02-01')
  TABLESPACE fast_ssd;

-- архивная партиция на дешёвом диске
ALTER TABLE events_2024_01 SET TABLESPACE slow_hdd;

-- индекс по горячей партиции тоже можно унести на SSD
CREATE INDEX idx_events_2026_01_created_at
  ON events_2026_01 (created_at)
  TABLESPACE fast_ssd;
```

