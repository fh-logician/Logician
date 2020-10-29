# Logician
Logician is a boolean expression evaluation application. 
You can enter a boolean expression such as:
 * ``a or b``
 * ``alpha or beta``
 * ``a ^ ~c``
 * ``!a || !b``
 
The recognized operators include: 

| Style         | NOT   | AND   | OR     | NAND   | NOR     | XOR   | XNOR   |
|-------        |-----  |-----  |----    |------  |-----    |------ |-----   |
|C-Like         |``!``  |``&&`` |``\|\|``|``!&&`` |``!\|\|``|``^``  |``!^``  |
|English        |``not``|``and``|``or``  |``nand``|``nor``  |``xor``|``xnor``|
|Bitwise        |``~``  |``&``  |``\|``  |``~&``  |``~\|``  |``^``  |``~^``  |
|Boolean Algebra|``-``  |``*``  |``+``   |``-*``  |``-+``   |``^``  |``-^``  |

## Simplification and Truth Table
There are two fields called *Simplified Minterm* and *Simplified Maxterm* that will show the results of
a simplified boolean expression in two different styles.

For example, the expression ``(a and b) or (a and c)`` can be simplified the following ways:
 * **Simplified Minterm**: ``(a AND b) OR (a AND c)`` (which isn't really simplified)
 * **Simplified Maxterm**: ``(a AND b) OR c``
 
The simplest expression will be highlighted in green when an expression is entered.

The truth tables, which are at the bottom, will be the truth table for the entered expression and the simplest expression.

## Download

The Windows and MacOS versions of Logician can be downloaded on my [website](https://fellowhashbrown.com/downloads#logician)
