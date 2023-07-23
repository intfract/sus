# SUS

A new functional programming language!

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
    "x": Integer(0),
    "y": Integer(0),
}
```

SUS also supports setting multiple variables at once. 
> **Warning** This feature is unstable

```js
set x y to "hello"
```

### Functions

Functions can pretty much do anything. Who even needs objects? SUS functions can take a fixed number of arguments and return `Integer`, `Float`, or `Text` data.

```js
set x to add(1, 1) set y to add(x, 1)
```