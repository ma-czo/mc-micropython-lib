# mc-micropython-lib
Set of minimalistic libs for micropython. 

Each lib is separate package without external dependencies.
Libraries are intended to have educational value and promote good programing practices.

Tested on:
* ESP8266 (LoLin Node MCU v3) and PCA9685 16-Channel 12-bit PWM driver.

# How to run example
Connect PCA9685 I2C to NodeMCU v3.
* GND
* VCC (3.3V)
* SDA
* SCL
Attach external 5V power supply to V+ or terminals.
Connect servo-motor of your robot to channel 0 (like specified in example).   
Copy files to flash.
Open REPL.

`import example`

`example.pca9685_demo()`

Robot will wave his arm once in two steps.

# External documentation
![PCA9685 datasheet](https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf "NXP PCA9685.pdf")

Enjoy your development!