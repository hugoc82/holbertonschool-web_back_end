const assert = require("assert");
const calculateNumber = require("./0-calcul");

describe("calculateNumber", () => {
  it("addition de 1 et 3", () => {
    assert.strictEqual(calculateNumber(1, 3), 4);
  });

  it("arrondi 3.7 vers le haut", () => {
    assert.strictEqual(calculateNumber(1, 3.7), 5);
  });

  it("arrondi mixte (1.2 et 3.7)", () => {
    assert.strictEqual(calculateNumber(1.2, 3.7), 5);
  });

  it("arrondi de 1.5 vers le haut", () => {
    assert.strictEqual(calculateNumber(1.5, 3.7), 6);
  });

  it("nombres négatifs", () => {
    assert.strictEqual(calculateNumber(-1.4, 2.6), 2);
    assert.strictEqual(calculateNumber(-1.5, 2.5), 2);
  });
});
