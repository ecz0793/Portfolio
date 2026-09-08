#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>
#include <conio.h>
#include <windows.h>

int selec_get_(char* touche, int* tsec, int* tmicrosec)
{
int retval=0 ;

*touche='\0' ;

Sleep(*tsec*1000+*tmicrosec/1000) ;

if (kbhit()) { *touche=getch() ; retval=1 ;}

return (retval) ;
}
