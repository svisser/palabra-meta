from bson.code import Code
from database import db


def run(args):
    mapper = Code("""
    function() {
        var cells = {}
        this.grid.cells.forEach(function(cell) {
            cells[cell.x + "-" + cell.y] = {
                "x": cell.x,
                "y": cell.y,
                "block": cell.block,
                "void": cell.void,
            };
        });
        var width = parseInt(this.width);
        var height = parseInt(this.height);
        
        function iterate(x, y, dx, dy) {
            var cx = x;
            var cy = y;
            var length = 0;
            for (var d = 0; true; d++) {
                var next = (cx + "-" + cy);
                if (!(next in cells)) {
                    break;
                }
                if (cells[next].block || cells[next].void) {
                    break;
                }
                length += 1;
                cx += dx;
                cy += dy;
            }
            return length;
        }
        function across_word_length(x, y) {
            var prev = ((x - 1) +  "-" + y);
            if (!(prev in cells) || cells[prev].block || cells[prev].void) {
                var length = iterate(x, y, 1, 0);
                if (length >= 2) {
                    return length;
                }
            }
            return -1;
        }
        function down_word_length(x, y) {
            var prev = (x +  "-" + (y - 1));
            if (!(prev in cells) || cells[prev].block || cells[prev].void) {
                var length = iterate(x, y, 0, 1);
                if (length >= 2) {
                    return length;
                }
            }
            return -1;
        }
        
        var counts = {};
        for (var y = 0; y < height; y++) {
            for (var x = 0; x < width; x++) {
                var a_length = across_word_length(x, y);
                var d_length = down_word_length(x, y);
                if (a_length > 1) {
                    if (a_length in counts) {
                        counts[a_length] += 1;
                    } else {
                        counts[a_length] = 1;
                    }
                }
                if (d_length > 1) {
                    if (d_length in counts) {
                        counts[d_length] += 1;
                    } else {
                        counts[d_length] = 1;
                    }
                }
            }
        }
        emit("counts", counts); 
    }
    """)
    reducer = Code("""
    function(key, values) {
        var counts = {};
        values.forEach(function(value) {
            for (var c in value) {
                if (c in counts) {
                    counts[c] += value[c];
                } else {
                    counts[c] = value[c];
                }
            }
        });
        return { "counts": counts };
    }
    """)
    result = db.crosswords.map_reduce(mapper, reducer, "wordcount")
    counts = None
    for d in result.find():
        if d['_id'] == "counts":
            counts = d['value']['counts']
    if counts is None:
        print "The total number of words by length could not be determined."
        return
    print "Total number of words (ordered by length)"
    n_counts = {}
    for key, value in counts.iteritems():
        n_counts[int(key)] = int(value)
    for length in sorted(n_counts.keys()):
        print str(length) + ": " + str(n_counts[length])
