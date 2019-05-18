start cmd /k "d: &&cd d:\software\nginx &&nginx"
start cmd /k "mysqld"
rem start cmd /k "c: &&cd ""C:\Program Files\Redis\"" &&redis-server.exe redis.windows.conf"
start cmd /k "d: &&cd d:\tools\xxfpm &&call run"
cd d:\WandS\Graduation_Project\graphTraversal-submit\
chcp 65001
call env\Scripts\activate
cd handle
python main.py
