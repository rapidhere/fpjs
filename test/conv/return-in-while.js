var f = function() {
  while(1) {
    return 2;
  }

  console.log("should not reach");
};

console.log("the num is " + f());

var g = function() {
  while(0) {
    return 2;
  }

  console.log("should reach");
};

console.log(g());
