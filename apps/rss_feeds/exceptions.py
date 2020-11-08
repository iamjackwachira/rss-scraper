from django.utils.translation import ugettext as _


class RssFeedUpdateError(Exception):
    """
    Exception thrown when an error
    occurs during a feed update.
    """

    def __init__(self, msg=None):
        if not msg:
            self.msg = _("RSS feed update failed.")
        super().__init__(msg)
