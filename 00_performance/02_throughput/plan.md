1. “Добьём” интуицию: рост нагрузки → рост concurrency → рост latency.
2. Amdahl’s Law: непараллелящаяся часть.
3. Gustafson: масштабируем задачу, а не ускоряем одну и ту же.
4. Contention и coherence: shared ресурсы, lock’и, hot keys, кластеры БД.
5. Примеры из практики: БД, Redis, PHP-FPM.
6. Приёмы:

    * backpressure;
    * queue-based load leveling;
    * разделение нагрузок и данных;
    * изоляция hot ресурсов.
7. Вывод: что именно надо делать, чтобы throughput рос устойчиво.
