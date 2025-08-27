const express = require("express");

const app = express();

// pour parser le JSON du body (POST /login)
app.use(express.json());

app.get("/", (req, res) => {
  res.send("Welcome to the payment system");
});

// Route validée par regex : uniquement chiffres
app.get("/cart/:id(\\d+)", (req, res) => {
  const { id } = req.params;
  res.send(`Payment methods for cart ${id}`);
});

// Nouveau: GET /available_payments
app.get("/available_payments", (req, res) => {
  res.json({
    payment_methods: {
      credit_cards: true,
      paypal: false,
    },
  });
});

// Nouveau: POST /login
// Attend un JSON { "userName": "<nom>" }
app.post("/login", (req, res) => {
  const { userName } = req.body || {};
  res.send(`Welcome ${userName}`);
});

const PORT = 7865;
app.listen(PORT, () => {
  console.log(`API available on localhost port ${PORT}`);
});

module.exports = app;
