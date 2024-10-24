---
layout: default
---

# Navigation<br>
### **[Work History](WorkHistory.md)   [Education](Education.md)   [Achivements](Achivements.md)   [Guides](Guides.md)**<br>

**[BACK TO INDEX](index.md)**


## Windows winks
**Change the Color of the Command Prompt Window**

> Launch CMD and Right-click on the title bar
>Click on “Properties” and in the separate window that opens, click on “Colors”`
>Here you can choose the colors for the screen text or background as well as for the popup text and background, and also change the transparency of the CMD window
>After you’re done choosing the most fitting colors for your personality, Click OK
<br>

**List Every Driver Installed on Your Windows 10 PC**<br>
> driverquery /FO list /v in CMD

**Windows Recall**<br>
To see if it is on. Go in as Administrator into Powershell. change <username> to your own user (Like john, Mary, Pekka, Jussi):<br>
>Get-Mailbox -Identity <username> | Select-Object -ExpandProperty RecallEnabled<br><br>

**To Disable it**<br>
>Set-Mailbox -Identity <username> -RecallEnabled $false<br><br>
# Header 1

This is a normal paragraph following a header. GitHub is a code hosting platform for version control and collaboration. It lets you and others work together on projects from anywhere.

## Header 2

> This is a blockquote following a header.
>
> When something is important enough, you do it even if the odds are not in your favor.

### Header 3

```js
// Javascript code with syntax highlighting.
var fun = function lang(l) {
  dateformat.i18n = require('./lang/' + l)
  return true;
}
```

```ruby
# Ruby code with syntax highlighting
GitHubPages::Dependencies.gems.each do |gem, version|
  s.add_dependency(gem, "= #{version}")
end
```

#### Header 4

*   This is an unordered list following a header.
*   This is an unordered list following a header.
*   This is an unordered list following a header.

##### Header 5

1.  This is an ordered list following a header.
2.  This is an ordered list following a header.
3.  This is an ordered list following a header.

###### Header 6

| head1        | head two          | three |
|:-------------|:------------------|:------|
| ok           | good swedish fish | nice  |
| out of stock | good and plenty   | nice  |
| ok           | good `oreos`      | hmm   |
| ok           | good `zoute` drop | yumm  |

### There's a horizontal rule below this.

* * *

### Here is an unordered list:

*   Item foo
*   Item bar
*   Item baz
*   Item zip

### And an ordered list:

1.  Item one
1.  Item two
1.  Item three
1.  Item four

### And a nested list:

- level 1 item
  - level 2 item
  - level 2 item
    - level 3 item
    - level 3 item
- level 1 item
  - level 2 item
  - level 2 item
  - level 2 item
- level 1 item
  - level 2 item
  - level 2 item
- level 1 item

### Small image

![Octocat](https://github.githubassets.com/images/icons/emoji/octocat.png)

### Large image

![Branching](https://guides.github.com/activities/hello-world/branching.png)


### Definition lists can be used with HTML syntax.

<dl>
<dt>Name</dt>
<dd>Godzilla</dd>
<dt>Born</dt>
<dd>1952</dd>
<dt>Birthplace</dt>
<dd>Japan</dd>
<dt>Color</dt>
<dd>Green</dd>
</dl>

```
Long, single-line code blocks should not wrap. They should horizontally scroll if they are too long. This line should be long enough to demonstrate this.
```

```
The final element.
```
