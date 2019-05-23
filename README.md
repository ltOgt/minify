# What is this
This lets me define and cut out the content of pages for simpler reading and archiving, which is nice.
The minimal target HTML uses [readable-css](https://github.com/nicokant/readable-css).

# How
Find the youngest child node that encapsulates all of the actual content.
Define a beautiful soup filter lambda.
```py
SWITCH = {
	"subsite.mysite.top" : lambda soup: soup.find(
		'div', id="all-content-is-here"
	).find(
		'div', {"class" : "but-actually-it-starts-here"}
	),
}
```

Run the script `$ ./minify <url>`

# OK
