# Simple url shortening webapp running on openshift platform

change this value on source code :
>SALT = "INSERT SECURE RANDOM SALT HERE"

change username and password for mongodb :
>client = MongoClient('mongodb://username:password@%s:%s'%(MONGODB_HOST,MONGODB_PORT))
