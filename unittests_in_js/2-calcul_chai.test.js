const { expect } = require("chai");
const calculateNumber = require("./2-calcul_chai");

describe("calculateNumber (Chai)", () => {
  describe("type = SUM", () => {
    it("somme simple avec entiers", () => {
      expect(calculateNumber("SUM", 1, 3)).to.equal(4);
    });

    it("somme avec arrondis", () => {
      expect(calculateNumber("SUM", 1.4, 4.5)).to.equal(6); // 1 + 5
      expect(calculateNumber("SUM", 1.6, 3.3)).to.equal(5); // 2 + 3
    });

    it("somme avec négatifs", () => {
      expect(calculateNumber("SUM", -1.4, -3.6)).to.equal(-5); // -1 + -4
    });
  });

  describe("type = SUBTRACT", () => {
    it("soustraction simple", () => {
      expect(calculateNumber("SUBTRACT", 5, 3)).to.equal(2);
    });

    it("soustraction avec arrondis", () => {
      expect(calculateNumber("SUBTRACT", 1.4, 4.5)).to.equal(-4); // 1 - 5
      expect(calculateNumber("SUBTRACT", 1.6, 3.3)).to.equal(-1); // 2 - 3
    });

    it("soustraction avec négatifs", () => {
      expect(calculateNumber("SUBTRACT", -1.4, -3.6)).to.equal(3); // -1 - (-4)
    });
  });

  describe("type = DIVIDE", () => {
    it("division simple", () => {
      expect(calculateNumber("DIVIDE", 10, 2)).to.equal(5);
    });

    it("division avec arrondis", () => {
      expect(calculateNumber("DIVIDE", 1.4, 4.5)).to.equal(0.2); // 1 / 5
      expect(calculateNumber("DIVIDE", 1.6, 3.3)).to.equal(2 / 3); // 0.666...
    });

    it("division par zéro arrondi → Error", () => {
      expect(calculateNumber("DIVIDE", 1.4, 0)).to.equal("Error"); // 1 / 0
      expect(calculateNumber("DIVIDE", 1.4, 0.2)).to.equal("Error"); // 1 / 0
    });

    it("division avec négatifs", () => {
      expect(calculateNumber("DIVIDE", -1.4, 4.5)).to.equal(-0.2); // -1 / 5
      expect(calculateNumber("DIVIDE", -1.6, -3.3)).to.equal(2 / 3);
    });
  });

  describe("cas invalides", () => {
    it("lève une erreur si type invalide", () => {
      expect(() => calculateNumber("MULTIPLY", 1, 2)).to.throw("Invalid type");
    });
  });
});
