## Тестовое задание
Выполнено тестовое задание в соответсвии со спецификацией: https://github.com/fedorovpv/testing . Автотест проверяет корректность списания денежных средств с баланса клиента при подключении ему услуги. 
Ошибка возникает по причине того, что при активации сервиса появляется разница между базой данных в папке web, которую проверяем, 
и базой данных в запущенном контейнере, которую изменяет тестируемое приложение. Ошибка является ошибкой окружения. Необходимо добиться проверки одного и того же экземпляра БД.


### Реализация
Тест реализован на Robot Framework с использованием библиотек для работы с БД и API.
Эти библиотеки были созданы на Python 2.7 также в рамках выполнения тестового задания.
В тесте реализована следущая логика проверки:
1. Из БД выбирается тестовый клиент, удовлетворяющий требованиям (положительный баланс). 
2. Если такой клиент не находится, создается новый клиент со случайным именем из 6-ти символов и балансом, равным 5.
3. С помощью API список подключенных клиенту сервисов.
4. Так же с помощью API получаем список всех сервисов.
5. Получаем список доступных для подключения клиенту сервисов.
При неоднократном прогоне тестов может сложиться ситуация, что у всех клиентов не будет доступных сервисов. 
Таким образом тест будет провален до проверки целевого бага. 
Варианты решения проблемы: 
      - Доработать выборку из базы подходящего клиента, учитывая, есть ли еще доступные для него сервисы.
      - Создавать нового клиента с заведомо пустым пулом сервисов для дальнейшего их подключения, и удалять его после завершения тестов.
6. Поключается услуга, происходит проверка ответа сервера.
7. Выполняется ожидание и проверка появления нового сервиса в подключенных клиенту.
Максимальное время ожидания - 1 митута. Иначе тест провален.
8. Выполняется сравнение {конечный баланс} = {начальный баланс} - {стоимость подключения услуги}
При несовпадении результатов - тест провален.

### Запуск
Запустить Docker:
Из корневой директории репозитория выполнить:
  - `cd app`
  - `docker-compose build`
  - `docker-compose up`
  
Запустить автотест:
Из корневой директории репозитория выполнить:
  - `robot -d test/test_result CheckServiceActivate.robot`




