"""*MongoDB* connector based on *pymongo* and *Mongoengine*

See Also
--------
pymongo
mongoengine
"""
import os
import mongoengine

MONGO_URI = 'mongodb://{username}:{password}@{host}:{port}/{db}'


def init(user, password, host, port, db, authentication_db=None, use_envvars=True):
    """Initilize Mongoengine ODM.

    Parameters
    ----------
    user : str
        Username to authenticate with.
    password : str
        User authentication password.
    host : str
        Host IP address/name.
    port : str
        Port number.
    db : str
        Database name.
    authentication_db : str or None
        Authentication databse name.
        Use `db` if `None`.
    use_envvars : bool
        If `True`, then arguments are used to lookup
        values in environmental variables.
    """
    if use_envvars:
        user = os.environ[user]
        password = os.environ[password]
        host = os.environ[host]
        port = os.environ[port]
        db = os.environ[db]
    if not authentication_db:
        authentication_db = db
    uri = MONGO_URI.format(
        username=user,
        password=password,
        host=host,
        port=port,
        db=db
    )
    mdb = mongoengine.connect(host=uri, authentication_source=authentication_db)
    return mdb
