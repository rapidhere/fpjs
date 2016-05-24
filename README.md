Functional-Way-Onelined-ECMAScript5
===

[![Build Status](https://travis-ci.org/rapidhere/fpjs.svg?branch=master)](https://travis-ci.org/rapidhere/fpjs)

> Author: rapidhere@gmail.com
>
> Maintainer: rapidhere@gmail.com
>

convert your javascript code into functional-programming way

Aim
---

Convert ANY javascript programms into one line, without semicolons and braces.

Usage
---

`python fpjs.py input_file output_file`

Convertion Example:

```js
// Eight Quuens problem
// Raw Programm
var nQueen;
for(nQueen = 1; nQueen <= 13; nQueen += 1) {
    console.log("Queen ", nQueen, solve(nQueen));
}

function solve(n) {
    var colAva = [];
    var croAva = [];
    var ncrAva = [];

    initArray(colAva, n, true);
    initArray(croAva, n + n - 1, true);
    initArray(ncrAva, n + n - 1, true);

    var put = function(row) {
        if(row === n)
            return 1;

        var col, ret = 0;
        for(col = 0;col < n;col += 1) {
            if(colAva[col] && croAva[row + col] && ncrAva[row - col + n - 1]) {
                colAva[col] = false;
                croAva[row + col] = false;
                ncrAva[row - col + n - 1] = false;

                ret += put(row + 1);

                colAva[col] = true;
                croAva[row + col] = true;
                ncrAva[row - col + n - 1] = true;
            }
        }

        return ret;
    };

    return put(0);
}

function initArray(arr, n, val) {
    var i;
    for(i = 0;i < n;i += 1) {
        arr[i] = val;
    }
}

/*******************************************/
// Converted
((__Y,__OC)=>((initArray,nQueen,solve)=>(solve=(n)=>((colAva,croAva,ncrAva,put)=>((colAva=[]),(croAva=[]),(ncrAva=[]),initArray(colAva,n,true),initArray(croAva,((n)+(n))-(1),true),initArray(ncrAva,((n)+(n))-(1),true),(put=(row)=>((col,ret)=>(((__T,__A)=>(__T?((1)):((__A()))))((row)===(n),(()=>((ret=0),((__WA,__WN)=>(col=0,__Y((__W)=>(((__T,__A)=>(__T?((colAva[col]=false,croAva[(row)+(col)]=false,ncrAva[(((row)-(col))+(n))-(1)]=false,ret+=put((row)+(1)),colAva[col]=true,croAva[(row)+(col)]=true,ncrAva[(((row)-(col))+(n))-(1)]=true,__A())):((__A()))))(((colAva[col])&&(croAva[(row)+(col)]))&&(ncrAva[(((row)-(col))+(n))-(1)]),(()=>(__WN(__W,__WA))))))))((()=>(ret)),(__W,__WA)=>(col+=1,((col)<(n))?__W():__WA())))))))()),put(0)))(),initArray=(arr,n,val)=>((i)=>(undefined,((__WA,__WN)=>(i=0,__Y((__W)=>(arr[i]=val,__WN(__W,__WA)))))((()=>undefined),(__W,__WA)=>(i+=1,((i)<(n))?__W():__WA()))))(),undefined,((__WA,__WN)=>(nQueen=1,__Y((__W)=>(console.log("Queen ",nQueen,solve(nQueen)),__WN(__W,__WA)))))((()=>undefined),(__W,__WA)=>(nQueen+=1,((nQueen)<=(13))?__W():__WA()))))())((F)=>((G)=>G(G))((self)=>F(()=>self(self))),(o, ro)=>(ro=new Object(),o.forEach((i)=>(ro[i[0]]=i[1])),ro));

```


HOW TO
---

### Sequential Statements

Just linked with comma `,`

For example:
```js
a = 1;
b = 2;
c = a + b;
```

will convert into

```js
(a = 1, b = 2, c = a + b)
```

### Functions

Return statements will be disscussed later.

Just rewrite functions into ES6's lambda style, then we can omit all braces.

### Object Literals

Beacause we cannot use braces, object Literal is build by a Object Constructor Function `__OC`

```js
(o, ro)=>(ro=new Object(),o.forEach((i)=>(ro[i[0]]=i[1])),ro)
```

### Variable declarations

Whenever enter a scope (Programm, Function Statement, Function Expression), we first do a DFS on AST to collect all variables in this scope,
and declare them at the TOP OF THE SCOPE.

BUT, we cannot use `var` in expressions (i.e., `(var a = 1, a + 1)` is illegal), so we have to find another way to declare variables.

The answer is wrapping the scope with a **immediate call function expression**, and declare variables as function's arguments.

For example:
```js
function func(c) {
  var a = 1, b;
  return a + c; 
}
```

will convert to

```js
function func(c) {
  // NOTE must wrap inside the func,
  // Or will buggy on recursion functions
  return (function(a, b) {
    a = 1;
    return a + c；
  })();
}
```

and then the fragment can rewrite with ES6

### IF Statement

Conditional Expression is well enough

### Loop And Recursion

Loop can be convert into Recursion.

So the left problem is how to implement Recursions in functional-programming way. This is the most hard problem I have to solve. The answer is
to use [Y-combinator](https://en.wikipedia.org/wiki/Fixed-point_combinator)

In detail, first we have a recursion function like `factorial`:
```js
var fact = function(n) {
  if(n === 0)
    return 1;
  return fact(n - 1) * n;
};
```

And we have the Y-combinator:
```js
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
```js
var Y = (F)=>((G)=>G(G))((self)=>F((...args)=>self(self).apply(this, args)));
```

Then, we have to wrap the function `fact` to use Y-combinator:
```js
var fact = Y(function(fact) {
  return function(n) {
    if(n === 0)
      return 1;
    return fact(n - 1) * n;
  };
});
```

then we get the recursion function `fact`
```js
fact(10); // return 3628800
```

but we only need Y-combinator for loops, so the arguments is useless, the simplified Y-combinator is

```js
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

And if we need it to run at once, we can change it to

```js
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

```js
(F)=>((G)=>G(G))((self)=>F(()=>self(self)))
```

Then we can implemented LOOPs

### break, continue And return

TODO

### Function Statement

TODO


LICENSE
---

> This program is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
>
> This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
>
> You should have received a copy of the Lesser GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
