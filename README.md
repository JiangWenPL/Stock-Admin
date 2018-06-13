# Stock administrator

## Requirement:
- Sqlite and MySQL(8.0 preferred)
- Anaconda

## Setup:

- Install required python package.
    ```bash
    conda create -f environments.yml
    conda activate se
    ```
- Configure MySQL location in config.py
    default setting is `username: root password: root`
    ```python
    SQLALCHEMY_BINDS = {
        'record':        'mysql://root:root@localhost/record'
    }
    ```
- Initialize MysQL storage if necessary:
    ```mysql
    CREATE DATABASE record;
    USE record;
    
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
    ```
- Run the server in conda enviroment at this directory:
    ```python
    python run.py
    ```
- You are all set.
    