import redis from 'redis';

// Création du client Redis
const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// --- Stockage du hash ---
const key = 'HolbertonSchools';

client.hset(key, 'Portland', 50, redis.print);
client.hset(key, 'Seattle', 80, redis.print);
client.hset(key, 'New York', 20, redis.print);
client.hset(key, 'Bogota', 20, redis.print);
client.hset(key, 'Cali', 40, redis.print);
client.hset(key, 'Paris', 2, redis.print);

// --- Affichage du hash ---
client.hgetall(key, (err, value) => {
  if (err) {
    console.log(err);
  } else {
    console.log(value);
  }
});

