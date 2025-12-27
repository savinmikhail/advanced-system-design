```text
обычный путь:
  key → (hash / range) → shard

с hot-key isolation:
  if key in HOT_MAP:
      → hot_shard_for(key)
  else:
      → (hash / range) → shard
```

