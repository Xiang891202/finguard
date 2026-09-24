"""seed default tenant and genetic markers

Revision ID: b93f21a4aec3
Revises: fafac0678418
Create Date: 2026-09-24

"""
import json

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = "b93f21a4aec3"
down_revision = "fafac0678418"
branch_labels = None
depends_on = None


DEFAULT_TENANT_ID = "00000000-0000-0000-0000-000000000001"

GENETIC_MARKERS = [
    ("BRCA1", "BRCA1 基因", ["乳癌", "卵巢癌"], ["reproductive"], 3.0, 1),
    ("BRCA2", "BRCA2 基因", ["乳癌", "卵巢癌", "胰臟癌"], ["reproductive"], 3.0, 2),
    ("APOE", "APOE 基因", ["阿茲海默症"], ["brain"], 2.5, 3),
    ("LDLR", "LDLR 基因", ["家族性高膽固醇", "心血管疾病"], ["heart"], 2.0, 4),
    ("TP53", "TP53 基因", ["多種癌症"], ["reproductive", "lungs"], 3.0, 5),
    ("HFE", "HFE 基因", ["血色素沉著症"], ["liver"], 2.0, 6),
    ("MTHFR", "MTHFR 基因", ["血栓", "葉酸代謝異常"], ["heart"], 1.5, 7),
    ("ALDH2", "ALDH2 基因", ["酒精代謝異常", "食道癌"], ["liver"], 1.8, 8),
]


def upgrade() -> None:
    conn = op.get_bind()

    conn.execute(
        text("""
            INSERT INTO tenants (id, name, slug, plan, status, max_users, max_models)
            VALUES (:id, :name, :slug, :plan, :status, :max_users, :max_models)
            ON CONFLICT (id) DO NOTHING
        """),
        {
            "id": DEFAULT_TENANT_ID,
            "name": "預設租戶",
            "slug": "default",
            "plan": "free",
            "status": "active",
            "max_users": 5,
            "max_models": 10,
        },
    )

    for code, name, diseases, parts, risk_high, order in GENETIC_MARKERS:
        conn.execute(
            text("""
                INSERT INTO genetic_markers
                (id, marker_code, marker_name, related_diseases, related_body_parts,
                 risk_level_high, display_order, is_active)
                VALUES (gen_random_uuid()::text, :code, :name, :diseases, :parts,
                        :risk, :order, TRUE)
                ON CONFLICT (marker_code) DO UPDATE SET is_active = TRUE
            """),
            {
                "code": code,
                "name": name,
                "diseases": json.dumps(diseases, ensure_ascii=False),
                "parts": json.dumps(parts, ensure_ascii=False),
                "risk": risk_high,
                "order": order,
            },
        )


def downgrade() -> None:
    conn = op.get_bind()
    codes = [m[0] for m in GENETIC_MARKERS]
    conn.execute(
        text("DELETE FROM genetic_markers WHERE marker_code = ANY(:codes)"),
        {"codes": codes},
    )
    conn.execute(
        text("DELETE FROM tenants WHERE id = :id"),
        {"id": DEFAULT_TENANT_ID},
    )