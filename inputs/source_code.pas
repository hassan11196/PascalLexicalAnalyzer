program checkMyAbility;
var
counter: integer;
number: integer;
factorial: integer;
height : real;
width : real;
breadth : real;
volume : real;
begin
number := 6;
counter := number;
factorial := 1
while counter > 0 do begin
number := number * counter;
counter := counter - 1;
end;
height := 8.5;
width := 4.5;
breadth := 2.25;
volume := height * width * breadth;
if volume >= 100 and number < 5 then begin
volume := volume / 4;
end
else begin
if volume >= 50 or number < 10 then begin
volume := volume / 2;
end
end;
write("Factorial of ");
write(number);
write(" is ");
writeln(factorial);
write("Some odd value is: ");
writeln(volume);
end.