#ifndef HAL9000_H
#define HAL9000_H

#include <string>

// Basic HAL9000 interface skeleton
class Hal9000 {
public:
    Hal9000();
    std::string processInput(const std::string& input);
    void speak(const std::string& message);
};

#endif // HAL9000_H
