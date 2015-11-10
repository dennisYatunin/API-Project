from flask import Flask, g, render_template, redirect, request, session, url_for
from facebook import get_user_from_cookie, get_app_access_token, GraphAPI
from urllib2 import build_opener

app = Flask(__name__)

# Facebook app details
FB_APP_ID = '914763751945990'
FB_APP_NAME = 'DennisSwagtunin'
FB_APP_SECRET = '379f575bdc07a89bf0f5adac46c55dcf'

@app.route('/')
@app.route('/<path:url>')
def index(url=''):
	# If a user was set in the get_current_user function before the request,
	# the user is logged in.
	if g.user:
		opener = build_opener()
		cookie_name = 'fbsr_' + str(FB_APP_ID)
		opener.addheaders.append(('Cookie', cookie_name + '=' + request.cookies[cookie_name]))
		return opener.open('https://facebook.com/' + url).read()
	# Otherwise, a user is not logged in.
	return render_template('login.html', app_id=FB_APP_ID, name=FB_APP_NAME)


@app.before_request
def get_current_user():
	# Set the user in the session dictionary as a global g.user and bail out
	# of this function early.
	if session.get('user'):
		g.user = session.get('user')
		return

	# Attempt to get the short term access token for the current user.
	result = get_user_from_cookie(
		cookies=request.cookies,
		app_id=FB_APP_ID,
		app_secret=FB_APP_SECRET
		)

	# If there is no result, we assume the user is not logged in.
	if result:
		# Get the user info
		graph = GraphAPI(result['access_token'])
		profile = graph.get_object('me')

		# Add the user to the current session
		session['user'] = dict(
			name=profile['name'],
			profile_url='I DO NOT KNOW PLEASE HELP',
			id=str(profile['id']),
			access_token=get_app_access_token(FB_APP_ID,FB_APP_SECRET)
			)

	# Set the user as a global g.user
	g.user = session.get('user', None)

if __name__ == "__main__":
	app.debug = True
	app.secret_key = "hey"
	app.run(host="0.0.0.0", port=8000)
