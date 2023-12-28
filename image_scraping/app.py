# Importing the necessary Libraries
from flask import Flask, render_template, request,jsonify
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

app = Flask(__name__) # initialising the flask app with the name 'app'

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/review",methods = ["GET","POST"])
def index():
    if request.method == 'POST':
        try:
            # Remove space in search
            query = request.form['content'].replace(" ","")

            # Create directory if not exists
            save_dir = "images/"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # To preve blocked bt the google due to many continuous download
            header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

            # Google image search URL
            response = requests.get(f"https://www.google.com/search?q=tata&sca_esv=594212558&tbm=isch&sxsrf=AM9HkKnp5RIZ8oDVgfD65ioF_FY382lS9w:1703765045655&source=lnms&sa=X&ved=2ahUKEwiqs86yi7KDAxXQmVYBHUe9B-oQ_AUoAnoECAMQBA&cshid=1703765060437799&biw=1536&bih=730&dpr=1.25")
            
            # Parsing the Content
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract all images and store in list
            image_tags = soup.find_all("img")

            # Remove first image because it is does not store valid data
            del image_tags[0]
            img_data = []

            for i in image_tags:
                image_url = i['src']
                image_data = requests.get(image_url).content
                mydict = {"Index":image_url, "Image":image_data}
                img_data.append(mydict)
                with open(os.path.join(save_dir, f"{query}_{image_tags.index(i)}.jpg"),"wb") as f:
                    f.write(image_data)
            return render_template('showResult.html', result="Image Loaded")
        except:
            return render_template('showResult.html', result="Something is wrong")
    else:
        return render_template("index.html")
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)