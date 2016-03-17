var sum = 0, i = 0, j;

while(i < 10) {
  j = i;
  while(j > 0) {
    sum += j;
    j -= 1;
  }
  i += 1;
}

console.log("sum is " + sum);
