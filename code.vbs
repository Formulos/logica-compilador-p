Function fibonacci(n as integer) as integer

    if n = 0 then
        fibonacci = 1
    end if

    if n >0 then
        fibonacci = fibonacci(n-1)
    end if

End Function

Sub Main()
    print fibonacci(1)
End Sub