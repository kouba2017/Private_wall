from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math

class Message:
    def __init__(self,data) :
        self.id= data['id']
        self.content=data['content']
        self.user_id=data['user_id']
        self.contact_id=data['contact_id']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    """def time_span(self):
        now=datetime.now()
        delta= now-self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days >0:
            return print(f"{delta.days} days ago")
        elif (math.floor(delta.total_seconds()/60)>=60):
            return f"{math.floor(math.floor(delta.total_seconds()/60)/60)} hours ago"
        elif(delta.total_seconds()>=60):
            return f"{math.floor(delta.total_seconds()/60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"""""
    
    def time_span(self):
        now=datetime.now()
        x=now-self.created_at
        if x.days>0:
            return f"{x.days} days ago"
        elif math.floor(x.total_seconds()/60)>=60:
            return f"{math.floor(x.total_seconds()/3600)} hours ago"
        elif math.floor(x.total_seconds())>60:
            return f"{math.floor(x.total_seconds()/60)} minutes ago"
        else:
            return f"{math.floor(x.total_seconds())} seconds ago"

    @classmethod
    def save(cls,data):
        query ="INSERT INTO messages ( content, user_id, contact_id,created_at,updated_at) VALUES ( %(content)s, %(user_id)s, %(contact_id)s,NOW(),NOW());"
        return connectToMySQL('private_wall').query_db(query,data)
    
    @classmethod
    def get_by_user_id(cls,data):
        query="SELECT * from messages where contact_id='%(id)s'" #data must be user.id
        all_messages=[]
        results= connectToMySQL('private_wall').query_db(query,data)
        for msg in results:
            all_messages.append(cls(msg))
        return all_messages
    @classmethod
    def get_by_contact_id(cls,data):
        query="SELECT * from messages where contact_id!='%(id)s'" #data must be user.id
        all_messages=[]
        results= connectToMySQL('private_wall').query_db(query,data)
        for msg in results:
            all_messages.append(cls(msg))
        return all_messages
    
    @classmethod
    def delete(cls,data):
        query="delete from messages where id=%(id)s"
        return connectToMySQL('private_wall').query_db(query,data)

