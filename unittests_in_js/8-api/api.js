const express = require("express");

const app = express();

app.get("/", (req, res) => {
  res.send("Welcome to the payment system");
});

const PORT = 7865;
app.listen(PORT, () => {
  console.log(`API available on localhost port ${PORT}`);
});

// On exporte app si jamais tu veux réutiliser dans d'autres tests
module.exports = app;
