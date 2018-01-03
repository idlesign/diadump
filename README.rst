diadump
=======
https://github.com/idlesign/diadump

|release| |lic|

.. |release| image:: https://img.shields.io/pypi/v/diadump.svg
    :target: https://pypi.python.org/pypi/diadump

.. |lic| image:: https://img.shields.io/pypi/l/diadump.svg
    :target: https://pypi.python.org/pypi/diadump


Описание
--------

*Скачиватель диафильмов*

Позволяет скачать оцифрованные изображения диафильмов с замечательного сайта *http://diafilmy.su*
для последующего локального просмотра.

.. code-block:: bash

    ; Скачиваем все диафильмы раздела "Сказки" в поддиректорию директории dia
    $ diadump many http://diafilmy.su/diafilmy/skazki/ /home/idle/dia/

    ; Скачиваем только один диафильм - "Огниво"
    $ diadump one http://diafilmy.su/5180-ognivo.html /home/idle/dia/


Установка
---------

Приложение требует для работы **Python 3**.

Чтобы установить приложение для Python 3 в операционной системе часто существует отдальная команда **pip3**,
ею и воспользуемся:

.. code-block:: bash

    $ sudo pip3 install diadump


После установки можно выполнять команду **diadump**, как показано в описании выше.
