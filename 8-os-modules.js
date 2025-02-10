//Modules
//CommonJS, every file is module (by default)
//Modules - Encapsulated Code (only share minimum)
const names = require('./4-names');
const sayhi = require('./5-utils');
const data = require('./6-alternative-flavor');

require('./7-mind-grenade');

sayhi('susan');
sayhi(names.john);
sayhi(names.peter);




const os = require('os')

// info about current user
const user = os.userInfo()


// method returns the system uptime in seconds
console.log('the system uptime is ' + os.uptime() + 'seconds')
console.log(`the system uptime is ${os.uptime()} seconds`)

const currentOS = {
  name: os.type(),
  release: os.release(), 
  totalmem: os.totalmem(),
  freemem: os.freemem(),
}
console.log(currentOS)






