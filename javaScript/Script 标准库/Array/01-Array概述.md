数组是一种类列表对象，它的原型中提供了遍历和修改元素的相关操作。JavaScript 数组的长度和元素类型都是非固定的。因为数组的长度可随时改变，并且其数据在内存中也可以不连续，所以 JavaScript 数组不一定是密集型的，这取决于它的使用方式。一般来说，数组的这些特性会给使用带来方便，但如果这些特性不适用于你的特定使用场景的话，可以考虑使用类型数组 TypedArray。

只能用整数作为数组元素的索引，而不能用字符串。后者称为关联数组。使用非整数并通过方括号或点号来访问或设置数组元素时，所操作的并不是数组列表中的元素，而是数组对象的属性集合上的变量。数组对象的属性和数组元素列表是分开存储的，并且数组的遍历和修改操作也不能作用于这些命名属性。
## Array的基本使用
创建数组
```js
var fruits = ['Apple', 'Banana'];

console.log(fruits.length);
// 2
```

通过索引访问数组元素
```js
var first = fruits[0];
// Apple

var last = fruits[fruits.length - 1];
// Banana
```

遍历数组
```js
fruits.forEach(function (item, index, array) {
    console.log(item, index);
});
// Apple 0
// Banana 1
```

添加元素到数组的末尾
```js
var newLength = fruits.push('Orange');
// newLength:3; fruits: ["Apple", "Banana", "Orange"]
```

删除数组末尾的元素
```js
var last = fruits.pop(); // remove Orange (from the end)
// last: "Orange"; fruits: "Apple", "Banana"];
```

删除数组最前面（头部）的元素
```js
var first = fruits.shift(); // remove Apple from the front
// first: "Apple"; fruits: ["Banana"];
```

添加元素到数组的头部
```js
var newLength = fruits.unshift('Strawberry') // add to the front
// ["Strawberry", "Banana"];
```

找出某个元素在数组中的索引
```js
fruits.push('Mango');
// ["Strawberry", "Banana", "Mango"]

var pos = fruits.indexOf('Banana');
// 1
```

通过索引删除某个元素
```js
var removedItem = fruits.splice(pos, 1); // this is how to remove an item

// ["Strawberry", "Mango"]
```

从一个索引位置删除多个元素
```js
var vegetables = ['Cabbage', 'Turnip', 'Radish', 'Carrot'];
console.log(vegetables); 
// ["Cabbage", "Turnip", "Radish", "Carrot"]

var pos = 1, n = 2;

var removedItems = vegetables.splice(pos, n);
// this is how to remove items, n defines the number of items to be removed,
// from that position(pos) onward to the end of array.

console.log(vegetables); 
// ["Cabbage", "Carrot"] (the original array is changed)

console.log(removedItems); 
// ["Turnip", "Radish"]
```

复制一个数组
```js
var shallowCopy = fruits.slice(); // this is how to make a copy 
// ["Strawberry", "Mango"]
```

## 创建数组（Array）的方法
```js
[element0, element1, ..., elementN]
new Array(element0, element1[, ...[, elementN]])
new Array(arrayLength)
```

## 访问数组元素
JavaScript 数组的索引是从0开始的，第一个元素的索引为0，最后一个元素的索引等于该数组的长度减1。如果指定的索引是一个无效值，JavaScript 数组并不会报错，而是会返回 undefined。

```js
var arr = ['this is the first element', 'this is the second element', 'this is the last element'];
console.log(arr[0]);              // 打印 'this is the first element'
console.log(arr[1]);              // 打印 'this is the second element'
console.log(arr[arr.length - 1]); // 打印 'this is the last element'
```

虽然数组元素可以看做是数组对象的属性，就像 toString 一样，但是下面的写法是错误的，运行时会抛出 SyntaxError 异常，而原因则是使用了非法的属性名：
```js
console.log(arr.0); // a syntax error
```

并不是 JavaScript 数组有什么特殊之处，而是因为在 JavaScript 中，以数字开头的属性不能用点号引用，必须用方括号。比如，如果一个对象有一个名为 3d 的属性，那么只能用方括号来引用它。下面是具体的例子：
```js
var years = [1950, 1960, 1970, 1980, 1990, 2000, 2010];
console.log(years.0);   // 语法错误
console.log(years[0]);  // √
   
renderer.3d.setTexture(model, 'character.png');     // 语法错误
renderer['3d'].setTexture(model, 'character.png');  // √
```
 
注意在 3d 那个例子中，引号是必须的。你也可以将数组的索引用引号引起来，比如 years[2] 可以写成 years['2']。 years[2] 中的 2 会被 JavaScript 解释器通过调用 toString 隐式转换成字符串。正因为这样，'2' 和 '02' 在 years 中所引用的可能是不同位置上的元素。而下面这个例子也可能会打印 true：
```js
console.log(years['2'] != years['02']);
```
 
类似地，如果对象的属性名称是保留字（最好不要这么做！），那么就只能通过字符串的形式用方括号来访问（从 firefox 40.0a2 开始也支持用点号访问了）：
```js
var promise = {
  'var'  : 'text',
  'array': [1, 2, 3, 4]
};

console.log(promise['var']);
```

## length 和数字下标之间的关系
JavaScript 数组的 length 属性和其数字下标之间有着紧密的联系。数组内置的几个方法（例如 join、slice、indexOf 等）都会考虑 length 的值。另外还有一些方法（例如 push、splice 等）还会改变 length 的值。
```js
var fruits = [];
fruits.push('banana', 'apple', 'peach');

console.log(fruits.length); // 3
```
    
使用一个合法的下标为数组元素赋值，并且该下标超出了当前数组的大小的时候，解释器会同时修改 length 的值：
```js
fruits[5] = 'mango';
console.log(fruits[5]); // 'mango'
console.log(Object.keys(fruits));  // ['0', '1', '2', '5']
console.log(fruits.length); // 6
```

也可以显式地给 length 赋一个更大的值：
```js
fruits.length = 10;
console.log(Object.keys(fruits)); // ['0', '1', '2', '5']
console.log(fruits.length); // 10
```

而为 length 赋一个更小的值则会删掉一部分元素：
```js
fruits.length = 2;
console.log(Object.keys(fruits)); // ['0', '1']
console.log(fruits.length); // 2
```

## 数组的静态方法
<font color=#3d7e9a size=4>Array.from()</font>
从类数组对象或者可迭代对象中创建一个新的数组实例。

<font color=#3d7e9a size=4>Array.isArray()</font>
用来判断某个变量是否是一个数组对象。

<font color=#3d7e9a size=4>Array.of()</font>
根据一组参数来创建新的数组实例，支持任意的参数数量和类型。

## 数组的方法
#### 修改器方法
下面的这些方法会改变调用它们的对象自身的值：

<font color=#3d7e9a size=4>Array.prototype.pop()</font>
删除数组的最后一个元素，并返回这个元素。

<font color=#3d7e9a size=4>Array.prototype.push()</font>
在数组的末尾增加一个或多个元素，并返回数组的新长度。

<font color=#3d7e9a size=4>Array.prototype.reverse()</font>
颠倒数组中元素的排列顺序，即原先的第一个变为最后一个，原先的最后一个变为第一个。

<font color=#3d7e9a size=4>Array.prototype.shift()</font>
删除数组的第一个元素，并返回这个元素。

<font color=#3d7e9a size=4>Array.prototype.sort()</font>
对数组元素进行排序，并返回当前数组。

<font color=#3d7e9a size=4>Array.prototype.splice()</font>
在任意的位置给数组添加或删除任意个元素。

<font color=#3d7e9a size=4>Array.prototype.unshift()</font>
在数组的开头增加一个或多个元素，并返回数组的新长度。

#### 访问方法
下面的这些方法绝对不会改变调用它们的对象的值，只会返回一个新的数组或者返回一个其它的期望值。

<font color=#3d7e9a size=4>Array.prototype.concat()</font>
返回一个由当前数组和其它若干个数组或者若干个非数组值组合而成的新数组。

<font color=#3d7e9a size=4>Array.prototype.join()</font>
连接所有数组元素组成一个字符串。

<font color=#3d7e9a size=4>Array.prototype.slice()</font>
抽取当前数组中的一段元素组合成一个新数组。

<font color=#3d7e9a size=4>Array.prototype.toString()</font>
返回一个由所有数组元素组合而成的字符串。遮蔽了原型链上的 Object.prototype.toString() 方法。

<font color=#3d7e9a size=4>Array.prototype.toLocaleString()</font>
返回一个由所有数组元素组合而成的本地化后的字符串。遮蔽了原型链上的 Object.prototype.toLocaleString() 方法。

<font color=#3d7e9a size=4>Array.prototype.indexOf()</font>
返回数组中第一个与指定值相等的元素的索引，如果找不到这样的元素，则返回 -1。

<font color=#3d7e9a size=4>Array.prototype.lastIndexOf()</font>
返回数组中最后一个（从右边数第一个）与指定值相等的元素的索引，如果找不到这样的元素，则返回 -1。

#### 迭代方法
在下面的众多遍历方法中，有很多方法都需要指定一个回调函数作为参数。在每一个数组元素都分别执行完回调函数之前，数组的length属性会被缓存在某个地方，所以，如果你在回调函数中为当前数组添加了新的元素，那么那些新添加的元素是不会被遍历到的。此外，如果在回调函数中对当前数组进行了其它修改，比如改变某个元素的值或者删掉某个元素，那么随后的遍历操作可能会受到未预期的影响。总之，不要尝试在遍历过程中对原数组进行任何修改，虽然规范对这样的操作进行了详细的定义，但为了可读性和可维护性，请不要这样做。

<font color=#3d7e9a size=4>Array.prototype.forEach()</font></font>
为数组中的每个元素执行一次回调函数。

<font color=#3d7e9a size=4>Array.prototype.every()</font>
如果数组中的每个元素都满足测试函数，则返回 true，否则返回 false。

<font color=#3d7e9a size=4>Array.prototype.some()</font>
如果数组中至少有一个元素满足测试函数，则返回 true，否则返回 false。

<font color=#3d7e9a size=4>Array.prototype.filter()</font>
将所有在过滤函数中返回 true 的数组元素放进一个新数组中并返回。

<font color=#3d7e9a size=4>Array.prototype.map()</font>
返回一个由回调函数的返回值组成的新数组。

<font color=#3d7e9a size=4>Array.prototype.reduce()</font>
从左到右为每个数组元素执行一次回调函数，并把上次回调函数的返回值放在一个暂存器中传给下次回调函数，并返回最后一次回调函数的返回值。

<font color=#3d7e9a size=4>Array.prototype.reduceRight()</font>
从右到左为每个数组元素执行一次回调函数，并把上次回调函数的返回值放在一个暂存器中传给下次回调函数，并返回最后一次回调函数的返回值。














