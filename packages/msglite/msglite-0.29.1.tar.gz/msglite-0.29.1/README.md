# msglite

[![Actions Status](https://github.com/alephdata/msglite/workflows/package/badge.svg)](https://github.com/alephdata/msglite/actions)

Extracts emails and attachments saved in Microsoft Outlook's .msg files

The python package extract_msg automates the extraction of key email
data (from, to, cc, date, subject, body) and the email's attachments.

### Usage

You can install the package from PyPI as `msglite`. Then use the API
as follows:

```python
from msglite import Message

msg = Message('path/to/message.msg')
print(msg.subject)
print(msg.to)
# The API currently does not differentiate Sender and From cleanly:
print(msg.sender)
print(msg.body)
```

### Notes on encoding 

Field types:

* 001E - PtypString8 - Non-unicode string
* 001F - PtypString - UTF-18 LE string
* 0102 - PtypBinary - Blob

### Credits

This package is a lightweight and functionally extended fork of [msg-extractor](https://github.com/mattgwwalker/msg-extractor) written by Matthew Walker and Ken Peterson.