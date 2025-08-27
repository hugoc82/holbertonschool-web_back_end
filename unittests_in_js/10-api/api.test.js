const request = require("request");
const { expect } = require("chai");

const baseURL = "http://localhost:7865";

describe("Index page", () => {
  it("Correct status code?", (done) => {
    request.get(`${baseURL}/`, (err, res) => {
      if (err) return done(err);
      expect(res.statusCode).to.equal(200);
      done();
    });
  });

  it("Correct result?", (done) => {
    request.get(`${baseURL}/`, (err, res, body) => {
      if (err) return done(err);
      expect(body).to.equal("Welcome to the payment system");
      done();
    });
  });
});

describe("Cart page", () => {
  it("200 when :id is a number", (done) => {
    request.get(`${baseURL}/cart/12`, (err, res) => {
      if (err) return done(err);
      expect(res.statusCode).to.equal(200);
      done();
    });
  });

  it("body OK when :id is a number", (done) => {
    request.get(`${baseURL}/cart/12`, (err, res, body) => {
      if (err) return done(err);
      expect(body).to.equal("Payment methods for cart 12");
      done();
    });
  });

  it("404 when :id is NOT a number", (done) => {
    request.get(`${baseURL}/cart/hello`, (err, res) => {
      if (err) return done(err);
      expect(res.statusCode).to.equal(404);
      done();
    });
  });
});

/* -------- Nouveaux tests -------- */

// /available_payments
describe("GET /available_payments", () => {
  it("returns 200 and the expected JSON", (done) => {
    request.get(
      { url: `${baseURL}/available_payments`, json: true },
      (err, res, body) => {
        if (err) return done(err);
        expect(res.statusCode).to.equal(200);
        expect(body).to.deep.equal({
          payment_methods: {
            credit_cards: true,
            paypal: false,
          },
        });
        done();
      }
    );
  });
});

// /login
describe("POST /login", () => {
  it('returns "Welcome <name>" for provided userName', (done) => {
    request.post(
      {
        url: `${baseURL}/login`,
        json: { userName: "Betty" }, // envoie JSON + Content-Type
      },
      (err, res, body) => {
        if (err) return done(err);
        // body est du texte (pas du JSON) -> "Welcome Betty"
        expect(res.statusCode).to.equal(200);
        expect(body).to.equal("Welcome Betty");
        done();
      }
    );
  });
});
