var sum = 0, i = 0, j;

while(1) {
  j = 0;

  if(i >= 12)
    break;

  if(i % 3 == 0) {
    i += 1;
    continue;
  }

  while(1) {
    j += 1;

    if(j >= i + 1) {
      break;
    }

    if((i + j) % 4 == 0)
      continue;

    sum += i + j;
  }

  i += 1;
}

console.log(sum);
