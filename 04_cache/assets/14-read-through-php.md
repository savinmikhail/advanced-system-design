```php
$value = $cache->get('user:123', function(ItemInterface $item) use($db): array {
    $item->expiresAfter(300);

    return $db->query('SELECT * FROM users WHERE id = 123');
});

```

