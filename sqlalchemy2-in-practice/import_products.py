import csv

from db import Model, Session, engine
from models import Manufacturer, Product


def main():
    Model.metadata.drop_all(engine)  # warning: this deletes all data!
    Model.metadata.create_all(engine)

    with Session() as session:
        with session.begin():
            with open('products.csv') as f:
                reader = csv.DictReader(f)
                all_manufacturers = {}

                for row in reader:

                    
                    # pass
                    # print(row)
                    # {'country': 'UK', 'manufacturer': 'Acorn Computers Ltd', 'name': 'Acorn Atom', 'cpu': '6502', 'year': '1980'}



                    # row['year'] = int(row['year'])

                    # pop (k,v) from row_dict because Product object only have manufacturer_id not manufacturer field
                    manufacturer = row.pop('manufacturer') 


                    p = Product(**row)

                    if manufacturer not in all_manufacturers:
                        m = Manufacturer(name=manufacturer)
                        session.add(m)
                        all_manufacturers[manufacturer] = m
                    all_manufacturers[manufacturer].products.append(p)


if __name__ == '__main__':
    main()
