function soma(h as Integer,m AS BOOLEAN) as Integer
    soma = h
End Function

Sub Main()
    Dim a as Integer
    a = 1

    a = a +soma(a,true)
    print a

End Sub
