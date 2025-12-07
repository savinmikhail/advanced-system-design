```php
function getUserShardConnection(int $userId): PDO
{
    $shard = $userId % 4;

    return match ($shard) {
        0 => $this->connShard0,
        1 => $this->connShard1,
        2 => $this->connShard2,
        3 => $this->connShard3,
    };
}
```

