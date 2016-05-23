console.log(func());
console.log(func1());

function func() {
    return 1 + 1;
}

var func = function() {

};

function func1() {
    return func() + func2();

    function func2() {
        return 2;
    }
}