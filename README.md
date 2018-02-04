爬取蜻蜓fm的电台信息
播放链接： http://lhttp.qingting.fm/live/+电台编号+/64k.mp3
分类api： http://rapi.qingting.fm/categories?type=channel 
分类底下电台的api： http://rapi.qingting.fm/categories/433/channels?with_total=true&page=1&pagesize=50
认证
```
db.createUser({ user: 'lx0hacker', pwd: 'qwe123', roles: [ { role: 'userAdminAnyDatabase', db: 'admin' } ]});
docker exec -it mongo mongo -u lx0hacker -p qwe123 --authenticationDatabase admin
```
创建用户：
```
use databasename
db.createUser({user:"qtfm",pwd:"qwe123",roles:[{"role":"readWrite","db":"qingtingfm"}]})
```
python操作：
https://api.mongodb.com/python/current/  
