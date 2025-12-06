### План видео (high level)

1. Источники хвостов: железо, сеть, софт (только практические кейсы).
2. Как ретраи раздувают проблему: “всё ретраит” → retry storm.
3. Техники уменьшения хвоста:
  * hedged requests;
  * tied requests;
  * request coalescing;
  * latency-aware load balancing;
  * background jittering;
  * частично: backpressure / ограничение конкуренции.
4. Техники маскировки/обхода хвоста:
  * deadlines и deadline propagation;
  * circuit breaker;
  * graceful degradation (fallback).
5. Метрики и наблюдаемость:
  * перцентили, rate of retries, длина очередей;
  * distributed tracing;
  * алертинг по хвосту.
