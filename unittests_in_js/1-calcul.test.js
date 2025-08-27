const assert = require("assert");
const calculateNumber = require("./1-calcul");

describe("calculateNumber", () => {
  describe("type = SUM", () => {
    it("somme simple avec entiers", () => {
      assert.strictEqual(calculateNumber("SUM", 1, 3), 4);
    });

    it("somme avec arrondis", () => {
      assert.strictEqual(calculateNumber("SUM", 1.4, 4.5), 6); // 1 + 5
      assert.strictEqual(calculateNumber("SUM", 1.6, 3.3), 5); // 2 + 3
    });

    it("somme avec négatifs", () => {
      assert.strictEqual(calculateNumber("SUM", -1.4, -3.6), -5); // -1 + -4
    });
  });

  describe("type = SUBTRACT", () => {
    it("soustraction simple", () => {
      assert.strictEqual(calculateNumber("SUBTRACT", 5, 3), 2);
    });

    it("soustraction avec arrondis", () => {
      assert.strictEqual(calculateNumber("SUBTRACT", 1.4, 4.5), -4); // 1 - 5
      assert.strictEqual(calculateNumber("SUBTRACT", 1.6, 3.3), -1); // 2 - 3
    });

    it("soustraction avec négatifs", () => {
      assert.strictEqual(calculateNumber("SUBTRACT", -1.4, -3.6), 3); // -1 - (-4)
    });
  });

  describe("type = DIVIDE", () => {
    it("division simple", () => {
      assert.strictEqual(calculateNumber("DIVIDE", 10, 2), 5);
    });

    it("division avec arrondis", () => {
      assert.strictEqual(calculateNumber("DIVIDE", 1.4, 4.5), 0.2); // 1 / 5
      assert.strictEqual(
        calculateNumber("DIVIDE", 1.6, 3.3),
        0.6666666666666666
      ); // 2 / 3
    });

    it("division par zéro arrondi → Error", () => {
      assert.strictEqual(calculateNumber("DIVIDE", 1.4, 0), "Error"); // 1 / 0
      assert.strictEqual(calculateNumber("DIVIDE", 1.4, 0.2), "Error"); // 1 / 0
    });

    it("division avec négatifs", () => {
      assert.strictEqual(calculateNumber("DIVIDE", -1.4, 4.5), -0.2); // -1 / 5
      assert.strictEqual(
        calculateNumber("DIVIDE", -1.6, -3.3),
        0.6666666666666666
      ); // -2 / -3
    });
  });

  describe("cas invalides", () => {
    it("doit lever une erreur si type invalide", () => {
      assert.throws(() => calculateNumber("MULTIPLY", 1, 2), /Invalid type/);
    });
  });
});
