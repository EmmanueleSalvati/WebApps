"""Functions to connect to the MongoDB on DigitalOcean cloud"""

from pymongo import MongoClient
from textblob import TextBlob
from collections import OrderedDict
from collections import Counter
from datetime import datetime
import pickle as pkl


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


def electrons_in_abstract(abstract=None, particle=None):
    """Temporary: returns a csv file like this:
    date,electrons
    u'2011-01-10',4
    ...
    """

    if not particle:
        filename = 'electrons.csv'
    else:
        filename = str(particle) + "s.csv"

    import csv
    with open(filename, 'w') as csvfile:
        fieldnames = ['rollingmonth', 'year', 'month', 'electrons']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for k, v in abstract.iteritems():
            writer.writerow({"rollingmonth": k[0],
                             "year": k[1],
                             "month": k[2],
                             "electrons": v})


def sum_electrons(particle_row, particle='electron'):
    """Get a list [u'muon', u'electron', u'electron', etc.]
    and return the number of electrons"""

    from collections import Counter

    return Counter(particle_row)[particle]


# def write_csv(filename):
#     """Write electrons.csv from the filename=abs_yearmonth.pkl"""

#     import pickle as pkl
#     with open(filename, 'r') as pklfile:
#         abs_dict = pkl.load(pklfile)

#     electrons_in_abstract(abs_dict)


def convert_date_to_yearmonth(filename):
    """Takes the abstract dictionary and turns the datetime objects
    into year, date"""

    from datetime import datetime
    import pickle as pkl
    with open(filename, 'r') as pklfile:
        abs_dict = pkl.load(pklfile)

    ym_dict = {}
    for k, v in abs_dict.iteritems():
        year = k.year
        month = k.month
        if (year, month) in ym_dict:
            ym_dict[(year, month)].extend(v)
        else:
            ym_dict[(year, month)] = v

    return ym_dict


def convert_ym_to_sumofmonths(ym_dict, particle='electron'):
    """Takes the ym_dict dictionary and returns a dict of the form:
    month order, datestring, electroncount"""

    from collections import Counter
    from collections import OrderedDict
    # import pickle as pkl
    # with open(filename, 'r') as pklfile:
    #     ym_dict = pkl.load(pklfile)

    ordered_ym_dict = OrderedDict(sorted(ym_dict.iteritems()))
    months = len(ordered_ym_dict)

    rolling_dict = {}
    for i in range(months):
        my_index = (i,
                    ordered_ym_dict.items()[i][0][0],
                    ordered_ym_dict.items()[i][0][1])

        rolling_dict[my_index] = sum_electrons(ordered_ym_dict.
                                               items()[i][1], particle)

    return rolling_dict


def create_particle_csv(particle_name):
    """This function calls all the others; I give it a particle name (electron,
    muon, etc.) and it creates the csv file"""

    ym_dict = convert_date_to_yearmonth('../abs_dict.pkl')
    roll_dict = convert_ym_to_sumofmonths(ym_dict, particle_name)
    electrons_in_abstract(roll_dict, particle_name)
