# -*- coding: utf-8 -*-
from alembic import context
import traceback
import transaction

from endi.alembic.exceptions import MigrationError, RollbackError
from endi_base.models.base import DBSESSION
from endi.models import DBBASE


def run_migrations_online():
    from endi_payment.models import EndiPaymentHistory
    from endi_payment.database import ModelBase
    bind = DBSESSION.get_bind(EndiPaymentHistory)
    if bind is None:
        raise ValueError(
"\nYou must do enDI migrations using the 'endi-migrate' script"
"\nand not through 'alembic' directly."
            )

    transaction.begin()
    connection = DBSESSION.connection(EndiPaymentHistory)

    context.configure(
        connection=connection,
        target_metadata=ModelBase.metadata,
        compare_type=True,
    )

    try:
        context.run_migrations()
    except Exception as migration_e:
        traceback.print_exc()
        try:
            transaction.abort()
        except Exception as rollback_e:
            traceback.print_exc()
            raise RollbackError(rollback_e)
        else:
            raise MigrationError(migration_e)
    else:
        transaction.commit()
    finally:
        #connection.close()
        pass

run_migrations_online()
