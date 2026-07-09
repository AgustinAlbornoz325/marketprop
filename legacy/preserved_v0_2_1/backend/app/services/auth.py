import hashlib, secrets
from app.core.database import conn

SESSIONS={}

def h(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def create_session(user_id):
    token=secrets.token_hex(32)
    SESSIONS[token]=user_id
    return token

def by_token(token):
    uid=SESSIONS.get(token)
    if not uid:
        return None
    c=conn()
    row=c.execute("""SELECT users.id, users.name, users.email, users.role,
    organizations.id organization_id, organizations.name organization_name, organizations.plan plan
    FROM users JOIN organizations ON organizations.id=users.organization_id
    WHERE users.id=?""",(uid,)).fetchone()
    c.close()
    return dict(row) if row else None

def register_user(name,email,password,organization_name):
    c=conn()
    cur=c.cursor()
    if cur.execute("SELECT id FROM users WHERE email=?",(email,)).fetchone():
        c.close()
        raise ValueError("Ese email ya está registrado.")
    cur.execute("INSERT INTO organizations(name,plan) VALUES(?,?)",(organization_name,"Plan Básico"))
    org_id=cur.lastrowid
    cur.execute("INSERT INTO users(organization_id,name,email,password,role) VALUES(?,?,?,?,?)",(org_id,name,email,h(password),"admin"))
    user_id=cur.lastrowid
    c.commit()
    c.close()
    token=create_session(user_id)
    return token, by_token(token)

def login_user(email,password):
    c=conn()
    row=c.execute("SELECT id,password FROM users WHERE email=?",(email,)).fetchone()
    c.close()
    if not row or row["password"]!=h(password):
        raise ValueError("Email o contraseña incorrectos.")
    token=create_session(row["id"])
    return token, by_token(token)
