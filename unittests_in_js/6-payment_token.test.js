const assert = require("assert");
const getPaymentTokenFromAPI = require("./6-payment_token");

describe("getPaymentTokenFromAPI", () => {
  it('should resolve with {data: "Successful response from the API"} when success is true', (done) => {
    getPaymentTokenFromAPI(true)
      .then((res) => {
        assert.deepStrictEqual(res, {
          data: "Successful response from the API",
        });
        done(); // important pour indiquer à Mocha que le test est fini
      })
      .catch((err) => done(err)); // au cas où une erreur survient
  });
});
