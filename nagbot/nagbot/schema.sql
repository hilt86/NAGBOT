drop table if exists elasticsearch_servers;
create table servers (
  id integer primary key autoincrement,
  hostname text not null,
  port integer not null
);