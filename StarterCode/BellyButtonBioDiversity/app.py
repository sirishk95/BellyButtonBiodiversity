{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'flask_sqlalchemy'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-1-31f7a0a05321>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m     10\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     11\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mflask\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mFlask\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mjsonify\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mrender_template\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 12\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0mflask_sqlalchemy\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mSQLAlchemy\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     13\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     14\u001b[0m \u001b[0mapp\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mFlask\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0m__name__\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'flask_sqlalchemy'"
     ]
    }
   ],
   "source": [
    "import os\n",
    "\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine\n",
    "\n",
    "from flask import Flask, jsonify, render_template\n",
    "from flask_sqlalchemy import SQLAlchemy\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "\n",
    "#################################################\n",
    "# Database Setup\n",
    "#################################################\n",
    "\n",
    "app.config[\"SQLALCHEMY_DATABASE_URI\"] = \"sqlite:///db/bellybutton.sqlite\"\n",
    "db = SQLAlchemy(app)\n",
    "\n",
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "# reflect the tables\n",
    "Base.prepare(db.engine, reflect=True)\n",
    "\n",
    "# Save references to each table\n",
    "Samples_Metadata = Base.classes.sample_metadata\n",
    "Samples = Base.classes.samples\n",
    "\n",
    "\n",
    "@app.route(\"/\")\n",
    "def index():\n",
    "    \"\"\"Return the homepage.\"\"\"\n",
    "    return render_template(\"index.html\")\n",
    "\n",
    "\n",
    "@app.route(\"/names\")\n",
    "def names():\n",
    "    \"\"\"Return a list of sample names.\"\"\"\n",
    "\n",
    "    # Use Pandas to perform the sql query\n",
    "    stmt = db.session.query(Samples).statement\n",
    "    df = pd.read_sql_query(stmt, db.session.bind)\n",
    "\n",
    "    # Return a list of the column names (sample names)\n",
    "    return jsonify(list(df.columns)[2:])\n",
    "\n",
    "\n",
    "@app.route(\"/metadata/<sample>\")\n",
    "def sample_metadata(sample):\n",
    "    \"\"\"Return the MetaData for a given sample.\"\"\"\n",
    "    sel = [\n",
    "        Samples_Metadata.sample,\n",
    "        Samples_Metadata.ETHNICITY,\n",
    "        Samples_Metadata.GENDER,\n",
    "        Samples_Metadata.AGE,\n",
    "        Samples_Metadata.LOCATION,\n",
    "        Samples_Metadata.BBTYPE,\n",
    "        Samples_Metadata.WFREQ,\n",
    "    ]\n",
    "\n",
    "    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()\n",
    "\n",
    "    # Create a dictionary entry for each row of metadata information\n",
    "    sample_metadata = {}\n",
    "    for result in results:\n",
    "        sample_metadata[\"sample\"] = result[0]\n",
    "        sample_metadata[\"ETHNICITY\"] = result[1]\n",
    "        sample_metadata[\"GENDER\"] = result[2]\n",
    "        sample_metadata[\"AGE\"] = result[3]\n",
    "        sample_metadata[\"LOCATION\"] = result[4]\n",
    "        sample_metadata[\"BBTYPE\"] = result[5]\n",
    "        sample_metadata[\"WFREQ\"] = result[6]\n",
    "\n",
    "    print(sample_metadata)\n",
    "    return jsonify(sample_metadata)\n",
    "\n",
    "\n",
    "@app.route(\"/samples/<sample>\")\n",
    "def samples(sample):\n",
    "    \"\"\"Return `otu_ids`, `otu_labels`,and `sample_values`.\"\"\"\n",
    "    stmt = db.session.query(Samples).statement\n",
    "    df = pd.read_sql_query(stmt, db.session.bind)\n",
    "\n",
    "    # Filter the data based on the sample number and\n",
    "    # only keep rows with values above 1\n",
    "    sample_data = df.loc[df[sample] > 1, [\"otu_id\", \"otu_label\", sample]]\n",
    "\n",
    "    # Sort by sample\n",
    "    sample_data.sort_values(by=sample, ascending=False, inplace=True)\n",
    "\n",
    "    # Format the data to send as json\n",
    "    data = {\n",
    "        \"otu_ids\": sample_data.otu_id.values.tolist(),\n",
    "        \"sample_values\": sample_data[sample].values.tolist(),\n",
    "        \"otu_labels\": sample_data.otu_label.tolist(),\n",
    "    }\n",
    "    return jsonify(data)\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run()"
   ]
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
   "version": "3.7.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
