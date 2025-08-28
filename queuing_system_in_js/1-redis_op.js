import redis from 'redis';

// Création du client Redis
const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// --- Fonctions demandées ---

// 1) Ajouter une nouvelle école (SET)
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print); // redis.print affiche "Reply: OK"
}

// 2) Afficher la valeur d’une école (GET)
function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, reply) => {
    if (err) {
      console.log(err);
    } else {
      console.log(reply);
    }
  });
}

// --- Exécution demandée ---
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');

