# Create MySQL using Docker
Run this command to change MySQL root password
Get generated root password
```bash
docker logs mysql 2>&1 | grep GENERATED
```

Login into MySQL
```bash
docker exec -it mysql mysql -uroot -p
```

Change root password
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
```