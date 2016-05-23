console.log(func());

function func() {

    var i, ret = 0;
    for(i = 0;i < 10;i += 1) {
        if(1) {
            ret += 1;
        }
    }

    return ret;
}