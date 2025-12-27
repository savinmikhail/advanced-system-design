```php
$redis->watch("product:123");

$current = $redis->get("product:123");
$new = $current + 100;

$redis->multi();
$redis->set("product:123", $new);
$ok = $redis->exec();

if (!$ok) {
    throw new ConflictException("Race detected");
}
```

