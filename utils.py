from urllib2 import urlopen, Request
from urllib import quote_plus
from json import loads
from re import search
from os import urandom

def get_salary(first_name, last_name):
    '''Returns a dictionary with the keys 'full_name' and 'salary'

    Takes in the first and last names of the teacher (first_name
    cannot be a nickname or abbreviation; otherwise, no data will
    be found).

    Uses the Citywide Payroll Database from 2014 to get his
    or her salary (a float), which is calculated per annum,
    and his or her full name, as stored in the official database.

    If the teacher cannot be found, full_name is set to the given
    first_name and last_name, and salary is set to None.
    '''
    uri = (
        'https://data.cityofnewyork.us/resource/k397-673e.json?'
        'first_name=%s&last_name=%s&agency_name=%s'
        )
    # Teachers in NYC are listed as working for the following 5 agencies:
    agency_names = (
        'DEPT OF ED PEDAGOGICAL        ',
        'DEPT OF ED PER SESSION TEACHER',
        'DEPT OF ED PER DIEM TEACHERS  ',
        'DEPT OF ED PARA PROFESSIONALS ',
        'DEPT OF ED HRLY SUPPORT STAFF '
        )
    i = 0
    
    while True:
        if i == len(agency_names):
            full_name = ' '.join(filter(None, (first_name, last_name)))
            salary = None
            return {'full_name': full_name, 'salary': salary}
        url = uri % (
        	quote_plus(first_name),
        	quote_plus(last_name),
        	quote_plus(agency_names[i])
        	)
        request = Request(url)
        request.add_header('X-App-Token', 'wLV7RwuxVb6qKDLYtE00B2eLV')
        page = urlopen(request).read()
        result = loads(page)
        if result:
            teacher_dict = result[0]
            break
        i += 1
    
    # New York has, on average, 182 school days per year and 6.59 hours per school day.
    # Source: https://nces.ed.gov/surveys/sass/tables/sass0708_035_s1s.asp
    salary = float(teacher_dict['base_salary'])
    if teacher_dict['pay_basis'] == ' per Day':
        salary *= 182
    elif teacher_dict['pay_basis'] == ' per Hour':
        salary *= 182 * 6.59
    
    if first_name:
        first = first_name
    else:
        first = teacher_dict['first_name'][0] + teacher_dict['first_name'][1:].lower()
    if 'mid_init' in teacher_dict:
        middle = teacher_dict['mid_init'] + '.'
    else:
        middle = None
    if last_name:
        last = last_name
    else:
        last = teacher_dict['last_name'][0] + teacher_dict['last_name'][1:].lower()
    full_name = ' '.join(filter(None, (first, middle, last)))
    
    return {'full_name': full_name, 'salary': salary}

def get_name_and_rating(query, high_school):
    '''Returns a dictionary with the keys 'first_name', 'last_name',
    'subject', 'rating', and 'num_ratings'.

    Takes in any string of text (hopefully the teacher's name) and
    the name of a high school.

    Scrapes ratemyteachers.com to find a teacher who works at the
    given high school and whose name is related to the query, and
    then determines the subject taught by the teacher, the teacher's
    rating (a float), and the number of students he or she was rated
    by (an int).

    If no such teacher can be found, first_name is set to the query,
    last_name is set to an empty string, subject is set to an empty
    string, rating is set to None, and num_ratings is set to None.
    '''
    uri = (
        'http://www.ratemyteachers.com/search_page?'
        'search=teachers&q=%s%%2C+%s&state=ny'
        )
    url = uri % (quote_plus(query), quote_plus(high_school))
    page = urlopen(url).read()
    try:
        first_teacher_match = search(
            (
                '(?s)<h3 class=\'name\'>.*?target=\'_blank\'>\n(.*?)'
                '</a>\n</h3>.*?<span>\nRating:\n(.*?)ratings\n</span>'
                ), page
            )
        title_text = first_teacher_match.group(1).split('\n')
        full_name = title_text[0].split(' ')
        first_name = full_name[0]
        last_name = full_name[-1]
        subject = title_text[1][3:-8]
        rating_text = first_teacher_match.group(2).split('\n')
        rating = float(rating_text[0])
        num_ratings = int(rating_text[2])
    except:
        first_name = query
        last_name = ''
        subject = ''
        rating = None
        num_ratings = None
    return {
        'first_name': first_name, 'last_name': last_name, 'subject': subject,
        'rating': rating, 'num_ratings': num_ratings
        }

def get_rating(name, high_school):
    '''Returns a dictionary with the keys 'subject', 'rating',
    and 'num_ratings'.

    Takes in the name of the teacher and his or her high school.

    Scrapes ratemyteachers.com to determine the subject taught by the
    teacher, the teacher's rating (a float), and the number of students
    he or she was rated by (an int).

    If the teacher cannot be found, subject is set to an empty string,
    rating is set to None, and num_ratings is set to None.
    '''
    uri = (
        'http://www.ratemyteachers.com/search_page?'
        'search=teachers&q=%s%%2C+%s&state=ny'
        )
    url = uri % (quote_plus(name), quote_plus(high_school))
    page = urlopen(url).read()
    try:
        first_teacher_match = search(
            (
                '(?s)<h3 class=\'name\'>.*?target=\'_blank\'>\n(.*?)'
                '</a>\n</h3>.*?<span>\nRating:\n(.*?)ratings\n</span>'
                ), page
            )
        title_text = first_teacher_match.group(1).split('\n')
        subject = title_text[1][3:-8]
        rating_text = first_teacher_match.group(2).split('\n')
        rating = float(rating_text[0])
        num_ratings = int(rating_text[2])
    except:
        subject = ''
        rating = None
        num_ratings = None
    return {'subject': subject, 'rating': rating, 'num_ratings': num_ratings}

def get_photo(name, high_school):
    '''Returns a URL string for the most probable photo of the
    specified teacher.
	
    Takes in any string of text (hopefully the teacher's name) and
    the name of a high school.
	
    Uses the Google Image Search API and extracts the URL for the 
    first image result.
    '''
    namesplit = name.split(" ")
    querylist = []
    querylist.append(namesplit[0])
    querylist.append(namesplit[-1])
    querylist += high_school.split(" ")
    querystring = ""
    for i in querylist:
        querystring += i + "+"
    querystring = querystring[:-1]
    querystring = quote_plus(querystring)
    inputurl = "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + querystring +"&start=0"
    response = Request(inputurl)
    return loads(urlopen(response).read())['responseData']['results'][0]['url']

def get_efficiency(salary, rating):
    '''Returns the efficiency of a teacher.

    Efficiency is calculated as the fraction of the maximum rating
    divided by the fraction of the maximum salary.

    If the salary or rating is None (or 0), the efficiency is set to None.
    '''
    if not salary or not rating:
        return None
    return (rating / 5) / (salary / 100049)

def get_secret_key():
    '''Returns a key that may be used to secure a Flask session

    The key is a 32-character string generated with the os.urandom function.
    '''
    return urandom(32)
