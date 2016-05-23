/**
 * Full Functional Test Case:
 *
 * 8-Queen Problem
 */

var nQueen;
for(nQueen = 5; nQueen <= 5; nQueen += 1) {
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