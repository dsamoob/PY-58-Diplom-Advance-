# PY-58-Diplom-Advance-

Нужно создать:
    сообщенство в ВК согласно условиям задачи
    БД на postgress

Необходимо создать фаил config.py и поместить его в корень PY-58-Diplom(Advance)
В созданном файле необходимо указать переменные:
    db_login = 'логин postgres'
    db_password = "Пароль от бд"
    db_name = 'Имя базы данных'
    vk_token_prog = 'ВК токен приложения'
    vk_token_my = 'вк Токен сообщества'


Описание приложения:
Данное приложение реагирует на любой текст написанный в сообщество за исключением текста из списка комманд (указан в переменной 
commands в корневом мейне)

Если пользователь ранее использовал данное приложение, то работа начинается с того места/анкеты, на котором он остановился.

После отправки первого сообщения появится кнопка старт, ее нажатие запускает процесс поиска людей по параметрам
пользователя и добавления их в БД за вычетом пользовательских списков избранного / черных (если таковые были)
По завершению загрузки в бд, в чате вк появится набор кнопок: предыдущая, в черный, в избранное, следующая, черный, 
обновить, избранное.

Предыдущая/следующая - перемещают пользователя между анкетами по круговой без учета добавленных в черный или список избранных,
для того, чтобы при перемещении учлись списки пользователя, и скорректировался поиск - нужно нажать обновить(перезагрузит
поисковый список в бд). 
Соответственно, кнопки в черный / в избранное добавлют текущую анкету в тот или иной список. 
При нажатии кнпок "Черный список" или "Список избранных" - отправляет пользователю список перебирая его циклом,
в каждом сообщении фиксируется кнопка "удалить" и при нажатии удаляет анкету из списка.

Что не проработано:
    -Одну и ту-же анкету можно добавить в список избранных и в черный список. Решить это можно посредством написания функции,
которая будет удалять анкету из одного списка и перемещать в другой, или выдавать невозможность такого действия сообщением
"Данная анкета уже добавлена в список", или просто перезаписывать.
    -В случае отсутствия у пользователя информации по городу/возрасту/полу или иным пунктам - не выдает запрос с уточнением.
    -Нет завершения работы.
    
