```php
function getClusterForRegion(string $region): string
{
    return match ($region) {
        'EU'   => 'pg-eu-cluster',
        'US'   => 'pg-us-cluster',
        'APAC' => 'pg-apac-cluster',
    };
}
```

