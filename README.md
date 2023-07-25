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

### Loops

Loops can also be used as **conditional** `if` statements. The `repeat` keyword will repeat a code block a certain number of times.

```js
set i to 0 repeat (2) { set i to add(i, 1) }
set x to 0 repeat (add(1,1)) { set x to add(x,1) }
set b to "false" repeat (xor(0, 1)) { set b to "true" }
```