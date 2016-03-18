var a = 10;

while(a > 0) {
  console.log("a is :" + a);
  if(a < 5) {
    break;
  }
  a -= 1;
}

while(1) {
  console.log("working");
  break;
  console.log("should not reach");
}

console.log("end");
