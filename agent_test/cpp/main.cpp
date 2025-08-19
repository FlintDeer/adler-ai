#include "hal9000.h"
#include <iostream>

int main() {
    Hal9000 hal;
    std::string response = hal.processInput("Hello, HAL");
    hal.speak(response);
    return 0;
}
