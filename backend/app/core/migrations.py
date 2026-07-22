from sqlalchemy import inspect, text

WORKSPACE_COLUMNS = {
    "properties": "ALTER TABLE properties ADD COLUMN workspace_id INTEGER DEFAULT 1",
    "content_items": "ALTER TABLE content_items ADD COLUMN workspace_id INTEGER DEFAULT 1",
    "pipeline_items": "ALTER TABLE pipeline_items ADD COLUMN workspace_id INTEGER DEFAULT 1",
    "calendar_items": "ALTER TABLE calendar_items ADD COLUMN workspace_id INTEGER DEFAULT 1",
    "marketdna_sources": "ALTER TABLE marketdna_sources ADD COLUMN workspace_id INTEGER DEFAULT 1",
}

def run_light_migrations(engine):
    inspector = inspect(engine)
    with engine.begin() as conn:
        for table, sql in WORKSPACE_COLUMNS.items():
            if table not in inspector.get_table_names():
                continue
            cols = [c["name"] for c in inspector.get_columns(table)]
            if "workspace_id" not in cols:
                conn.execute(text(sql))
