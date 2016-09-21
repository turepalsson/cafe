import json, sys
import psycopg2

with psycopg2.connect(dbname = 'sweden') as conn:
    c = conn.cursor()
    c.execute('''SELECT id, ST_AsGeoJSON(g) AS g, tags->'name' AS name
      FROM feature
      WHERE tags @> 'amenity=>cafe'
            AND st_dwithin(g, (SELECT g FROM feature
                                WHERE tags->'name' LIKE 'Ejes%'),
                           1.0/300)''')
    features = []
    for row in c.fetchall():
        fid, geom, name = row
        props = { 'id': fid, 'name': name }
        obj = { 'type': 'feature', 'properties': props, 'geometry': geom }
        features.append(obj)

coll = { 'type': 'featurecollection', 'features': features }

json.dump(coll, sys.stdout)
