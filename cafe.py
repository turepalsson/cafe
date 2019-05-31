import json, sys
import psycopg2

def cafes(out):
    with psycopg2.connect(dbname = 'sweden') as conn:
        c = conn.cursor()
        c.execute('''SELECT id, ST_AsGeoJSON(g) AS g, tags->'name' AS name
          FROM feature
          WHERE tags @> 'amenity=>cafe'
                AND st_dwithin(g, (SELECT g FROM feature
                                    WHERE tags->'name' LIKE 'Ejes%'),
                               1.0/300)''')
        features = [
            {
                'type': 'Feature',
                'properties': {
                    'id': row[0],
                    'name': row[2]
                },
                'geometry': json.loads(row[1])
            } for row in c ]

    coll = { 'type': 'FeatureCollection', 'features': features }

    json.dump(coll, out, indent = 2)
    out.write('\n')

def main():
    cafes(sys.stdout)

if __name__ == '__main__':
    main()
