### Why is there a nagbot directory within the "nagbot" directory?

It does look confusing however this is required if we want to be able to neatly package up nagbot. This will make it easy for others to download, install and use nagbot. See http://flask.pocoo.org/docs/0.12/tutorial/packaging/#tutorial-packaging

### How do I run it?

```
export FLASK_APP=nagbot
export FLASK_DEBUG=true
flask run -h 0.0.0.0
```

The "-h 0.0.0.0" switch tells flask to listen on all interfaces
