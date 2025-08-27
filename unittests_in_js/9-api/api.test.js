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
  it("Correct status code when :id is a number", (done) => {
    request.get(`${baseURL}/cart/12`, (err, res) => {
      if (err) return done(err);
      expect(res.statusCode).to.equal(200);
      done();
    });
  });

  it("Correct body when :id is a number", (done) => {
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

  // optionnels “etc.”
  it("accepts leading zeros", (done) => {
    request.get(`${baseURL}/cart/0007`, (err, res, body) => {
      if (err) return done(err);
      expect(res.statusCode).to.equal(200);
      expect(body).to.equal("Payment methods for cart 0007");
      done();
    });
  });

  it("rejects negative numbers", (done) => {
    request.get(`${baseURL}/cart/-5`, (err, res) => {
      if (err) return done(err);
      expect(res.statusCode).to.equal(404);
      done();
    });
  });
});
