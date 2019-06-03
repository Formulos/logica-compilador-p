function soma(h as Integer,m AS BOOLEAN) as Integer
    h = h+1
    if h < 3 then
        h = soma(h,true)
    end if
    soma = h




End Function

Sub Main()
    Dim a as Integer
    a = 1

    a = a +soma(a,true)
    print a

End Sub
