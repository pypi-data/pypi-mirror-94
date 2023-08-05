#include "Chronometer.h"

#include <iostream>
#include <string>

namespace pinkIndexer
{
    Chronometer::Chronometer(const std::string& key)
        : key_(key)
        , startTime_(std::chrono::system_clock::now())
    {
    }

    Chronometer::~Chronometer()
    {
        auto duration = std::chrono::system_clock::now() - startTime_;
        std::cout << key_ << " elapsed: " << std::chrono::duration_cast<std::chrono::milliseconds>(duration).count() << "\n";
    }
} // namespace pinkIndexer