<tokenizer>
<keyword>class</keyword>
<identifier>Main</identifier>
<symbol>{</symbol>
<keyword>function</keyword>
<keyword>void</keyword>
<identifier>main()</identifier>
<symbol>{</symbol>
<keyword>var</keyword>
<identifier>Array</identifier>
<identifier>a;</identifier>
<keyword>var</keyword>
<keyword>int</keyword>
<identifier>length;</identifier>
<keyword>var</keyword>
<keyword>int</keyword>
<identifier>i,</identifier>
<identifier>sum;</identifier>
<keyword>let</keyword>
<identifier>length</identifier>
<symbol>=</symbol>
<identifier>Keyboard.readInt("HOW</identifier>
<identifier>MANY</identifier>
<identifier>NUMBERS?</identifier>
<identifier>");</identifier>
<keyword>let</keyword>
<identifier>a</identifier>
<symbol>=</symbol>
<identifier>Array.new(length);</identifier>
<keyword>let</keyword>
<identifier>i</identifier>
<symbol>=</symbol>
<identifier>0;</identifier>
<keyword>while</keyword>
<identifier>(i</identifier>
<symbol><</symbol>
<identifier>length)</identifier>
<symbol>{</symbol>
<keyword>let</keyword>
<identifier>a[i]</identifier>
<symbol>=</symbol>
<identifier>Keyboard.readInt("ENTER</identifier>
<identifier>THE</identifier>
<identifier>NEXT</identifier>
<identifier>NUMBER:</identifier>
<identifier>");</identifier>
<keyword>let</keyword>
<identifier>i</identifier>
<symbol>=</symbol>
<identifier>i</identifier>
<symbol>+</symbol>
<identifier>1;</identifier>
<symbol>}</symbol>
<keyword>let</keyword>
<identifier>i</identifier>
<symbol>=</symbol>
<identifier>0;</identifier>
<keyword>let</keyword>
<identifier>sum</identifier>
<symbol>=</symbol>
<identifier>0;</identifier>
<keyword>while</keyword>
<identifier>(i</identifier>
<symbol><</symbol>
<identifier>length)</identifier>
<symbol>{</symbol>
<keyword>let</keyword>
<identifier>sum</identifier>
<symbol>=</symbol>
<identifier>sum</identifier>
<symbol>+</symbol>
<identifier>a[i];</identifier>
<keyword>let</keyword>
<identifier>i</identifier>
<symbol>=</symbol>
<identifier>i</identifier>
<symbol>+</symbol>
<identifier>1;</identifier>
<symbol>}</symbol>
<keyword>do</keyword>
<identifier>Output.printString("THE</identifier>
<identifier>AVERAGE</identifier>
<identifier>IS:</identifier>
<identifier>");</identifier>
<keyword>do</keyword>
<identifier>Output.printInt(sum</identifier>
<symbol>/</symbol>
<identifier>length);</identifier>
<keyword>do</keyword>
<identifier>Output.println();</identifier>
<identifier>return;</identifier>
<symbol>}</symbol>
<symbol>}</symbol>
</tokenizer>