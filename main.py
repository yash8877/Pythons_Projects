from flask import Flask,render_template,request
import pickle
import string
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import numpy as np
from urllib.parse import urlparse
from tld import get_tld
import numpy as np

app = Flask(__name__)


pipe = pickle.load(open("Naive_model.pkl","rb"))
tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

# home webpage
@app.route('/')
def render_index():
    return render_template('index.html')
    

# sms webpage
def transformText(text):
    ps = PorterStemmer()
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))
            
    return " ".join(y)

@app.route('/sms',methods=["GET","POST"])
def render_sample():
    if request.method == 'POST':
        # Get the input text from the form
        input_sms = request.form['sms']
        # Perform detection
        transformed_sms = transformText(input_sms)
        # Here, perform the vectorization and prediction as you did in the Streamlit code
        vector_input = tfidf.transform([transformed_sms])
        # Placeholder for the result
        result = model.predict(vector_input)[0]  # Placeholder
        print(result)
        return render_template('result.html', result=result)
    else:  # Render the result template with the detected result
        return render_template('sms.html')
 



# url webpage

def fd_length(url):
    urlpath= urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0

    df['fd_length'] = df['url'].apply(lambda i: fd_length(i))

#Length of Top Level Domain
    df['tld'] = df['url'].apply(lambda i: get_tld(i,fail_silently=True))


def tld_length(tld):
    try:
        return len(tld)
    except:
        return -1

    df['tld_length'] = df['tld'].apply(lambda i: tld_length(i))

def main(url):
    
    status = []

    status.append(having_ip_address(url))
    status.append(abnormal_url(url))
    status.append(count_dot(url))
    status.append(count_www(url))
    status.append(count_atrate(url))
    status.append(no_of_dir(url))
    status.append(no_of_embed(url))
    
    status.append(shortening_service(url))
    status.append(count_https(url))
    status.append(count_http(url))
    
    status.append(count_per(url))
    status.append(count_ques(url))
    status.append(count_hyphen(url))
    status.append(count_equal(url))
    
    status.append(url_length(url))
    status.append(hostname_length(url))
    status.append(suspicious_words(url))
    status.append(digit_count(url))
    status.append(letter_count(url))
    status.append(fd_length(url))
    tld = get_tld(url,fail_silently=True)
      
    status.append(tld_length(tld))
    return status


def get_prediction_from_url(test_url):
    features_test = main(test_url)
    # Due to updates to scikit-learn, we now need a 2D array as a parameter to the predict function.
    features_test = np.array(features_test).reshape((1, -1))
    pred = lgb.predict(features_test)
    if int(pred[0]) == 0:
        
        res="SAFE"
        return res
    elif int(pred[0]) == 1.0:
        
        res="DEFACEMENT"
        return res
    elif int(pred[0]) == 2.0:
        res="PHISHING"
        return res
        
    elif int(pred[0]) == 3.0:
        
        res="NOT SAFE"
        return res
    

    
@app.route('/url')
def render_url():
    return render_template('url.html')







# email webpage
@app.route('/email', methods=["GET","POST"])
def main_function():
    if request.method == "POST":
        text = request.form
        # print(text)
        emails = text['email']
        print(emails)
        
        list_email = [emails]
        # print(list_email)
        output = pipe.predict(list_email)[0]
        print(output)


        return render_template("show.html", prediction = output)
    
    else:
        return render_template("email.html")



if __name__ == '__main__':
    app.run(debug=True)