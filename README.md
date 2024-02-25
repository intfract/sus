# SUS

A new functional programming language!

## Get Started

1. Fork the repository or use the `git clone` command
2. Create any `*.sus` file
3. Run `src/main.py` in the terminal and pass your sus file as the first argument

```sh
cd src
python main.py my_program_name.sus
```
> Replace `my_program_name` with the name of your SUS file!

## Examples

### Assignment

SUS uses intuitive keywords such as `set` and `to` for assigning variables values. This leaves the `=` for use as a comparison operator.

```js
set x to 0
set y to x
```

> **Warning** SUS does not support negative numbers yet...

SUS stores data in a python dictionary.

```py
memory = {
    "x": Integer(0), # set x to 0
    "y": Integer(0), # set y to x
}
```

SUS also supports setting multiple variables at once.

> **Warning** This feature is unstable!

```js
set x y to "hello"
```

### Functions

Functions can pretty much do anything. Who even needs objects? SUS functions can take a fixed number of arguments and return `Integer`, `Float`, or `Text` data.

```js
set x to add(1, 1) set y to add(x, 1)
```

There are enough arithmetic and boolean functions to write basic programs. The code below shows how a *modulo* operations works.

```js
set x to 10 set y to 3 set z to add(x, multiply(-1, multiply(y, floor(multiply(x, power(y, -1))))))
```

### Input Output

SUS uses functions to control IO. However, SUS is superior to all other languages when it comes to inferencing user input. SUS can automatically convert `Text` to `Integer` or `Float` depending on the type of the first argument.

```js
set x to input(0)
output(x)
```

> 0 is an `Integer` making the value of `x` and `Integer` too

SUS can also `read` and `write` to files.

```js
set file to read("one.sus")
write("two.sus", file)
```

```js
set x to []
set i to 0
set z to input(0)
repeat z {
    set x to append(x, i)
    set i to add(i, 1)
    output(i)
}
set y to []
repeat (add(z, -1)) {
    set y to append(y, pop(x, -1))
}
sort(y)
```

### Loops

While loops execute code if an expression evaluates to a **positive** number.

```js
set i to 3
while (i) {
    output(i)
    set i to add(i, -1)
}
```

Loops can also be used as **conditional** `if` statements by repeating a loop 0 times or 1 time. The `repeat` keyword will repeat a code block a certain number of times.

```js
set i to 0 repeat (2) { set i to add(i, 1) }
set x to 0 repeat (add(1,1)) { set x to add(x, 1) }
set b to "false" repeat (xor(0, 1)) { set b to "true" }
```

### Lists

There are currently 4 functions for lists.

```js
set x to []
set i to 0
repeat 3 {
    set x to append(x, i)
    set i to add(i, 1)
}
set y to []
repeat 2 {
    set y to append(y, pop(x, -1))
}
sort(y)
```