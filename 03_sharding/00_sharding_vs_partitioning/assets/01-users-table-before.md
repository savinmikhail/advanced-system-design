```text
users
──────────────────────────────────────────────────────────────────────
id (bigint, PK)
email (text, unique)
password_hash (text)
state (smallint)
middle_name (text)
google_id (text)
github_id (text)
vk_id (text)
avatar_url (text)
bio (text)
settings_json (jsonb)
... ещё пачка флагов/полей
```

