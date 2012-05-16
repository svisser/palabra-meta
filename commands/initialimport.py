import constants
from database import connection, db


def run(*args, **kwargs):
    result = raw_input("""This will delete all content in the database. Do you wish to continue (yes/no)? """)
    if result != 'yes':
        print "No actions were performed. Exiting."
        return
    connection.drop_database('palabra')
    p1 = {
        constants.META_TITLE: "Author 1",
        constants.META_CREATOR: "John Johnsson",
        constants.META_CONTRIBUTOR: "Contributor",
        constants.META_RIGHTS: "Copyright notice",
        constants.META_PUBLISHER: "The publisher",
        constants.META_DATE: "The date",
    }
    db.crosswords.insert(p1)
