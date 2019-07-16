### JS自定义字符串格式化函数
python的字符串格式化
```python
test = 'name: {name} age: {age}'
print(test.format(name='zq',age=22))
输出： name: zq age: 22
```
JS里没有这种方式，但可以自定义一个类似的方法

#### 类Python关键字参数字符串格式化函数

```js
//自定义字符处理函数---- 字符串替换格式化
String.prototype.format = function (kwargs) {
    console.log(this) // this表示调用这个函数的字符串对象 String {"nihao:{name}-{age}"}
    // 正则表达式是在/ /内表示， 正则后的g表示去this里面匹配所有的字符(执行全局匹配（查找所有匹配而非在找到第一个匹配后停止）)  i表示执行对大小写不敏感的匹配  m表示执行多行匹配
    var ret = this.replace(/\{(\w+)\}/g,function (k,m) { //k表示匹配到的字符串，m表示匹配到的分组里的值，在正则中用()表示一个分组
        console.log(k,m);  //{name} name
        return kwargs[m]  // 把匹配到的字符串用参数的值替换
    });

    return ret;  //把替换完的字符串返回
};
```
使用
```js
text = "nihao:{name}-{age}";
result = text.format({'name':'zq','age':21});
console.log(result);  // nihao:zq-21
```

#### 类Python位置参数字符串格式化函数
```js
String.prototype.format = function() {
    var e = this, len = arguments.length;
    if (len > 0) {
        for ( var d = 0; d < len; d++) {
            e = e.replace(new RegExp("\\{" + d + "\\}", "g"), arguments[d])
        }
    }
    return e;
};
```
格式化字符串string.format(arg1…)

使用
```js
for(var i = 0 ; i < l; i++){
	var h;
	h = '<option value ={0}>{1}</option>';
	h = h.format(i,'No.'+parseInt(i+1));
	console.log(h);
}
```












