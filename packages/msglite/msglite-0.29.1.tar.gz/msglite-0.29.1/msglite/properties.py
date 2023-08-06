import logging

from msglite import constants
from msglite.prop import create_prop
from msglite.utils import divide, fromTimeStamp, msgEpoch

log = logging.getLogger(__name__)


class Properties(object):
    """Parser for msg properties files."""

    def __init__(self, stream, type=None, skip=None):
        self.stream = stream
        self.props = {}
        self.__naid = None
        self.__nrid = None
        self.__ac = None
        self.__rc = None
        if type is not None:
            if type == constants.TYPE_MESSAGE:
                skip = 32
                self.__naid, self.__nrid, self.__ac, self.__rc = constants.ST1.unpack(
                    self.stream[:24]
                )
            elif type == constants.TYPE_MESSAGE_EMBED:
                skip = 24
                self.__naid, self.__nrid, self.__ac, self.__rc = constants.ST1.unpack(
                    self.stream[:24]
                )
            else:
                skip = 8
        else:
            if skip is None:
                # This section of the skip handling is not very good.
                # While it does work, it is likely to create extra
                # properties that are created from the properties file's
                # header data. While that won't actually mess anything
                # up, it is far from ideal. Basically, this is the dumb
                # skip length calculation. Preferably, we want the type
                # to have been specified so all of the additional fields
                # will have been filled out
                skip = len(stream) % 16
                if skip == 0:
                    skip = 32
        streams = divide(self.stream[skip:], 16)
        for st in streams:
            a = create_prop(st)
            self.props[a.name] = a

    def get(self, name):
        """
        Retrieve the property of :param name:.
        """
        try:
            return self.props[name]
        except KeyError:
            return None

    def items(self):
        return self.props.items()

    def keys(self):
        return self.props.keys()

    def values(self):
        return self.props.values()

    def __contains__(self, key):
        return key in self.props

    def __getitem__(self, key):
        return self.props.__getitem__(key)

    def __iter__(self):
        return iter(self.props)

    def __len__(self):
        return len(self.props)

    def __repr__(self):
        return repr(self.props)

    @property
    def attachment_count(self):
        if self.__ac is None:
            raise TypeError(
                "Properties instance must be intelligent and of type TYPE_MESSAGE to get attachment count."
            )
        return self.__ac

    @property
    def date(self):
        """
        Returns the send date contained in the Properties file.
        """
        try:
            return self.__date
        except AttributeError:
            if "00390040" in self:
                self.__date = fromTimeStamp(
                    msgEpoch(self.get("00390040").value)
                ).__format__("%a, %d %b %Y %H:%M:%S %z")
            elif "30080040" in self:
                self.__date = fromTimeStamp(
                    msgEpoch(self.get("30080040").value)
                ).__format__("%a, %d %b %Y %H:%M:%S %z")
            elif "30070040" in self:
                self.__date = fromTimeStamp(
                    msgEpoch(self.get("30070040").value)
                ).__format__("%a, %d %b %Y %H:%M:%S %z")
            else:
                log.warning("Error retrieving date.")
                self.__date = None
            return self.__date

    @property
    def next_attachment_id(self):
        if self.__naid is None:
            raise TypeError(
                "Properties instance must be intelligent and of type TYPE_MESSAGE to get next attachment id."
            )
        return self.__naid

    @property
    def next_recipient_id(self):
        if self.__nrid is None:
            raise TypeError(
                "Properties instance must be intelligent and of type TYPE_MESSAGE to get next recipient id."
            )
        return self.__nrid

    @property
    def recipient_count(self):
        if self.__rc is None:
            raise TypeError(
                "Properties instance must be intelligent and of type TYPE_MESSAGE to get recipient count."
            )
        return self.__rc
