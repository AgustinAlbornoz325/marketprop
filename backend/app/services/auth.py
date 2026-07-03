import hashlib, secrets
from app.core.database import conn
SESSIONS={}

def h(p): return hashlib.sha256(p.encode()).hexdigest()

def session(user_id):
    t=secrets.token_hex(32); SESSIONS[t]=user_id; return t

def by_token(token):
    uid=SESSIONS.get(token)
    if not uid: return None
    c=conn()
    row=c.execute("""SELECT users.id,users.name,users.email,users.role,
    organizations.id organization_id, organizations.name organization_name, organizations.plan plan
    FROM users JOIN organizations ON organizations.id=users.organization_id WHERE users.id=?""",(uid,)).fetchone()
    c.close()
    return dict(row) if row else None

def register_user(name,email,password,organization_name):
    c=conn(); cur=c.cursor()
    if cur.execute("SELECT id FROM users WHERE email=?",(email,)).fetchone():
        c.close(); raise ValueError("Ese email ya está registrado.")
    cur.execute("INSERT INTO organizations(name,plan) VALUES(?,?)",(organization_name,"Plan Básico"))
    org=cur.lastrowid
    cur.execute("INSERT INTO users(organization_id,name,email,password,role) VALUES(?,?,?,?,?)",(org,name,email,h(password),"admin"))
    uid=cur.lastrowid
    c.commit(); c.close()
    t=session(uid); return t, by_token(t)

def login_user(email,password):
    c=conn(); row=c.execute("SELECT id,password FROM users WHERE email=?",(email,)).fetchone(); c.close()
    if not row or row["password"]!=h(password): raise ValueError("Email o contraseña incorrectos.")
    t=session(row["id"]); return t, by_token(t)
