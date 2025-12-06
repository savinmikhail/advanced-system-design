
## Ссылки на материалы

Подборка для углубления, чтобы оттуда вытаскивать идеи, примеры и формулировки.

### Русскоязычные источники

- **Когерентность кэша — Википедия**  
  Базовые определения и терминология.  
  https://ru.wikipedia.org/wiki/Когерентность_кэша

- **«Мифы о кэше процессора, в которые верят программисты» (Habr)**  
  Хорошее интуитивное объяснение когерентности кэша на уровне процессора, можно брать метафоры и объяснения.  
  https://habr.com/ru/articles/354748/

- **«Проектирование эффективной системы кэширования» (Habr)**  
  Обзор видов кэша, многоуровневого кэширования и distributed cache; хороший фон для твоей «продвинутой» части.  
  https://habr.com/ru/articles/853340/

- **«Что, если выкинуть все лишнее из базы в распределенный кэш» (ЮMoney + Hazelcast)**  
  Реальный кейс с распределённым кэшем, split-brain, согласованностью и проблемами под высокой нагрузкой.  
  https://habr.com/ru/companies/yoomoney/articles/332462/

- **«Как распилить монолит на сервисы и сохранить целостность данных» (T‑Банк)**  
  Про микросервисы, целостность данных и роль распределённого кэша в этом всём.  
  https://habr.com/ru/companies/tbank/articles/474994/

(Дополнительно можно поискать на YouTube по запросам «кэширование распределённые системы», «cache invalidation системный дизайн» — там есть доклады от Тинькофф, Avito, Яндекс, Ozon.)

### Англоязычные источники — распределённый кэш и согласованность

- **Martin Kleppmann — Designing Data‑Intensive Applications**  
  Главы про репликацию, кэширование и согласованность; хорошая база для понимания роли кэша в распределённых системах.
- **Meta Engineering — «Cache made consistent»**  
  История о том, как Facebook/Meta обеспечивали согласованность большого распределённого кэша.  
  https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/

- **«Distributed Caching Woes: Cache Invalidation» (Medium)**  
  Разбор боли с cache invalidation в распределённой системе и типовых паттернов.  
  https://medium.com/systems-architectures/distributed-caching-woes-cache-invalidation-c3d389198af3

- **ByteByteGo — «Distributed Caching: The Secret to High-Performance Systems»**  
  Обзор distributed cache, паттернов кэширования и проблем согласованности/инвалидации.  
  https://blog.bytebytego.com/p/distributed-caching-the-secret-to

- **Distributed cache — Wikipedia**  
  Общее представление о distributed cache, упоминание coherence, cache stampede и т.п.  
  https://en.wikipedia.org/wiki/Distributed_cache

- **Паттерны кэширования в Redis**  
  Официальные или околоредисные материалы по cache-aside, write-through, write-behind, read-through.  
  (Поиск: "Redis caching patterns" — актуальный раздел документации Redis.)
- **Инженерные блоги (Discord, крупные маркетплейсы, сервисы доставки)**  
  В блогах этих команд регулярно выходят разборы инцидентов с кэшем, stampede и split-brain — хороший источник живых историй и графиков для иллюстраций.

### Видео

- **«Effective Caching Strategies for Distributed Systems» (YouTube)**  
  Доклад про стратегии кэширования в распределённых системах, проблемы согласованности.  
  https://www.youtube.com/watch?v=vaUozFw-Y9k

- **«How Do You Achieve Cache Coherence In Distributed Systems» (YouTube)**  
  Короткое видео именно про cache coherence в распределённом контексте.  
  https://www.youtube.com/watch?v=L4OyfmIy-xU

