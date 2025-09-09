# first index dictates size of matrix, (width,depth)
#   each index must be a list for each row
#       each row much match the number of columns for entries
#   will throw error if data doesn't match size requirements of the matrix
# returns cleaned matrix values

from typing import Literal

def matrix_data(matrix_results:list, isnegative:bool=False)-> list:
    """
    Attempts to normalize input matrix data
    
    ---
    
    First index in the list must be the dimensions of the matrix. 
    i.e. [1,1]
    
    isnegative checks if matrix needs inverted. Default is assumed False (positive).

    ---

    Example:

      \t⎡ 1, 2, 3⎤\n
    A=\t⎢ 4, 5, 6⎥\n
      \t⎣ 7, 8, 9⎦\n

    Is equal to:

    A= [[3,3], [1,2,3][4,5,6][7,8,9]]

    ---

    Run function:

    matrix_data(a, False)
    """
    
    #region Clean dimensions from data
    mheight, mwidth= matrix_results[0]
    if not isinstance(mwidth,int):
        raise TypeError("Please ensure the width dimension is an integer")
    if not isinstance(mheight,int):
        raise TypeError("Please ensure the height dimension is an integer")

    if mwidth<1:
        raise ValueError("Width indicated is not a valid size. Minimum width must be 1")
    if mheight<1:
        raise ValueError("Height indicated is not a valid size. Minimum height must be 1")
    #endregion Clean dimensions from data
    #region Account for state
    mstate= "negative" if isnegative is True else "positive"
    #endregion Account for state
    
    input_format:tuple=(["width","depth"],"[contents],[in],[matrix]")
    
    #region Confirm dimensions
    if len(matrix_results)-(len(input_format)-1) != mheight:
        raise ValueError("Matrix results do NOT match number of rows indicated in the first entry")
    
    confirmed_matrix:list=[[mwidth,mheight],]
    for index,row in enumerate(matrix_results[len(input_format)-1:]):
        if len(row)<mwidth:
            raise ValueError(f"Matrix results contain too few columns in row {index+1}")
        elif len(row)>mwidth:
            raise ValueError(f"Matrix results contain too many columns in row {index+1}")
            
        new_rcontents:list= []
        for column, data in enumerate(row):
            if not isinstance(data,(int,float)):
                raise ValueError(f"Non-valid data({data}) found in row({index+1}), column({column+1})")
            if mstate=="negative":
                new_value= -data
                new_rcontents.append(new_value)
        if new_rcontents!=[]:
            row= new_rcontents
        confirmed_matrix.append(row)
    #endregion Confirm dimensions
    return confirmed_matrix

def addition(matrix_a,matrix_b)-> list:
    """Attempts to add to matrices together"""

    ma_dimensions,ma_contents= matrix_a[0],matrix_a[1:]
    mb_dimsensions,mb_contents= matrix_b[0],matrix_b[1:]

    if ma_dimensions!=mb_dimsensions:
        raise ValueError(
            "Dimensions of matrix A does NOT match dimension size of matrix B."+\
            "\nPlease ensure they are both of the same size."
            )

    mresults:list=[ma_dimensions,]
    for ma_index,ma_row in enumerate(ma_contents):
        row_results=[]
        for ma_column,ma_contents in enumerate(ma_row):
            content_a= ma_contents
            content_b= mb_contents[ma_index][ma_column]
            content_results= content_a+content_b

            row_results.append(content_results)
        mresults.append(row_results)
    
    return matrix_data(mresults)
def subtraction(matrix_a,matrix_b)-> list:
    """Attempts to subtract to matrices together"""

    ma_dimensions,ma_contents= matrix_a[0],matrix_a[1:]
    mb_dimsensions,mb_contents= matrix_b[0],matrix_b[1:]

    if ma_dimensions!=mb_dimsensions:
        raise ValueError(
            "Dimensions of matrix A does NOT match dimension size of matrix B."+\
            "\nPlease ensure they are both of the same size."
            )

    mresults:list=[ma_dimensions,]
    for ma_index,ma_row in enumerate(ma_contents):
        row_results=[]
        for ma_column,ma_contents in enumerate(ma_row):
            content_a= ma_contents
            content_b= mb_contents[ma_index][ma_column]
            content_results= content_a-content_b

            row_results.append(content_results)
        mresults.append(row_results)
    
    return matrix_data(mresults)

def transpose(matrix)-> list:
    """
    Swap rows and columns
    """

    mdimensions, mcontents= matrix[0],matrix[1:]

    temp_table:dict= {}
    for index, row in enumerate(mcontents):
        for column, contents in enumerate(row):
            
            try:
                temp_table[column][index]=contents
            except Exception:
                temp_table[column]={index:contents}

    new_matrix:list= [mdimensions,]
    for w in range(mdimensions[0]):
        new_rcontents:list= []
        for h in range(mdimensions[1]):
            new_rcontents.append(temp_table[w][h])
        new_matrix.append(new_rcontents)

    return matrix_data(new_matrix)

def multscalar(constant:int,matrix_a)-> list:
    """Attempts to multiply a matrix by a constant"""

    ma_dimensions,ma_contents= matrix_a[0],matrix_a[1:]


    mresults:list=[ma_dimensions,]
    for ma_index,ma_row in enumerate(ma_contents):
        row_results=[]
        for ma_column,ma_contents in enumerate(ma_row):
            row_results.append(round(constant*ma_contents,8))
        mresults.append(row_results)
    
    return matrix_data(mresults)
def multiplication(matrix_a,matrix_b)-> list:
    """Attempts to multiply a matrix by a matrix"""
    # resulting matrix width is determined by matrix B's width
    # resulting matrix height is determined by matrix A's height

    ma_dimensions,ma_contents= matrix_a[0],matrix_a[1:]

    matrix_bT:list= transpose(matrix_b)
    mb_dimsensions,mb_contents= matrix_bT[0],matrix_bT[1:]
    # multiply 1st row by each column in other matrix
    new_contents:list=[]
    for ma_index, ma_row in enumerate(ma_contents):
        new_row:list=[]
        for mb_index, mb_row in enumerate(mb_contents):
            temp_row:list=[]
            for value_a,value_b in list(zip(ma_row,mb_row)):
                temp_row.append(round(value_a*value_b,8))
            new_row.append(sum(temp_row))
        new_contents.append(new_row)

    # inserts the measured row and column count
    new_contents.insert(0,[len(new_contents),len(new_contents[0])])
    return matrix_data(new_contents)
            
    #   sum 1st row results & store in return value
    # repeat for each corresponding row until exhausted

def matrix_identity(rows:int=2)-> list:
    """
    Equivalent to the value 1
    
    ---

    - Will always be square

    - Minimum size must be 1x1
    """

    if rows<1:
        raise ValueError(f"Minimum valid size is a 1x1, not {rows}")

    mdimensions:list= [rows,rows]
    mcontents= [mdimensions]
    for row in range(rows):
        new_row:list=[]
        for column in range(rows):
            new_value=0 if row!=column else 1
            new_row.append(new_value)
        mcontents.append(new_row)
    return matrix_data(mcontents)

def determinant(matrix)-> int:
    """
    Attempts to find the value of the matrix
    
    NOTE: Must be a square matrix (i.e. 2x2)
    """
    # Work copied from https://stackoverflow.com/questions/71584302/matrix-determinant
    # Thank you for making this easy to use

    def det(contents):
        row = len(m_contents)
        col = len(m_contents[0])

        if (row,col) == (1,1):
            return contents[0][0]
        # hard coding for 2x2
        elif (row,col) == (2,2):
            return contents[0][0]*contents[1][1]-contents[0][1]*contents[1][0]
        # using sarrus method to solve for 3x3, it's a little faster.
        elif (row,col) == (3,3):
            contents1 = m_contents[:]
            # Extending matrix to use Sarrus Rule.
            for i in range(row-1):
                _col= []
                for j in range(col):
                    _col.append(contents1[i][j])
                contents1.append(_col)
            # Calculating Determinant
            # Adding part
            add_pointers= [(i, i) for i in range(row)]
            result= 0
            for pointer in range(row):
                temp= 1
                for tup in add_pointers:
                    i,j= tup
                    temp*= contents1[i+pointer][j]
                result+= temp
            # Subtracting part
            sub_pointers= [((row-1)-i, 0+i) for i in range(row)]
            for pointers in range(row):
                temp= 1
                for tup in sub_pointers:
                    i,j= tup
                    temp*= contents1[i+pointers][j]
                result-= temp
            return result
        else:
            sign= -1
            result= 0
            row1= [contents[0][i] * (sign ** i) for i in range(col)]
            for x, y in enumerate(row1):
                mat = contents[:][1:]
                sub_contents = [[mat[i][j] for j in range(col) if j != x] for i in range(row - 1)]
                result+= y*det(sub_contents)
            return result
    
    m_dimensions, m_contents= matrix[0],matrix[1:]
    width,height= m_dimensions

    if width!=height:
        raise ValueError(
            "Please ensure your input is a square matrix."+\
            f" Your current detected dimensions are ({m_dimensions[0]}x{m_dimensions[1]})"
            )
    elif width<1 or height<1:
        raise ValueError(
            "Please ensure your input minimum size is a (1x1)."+\
            f" Your current detected dimensions are ({m_dimensions[0]}x{m_dimensions[1]})"
            )

    if width==1:
        return m_contents[0][0]
    return det(m_contents)
def matinv(matrix)-> list|None:
    """Returns the inverse of a matrix"""
    print(matrix)
    det:int|float=determinant(matrix)
    detinv:int|float= round(1/det,8)
    temp:list=matrix[1:]
    for index,row in enumerate(matrix[1:]):
        for column,value in enumerate(row):
            if index==0 and column==0:
                temp[0][0]=round(value*detinv,8)
            elif index%2==0 and column%2!=0:
                temp[index][column]=round(-value*detinv,8)
            elif index%2!=0 and column%2==0:
                temp[index][column]=round(-value*detinv,8)
            else:
                temp[index][column]=round(value*detinv,8)
    temp.insert(0,matrix[0])
    
    print()
    new_matrix=[temp[0],]
    new_contents=[]
    for row in temp[1:]:
        new_contents.append(row[::-1])
    new_matrix=transpose(new_matrix+new_contents[::-1])
    print()
    
            

    return None if det==0 else matrix_data(
        multiplication(
            matrix,
            [[2, 2], [0.6, -0.7], [-0.2, 0.4]],
            )
        )

raw_matrix_A= [[2,2], [4,7],[2,6]]
cleaned_matrix_A:list= matrix_data(raw_matrix_A, False)

raw_matrix_B= [[3,1], [4],[5],[6]]
cleaned_matrix_B:list= matrix_data(raw_matrix_B, False)

print(
    f"{matinv(cleaned_matrix_A)}",
    sep="\n"
    )