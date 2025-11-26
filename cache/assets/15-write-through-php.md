```php
 $cacheKey = "profile:user:$userId";

// 1. Пишем в кэш новое значение
$this->cache->get($cacheKey, function (ItemInterface $item) use ($data) {
    $item->expiresAfter(300);
    return $data;
});

// 2. Синхронно пишем в БД
$this->db->update('users', $data, ['id' => $userId]);
```

