from alembic import op
import sqlalchemy as sa

revision = '5357eaecfd4d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('reports', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_report_user', 'users', ['user_id'], ['id'])


def downgrade():
    with op.batch_alter_table('reports', schema=None) as batch_op:
        batch_op.drop_constraint('fk_report_user', type_='foreignkey')
        batch_op.drop_column('user_id')
