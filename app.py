from flask import Flask, render_template, request
import pickle
import numpy as np

# Load pickled objects
popular_df = pickle.load(open('popular.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['title'].values),
                           author=list(popular_df['author'].values),
                           image=list(popular_df['coverImg'].values),
                           votes=list(popular_df['numRatings'].values),
                           rating=list(popular_df['rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html', book_list=list(books['title'].values))

@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    user_input = request.form.get('user_input')

    # Check if book exists in books['title']
    matching_index = books[books['title'] == user_input].index
    if len(matching_index) == 0:
        return render_template('recommend.html', data=[], book_list=list(books['title'].values),
                               message="❌ Book not found. Please choose from suggestions.")

    index = matching_index[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_book = books.iloc[i[0]]
        item.append(temp_book['title'])
        item.append(temp_book['author'])
        item.append(temp_book['coverImg'])
        data.append(item)

    return render_template('recommend.html', data=data, book_list=list(books['title'].values))

if __name__ == '__main__':
    app.run(debug=True)