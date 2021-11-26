import mysql.connector, psycopg2    
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

try:
    # conn = mysql.connector.connect(user='root', password='jayshah', host='127.0.0.1', database='python_api')
    conn = psycopg2.connect(user='postgres', password='jayshah', host='127.0.0.1', database='python_api')
    cursor = conn.cursor()
    print("Database connection successful")
except mysql.connector.Error as err:
    print(err)

def getRecent():
    cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Database is empty")
    return post

def getPostById(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id),)) # Since you are using mysql module, cursor.execute requires a sql query and a tuple as parameters
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return post

@app.get("/")
def root():
    return {"Message": "Hello Jay"}

@app.get("/posts")
def getPosts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"Posts": posts}

@app.post("/createpost")
def createPost(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """, (post.title, post.content, post.published))
    conn.commit()
    return {"Message": "Post created successfully", "Post": getRecent()}

@app.get("/getpost/latest")
def getLatestPost():
    return {"Post": getRecent()}

@app.get("/getpost/{id}")
def getPost(id: int):
    return {"Post": getPostById(id)}

@app.put("/updatepost/{id}")
def updatePost(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s""", (post.title, post.content, post.published))
    conn.commit()
    return {"Message": "Post created successfully", "Post": getPostById(id)}

@app.delete("/deletepost/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePOst(id: int):
    post = getPostById(id)
    cursor.execute("""DELETE FROM posts WHERE id=%s""", (str(id),))
    post = cursor.fetchone()
    conn.commit()
    return {"Post": post}