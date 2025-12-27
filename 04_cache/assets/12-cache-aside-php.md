```php
$cacheKey = "profile:user:$userId";

// 1. Попытка прочитать из кеша
$cached = $this->cache->get(key: $cacheKey);

if ($cached !== null) {
    return $cached;
}

// 2. MISS → читаем из базы
$profile = $this->db->fetchAssociative(
    'SELECT id, name, address FROM users WHERE id = ?',
    [$userId]
);

// 3. Пишем результат в Redis
$this->cache->delete(key: $cacheKey);
$this->cache->set(key: $cacheKey, value: $profile, ttl: 300);

```

