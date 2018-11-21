# CCTV with raspberry pi

## required functions for CCTV
1. camera functions
2. adaptive recording functions
3. live web streaming functions

### Camera functions

### Adaptive recording functions
Approach 1. CV
Approach 2. ML

### Live web streaming functions
Web streaming by flask : flask supports streamming service by Python Generator.

#### Python Generator
Python generator is a special function or routine to control iteration efficiently. Acutally, all Generators are Iterators. Generator is simillar to a function returning arrays or lists in a regard that it has parameters and creates consequential values. However, Generator returns only one value by "yield" and this makes Generator occupy very small memory compared to Iterator.

Normal functions or iterators return all controls to the caller when they end. The same functions or iterators are executed from the scratch when they are called again. However, Generator can hold the previous works and continue its work continually. Therefore, Generator is very useful and shows great performance with small resources.

#### Flask Streaming
reference : http://flask.pocoo.org/docs/1.0/patterns/streaming/

According to Flask reference, it is recommended to use generator and direct responses. This technique is used for this. More than that, multipart responses is used for video streaming. It is because the frame should be specified. Therefore, after defining the frame, The recommended method is used.
