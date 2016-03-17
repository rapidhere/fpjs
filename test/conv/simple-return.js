var f = function(a) {
  if(a > 10)
    return 1;
  else
    return 2;

  console.log("should not reach");
};


console.log(f(10));
console.log(f(11));
