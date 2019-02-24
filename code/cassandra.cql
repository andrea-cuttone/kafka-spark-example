CREATE KEYSPACE myks
  WITH REPLICATION = { 
   'class' : 'SimpleStrategy', 
   'replication_factor' : 1 
  };

DROP TABLE myks.test;
CREATE TABLE myks.test (
  timestamp bigint,
  word text,
  count int,
  primary key (timestamp, word));