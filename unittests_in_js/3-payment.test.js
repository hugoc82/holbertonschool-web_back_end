const assert = require("assert");
const sinon = require("sinon");
const Utils = require("./utils");
const sendPaymentRequestToApi = require("./3-payment");

describe("sendPaymentRequestToApi", () => {
  afterEach(() => sinon.restore()); // toujours restaurer

  it('appelle Utils.calculateNumber("SUM", 100, 20) et log le résultat', () => {
    const calcSpy = sinon.spy(Utils, "calculateNumber");
    const logSpy = sinon.spy(console, "log");

    sendPaymentRequestToApi(100, 20);

    // Vérifie l’usage de Utils.calculateNumber
    assert.strictEqual(calcSpy.calledOnce, true);
    assert.strictEqual(calcSpy.calledWithExactly("SUM", 100, 20), true);

    // Vérifie le message affiché
    assert.strictEqual(logSpy.calledOnce, true);
    assert.strictEqual(logSpy.calledWithExactly("The total is: 120"), true);
  });
});
