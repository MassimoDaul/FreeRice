"""

Author - Massimo Daul

A selenium WebDriver based tool to interact with the website freerice.com 
and answer questions correctly, restarting when question syntax becomes too difficult,
or when the url refuses another connection.

This tool is built to automate the donating rice process,
and for fun.


"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fractions import Fraction

indicator = True

while True:
    if indicator:
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get('http://freerice.com/#/basic-math-pre-algebra/16953')
    question = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "question-link")))
    question_text = question.text.replace('x', '*').split(' =')[0]

    try:
        expression = eval(question_text.split(' =')[0])
        xpath = '//a[@class="answer-item" and . = %s]' % str(expression).lstrip('0') \
            if str(expression).startswith('.') \
            else '//a[@class="answer-item" and . = %s]' % Fraction(expression).limit_denominator(10)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        WebDriverWait(driver, 5).until(EC.staleness_of(question))
        indicator = False

    except:
        driver.quit()
        indicator = True

