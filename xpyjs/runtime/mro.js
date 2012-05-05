// http://www.python.org/getit/releases/2.3/mro/

type.mro = function(c) {

    var seqs = [[c]];
    for (var i=0; i<c.__bases__.length; i++) {
        seqs.push(c.__bases__[i].__mro__.slice(0));
    }
    seqs.push(c.__bases__.slice(0));

    return $merge(seqs);
}

function $merge(seqs) {

    var result = [];

    while (1) {

        seqs = seqs.filter(function(seq){return seq.length>0});

        if (seqs.length === 0) return result;

        var head = null;

        for (var i=0; i<seqs.length; i++) {
            var head = seqs[i][0];

            check_tail:
            for (var j=0; j<seqs.length; j++) {
                var tail = seqs[j].slice(1);
                for (var k=0; k<tail.length; k++) {
                    if (tail[k] === head) {
                        head = null;
                        break check_tail;
                    }
                }
            }

            if (head !== null)
                break;
        }

        if (head === null)
            throw "Inconsistent hierarchy";

        result.push(head);

        for (var i=0; i<seqs.length; i++) {
            if (seqs[i][0] === head) {
                seqs[i].shift();
            }
        }
    }

    return result;
}
