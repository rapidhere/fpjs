var a = {
    1: 2,
    "a": {
        "a": a
    },
};

console.log(a[1], a["a"], a["none"], a.a.a);