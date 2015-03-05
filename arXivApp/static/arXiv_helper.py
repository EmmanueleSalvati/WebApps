"""Functions to connect to the MongoDB on DigitalOcean cloud"""

from pymongo import MongoClient
from textblob import TextBlob
from collections import OrderedDict
from collections import Counter


def str_to_datetime(datestr):
    """Takes a string like 7/31/92 and returns a datetime object"""

    from dateutil.parser import parse

    date = parse(datestr)
    return date


def particles_in_abstract(words, keywords):
    """Returns a list of particles in this abstract"""

    particles_in_abs = [word for word in words if word in keywords]
    return particles_in_abs


def get_cursor(client, coll='hepex', from_date=None, to_date=None):
    """Returns the cursor in the given date range"""

    if coll == 'hepph':
        collection = client.arXivpapers.hepph
    else:
        collection = client.arXivpapers.hepex

    cursor = collection.find()
    return cursor


def loop_events(cursor, keywords):
    """Dumps all the particle names into a dictionary, whose keys are dates"""

    assert cursor, "there is no cursor!"
    abs_dict = {}

    # FOR THE MOMENT WE KEEP DATES IN STRING FORMAT!!!
    for record in cursor:
        # date = str_to_datetime(record['date'])
        date = record['date']
        ABSTRACT = record['abstract']
        abstract = TextBlob(ABSTRACT)
        blob = list(abstract.words.singularize())
        if 'higg' in blob:
            blob.remove('higg')
            blob.append('higgs')
        particles = particles_in_abstract(blob, keywords)
        abs_dict[date] = particles

    return abs_dict


def date_range(abstracts=None, from_date=None, to_date=None):
    """Returns a counter of all particles in the specified range"""

    counter = Counter()
    od = OrderedDict(sorted(abstracts.items()))
    for date, particles in od.iteritems():
        if date < from_date or date >= to_date:
            continue
        for particle in particles:
            counter[particle] += 1

    return counter
