var i, sum;

for(i = 0, sum = 0;i < 10;i += 1) {
  if(i === 1)
    continue;
  sum += i;

  if(i === 8)
    break;
}

console.log(sum);
