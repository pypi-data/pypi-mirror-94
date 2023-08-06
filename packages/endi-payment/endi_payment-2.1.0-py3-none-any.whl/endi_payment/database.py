# -*- coding: utf-8 -*-
"""
Specific session stuff used to store the payment history logs
"""
import logging

from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)
ModelBase = declarative_base()


def includeme(config):
    """
    Pyramid Include's mechanism
    Setup the library specific session
    """
    logger.debug("Setting up database configuration for endi_payment")
    settings = config.get_settings()
    from endi_base.models.base import DBBASE, DBSESSION

    if 'endi_payment_db.url' in settings:
        # On a une connexion particulière pour l'édition des journaux
        prefix = 'endi_payment_db.'
        endi_payment_engine = engine_from_config(settings, prefix=prefix)
        main_bind = DBSESSION.bind

        # Pour éviter un warning
        # https://bitbucket.org/zzzeek/sqlalchemy_old/issues/3977/
        DBSESSION.remove()

        DBSESSION.configure(
            binds={ModelBase: endi_payment_engine, DBBASE: main_bind},
        )

    else:
        # On utilise l'engine sqlalchemy par défaut (celui d'endi)
        # Pas besoin de spécifier le bind qui est le même qu'avant
        endi_payment_engine = DBSESSION.bind

    # Pour que le create_all fonctionne on doit importer les modèles
    from endi_payment.models import EndiPaymentHistory  # NOQA
    ModelBase.metadata.bind = endi_payment_engine
    ModelBase.metadata.create_all(endi_payment_engine)
    return True
