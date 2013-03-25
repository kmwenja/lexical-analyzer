function power(x: real; n: 0 .. maxint): real;
var y: real;  i, n: 0 .. maxint;
begin
   y:= 0.0;
   for i := 1 to n do y:= y*x;
   power := y
end; 
