from urllib2 import urlopen, Request
from json import loads
from re import search
from os import urandom

def get_rating(name, high_school):
    '''Returns a dictionary with the keys 'rating' and 'num_ratings'

    Takes in the name of the teacher and his or her high school.
    
    Scrapes ratemyteachers.com to find the teacher's rating (a float)
    and the number of students he or she was rated by (an int).
    
    If the teacher cannot be found, rating and num_ratings are set to None.
    '''
    uri = "http://www.ratemyteachers.com/search_page?search=teachers&q=%s%%2C+%s&state=ny"
    url = uri % (name.replace(' ','+'), high_school.replace(' ','+'))
    page = urlopen(url).read()
    try:
        rating_string = search('(?s)<span>\nRating:\n(.*?)ratings\n</span>',page).group(1)
        lines = rating_string.split('\n')
        rating = float(lines[0])
        num_ratings = int(lines[2])
    except:
        rating = None
        num_ratings = None
    return {'rating':rating, 'num_ratings':num_ratings}

def get_salary(first_name, last_name):
    '''Returns a dictionary with the keys 'full_name' and 'salary'

    Takes in the first and last names of the teacher.
    
    Uses the Citywide Payroll Database from 2014 to get his
    or her salary (a float), which is calculated per annum,
    and his or her full name, as stored in the official database.
    
    If the teacher cannot be found, full_name is set to the given
    first_name and last_name, and salary is set to None.
    '''
    uri = 'https://data.cityofnewyork.us/resource/k397-673e.json?first_name=%s&last_name=%s&agency_name=%s'
    agency_name = 'DEPT OF ED PEDAGOGICAL        '
    url = uri % (first_name, last_name, agency_name)
    request = Request(url)
    request.add_header('X-App-Token', 'wLV7RwuxVb6qKDLYtE00B2eLV')
    page = urlopen(request).read()
    result = loads(page)
    if not result:
        agency_name = 'DEPT OF ED PEDAGOGICAL        '
        url = uri % (first_name, last_name, agency_name)
        request = Request(url)
        request.add_header('X-App-Token', 'wLV7RwuxVb6qKDLYtE00B2eLV')
        page = urlopen(request).read()
        result = loads(page)
        if not result:
            agency_name = 'DEPT OF ED PER SESSION TEACHER'
            url = uri % (first_name, last_name, agency_name)
            request = Request(url)
            request.add_header('X-App-Token', 'wLV7RwuxVb6qKDLYtE00B2eLV')
            page = urlopen(request).read()
            result = loads(page)
            salary = float(teacher_dict['base_salary'])
            if not result:
                agency_name = ''
                url = uri % (first_name, last_name, agency_name)
                request = Request(url)
                request.add_header('X-App-Token', 'wLV7RwuxVb6qKDLYtE00B2eLV')
                page = urlopen(request).read()
                result = loads(page)
                salary = float(teacher_dict['base_salary'])
                if not result:
                    full_name = first_name + ' ' + last_name
                    salary = None
                    return {'full_name':full_name, 'salary':salary}
    # New York has, on average, 182 school days per year and 6.59 hours per school day.
    # Source: https://nces.ed.gov/surveys/sass/tables/sass0708_035_s1s.asp
    if teacher_dict['pay_basis'] == ' per Day':
        salary *= 182
    elif teacher_dict['pay_basis'] == ' per Hour':
        salary *= 182 * 6.59
    first = teacher_dict['first_name'][0] + teacher_dict['first_name'][1:].lower() + ' '
    if 'mid_init' in teacher_dict:
        middle = teacher_dict['mid_init'] + '. '
    else:
        middle = ''
    last = teacher_dict['last_name'][0] + teacher_dict['last_name'][1:].lower()
    full_name = first + middle + last
    return {'full_name':full_name, 'salary':salary}

def get_secret_key():
    '''Returns a key that may be used to secure a Flask session

    The key is a 32-character string generated with the os.urandom function.
    '''
    return urandom(32)
