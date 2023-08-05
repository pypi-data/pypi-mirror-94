mailru-parser
==========

Class for getting snippets from mail.ru html


```
from mailru_parser import MailRuParser

snippets = MailRuParser("<html><body>...</body></html>").get_snippets()

Testing

python -m unittest mailru_parser.tests.test_mailru

```
