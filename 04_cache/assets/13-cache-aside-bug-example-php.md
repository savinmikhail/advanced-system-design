```php
// ❌ Забыли инвалидировать связанные ключи
$this->cache->delete("product:{$productId}"); // ✅
// Забыли:
// $this->cache->delete("cart:user:123"); // адрес был тут
// $this->cache->delete("search:results"); // товар был тут
```

