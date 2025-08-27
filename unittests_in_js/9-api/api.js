const express = require("express");

const app = express();

app.get("/", (req, res) => {
  res.send("Welcome to the payment system");
});

// :id doit être uniquement numérique -> regex \d+
app.get("/cart/:id(\\d+)", (req, res) => {
  const { id } = req.params;
  res.send(`Payment methods for cart ${id}`);
});

const PORT = 7865;
app.listen(PORT, () => {
  console.log(`API available on localhost port ${PORT}`);
});

module.exports = app;
