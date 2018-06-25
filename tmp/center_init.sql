USE stcok;
DROP TABLE message;
CREATE TABLE message
(
  stock_name     VARCHAR(40),
  stock_id       CHAR(10),
  stock_price    DECIMAL(7, 2),
  continue_trans BOOL          DEFAULT 1,
  up_confine     DECIMAL(4, 2) DEFAULT 0.1,
  down_confine   DECIMAL(4, 2) DEFAULT 0.1,
  PRIMARY KEY (stock_name)
);
INSERT INTO message VALUE ("基金裕阳", "0000500006", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("基金兴华", "0000500008", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("基金安顺", "0000500009", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("基金科瑞", "0000500056", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("基金银丰", "0000500006", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("财通精选", "0000501001", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("长信优选", "0000501003", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("互联医疗", "0000501007", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("互联医C", "0000500068", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("生物科技", "0000501009", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("财通升级", "0000501015", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("券商基金", "0000501016", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("南方原油", "0000501018", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("上50A", "0000501041", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("APPLE", "0000101041", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("HK_TENCENT", "0000101042", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("CMCC", "0000101043", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("BMW", "0000101044", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("浦发银行", "0000600000", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("邯郸钢铁", "0000600001", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("白云机场", "0000600004", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("武钢股份", "0000600005", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("东风汽车", "0000600006", 100, 1, 0.1, 0.1);
INSERT INTO message VALUE ("中国国贸", "0000600007", 100, 1, 0.1, 0.1);