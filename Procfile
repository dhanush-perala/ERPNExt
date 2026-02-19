redis_cache: redis-server --port 13002
redis_queue: redis-server --port 12002
redis_socketio: redis-server --port 11002
web: bench serve --port 8000
socketio: /usr/bin/node apps/frappe/socketio.js
watch: bench watch
schedule: bench schedule
worker_short: bench worker --queue short
worker_long: bench worker --queue long
worker_default: bench worker --queue default

