import json
import sys

import psycopg2

from contextlib import closing

def cafes(out):
    with closing(psycopg2.connect(dbname='sweden')) as conn:
        c = conn.cursor()
        c.execute('''SELECT to_json(t)
                     FROM (SELECT cafe.g AS geometry, cafe.tags AS properties
                           FROM feature cafe, feature ref
                           WHERE cafe.tags @> 'amenity=>cafe'
                             AND ref.tags @> 'shop=>chocolate,name=>Ejes'
                             AND ST_DWithin(cafe.g, ref.g, 1.0/150)) t''')

        col = {
            'type': 'FeatureCollection',
            'features': [{'type': 'Feature', **row[0]} for row in c]
        }

    json.dump(col, out, indent=2)

    out.write('\n')

def main():
    cafes(sys.stdout)

if __name__ == '__main__':
    main()
