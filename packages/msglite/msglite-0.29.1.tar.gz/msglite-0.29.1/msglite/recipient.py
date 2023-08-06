import logging

from msglite import constants
from msglite.properties import Properties
from msglite.utils import format_party, join_path

log = logging.getLogger(__name__)


class Recipient(object):
    """Contains one of the recipients in an msg file."""

    def __init__(self, msg, dir_):
        self.dir = dir_
        stream = msg._getStream(join_path(dir_, "__properties_version1.0"))
        self.props = Properties(stream, constants.TYPE_RECIPIENT)
        self.email = msg._getStringStream(join_path(dir_, "__substg1.0_39FE"))
        if not self.email:
            self.email = msg._getStringStream(join_path(dir_, "__substg1.0_3003"))
        self.name = msg._getStringStream(join_path(dir_, "__substg1.0_3001"))
        self.type = self.props.get("0C150003").value
        self.formatted = format_party(self.email, self.name)

    def __repr__(self):
        return "<Recipient(%s)>" % self.formatted
