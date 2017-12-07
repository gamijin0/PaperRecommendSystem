from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey

engine=create_engine("mysql+pymysql://root:xlsd1996@chaos.ac.cn:3306/dblp",echo=True)

