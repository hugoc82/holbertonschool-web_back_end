const assert = require("assert");
const sinon = require("sinon");
const sendPaymentRequestToApi = require("./5-payment");

describe("sendPaymentRequestToApi with hooks", () => {
  let logSpy;

  beforeEach(() => {
    logSpy = sinon.spy(console, "log");
  });

  afterEach(() => {
    sinon.restore();
  });

  it('logs "The total is: 120" and is called once for (100, 20)', () => {
    sendPaymentRequestToApi(100, 20);
    assert.strictEqual(logSpy.calledOnce, true);
    assert.strictEqual(logSpy.calledWithExactly("The total is: 120"), true);
  });

  it('logs "The total is: 20" and is called once for (10, 10)', () => {
    sendPaymentRequestToApi(10, 10);
    assert.strictEqual(logSpy.calledOnce, true);
    assert.strictEqual(logSpy.calledWithExactly("The total is: 20"), true);
  });
});
