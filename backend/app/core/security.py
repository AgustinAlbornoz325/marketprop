import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256((password or "").encode("utf-8")).hexdigest()

def verify_password(password: str, password_hash: str | None) -> bool:
    if not password_hash:
        return True
    return hash_password(password) == password_hash

def slugify(value: str) -> str:
    raw = (value or "workspace").lower().strip()
    out = []
    for ch in raw:
        if ch.isalnum():
            out.append(ch)
        elif ch in [" ", "-", "_"]:
            out.append("-")
    slug = "".join(out).strip("-") or "workspace"
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:80]
