#define ASSIGN1 
    area:=0.5*pi*power(r,2);
#enddef
/* this is an example */
program myprog;
var area, pi, r: integer;
#include <power.pas>
begin   /* main line */
#ASSIGN1 ;
end.
