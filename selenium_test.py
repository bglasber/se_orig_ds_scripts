import os
import string
import random
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
    done = (i > 90)
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
    done = ( i > 90 )
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
    done = ( i > 90 )
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

def register_account_from_main_page( driver ):
    sign_in_button = driver.find_element_by_xpath("/html/body/table[1]/tbody/tr/td[2]/a[2]")
    sign_in_button.click()
    print( "On Signin page" )
    register_button = driver.find_element_by_xpath("/html/body/center[2]/a")
    register_button.click()
    print( "On Register Page" )
    table = driver.find_element_by_xpath("/html/body/form/table/tbody/tr/td")
    inp_fields = table.find_elements_by_tag_name("input")
    user = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
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

def buy_single_item( driver ):
    click_random_animal_link( driver )
    click_random_link_in_table( driver )
    click_random_link_in_table( driver )
    # get the add to cart button and click it
    add_to_cart = driver.find_element_by_xpath("/html/body/p[1]/table/tbody/tr[7]/td/a")
    add_to_cart.click()
    # click checkout
    checkout = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[2]/center/a")
    checkout.click()
    # click continue
    cont = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[2]/center[2]/a")
    cont.click()
    # click submit
    sub = driver.find_element_by_xpath("/html/body/form/p/input")
    sub.click()


os.environ['MOZ_HEADLESS'] = '1'
d = webdriver.Firefox()
go_to_main_page( d )
#do_main_page_browse( d )
#do_animal_group_browse( d )
register_account_from_main_page( d )
buy_single_item( d )
d.quit()
