CREATE TABLE buy (
  buy_no      INT(11) NOT NULL AUTO_INCREMENT,
  stock_name  VARCHAR(40),
  stock_price DECIMAL(7, 2),
  stock_num   INT(11),
  time        TIMESTAMP        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (buy_no)
);
CREATE TABLE sell (
  sell_no     INT(11) NOT NULL AUTO_INCREMENT,
  stock_name  VARCHAR(40),
  stock_price DECIMAL(7, 2),
  stock_num   INT(11),
  time        TIMESTAMP        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (sell_no)
);
CREATE TABLE tran (
  trans_no        INT(11) NOT NULL  AUTO_INCREMENT,
  stock_name      CHAR(11),
  trans_price     DECIMAL(7, 2),
  trans_stock_num INT(11),
  time            TIMESTAMP         DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (trans_no)
);