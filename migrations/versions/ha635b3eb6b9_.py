"""empty message

Revision ID: da635b3eb6b9
Revises: g8df7b6ecb72
Create Date: 2020-06-16 16:17:23.042272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ha635b3eb6b9'
down_revision = 'g8df7b6ecb72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Backbone', sa.Column('features', sa.Text(), nullable=False, server_default = ""))
    op.add_column('Backbone', sa.Column('seqAfter', sa.Text(), nullable=False, server_default = ""))
    op.add_column('Backbone', sa.Column('seqBefore', sa.Text(), nullable=False, server_default = ""))
    op.add_column('Backbone', sa.Column('type', sa.String(length=1), nullable=False, server_default = "i"))
    op.alter_column('UserData', 'googleAssoc',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.drop_column('Backbone', 'seq')
    # ### end Alembic commands ###
    return


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('UserData', 'googleAssoc',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.drop_column('Backbone', 'type')
    op.drop_column('Backbone', 'seqBefore')
    op.drop_column('Backbone', 'seqAfter')
    op.drop_column('Backbone', 'features')
    op.add_column('Backbone', sa.Column('seq', sa.TEXT(), nullable=True))
    # ### end Alembic commands ###
    return