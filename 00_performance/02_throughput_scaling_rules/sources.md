
---

## 📘 ТОП 5 обязательных к прочтению

### 1) **The Tail at Scale — Jeff Dean, Google**

[https://queue.acm.org/detail.cfm?id=1855848](https://queue.acm.org/detail.cfm?id=1855848)
Это база. Про tail latency, hedging, tied requests.
Обязательно.

### 2) **Universal Scalability Law — Neil Gunther**

Книга: *Guerrilla Capacity Planning*
Короткое объяснение: [http://www.perfdynamics.com/manifesto/USLscalability.html](http://www.perfdynamics.com/manifesto/USLscalability.html)
Это реально практическая формула для throughput.

### 3) **AWS Builders Library — Timeouts, Retries, and Backoff**

[https://aws.amazon.com/builders-library/timeouts-retries-and-backoff/](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff/)
Объясняет tail amplification + retry storms.

### 4) **Martin Kleppmann — Designing Data-Intensive Applications (глава 1–3)**

Глава про конкуренцию, очереди, CAS, lock-free алгоритмы.
Очень практично.

### 5) **Mechanical Sympathy — обсуждения от Martin Thompson**

[https://mechanical-sympathy.blogspot.com/](https://mechanical-sympathy.blogspot.com/)
NUMA, head-of-line blocking, memory barriers.
Жизненно.

---

# 📕 Дополнительные, но очень хорошие

### Facebook: *Scaling Memcache at Facebook*

[https://www.usenix.org/conference/nsdi13/scaling-memcache-facebook](https://www.usenix.org/conference/nsdi13/scaling-memcache-facebook)
Про hot keys и tail latency.

### Netflix: *Making retries safe*

[https://netflixtechblog.com/making-retries-safe-8f88e1388013](https://netflixtechblog.com/making-retries-safe-8f88e1388013)
Про coordinated omission и retry storms.

### Google SRE Book

Глава "Addressing Cascading Failures".
