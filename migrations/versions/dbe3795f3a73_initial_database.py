"""Initial Database

Revision ID: dbe3795f3a73
Revises:
Create Date: 2019-05-26 23:48:06.521619

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'dbe3795f3a73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('customers',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('first_name', sa.Text(), nullable=False),
                    sa.Column('last_name', sa.Text(), nullable=False),
                    sa.Column('street_address', sa.Text(), nullable=False),
                    sa.Column('state', sa.String(length=2), nullable=False),
                    sa.Column('zipcode', sa.String(length=5), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('products',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('order_statuses',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('customer_id', sa.Integer(), nullable=False),
                    sa.Column('product_id', sa.Integer(), nullable=False),
                    sa.Column('price', sa.Text(), nullable=False),
                    sa.Column('status', sa.Enum('new', 'canceled', name='order_enum'), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
                    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
                    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
                    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
                    sa.UniqueConstraint('customer_id', 'product_id', name='customer_product_uc'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('order_statuses')
    op.drop_table('products')
    op.drop_table('customers')
