```php
$cacheKey = "profile:user:$userId";

// 1. Пишем в кэш НЕМЕДЛЕННО
$this->cache->get($cacheKey, function (ItemInterface $item) use ($data) {
    $item->expiresAfter(300);
    return $data;
});

// 2. Отправляем событие в очередь для асинхронного обновления БД
$this->bus->dispatch(new UpdateUserProfileMessage($userId, $data));
```

