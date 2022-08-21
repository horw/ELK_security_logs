# ELK_security_logs
>Предоставлены 2 файла:
>Журнал windows security и лог proxy

Необходимо:\
	* [Развернуть ELK стек](#Развертывание-ELK)\
	* [Переслать лог в стек elk](#Переслать-лог-в-стек-elk)\
	* [Реализовать парсинг событий](#Реализовать-парсинг-событий)\
	* [Обогатить событие сетевого подключения url адресом из лога proxy](#Обогатить-событие-сетевого-подключения-url-адресом-из-лога-proxy)\
	* [Составить запрос для поиска цепочки событий от запроса url до аутентификации пользователя на хосте](#Составить-запрос-для-поиска-цепочки-событий-от-запроса-url-до-аутентификации-пользователя-на-хосте)
	
Результат оформить в виде отчета

## Развертывание ELK
> **Note**
> Для этого воспользуемся готовой сборкой:\
> https://github.com/deviantony/docker-elk\
Распакуем файлы и  с помошью команды:\

```docker-compose up```
После загрузки дополнительных пакетов, запуститься ELK\
> Для того чтобы отключить аунтификация в config файле: docker-elk-main/elasticsearch/config/elasticsearch.yml изменим значение xpack.security.enabled на false (```xpack.security.enabled: false```)


## Переслать лог в стек elk 
> Воспользуемся winlogbeat

[Установочный фаил winlogbeat](https://www.elastic.co/downloads/beats/winlogbeat)

После того как установили файл с winlogbeat, необходимо обносить его config файл (В данном случае передача данных идет непосредственно elasticsearch, не через logstash)
[Пример config файла](https://www.elastic.co/guide/en/beats/winlogbeat/current/reading-from-evtx.html)

```
winlogbeat.event_logs:
  - name: ${EVTX_FILE} 
    no_more_events: stop 

winlogbeat.shutdown_timeout: 30s 
winlogbeat.registry_file: evtx-monitor.yml 

output.elasticsearch.hosts: ['http://localhost:9200']

output.elasticsearch.index: "security-%{[agent.version]}"
setup.template.name: "security"
setup.template.pattern: "security-%{[agent.version]}"
```

После необходимо открыть консоль и воспользоваться следуещей коммандой\
```.\winlogbeat\winlogbeat.exe -e -c .\winlogbeat\winlogbeat-evtx.yml -E EVTX_FILE=(Полный путь к Security.evtx)```\
Пример: ```.\winlogbeat\winlogbeat.exe -e -c .\winlogbeat\winlogbeat-evtx.yml -E EVTX_FILE=C:/Security.evtx```

После успешной загрузки данных в консоли [Kibana](http://localhost:5601/app/dev_tools#/console) можно проверить правильность данных.
![image](https://user-images.githubusercontent.com/47724762/185793795-c278e2e6-e6c0-44d3-b7f6-776a0c617463.png)

## Реализовать парсинг событий
> Реализация с помощью Regular expression

> ** Note **
> Proxy log файл представляет собой строки определенного вида.

Нас интересуют данные относящиеся к destination и source, поэтому re строка будет иметь следующий вид:
```r'dst=(.*?) dhost=(.*?) suser=(.*?) src=(.*?) sport=(.*?) tierep=(.*?) in=(.*?) out=(.*?) requestMethod=(.*?) request=(.*?) '```

## Обогатить событие сетевого подключения url адресом из лога proxy 
> Реализация с помощью elasticsearch's update_by_query
update_by_query позволяет нам изменять данные, которые мы получили из запроса(query). Преимущества данного метода: лаконичность его написания, во всех других вариантах неоходимо сначало обновить/создать \_mapping nested field 

1.![image](https://user-images.githubusercontent.com/47724762/185794271-b7cb40d3-c766-42ca-b4d3-bed3aa85ce52.png)
2.![image](https://user-images.githubusercontent.com/47724762/185794286-8a30f87a-d237-4482-a747-a493a414d82a.png)

## Составить запрос для поиска цепочки событий от запроса url до аутентификации пользователя на хосте 
> Реализация с помощью \_search запросов для нахождения стартового времени - Logon и конечного времени запроса - URL

Необходимо найти все логи произошедшие в интервале времени аутентификации пользователя на хосте и запроса некого url.

Запрос для нахождения времени Logon
![image](https://user-images.githubusercontent.com/47724762/185794647-333fcba0-70b4-4da0-83e4-8f4bd409d876.png)

Запрос для находжения времени, когда просходил запрос к заданой URL
![image](https://user-images.githubusercontent.com/47724762/185794751-9a5a1714-d143-4b70-bde0-a2fc5932b86d.png)

Итоговый запрос для нахождения событий в промежутке времени
![image](https://user-images.githubusercontent.com/47724762/185794896-74756323-ba8f-4b7b-9f90-d0e75e24d09a.png)

 
