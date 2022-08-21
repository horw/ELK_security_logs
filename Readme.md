# ELK_security_logs
>Предоставлены 2 файла:
>Журнал windows security и лог proxy

Необходимо:\
	0. Развернуть ELK стек\
	1. Переслать лог в стек elk\
	2. Реализовать парсинг событий\
	3. Обогатить событие сетевого подключения url адресом из лога proxy\
	4. Составить запрос для поиска цепочки событий от запроса url до аутентификации пользователя на хосте
	
Результат оформить в виде отчета

## Развертывание ELK
> **Note**
> Для этого воспользуемся готовой сборкой:\
> https://github.com/deviantony/docker-elk\
Распакуем файлы и  с помошью команды:\

```docker-compose up```
После загрузки дополнительных пакетов, запуститься ELK\
> Для того чтобы отключить аунтификация в config файле: docker-elk-main/elasticsearch/config/elasticsearch.yml изменим значение xpack.security.enabled на false (```xpack.security.enabled: false```)


## Реализовать парсинг событий - Воспользуемся winlogbeat
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
ex: ```.\winlogbeat\winlogbeat.exe -e -c .\winlogbeat\winlogbeat-evtx.yml -E EVTX_FILE=C:/Security.evtx```


