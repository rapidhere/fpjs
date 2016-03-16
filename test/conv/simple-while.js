var a = 11;

while(a > 1) console.log("running " + (a -= 1));

a = 10;

while(a) {
  var sum = 0;
  sum += a;
  a -= 1;
}
console.log("sum is " + sum);

a = 0;
sum = 0;

while(a < 10) {
  sum += a;
  a += 1;
}
console.log("sum is " + sum);
