Email to Github Issues
======

Creates github issues from a specified email address to specified git repo.

### How do I use it?
1. Clone code in your workspace using:
```sh
$ git clone https://github.com/imsahilt/sahilt.git
```
2. Create a Personal access token [here](https://github.com/settings/applications). Do remember to give gist access to your token.
3. Enable access to unsecure apps in gmail: [here](https://www.google.com/settings/security/lesssecureapps)
4. Edit configs.py with your account details. You can also change other configs if you want.
5. And finally run it using:
```sh
$ python bot.py start
```
6. See logs in bot.log
```sh
$ tail -f bot.log
```
P.S. you can also deploy this bot on heroku: [follow these steps](https://devcenter.heroku.com/articles/getting-started-with-python)
