const gpio = require('onoff').Gpio;

class LED{
    /**
     * 
     * @param {number} pinNumber - GPIO port number
     * @param {number} interval - time between blinks
     * @param {number} timeout - time before ending
     */
    constructor(pinNumber, interval, timeout){
        this.pinNumber = pinNumber;
        this.interval = interval;
        this.timeout = timeout;
        this.led = new gpio(this.pinNumber, 'out');
    }

    blink(){
        // if off turn on, else turn off
        if(this.led.readSync() === 0){
            this.led.writeSync(1);
        }else{
            this.led.writeSync(0);
        }
    }

    start(){
        // need to bind the instance to the method being ran in the interval
        const blinkInterval = setInterval(this.blink.bind(this), this.interval);
        setTimeout(() => {
            clearInterval(blinkInterval);
            this.led.writeSync(0);
            // free up GPIO
            this.led.unexport();
        }, this.timeout);
    }
}

module.exports = {
    LED: LED
}