import datetime
import colander
import logging
from sqlalchemy import extract

from endi.views import BaseListView
from endi_payment.models import (
    EndiPaymentHistory,
    EndiPaymentArchiveSeal,
)
from endi.utils.widgets import Link, ButtonLink
from endi.models.task import Invoice, Payment

from endi_payment.interfaces import IPaymentArchiveService
from .forms import get_list_schema
from .routes import (
    ENDI_PAYMENT_HISTORY,
    ENDI_PAYMENT_HISTORY_ITEM,
    ENDI_PAYMENT_HISTORY_ITEM_ARCHIVE,
)


logger = logging.getLogger(__name__)


ACTION_LABELS = {
    'ADD': 'Ajout', 'UPDATE': 'Modification', 'DELETE': 'Suppression'
}


class HistoryListView(BaseListView):
    title = "Journal des modifications sur les encaissements"
    add_template_vars = (
        'title',
        'action_labels',
        'stream_actions',
        "archive_item_panel",
    )
    schema = get_list_schema()
    default_sort = "created_at"
    default_direction = "desc"
    sort_columns = {
        'created_at': 'created_at',
        'user_login': 'user_login',
        'action_type': 'action_type',
        'tva_value': 'tva_value',
        'amount': 'amount',
    }

    null_values = (colander.null, None, '')
    action_labels = ACTION_LABELS

    def __init__(self, *args, **kwargs):
        BaseListView.__init__(self, *args, **kwargs)
        self.archive_service = self.request.find_service(
            IPaymentArchiveService
        )
        self.archive_item_panel = self.archive_service.get_ui_list_plugin()

    def query(self):
        return self.dbsession.query(EndiPaymentHistory).outerjoin(
            EndiPaymentArchiveSeal
        )

    def filter_created_at(self, query, appstruct):
        period = appstruct.get('period', {})
        if period.get('start') not in self.null_values:
            logger.debug("  + Filtering by date : %s" % period)
            start = period.get('start')
            end = period.get('end')
            if end not in self.null_values:
                end = datetime.date.today()
            query = query.filter(
                EndiPaymentHistory.created_at.between(start, end)
            )
        else:
            year = appstruct.get('year')
            if year not in self.null_values:
                query = query.filter(
                    extract('year', EndiPaymentHistory.created_at) == year
                )
        return query

    def filter_amount(self, query, appstruct):
        amounts = appstruct.get('amount', {})
        if amounts.get('start') not in self.null_values:
            logger.debug("Filtering by amount : %s" % amounts)
            start = amounts.get('start')
            end = amounts.get('end')
            if end in self.null_values:
                query = query.filter(EndiPaymentHistory.amount >= start)
            else:
                query = query.filter(
                    EndiPaymentHistory.amount.between(start, end)
                )
        return query

    def filter_action_type(self, query, appstruct):
        action_type = appstruct.get('action_type')
        if action_type not in self.null_values:
            query = query.filter(EndiPaymentHistory.action_type == action_type)
        return query

    def filter_invoice_id(self, query, appstruct):
        invoice_id = appstruct.get('invoice_id')
        if invoice_id:
            logger.debug("Filtering by invoice_id {}".format(invoice_id))
            query = query.filter(EndiPaymentHistory.invoice_id == invoice_id)
        return query

    def filter_invoice_number(self, query, appstruct):
        invoice_number = appstruct.get('official_number')
        if invoice_number:
            invoice_id = self.dbsession.query(Invoice.id).filter(
                Invoice.official_number == invoice_number
            ).scalar()

            logger.debug(
                "Filtering by invoice_id {} (number {})".format(
                    invoice_id, invoice_number
                )
            )
            query = query.filter(EndiPaymentHistory.invoice_id == invoice_id)
        return query

    def stream_actions(self, item):
        yield Link(
            self.request.route_path(ENDI_PAYMENT_HISTORY_ITEM, id=item.id),
            "Voir",
            title="Voir le détail de cette entrée",
            icon="arrow-right"
        )
        seal = item.endi_payment_archive_seal
        for action in self.archive_service.stream_list_actions(seal):
            yield action


def history_item_view(request):
    """
    EndiPaymentHistory item view
    """
    logger.debug("endi_payment.EndiPaymentHistory view")
    history_id = request.matchdict['id']
    history = request.dbsession.query(EndiPaymentHistory).get(history_id)
    request.actionmenu.add(
        ButtonLink('Journal des modifications', ENDI_PAYMENT_HISTORY)
    )
    archive_service = request.find_service(IPaymentArchiveService)
    archive_seal = archive_service.find(history)

    panels = archive_service.get_ui_plugins()

    return dict(
        title="Vue détaillée d'une entrée du journal de modification des "
        "encaissements",
        history=history,
        payment=Payment.get(history.payment_id),
        invoice=Invoice.get(history.invoice_id),
        action_labels=ACTION_LABELS,
        archive=archive_seal,
        panels=panels
    )


def includeme(config):
    config.include('.routes')

    config.add_view(
        HistoryListView,
        route_name=ENDI_PAYMENT_HISTORY,
        permission='admin_treasury',
        renderer="endi_payment:views/templates/histories.mako"
    )
    config.add_view(
        history_item_view,
        route_name=ENDI_PAYMENT_HISTORY_ITEM,
        permission="admin_treasury",
        renderer="endi_payment:views/templates/history.mako"
    )

    config.add_admin_menu(
        parent="accounting",
        permission="admin_treasury",
        label="Journaux des encaissements",
        href=ENDI_PAYMENT_HISTORY,
    )
