```php
public function renew(string $resource): bool
{
    $key = "lease:$resource";

    // Проверяем, что lease ещё наш
    if ($this->redis->get($key) !== $this->token) {
        return false; // lease уже чужой → мы больше не владелец
    }

    // Продлеваем аренду только если токен совпадает
    return $this->redis->set(
        $key,
        $this->token,
        ['XX', 'PX' => $this->ttlMs] // XX → ключ должен существовать
    ) !== false;
}

```

