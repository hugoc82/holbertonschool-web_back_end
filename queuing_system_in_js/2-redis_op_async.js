import redis from 'redis';
import { promisify } from 'util';

// Client Redis (API callbacks)
const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Promisify de GET
const getAsync = promisify(client.get).bind(client);

// --- Fonctions demandées ---

// SET (garde les callbacks + redis.print)
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

// GET en async/await (via promisify)
async function displaySchoolValue(schoolName) {
  try {
    const value = await getAsync(schoolName);
    console.log(value);
  } catch (err) {
    console.log(err);
  }
}

// --- Exécution demandée ---
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');

