```php
$token = bin2hex(random_bytes(8));

$ok = $redis->set(
    "lock:product:123",
    $token,
    ['nx', 'px' => 5000]
);

if (!$ok) {
    throw new \RuntimeException("Lock already held");
}

try {
    // критическая секция
    $db->update(...);
    $cache->set(...);

} finally {
    // удаляем лок только если мы владелец
    if ($redis->get("lock:product:123") === $token) {
        $redis->del("lock:product:123");
    }
}
```

