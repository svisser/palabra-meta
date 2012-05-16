import constants
from database import connection, db


def create_crossword(i):
    s_i = str(i)
    return {
        constants.META_TITLE: "Author " + s_i,
        constants.META_CREATOR: "Creator " + s_i,
        constants.META_CONTRIBUTOR: "Contributor " + s_i,
        constants.META_RIGHTS: "Copyright " + s_i,
        constants.META_PUBLISHER: "Publisher " + s_i,
        constants.META_DATE: "Date " + s_i,
    }


def run(args):
    result = raw_input("""This will delete all content in the database. Do you wish to continue (yes/no)? """)
    if result != 'yes':
        print "No actions were performed. Exiting."
        return
    assert len(args) == 2, "Initial import got an unexpected number of arguments."
    try:
        n_crosswords = int(args[1])
    except ValueError:
        n_crosswords = None
    assert n_crosswords is not None, "The number of initial crosswords could not be determined."
    connection.drop_database('palabra')
    db.crosswords.insert([create_crossword(i) for i in xrange(n_crosswords)])
    print "Total crosswords inserted:", str(n_crosswords)
