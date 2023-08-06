def includeme(config):
    settings = config.get_settings()
    key = "endi_payment.interfaces.IPaymentRecordHistoryService"
    if key in settings and \
            settings[key] == "endi_payment.history.HistoryDBService":
        config.include(".history")

    key = "endi_payment.interfaces.IPaymentArchiveService"
    if key in settings and \
            settings[key] == "endi_payment.archive.FileArchiveService":
        config.include('.archive')
