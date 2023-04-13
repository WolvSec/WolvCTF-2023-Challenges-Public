#include <stdint.h>
#include "entry.h"

void _entry(void)
{
    char msg[] = "Another flag part: Y0_D4wg\n\0";
    write(STDOUT_FILENO, msg, sizeof(msg));
}
