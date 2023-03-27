
const readline = require("readline");
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// you can run code but you can't access the flag

rl.question(">>> ", (answer) => {
  flag = process.env['flag']
  if (answer.match(/flag/)) {
    console.log(':(');
    process.exit(1);
  }
  if (answer.match(/\./)) {
    console.log('hey, are you trying to access functions? :(');
    process.exit(1);
  }
  if (answer.match(/[{}]/)) {
    console.log('do you think calculators have curly braces? :(');
    process.exit(1);
  }
  eval(answer);
  rl.close();
});

rl.on('close', () => process.exit(0));
