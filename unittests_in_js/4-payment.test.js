const assert = require("assert");
const sinon = require("sinon");
const Utils = require("./utils");
const sendPaymentRequestToApi = require("./4-payment");

describe("sendPaymentRequestToApi (stub)", () => {
  let calcStub;
  let logSpy;

  beforeEach(() => {
    calcStub = sinon.stub(Utils, "calculateNumber").returns(10);
    logSpy = sinon.spy(console, "log");
  });

  afterEach(() => {
    sinon.restore(); // restaure stub + spy
  });

  it("stub Utils.calculateNumber -> 10; vérifie les arguments et le log", () => {
    sendPaymentRequestToApi(100, 20);

    // Le stub est appelé avec les bons paramètres
    assert.strictEqual(calcStub.calledOnce, true);
    assert.strictEqual(calcStub.calledWithExactly("SUM", 100, 20), true);

    // Le message console est correct
    assert.strictEqual(logSpy.calledOnce, true);
    assert.strictEqual(logSpy.calledWithExactly("The total is: 10"), true);
  });
});
