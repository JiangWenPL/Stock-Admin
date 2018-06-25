DROP DATABASE stock;
CREATE DATABASE stock;
USE stock;
CREATE TABLE message
(
  stock_name     VARCHAR(40),
  stock_id       CHAR(30),
  stock_price    DECIMAL(7, 2),
  continue_trans BOOL          DEFAULT 1,
  up_confine     DECIMAL(4, 2) DEFAULT 0.1,
  down_confine   DECIMAL(4, 2) DEFAULT 0.1,
  PRIMARY KEY (stock_name)
);
CREATE TABLE buy
(
  buy_no       INT(11) NOT NULL AUTO_INCREMENT,
  stock_id     CHAR(10),
  stock_name   VARCHAR(40),
  stock_price  DECIMAL(7, 2),
  stock_num    INT(11),
  time         TIMESTAMP        DEFAULT current_timestamp,
  state        ENUM ('1', '2', '3'),
  price        DECIMAL(7, 2),
  complete_num INT(11),
  user_id      INT(11),
  PRIMARY KEY (buy_no),
  FOREIGN KEY (stock_name) REFERENCES message (stock_name)
);
CREATE TABLE sell
(
  sell_no      INT(11) NOT NULL AUTO_INCREMENT,
  stock_id     CHAR(10),
  stock_name   VARCHAR(40),
  stock_price  DECIMAL(7, 2),
  stock_num    INT(11),
  time         TIMESTAMP        DEFAULT current_timestamp,
  state        ENUM ('1', '2', '3'),
  price        DECIMAL(7, 2),
  complete_num INT(11),
  user_id      INT(11),
  PRIMARY KEY (sell_no),
  FOREIGN KEY (stock_name) REFERENCES message (stock_name)
);
CREATE TABLE tran
(
  trans_no        INT(11) NOT NULL AUTO_INCREMENT,
  stock_id        CHAR(10),
  stock_name      VARCHAR(40),
  trans_price     DECIMAL(7, 2),
  trans_stock_num INT(11),
  time            TIMESTAMP        DEFAULT current_timestamp,
  sell_no         INT(11),
  buy_no          INT(11),
  PRIMARY KEY (trans_no),
  FOREIGN KEY (sell_no) REFERENCES sell (sell_no),
  FOREIGN KEY (buy_no) REFERENCES buy (buy_no),
  FOREIGN KEY (stock_name) REFERENCES message (stock_name)
);