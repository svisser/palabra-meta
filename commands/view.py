from database import db


def run(args):
    assert len(args) == 2, "You did not specify the id of the crossword that you wish to view."
    crossword = None
    for c in db.crosswords.find({ "identifier": args[1] }, limit=1):
        crossword = c
    if crossword is None:
        print "The crossword with identifier '" + args[1] + "' could not be found."
        return
    cells = {}
    for cell in crossword['grid']['cells']:
        cells[cell['x'], cell['y']] = cell
    for y in xrange(crossword['height']):
        line = ""
        for x in xrange(crossword['width']):
            if cells[x, y]['block'] or cells[x, y]['void']:
                line += "X"
            else:
                line += " "
        print line
