// ::AUTHOR::
// {{ project }}
// {{ date }}

#ifndef {{ classname.upper() }}_H
#define {{ classname.upper() }}_H
#include <iostream>
#include <vector>
#include <string>


class {{ classname }} {
    public:
        // Default constructor
        {{ classname }}(void);

        // Default destructor
        ~{{ classname }}(void);

        // Sample method
        int id(void);

    private:
        // Member variables
        int id_;
};

#endif // {{ classname.upper() }}_H