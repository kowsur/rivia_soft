'''
This module contains dummy classes to simulate that the classes actually exists.
This is to avoid getting errors while migrating database.
'''
# .fields.py
class Select:
        def __init__(self, *args, **kwargs):
                pass
class SearchableModelField:
        def __init__(self, *args, **kwargs) -> None:
                pass

# .forms.py
class InvoiceCreationForm:
        def __init__(self, *args, **kwargs) -> None:
                pass

class InvoiceChangeForm:
        def __init__(self, *args, **kwargs) -> None:
                pass

class InvoiceDeleteForm:
        def __init__(self, *args, **kwargs) -> None:
                pass


class InvoiceItemCreationForm:
        def __init__(self, *args, **kwargs) -> None:
                pass

class InvoiceItemChangeForm:
        def __init__(self, *args, **kwargs) -> None:
                pass

class InvoiceItemDeleteForm:
        def __init__(self, *args, **kwargs) -> None:
                pass

class TransactionCreationForm:
        def __init__(self, *args, **kwargs) -> None:
                pass


class TransactionChangeForm:
        def __init__(self, *args, **kwargs) -> None:
                pass

class TransactionDeleteForm:
        def __init__(self, *args, **kwargs) -> None:
                pass