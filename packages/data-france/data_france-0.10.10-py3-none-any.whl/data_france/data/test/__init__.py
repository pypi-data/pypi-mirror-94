from django.db import transaction


def importer_donnees_test(using=None):
    auto_commit = transaction.get_autocommit(using=using)
    if not auto_commit:
        transaction.set_autocommit(True, using=using)

    try:
        with transaction.atomic():
            pass
    finally:
        if not auto_commit:
            transaction.set_autocommit(False, using=using)
