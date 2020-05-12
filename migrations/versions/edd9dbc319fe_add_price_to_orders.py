"""Add price to orders

Revision ID: edd9dbc319fe
Revises: 209688e05724
Create Date: 2020-05-12 12:26:49.734213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from app import Order, db

revision = 'edd9dbc319fe'
down_revision = '209688e05724'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('price', sa.Integer(), nullable=False))

    # updating all prices for existing orders
    for order in Order.query.all():
        order.price = order.quantity * 5
        db.session.commit()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'price')
    # ### end Alembic commands ###
