JUST A JS AST
===

[![Build Status](https://travis-ci.org/rapidhere/fpjs.svg?branch=master)](https://travis-ci.org/rapidhere/fpjs)

> Author: rapidhere@gmail.com
>
> Maintainer: rapidhere@gmail.com
>

convert your javascript code into functional-programming way


HOW TO
---

### Loop And Recursion

Loop can be convert into Recursion.

So the left problem is how to implement Recursions in functional-programming way. This is the most hard problem I have to solve. The answer is
to use [Y-combinator](https://en.wikipedia.org/wiki/Fixed-point_combinator)

In detail, first we have a recursion function like `factorial`:
```
var fact = function(n) {
  if(n === 0)
    return 1;
  return fact(n - 1) * n;
};
```

And we have the Y-combinator:
```
var Y = function(F) {
  return (function(G) {
    return G(G);
  })(function(self) {
    F(function() {
      self(self).apply(this, arguments);
    });
  });
};
```
Rewrite with ES6(require `--harmony_rest_parameters` when run with node):
```
var Y = (F)=>((G)=>G(G))((self)=>F((...args)=>self(self).apply(this, args)));
```

Then, we have to wrap the function `fact` to use Y-combinator:
```
var fact = Y(function(fact) {
  return function(n) {
    if(n === 0)
      return 1;
    return fact(n - 1) * n;
  };
});
```

then we get the recursion function `fact`
```
fact(10); // return 3628800
```

but we only need Y-combinator for loops, so the arguments is useless, the simplified Y-combinator is

```
var Y = function(F) {
  var G = function(self) {
    return F(function() {
      return self(self);
    });
  };

  return function() {
    G(G);
  };
};
```

And if we need the it to run at once, we can change it to

```
var Y = function(F) {
  var G = function(self) {
    return F(function() {
      return self(self);
    });
  };

  return G(G);
};
```

rewrite with ES6

```
(F)=>((G)=>G(G))((self)=>F(()=>self(self)))
```

LICENSE
---

> This program is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
>
> This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
>
> You should have received a copy of the Lesser GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
