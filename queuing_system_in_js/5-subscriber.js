import redis from 'redis';

const channel = 'holberton school channel';
const sub = redis.createClient();

sub.on('connect', () => {
  console.log('Redis client connected to the server');
});

sub.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

sub.subscribe(channel);

sub.on('message', (_chan, message) => {
  console.log(message);
  if (message === 'KILL_SERVER') {
    sub.unsubscribe(channel);
    sub.quit();
  }
});

