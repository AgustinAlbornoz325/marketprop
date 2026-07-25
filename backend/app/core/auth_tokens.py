import base64
import hmac
import hashlib
import json
import os
import time
from typing import Any

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.core.models import UserAccount

AUTH_SECRET = os.getenv("MARKETPROP_AUTH_SECRET", "marketprop-dev-change-this-secret")
TOKEN_TTL_SECONDS = 60 * 60 * 24 * 7  # 7 days for local/dev

def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

def _unb64(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + pad).encode("utf-8"))

def issue_token(user: UserAccount) -> str:
    payload = {
        "sub": user.id,
        "workspace_id": user.workspace_id,
        "role": user.role,
        "email": user.email,
        "iat": int(time.time()),
        "exp": int(time.time()) + TOKEN_TTL_SECONDS,
    }
    raw = _b64(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    sig = hmac.new(AUTH_SECRET.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256).digest()
    return f"{raw}.{_b64(sig)}"

def decode_token(token: str) -> dict[str, Any]:
    try:
        raw, sig = token.split(".", 1)
        expected = _b64(hmac.new(AUTH_SECRET.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256).digest())
        if not hmac.compare_digest(sig, expected):
            raise ValueError("Firma inválida")
        payload = json.loads(_unb64(raw).decode("utf-8"))
        if int(payload.get("exp", 0)) < int(time.time()):
            raise ValueError("Token expirado")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Sesión inválida o expirada")

def token_from_request(request: Request) -> str:
    auth = request.headers.get("authorization") or ""
    if auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()
    token = request.query_params.get("token")
    if token:
        return token
    raise HTTPException(status_code=401, detail="Falta iniciar sesión")

def current_user_from_request(request: Request, db: Session) -> UserAccount:
    payload = decode_token(token_from_request(request))
    user = db.get(UserAccount, int(payload["sub"]))
    if not user or user.status not in ("active", "invited"):
        raise HTTPException(status_code=401, detail="Usuario inválido")
    return user

def require_role(user: UserAccount, roles: set[str]):
    if user.role not in roles:
        raise HTTPException(status_code=403, detail="No tenés permisos para esta acción")


ROLE_LEVELS = {
    "member": 10,
    "admin": 20,
    "owner": 30,
    "super_admin": 100,
}

def has_role_at_least(user: UserAccount, minimum_role: str) -> bool:
    return ROLE_LEVELS.get(user.role, 0) >= ROLE_LEVELS.get(minimum_role, 0)

def require_min_role(user: UserAccount, minimum_role: str):
    if not has_role_at_least(user, minimum_role):
        raise HTTPException(status_code=403, detail=f"Requiere rol {minimum_role} o superior")

def require_workspace_manager(user: UserAccount):
    require_role(user, {"owner", "admin", "super_admin"})

def require_workspace_owner(user: UserAccount):
    require_role(user, {"owner", "super_admin"})
