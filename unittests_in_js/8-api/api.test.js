const request = require("request");
const { expect } = require("chai");

const baseURL = "http://localhost:7865";

describe("Index page", () => {
  it("Correct status code?", (done) => {
    request.get(`${baseURL}/`, (err, res, body) => {
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

  it("Other? (Content-Type text/html)", (done) => {
    request.get(`${baseURL}/`, (err, res, body) => {
      if (err) return done(err);
      expect(res.headers).to.have.property("content-type");
      expect(res.headers["content-type"]).to.match(/text\/html/);
      done();
    });
  });
});
