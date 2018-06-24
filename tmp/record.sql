DROP DATABASE stock;
CREATE DATABASE stock;
USE stock;
CREATE TABLE buy
(
  buy_no       INT(11) NOT NULL AUTO_INCREMENT,
  stock_name   VARCHAR(40),
  stock_price  DECIMAL(7, 2),
  stock_num    INT(11),
  time         TIMESTAMP        DEFAULT current_timestamp,
  state        ENUM ('1', '2', '3'),
  price        DECIMAL(7, 2),
  complete_num INT(11),
  PRIMARY KEY (buy_no)
);
CREATE TABLE sell
(
  sell_no      INT(11) NOT NULL AUTO_INCREMENT,
  stock_name   VARCHAR(40),
  stock_price  DECIMAL(7, 2),
  stock_num    INT(11),
  time         TIMESTAMP        DEFAULT current_timestamp,
  state        ENUM ('1', '2', '3'),
  price        DECIMAL(7, 2),
  complete_num INT(11),
  PRIMARY KEY (sell_no)
);
CREATE TABLE tran
(
  trans_no        INT(11) NOT NULL AUTO_INCREMENT,
  stock_name      VARCHAR(40),
  trans_price     DECIMAL(7, 2),
  trans_stock_num INT(11),
  time            TIMESTAMP        DEFAULT current_timestamp,
  sell_no         INT(11),
  buy_no          INT(11),
  PRIMARY KEY (trans_no),
  FOREIGN KEY (sell_no) REFERENCES sell (sell_no),
  FOREIGN KEY (buy_no) REFERENCES buy (buy_no)
);