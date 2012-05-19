from bson.code import Code
from database import db


def run(args):
    mapper = Code("""
    function() {
        var count = 0;
        var cells = {}
        this.grid.cells.forEach(function(cell) {
            cells[cell.x + "-" + cell.y] = {
                "x": cell.x,
                "y": cell.y,
                "block": cell.block,
                "void": cell.void,
            };
        });
        for (var c in cells) {
            var cell = cells[c];
            if (!cell.block && !cell.void) {
                var x = cell.x;
                var y = cell.y;
                var pos_left = ((x - 1) + "-" + y);
                var pos_right = ((x + 1) + "-" + y);
                var pos_top = (x + "-" + (y - 1));
                var pos_bottom = (x + "-" + (y + 1));
                var n_left = cells[pos_left];
                var n_right = cells[pos_right];
                var n_top = cells[pos_top];
                var n_bottom = cells[pos_bottom];
                var has_empty_left = typeof n_left === "object" && !n_left.block && !n_left.void;
                var has_empty_right = typeof n_right === "object" && !n_right.block && !n_right.void;
                var has_empty_top = typeof n_top === "object" && !n_top.block && !n_top.void;
                var has_empty_bottom = typeof n_bottom === "object" && !n_bottom.block && !n_bottom.void;
                var n_words = 0;                
                if (has_empty_left || has_empty_right) {
                    n_words += 1;
                }
                if (has_empty_top || has_empty_bottom) {
                    n_words += 1;
                }
                if (n_words == 2) {
                    count += 1;
                }
            }
        }
        emit("checkcount", { "count": count });
    }""")
    reducer = Code("""
    function(key, values) {
        var count = 0;
        values.forEach(function(value) {
            count += value.count;
        });
        return { count: count };
    }""")
    result = db.crosswords.map_reduce(mapper, reducer, "checkcount")
    for d in result.find():
        print d