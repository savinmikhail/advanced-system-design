Phil Karlton famously said, “There are only two hard things in computer science: cache invalidation and naming things.” in 1997

receives cache invalidation events. For example, if Polaris receives an invalidation event that says “x=4 @version 4,” it then queries all cache replicas as a client to verify whether any violations of the invariant occur. If one cache replica returns “x=3 @version 3,” Polaris flags it as inconsistent and requeues the sample to later check it against the same target cache host. Polaris reports inconsistencies at certain timescales, e.g., one minute, five minutes or 10 minutes. If this sample still shows as inconsistent after one minute, Polaris reports it as an inconsistency for the corresponding timescale.

![img.png](img.png)

2.5. Типичные архитектуры кэшей - я бы инвертировал логику - сначала ситуация, потом решение. а не сначала решение потом для чего подходит

как считать stale reads?

Flow запроса "товар ID=123": - можно показать какая latency была до кеширования

нету связи между cache coherence и 2.4. Race Condition в Cache-Aside

про лизинг ниче не понятно

___

3 проблемы закрываемые кешом
метрики/понятия кеш хит кеш мисс
тегирование
слои
сдн
когерентность что это
когерентность как обеспечить
какие проблемы рождаются
stale data -> polaris
forever cache
грохочущее стадо
Jittered TTL (рандомизация)
request coalescing
прогрев кеша
blue green deploy
версионирование
doom loop
Кэширование негативных результатов
