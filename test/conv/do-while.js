var a = 0, sum = 0;

do {
  sum += a;
  a += 1;

  console.log("sum is " + sum);
} while(a < 10);

console.log("sum is " + sum);

a = 0, sum = 0;

do {
  sum += a;
  a += 1;

  if(a >= 10)
    break;
  if(a == 2)
    continue;
  console.log("sum is " + sum);
} while(1);

console.log("sum is " + sum);
