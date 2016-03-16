var f0 = 0, f1 = 1, n = 2, f;

while(n < 100) {
  f = f0 + f1;
  f0 = f1;
  f1 = f;
  n += 1;
  console.log(f);
}

console.log(f);
