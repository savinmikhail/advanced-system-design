```php
if ($cache->missing($key)) {

    if ($lock->acquire($key)) {
        $value = load_from_db();
        $cache->set($key, $value);
        $lock->release($key);
    } else {
        usleep(20000); // ждём 20мс
        $value = $cache->get($key);
    }
}
```

