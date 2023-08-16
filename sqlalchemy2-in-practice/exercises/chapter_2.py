# from db import Session
# from models import Product

# import sys
# from sqlalchemy import select, func
# sys.path.append('../sqlalchemy2-in-practice')

# from sqlalchemy2-in-practice.db import session 
# from .. import models

# session = db.Session()




# # execute on python shell maybe

# # 1. The first three products in alphabetical order built in the year 1983

# print("# 1. The first three products in alphabetical order built in the year 1983: \n")

# q1 = select(models.Product).filter(models.Product.year == 1983).limit(3)
# r1 = session.execute(q1).all()

# print(r1)