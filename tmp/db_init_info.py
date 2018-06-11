f = open ( 'tmp/db_init.json', 'w' )
import json

init_dict = {}
init_dict['admin'] = [('Alice', 'a'), ('Bob', 'b'), ('Curry', 'c'), ('王二狗', 'w'), ('李三蛋', 'l'), ('陈鸿宇', 'c')]
init_dict['buy'] = [("HK_TENCENT", 10.2, 100), ("APPLE", 1.2, 24), ("APPLE", 1.2, 24), ("BMW", 1.2, 24),
                    ("爱康科技", 2.3, 30000), ("恒大高新", 120, 24), ("永安行", 52.44, 668), ("CMCC", 10, 10)]
init_dict['sell'] = [("APPLE", 1.2, 24), ("APPLE", 1.2, 24), ("BMW", 1.2, 24), ("爱康科技", 2.3, 30000), ("恒大高新", 120, 24),
                     ("永安行", 52.44, 668), ("CMCC", 10, 10)]
init_dict['tran'] = [("APPLE", 1.2, 24), ("BMW", 1.2, 24), ("爱康科技", 2.3, 30000), ("恒大高新", 120, 24), ("电工合金", 12.2, 260)]
s = json.dumps ( init_dict, indent=4, separators=(',', ': ') )
f.write ( s )
2120
f.close ()
