from flask import Flask,render_template,request
import pickle
import numpy as np

populer_df = pickle.load(open("populer.pkl","rb"))

pt = pickle.load(open("pt.pkl","rb"))
similarity_score = pickle.load(open("similarity_score.pkl","rb"))
books = pickle.load(open("books.pkl","rb"))


app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return render_template("index.html",
                           book_name = list(populer_df["Book-Title"].values),
                           author = list(populer_df["Book-Author"].values),
                           image = list(populer_df["Image-URL-M"].values),
                           votes = list(populer_df["num-rating"].values),
                           rating = list(populer_df["Average-Rating"].values))

@app.route('/recommand')
def recommand_ui():
    return render_template('recommand.html')

@app.route('/recommand_books', methods=["post"])
def recommand():
    user_input = request.form.get("user_input")

    index = np.where(pt.index == user_input)[0][0]
    similer_item = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

    datas = []
    for i in similer_item:
        # print(pt.index[i[0]])
        item = []
        temp_df = books[books["Book-Title"] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))


        datas.append(item)
    print(datas)

    return render_template('recommand.html',data=datas)


if __name__ == "__main__":
    app.run(debug=True)




