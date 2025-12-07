```php
$version = $redis->incr("product:123:version"); // атомарно → 8
$key = "product:123:v$version";

$redis->set($key, json_encode($data));
```

