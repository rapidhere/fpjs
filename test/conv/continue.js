var a = 10;

while(a > 0) {
  console.log("a is :" + a);
  if(a === 5 || a === 7) {
    break;
  }
  a -= 1;
}

a = 10;
while(a > 0) {
  console.log("working");
  a -= 1;
  continue;
  break;
}

console.log("end");
