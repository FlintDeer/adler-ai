#include "hal9000.h"
#include <iostream>

Hal9000::Hal9000() {
    // Initialization logic can be added here
}

std::string Hal9000::processInput(const std::string& input) {
    // Placeholder processing
    return "Processing: " + input;
}

void Hal9000::speak(const std::string& message) {
    std::cout << "HAL9000: " << message << std::endl;
}
