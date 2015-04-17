' This is a simple Excel macro that converts a dense matrix in an Excel sheet
' to the sparse matrix format that can be processed with the iodb-Python scripts

Sub DenseToSparse()

    ' variable declarations
    Dim denseSheet, sparseSheet As String
    Dim rowCount, colCount As Integer
    Dim keyRow, keyCol As Integer
    Dim startRow, startCol As Integer
    Dim col, row As Integer
    Dim sparseRow as Long
    Dim val As Double
    Dim rowKey, colKey, sparseEntry As String
    Dim shouldWrite As Boolean

    ' TODO: you should adopt the following variable values
    ' Sheet names (values are copied from denseSheet to sparseSheet)
    denseSheet = "A_a"
    sparseSheet = "A_sparse"

    ' Numbers of rows and columns of the dense matrix
    rowCount = 430
    colCount = 430

    ' The row and column in the dense sheet with the cell-identifiers of the
    ' matrix
    keyRow = 5
    keyCol = 3

    ' The start row and column of the dense value block (the top left cell)
    startRow = 6
    startCol = 4

    sparseRow = 1
    For row = startRow To (startRow + rowCount - 1)

        rowKey = Sheets(denseSheet).Cells(row, keyCol)

        firstCol = True
        For col = startCol To (startCol + colCount - 1)

            colKey = Sheets(denseSheet).Cells(keyRow, col)
            val = Sheets(denseSheet).Cells(row, col)

            ' we force the first entries of the first column and row to be
            ' written into the sparse matrix in order to get also the row and
            ' column keys of zero-rows or -columns into the sparse matrix
            shouldWrite = (row = startRow) Or (col = startCol)

            If val <> 0 Or shouldWrite Then
                sparseEntry = """" & rowKey & """,""" & colKey & """," & val 
                Sheets(sparseSheet).Cells(sparseRow, 1) = sparseEntry
                sparseRow = sparseRow + 1
            End If

        Next col
    Next row

    MsgBox "Done: " & (sparseRow - 1) & " entries written to sheet " & sparseSheet

End Sub