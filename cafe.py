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
        features = []
        for row in c.fetchall():
            fid, geomstr, name = row
            geom = json.loads(geomstr)
            props = { 'id': fid, 'name': name }
            obj = { 'type': 'Feature', 'properties': props, 'geometry': geom }
            features.append(obj)
    
    coll = { 'type': 'FeatureCollection', 'features': features }
    
    json.dump(coll, out)
    out.write('\n')

def main():
    cafes(sys.stdout)

if __name__ == '__main__':
    main()
