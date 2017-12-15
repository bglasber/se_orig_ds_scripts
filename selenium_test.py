import os
import string
import random
import psycopg2
import threading
from selenium import webdriver


def click_random_animal_link( driver ):
    # Get center
    c = driver.find_element_by_xpath("/html/body/center")
    # Get "a" tags (birds,fish,etc)
    links = c.find_elements_by_tag_name("a")
    rand_link = random.randint(0, len(links)-1)
    link = links[rand_link]
    print( "Clicking on rand_animal link: {}".format( link.text ) )
    link.click()

def click_random_link_in_table( driver ):
    tbody = driver.find_element_by_xpath("/html/body/table[3]/tbody")
    links = tbody.find_elements_by_tag_name("a")
    links = [ link for link in links if not link.find_elements_by_tag_name("img") ]
    rand_link = random.randint(0, len(links)-1)
    link = links[rand_link]
    print( "Clicking on table link: {}".format( link.text ) )
    link.click()

def do_main_page_browse( driver ):
    click_random_animal_link( driver )

def do_animal_group_browse( driver ):
    h2 = driver.find_elements_by_tag_name("h2")[0]
    print( "Browsing {} Page".format( h2.text ) )
    i = random.randint(1,100)
    done = (i > 80)
    if done:
        # Pick another session type
        pass
    if i > 40:
        # Pick a link in the bar
        click_random_link_in_table( driver )
        do_animal_product_browse( driver )
    else:
        # Pick one of the links in the table
        click_random_animal_link( driver )
        do_animal_group_browse( driver )

def do_animal_product_browse( driver ):
    f = driver.find_element_by_xpath("/html/body/center[2]/b/font")
    print( "On Product Page: {}".format( f.text ) )

    i = random.randint(1,100)
    done = ( i > 80 )
    if done:
        # Pick another session type
        pass
    if i > 40:
        # There are two links for each item, one which browses and one which adds to cart
        # Since we are just browsing, don't try to add
        tbody = driver.find_element_by_xpath("/html/body/table[3]/tbody")
        links = tbody.find_elements_by_tag_name("a")
        links = [ link for link in links if not link.find_elements_by_tag_name("img") ]
        rand_link = random.randint(0, len(links)-1)
        link = links[rand_link]

        print( "Clicking on table link: {}".format( link.text ) )
        link.click()
        do_animal_item_browse( driver )
    else:
        # Pick a link in the bar
        click_random_animal_link( driver )
        do_animal_group_browse( driver )
    
def do_animal_item_browse( driver ):
    f = driver.find_element_by_xpath("/html/body/p[1]/table/tbody/tr[1]/td")
    print( "Browsing item: {}".format( f.text ) )

    i = random.randint(1,100)
    done = ( i > 80 )
    if done:
        # Pick another session type
        pass
    else:
        click_random_animal_link( driver )
        do_animal_group_browse( driver )

def go_to_main_page( driver ):
    driver.get("http://localhost:8080/jpetstore")
    print( "Loaded webpage" )
    e = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td/p[3]/a")
    e.click()
    print( "Clicked entry" )

def click_register_button( driver ):
    register_button = driver.find_element_by_xpath("/html/body/center[2]/a")
    register_button.click()
    print( "On Register Page" )

def create_user_on_register_page( driver ):
    table = driver.find_element_by_xpath("/html/body/form/table/tbody/tr/td")
    inp_fields = table.find_elements_by_tag_name("input")
    user = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(15))
    first = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    last = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    email = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + "@gmail.com"
    phone = ''.join(random.choice(string.digits) for _ in range(10))
    
    inp_fields[0].send_keys( user ) # username
    inp_fields[1].send_keys( user ) # password
    inp_fields[2].send_keys( user ) # password repeat
    inp_fields[3].send_keys( first ) # first name
    inp_fields[4].send_keys( last ) # last name
    inp_fields[5].send_keys( email ) # email
    inp_fields[6].send_keys( phone ) # phone
    inp_fields[7].send_keys( "133 addr lane" )
    inp_fields[8].send_keys( "Unit 12" )
    inp_fields[9].send_keys( "Unit 12" )
    inp_fields[10].send_keys( "Manhattan" )
    inp_fields[11].send_keys( "NY" )
    inp_fields[12].send_keys( "012345" )
    inp_fields[13].send_keys( "United States" )

    sub = driver.find_element_by_xpath("/html/body/form/center/input")
    sub.click()
    
    print( "Created User: {}".format( user ) )

def click_signin( driver ):
    sign_in_button = driver.find_element_by_xpath("/html/body/table[1]/tbody/tr/td[2]/a[2]")
    sign_in_button.click()
    print( "On Signin page" )

def register_account_from_main_page( driver ):
    click_signin( driver )
    click_register_button( driver )
    create_user_on_register_page( driver )

def do_checkout( driver ):
    # click checkout
    checkout = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[2]/center/a")
    checkout.click()
    # click continue
    cont = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[2]/center[2]/a")
    cont.click()
    print( "Checked out!" )

def click_submit( driver ):
    sub = driver.find_element_by_xpath("/html/body/form/p/input")
    sub.click()
    print( "Submitted!" )

def signout( driver ):
    so = driver.find_element_by_xpath("/html/body/table[1]/tbody/tr/td[2]/a[2]")
    so.click()
    print( "Signed out!" )

def buy_single_item_preamble( driver ):
    click_random_animal_link( driver )
    click_random_link_in_table( driver )
    click_random_link_in_table( driver )
    # get the add to cart button and click it
    add_to_cart = driver.find_element_by_xpath("/html/body/p[1]/table/tbody/tr[7]/td/a")
    add_to_cart.click()
    do_checkout( driver )

def register_then_buy_single_item( driver ):
    register_account_from_main_page( driver )
    buy_single_item_preamble( driver )
    click_submit( driver )

def do_signin( driver, user ):
    tbody = driver.find_element_by_xpath("/html/body/form/table/tbody")
    inp = tbody.find_elements_by_tag_name("input")
    print( "Found a bunch of inps: {}".format( len(inp) ) )
    inp[0].clear()
    inp[0].send_keys( user )
    inp[1].clear()
    inp[1].send_keys( user )
    inp[2].click()
    print( "Signed in as {}!".format( user ) )

def click_cart_button( driver ):
    button = driver.find_element_by_xpath("/html/body/table[1]/tbody/tr/td[2]/a[1]")
    button.click()
    print( "Clicked Cart button" )

def get_existing_user( driver ):
    conn = psycopg2.connect("dbname=petstore user=petstore password=petstore")
    cur = conn.cursor()
    cur.execute("SELECT userid FROM account ORDER BY random() LIMIT 1")
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user[0]

def buy_single_item_then_register( driver ):
    buy_single_item_preamble( driver )
    click_register_button( driver )
    create_user_on_register_page( driver )
    # for some reason this takes you back to the main page
    click_cart_button( driver )
    do_checkout( driver )
    click_submit( driver )

def browse_session( driver ):
    go_to_main_page( driver )
    do_main_page_browse( driver )
    do_animal_group_browse( driver )

def register_purchase_session( driver ):
    go_to_main_page( driver )
    register_then_buy_single_item( driver )
    signout( driver )

def purchase_register_session( driver ):
    go_to_main_page( driver )
    buy_single_item_then_register( driver )
    signout( driver )

def login_then_purchase( driver ):
    go_to_main_page( driver )
    user = get_existing_user( driver )
    click_signin( driver )
    do_signin( driver, user )
    while True:
        buy_single_item_preamble( driver )
        click_submit( driver )
        i = random.randint(1,100)
        done = (i > 70)
        if done:
            break
    signout( driver )

def do_endless_session(i):
    os.environ['MOZ_HEADLESS'] = '1'
    d = webdriver.Firefox()
    while True:
        i = random.randint(1,100)
        try:
            if i > 75:
                browse_session( d )
            elif i > 50:
                register_purchase_session( d )
            elif i > 25:
                purchase_register_session( d )
            else:
                login_then_purchase( d )
        except:
            
            d = webdriver.Firefox()

    d.quit()

for i in range(10):
    t = threading.Thread(target=do_endless_session, args=(i,))
    t.start()
do_endless_session()
