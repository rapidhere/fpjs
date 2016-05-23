console.log(func(0));

function func(deep) {
    if(deep === 3)
        return 1;

    var i, sum = 0;
    for(i = 0;i < 3;i += 1) {
        sum += func(deep + 1);
    }

    return sum;
}