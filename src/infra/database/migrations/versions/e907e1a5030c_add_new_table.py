"""Начальная миграция с созданием таблицы `calc_results`."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "e907e1a5030c"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Создать таблицу `calc_results`."""
    op.create_table(
        "calc_results",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "total_cost_rub",
            sa.Numeric(precision=18, scale=4),
            nullable=False,
            comment="Итоговая стоимость изделия в рублях",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Момент создания записи",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Удалить таблицу `calc_results`."""
    op.drop_table("calc_results")
