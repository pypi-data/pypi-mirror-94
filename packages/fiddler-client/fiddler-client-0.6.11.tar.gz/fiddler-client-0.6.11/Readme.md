Fiddler Client
=============

Python client for interacting with Fiddler. Provides a user-friendly interface to our REST API and enables event
publishing for use with our monitoring features.

Requirements
------------
Requires Python >= Python-3.6.3.

Installation
------------

    $ pip3 install fiddler-client


API Example Usage
-------------
For examples of interacting with our APIs, please check out our [Quick Start Guide](https://github.com/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/Quick%20Start.ipynb) as well as our [Samples Github](https://github.com/fiddler-labs/fiddler-samples) and tutorial notebooks:

- [Setup Fiddler client](https://github.com/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/00%20Setup.ipynb)
- [How to monitor data](https://github.com/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/01%20Basic%20model%20monitoring.ipynb)
- [How to monitor with surrogate explanation](https://github.com/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/01a%20Model%20monitoring%20with%20surrogate%20explanation.ipynb)
- [How to import sklearn regression model](https://github.com/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/02%20How%20to%20upload%20a%20simple%20sklearn%20regression%20model.ipynb)
- [Debug model import problems](https://github.com/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/03%20How%20to%20debug%20model%20upload.ipynb)
- [How to generate a model from your tabular data](https://github.com/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/04%20automodel.ipynb)
- [Publish realtime events to Fiddler](https://github.com/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/06%20publish_event.ipynb)
- [How to import a model hosted on an external server](https://github.com/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/05%20Import%20model%20hosted%20outside%20of%20Fiddler.ipynb)
- [Explaining model hosted on Sagemaker](https://github.com/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/09%20Importing%20model%20hosted%20on%20Sagemaker.ipynb)
- [How to upload a keras model using tabular data with IG enabled](https://github.com/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/07%20How%20to%20upload%20a%20keras%20model%20using%20tabular%20data%20with%20IG%20enabled.ipynb)
- [How to upload a tf model using text data with IG enabled](https://github.com/fiddler-labs/fiddler-samples/blob/master/content_root/tutorial/08%20How%20to%20upload%20a%20tf%20model%20using%20text%20data%20with%20IG%20enabled.ipynb)

Version History
-------------
###0.6.11
 - #####**Features**
   - Added `fdl.publish_parquet_s3()` to client
     -  *Publishes parquet events file from S3 to Fiddler instance.
        Experimental and may be expanded in the future.*

###0.6.10
 - #####**Features**
   - Added `fdl.register_model()` to client
     -  *Register a model in fiddler. This will generate a surrogate model,
       which can be replaced later with original model.*
