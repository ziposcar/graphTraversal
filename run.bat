rem start cmd /k "d: &&cd d:\software\nginx &&nginx"
rem start cmd /k "mysqld"
rem start cmd /k "c: &&cd ""C:\Program Files\Redis\"" &&redis-server.exe redis.windows.conf"
rem start cmd /k "d: &&cd d:\tools\xxfpm &&call run"
d:
cd d:\WandS\Graduation_Project\graphTraversal-submit\
chcp 65001
call env\Scripts\activate
cd handle
python main.py
