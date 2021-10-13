const gpio = require('onoff').Gpio;
const LED = new gpio(4, 'out');
const blinkInterval = setInterval(blinkLed, 250);


const blinkLed = () => {
    // if off turn on, else turn off
    if(LED.readSync() === 0){
        LED.writeSync(1);
    }else{
        LED.writeSync(0);
    }
}

const endBlink = () => {
    clearInterval(blinkInterval);
    LED.writeSync(0);
    // free up GPIO
    LED.unexport();
}

setTimeout(endBlink, 7500);