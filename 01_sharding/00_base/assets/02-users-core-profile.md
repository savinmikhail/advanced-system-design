```text
users_core
────────────────────────────────────────
id (bigint, PK)
email (text, unique)
password_hash (text)
state (smallint)
google_id (text)
github_id (text)
vk_id (text)

users_profile
────────────────────────────────────────
user_id (bigint, PK, FK → users_core.id)
avatar_url (text)
bio (text)
settings_json (jsonb)
... всё “редкое и жирное”
```

