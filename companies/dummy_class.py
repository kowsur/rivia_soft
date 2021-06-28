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
class SelfassesmentCreationForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class SelfassesmentChangeForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class SelfassesmentDeleteForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class SelfassesmentAccountSubmissionCreationForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class SelfassesmentAccountSubmissionChangeForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class SelfassesmentAccountSubmissionDeleteForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class Add_All_Selfassesment_to_SelfassesmentAccountSubmission_Form:
        def __init__(self, *args, **kwargs) -> None:
                pass
class SelfassesmentTrackerCreationForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class SelfassesmentTrackerChangeForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class SelfassesmentTrackerDeleteForm:
        def __init__(self, *args, **kwargs) -> None:
                pass

class LimitedCreationForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class LimitedChangeForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class LimitedDeleteForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class LimitedTrackerCreationForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class LimitedTrackerChangeForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class LimitedTrackerDeleteForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class LimitedSubmissionDeadlineTrackerCreationForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class LimitedSubmissionDeadlineTrackerChangeForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
class LimitedSubmissionDeadlineTrackerDeleteForm:
        def __init__(self, *args, **kwargs) -> None:
                pass
