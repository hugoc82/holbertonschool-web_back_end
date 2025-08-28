import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

// === Data ===
const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

// === Utils ===
function getItemById(id) {
  return listProducts.find((item) => item.itemId === id);
}

// === Redis client ===
const client = redis.createClient();
client.on('connect', () => console.log('Redis client connected to the server'));
client.on('error', (err) =>
  console.log(`Redis client not connected to the server: ${err}`)
);

const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

async function reserveStockById(itemId, stock) {
  await setAsync(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
  const value = await getAsync(`item.${itemId}`);
  return value ? parseInt(value, 10) : null;
}

// === Express app ===
const app = express();
const PORT = 1245;

// Route: GET /list_products
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Route: GET /list_products/:itemId
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);

  if (!item) {
    return res.json({ status: 'Product not found' });
  }

  const reserved = await getCurrentReservedStockById(itemId);
  const currentQuantity =
    reserved !== null ? item.initialAvailableQuantity - reserved : item.initialAvailableQuantity;

  res.json({ ...item, currentQuantity });
});

// Route: GET /reserve_product/:itemId
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const item = getItemById(itemId);

  if (!item) {
    return res.json({ status: 'Product not found' });
  }

  const reserved = await getCurrentReservedStockById(itemId);
  const currentQuantity =
    reserved !== null ? item.initialAvailableQuantity - reserved : item.initialAvailableQuantity;

  if (currentQuantity <= 0) {
    return res.json({ status: 'Not enough stock available', itemId });
  }

  await reserveStockById(itemId, (reserved || 0) + 1);
  res.json({ status: 'Reservation confirmed', itemId });
});

// Start server
app.listen(PORT, () => {
  console.log(`API available on localhost port ${PORT}`);
});

