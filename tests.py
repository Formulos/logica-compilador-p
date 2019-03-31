# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 13:36:00 2019

@author: Formulos
"""

import main

def test_1():
    code = "1+1"
    code +="\n"
    code = main.PrePro.filter(code)
    main.parser.token = main.tokenizer(code)
    main.parser.token.selectNext()
    assert main.parser.parseExpresion().evaluate() == eval(code)
    
def test_2():
    code = "1-1"
    code +="\n"
    code = main.PrePro.filter(code)
    main.parser.token = main.tokenizer(code)
    main.parser.token.selectNext()
    assert main.parser.parseExpresion().evaluate() == eval(code)
    
def test_3():
    code = "2*2"
    code +="\n"
    code = main.PrePro.filter(code)
    main.parser.token = main.tokenizer(code)
    main.parser.token.selectNext()
    assert main.parser.parseExpresion().evaluate() == eval(code)
    
def test_4():
    code = "2/2"
    code +="\n"
    code = main.PrePro.filter(code)
    main.parser.token = main.tokenizer(code)
    main.parser.token.selectNext()
    assert main.parser.parseExpresion().evaluate() == eval(code)
    
def test_5():
    code = "-1+1"
    code +="\n"
    code = main.PrePro.filter(code)
    main.parser.token = main.tokenizer(code)
    main.parser.token.selectNext()
    assert main.parser.parseExpresion().evaluate() == eval(code)
    
def test_6():
    code = " (3 + 2) /5"
    code +="\n"
    code = main.PrePro.filter(code)
    main.parser.token = main.tokenizer(code)
    main.parser.token.selectNext()
    assert main.parser.parseExpresion().evaluate() == eval(code)
    
def test_7():
    code = "+--++3"
    code +="\n"
    code = main.PrePro.filter(code)
    main.parser.token = main.tokenizer(code)
    main.parser.token.selectNext()
    assert main.parser.parseExpresion().evaluate() == eval(code)
    
def test_8():
    code = "3 - -2/4"
    code +="\n"
    code = main.PrePro.filter(code)
    main.parser.token = main.tokenizer(code)
    main.parser.token.selectNext()
    assert main.parser.parseExpresion().evaluate() == eval(code)
    
def test_9():
    code = "4/(1+1)*2"
    code +="\n"
    code = main.PrePro.filter(code)
    main.parser.token = main.tokenizer(code)
    main.parser.token.selectNext()
    assert main.parser.parseExpresion().evaluate() == eval(code)
    
def test_10():
    code = "11+22-33 'bla"
    code +="\n"
    code = main.PrePro.filter(code)
    main.parser.token = main.tokenizer(code)
    main.parser.token.selectNext()
    assert main.parser.parseExpresion().evaluate() == eval(code) # note: if eval returns a error it means that prepro failed
    
def test_11():
    code = "(2+3)/(5*1)"
    code +="\n"
    code = main.PrePro.filter(code)
    main.parser.token = main.tokenizer(code)
    main.parser.token.selectNext()
    assert main.parser.parseExpresion().evaluate() == eval(code)

def test_12():
    code = "1+1 \n 'bla"
    code +="\n"
    code = main.PrePro.filter(code)
    main.parser.token = main.tokenizer(code)
    main.parser.token.selectNext()
    assert main.parser.parseExpresion().evaluate() == eval(code)