```php
if ($repo->hasProcessed($operationId)) {
    return; // уже всё сделали, повтор просто проходит мимо
}

$repo->markProcessed($operationId);
$billing->withdraw($userId, $amount);
```

