const { execSync } = require('child_process');

function run(cmd) {
  return execSync(cmd, { encoding: 'utf8' });
}

module.exports = { run };
