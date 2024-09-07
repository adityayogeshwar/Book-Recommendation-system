from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
popular_books = pickle.load(open(r'popular.pkl','rb'))
pt = pickle.load(open(r'pt','rb'))
books = pd.read_csv(r'Books.csv')
similarity_score = pickle.load(open(r'similarity','rb'))
app= Flask(__name__)

@app.route('/')
def index():
    return  render_template('index.html',
                            book_name=list(popular_books['Book-Title'].values),
                            author=list(popular_books['Book-Author'].values),
                            votes=list(popular_books['Num_rating'].values),
                            rating=list(popular_books['Avg_rating'].values),
                            image= list(popular_books['Image-URL-M'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    s=[]
    idx = np.where(pt.index==user_input)[0][0]
    suggestions=sorted(enumerate(similarity_score[idx]),key= lambda x:x[1],reverse=True)[1:6]
    for i in suggestions:
        item=[]
        temp_df=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        s.append(item)
    return render_template('recommend.html',data=s)



if __name__ == '__main__':
    app.run(debug=True)



