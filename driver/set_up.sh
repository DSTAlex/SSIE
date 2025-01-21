

scp -P 2222 -r $(dirname $0)/session1 trainee@127.0.0.1:/home/trainee/
scp -P 2222 -r $(dirname $0)/session2 trainee@127.0.0.1:/home/trainee/
scp -P 2222 -r $(dirname $0)/session3 trainee@127.0.0.1:/home/trainee/
#ssh trainee@localhost -p 2222 