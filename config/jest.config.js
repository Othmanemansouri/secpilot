module.exports = {
  testEnvironment: 'node',
  testMatch: ['**/tests/javascript/**/*.test.js'],
  verbose: true,
  collectCoverage: true,
  coverageDirectory: 'coverage/javascript',
  coverageReporters: ['text', 'lcov'],
  testTimeout: 10000
};
