{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: Flask-PyMongo in /Users/jiaqisong/opt/anaconda3/lib/python3.7/site-packages (2.3.0)\n",
      "Requirement already satisfied: Flask>=0.11 in /Users/jiaqisong/opt/anaconda3/lib/python3.7/site-packages (from Flask-PyMongo) (1.1.1)\n",
      "Requirement already satisfied: PyMongo>=3.3 in /Users/jiaqisong/opt/anaconda3/lib/python3.7/site-packages (from Flask-PyMongo) (3.10.1)\n",
      "Requirement already satisfied: Werkzeug>=0.15 in /Users/jiaqisong/opt/anaconda3/lib/python3.7/site-packages (from Flask>=0.11->Flask-PyMongo) (1.0.0)\n",
      "Requirement already satisfied: itsdangerous>=0.24 in /Users/jiaqisong/opt/anaconda3/lib/python3.7/site-packages (from Flask>=0.11->Flask-PyMongo) (1.1.0)\n",
      "Requirement already satisfied: Jinja2>=2.10.1 in /Users/jiaqisong/opt/anaconda3/lib/python3.7/site-packages (from Flask>=0.11->Flask-PyMongo) (2.11.1)\n",
      "Requirement already satisfied: click>=5.1 in /Users/jiaqisong/opt/anaconda3/lib/python3.7/site-packages (from Flask>=0.11->Flask-PyMongo) (7.0)\n",
      "Requirement already satisfied: MarkupSafe>=0.23 in /Users/jiaqisong/opt/anaconda3/lib/python3.7/site-packages (from Jinja2>=2.10.1->Flask>=0.11->Flask-PyMongo) (1.1.1)\n"
     ]
    }
   ],
   "source": [
    "!pip install Flask-PyMongo"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "ename": "SyntaxError",
     "evalue": "invalid syntax (<ipython-input-2-ed0454cc5ff3>, line 2)",
     "output_type": "error",
     "traceback": [
      "\u001b[0;36m  File \u001b[0;32m\"<ipython-input-2-ed0454cc5ff3>\"\u001b[0;36m, line \u001b[0;32m2\u001b[0m\n\u001b[0;31m    from Flask-PyMongo\u001b[0m\n\u001b[0m              ^\u001b[0m\n\u001b[0;31mSyntaxError\u001b[0m\u001b[0;31m:\u001b[0m invalid syntax\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask, render_template, redirect\n",
    "from Flask-PyMongo\n",
    "import PyMongo\n",
    "import scrape_mars\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "# set up mongo connection and define document\n",
    "mongo = PyMongo(app, uri=\"mongodb://localhost:27017/mars_db\")\n",
    "\n",
    "\n",
    "@app.route(\"/\")\n",
    "def home():\n",
    "    mars_data = mongo.db.mars.find_one()\n",
    "    return render_template(\"index.html\", mars  = mars_data)\n",
    "\n",
    "\n",
    "@app.route(\"/scrape\")\n",
    "def scraper():\n",
    "    mars = mongo.db.mars\n",
    "    mars_data = scrape_mars.scrape()\n",
    "    mars.update({},mars_data, upsert = True)\n",
    "    return redirect(\"/\",code=302)\n",
    "\n",
    "@app.route(\"/images\")\n",
    "def images():\n",
    "    mars_data = mongo.db.mars.find_one()\n",
    "    return render_template(\"image.html\", mars  = mars_data)\n",
    "\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
