# Obsidian Bases Function Reference

Complete reference for all functions available in Obsidian Bases formulas.

## Global Functions

### `now()`
Returns the current date and time.

```yaml
formula: "now()"
# Returns: 2024-01-15T14:30:00
```

### `date(string)`
Parses a date string into a date object.

```yaml
formula: 'date("2024-01-15")'
formula: 'date("January 15, 2024")'
```

### `if(condition, thenValue, elseValue)`
Conditional expression returning one of two values.

```yaml
formula: 'if(status == "done", "Complete", "Pending")'
formula: 'if(priority > 3, "High", if(priority > 1, "Medium", "Low"))'
```

### `min(value1, value2, ...)`
Returns the minimum value from arguments.

```yaml
formula: "min(score1, score2, score3)"
formula: "min(due, deadline)"
```

### `max(value1, value2, ...)`
Returns the maximum value from arguments.

```yaml
formula: "max(rating, 0)"
formula: "max(progress, 100)"
```

### `link(path)`
Creates a link to a note.

```yaml
formula: 'link("Notes/Index")'
formula: "link(project)"
```

### `image(path)`
Displays an image from a path property.

```yaml
formula: "image(cover)"
formula: 'image("Attachments/logo.png")'
```

### `default(value, fallback)`
Returns fallback if value is null/undefined.

```yaml
formula: 'default(status, "Unknown")'
formula: "default(rating, 0)"
```

## String Functions

### `.upper()`
Converts string to uppercase.

```yaml
formula: "file.name.upper()"
# "My Note" → "MY NOTE"
```

### `.lower()`
Converts string to lowercase.

```yaml
formula: "status.lower()"
# "In Progress" → "in progress"
```

### `.trim()`
Removes leading/trailing whitespace.

```yaml
formula: "title.trim()"
```

### `.contains(substring)`
Returns true if string contains substring.

```yaml
formula: 'file.name.contains("Project")'
```

### `.startsWith(prefix)`
Returns true if string starts with prefix.

```yaml
formula: 'file.path.startsWith("Projects/")'
```

### `.endsWith(suffix)`
Returns true if string ends with suffix.

```yaml
formula: 'file.name.endsWith(".md")'
```

### `.replace(old, new)`
Replaces occurrences of old with new.

```yaml
formula: 'status.replace("-", " ")'
# "in-progress" → "in progress"
```

### `.split(separator)`
Splits string into a list.

```yaml
formula: 'tags.split(", ")'
# "a, b, c" → ["a", "b", "c"]
```

### `.slice(start, end)`
Extracts a substring by index.

```yaml
formula: "title.slice(0, 20)"
# First 20 characters
```

### `.length`
Returns the character count.

```yaml
formula: "description.length"
```

### `.match(regex)`
Tests string against regular expression.

```yaml
formula: 'title.match("^[A-Z]")'
# True if starts with capital letter
```

## Number Functions

### `.round(decimals)`
Rounds to specified decimal places.

```yaml
formula: "average.round(2)"
# 3.14159 → 3.14
```

### `.floor()`
Rounds down to nearest integer.

```yaml
formula: "score.floor()"
# 3.9 → 3
```

### `.ceil()`
Rounds up to nearest integer.

```yaml
formula: "score.ceil()"
# 3.1 → 4
```

### `.abs()`
Returns absolute value.

```yaml
formula: "difference.abs()"
# -5 → 5
```

### `.toFixed(decimals)`
Formats number with fixed decimal places.

```yaml
formula: "price.toFixed(2)"
# 9.5 → "9.50"
```

## Date Functions

### `.format(pattern)`
Formats date using pattern.

```yaml
formula: 'date.format("YYYY-MM-DD")'
formula: 'due.format("MMM DD, YYYY")'
formula: 'created.format("dddd, MMMM Do")'
```

**Pattern tokens:**
- `YYYY` - 4-digit year
- `YY` - 2-digit year
- `MM` - Month (01-12)
- `MMM` - Month short name (Jan)
- `MMMM` - Month full name (January)
- `DD` - Day of month (01-31)
- `Do` - Day with ordinal (1st, 2nd)
- `dddd` - Weekday name (Monday)
- `ddd` - Weekday short (Mon)
- `HH` - Hour 24h (00-23)
- `hh` - Hour 12h (01-12)
- `mm` - Minutes (00-59)
- `ss` - Seconds (00-59)
- `A` - AM/PM

### `.fromNow()`
Returns relative time from now.

```yaml
formula: "file.mtime.fromNow()"
# "2 days ago", "in 3 hours"
```

### `.toNow()`
Returns relative time to now.

```yaml
formula: "due.toNow()"
# "in 5 days", "3 hours ago"
```

### Date Arithmetic

```yaml
# Subtract dates to get duration
formula: "(due - now())"
# Returns duration object

# Access duration components
formula: "(due - now()).days"
formula: "(due - now()).hours"
formula: "(due - now()).minutes"
formula: "(due - now()).seconds"

# Round duration values
formula: "(due - now()).days.round(0)"
```

**Important:** Duration values must access a unit (`.days`, `.hours`, etc.) before applying number functions.

## List Functions

### `.length`
Returns item count.

```yaml
formula: "tags.length"
```

### `.first()`
Returns first element.

```yaml
formula: "items.first()"
```

### `.last()`
Returns last element.

```yaml
formula: "items.last()"
```

### `.join(separator)`
Joins list into string.

```yaml
formula: 'tags.join(", ")'
# ["a", "b", "c"] → "a, b, c"
```

### `.filter(expression)`
Filters list by condition.

```yaml
formula: 'items.filter(x => x > 5)'
formula: 'tags.filter(t => t.startsWith("project"))'
```

### `.map(expression)`
Transforms each element.

```yaml
formula: "numbers.map(x => x * 2)"
formula: "names.map(n => n.upper())"
```

### `.sort()`
Sorts list ascending.

```yaml
formula: "scores.sort()"
```

### `.reverse()`
Reverses list order.

```yaml
formula: "items.reverse()"
```

### `.unique()`
Removes duplicate values.

```yaml
formula: "categories.unique()"
```

### `.includes(value)`
Checks if list contains value.

```yaml
formula: 'tags.includes("important")'
```

### `.indexOf(value)`
Returns index of value (-1 if not found).

```yaml
formula: 'items.indexOf("target")'
```

### `.reduce(expression, initial)`
Reduces list to single value.

```yaml
formula: "numbers.reduce((acc, x) => acc + x, 0)"
# Sum of all numbers
```

## File Functions

### `hasTag(tag)`
Returns true if note has the tag.

```yaml
formula: 'hasTag("project")'
formula: 'hasTag("status/active")'
```

### `hasLink(path)`
Returns true if note links to path.

```yaml
formula: 'hasLink("Index")'
formula: 'hasLink("Projects/Main")'
```

### `inFolder(path)`
Returns true if note is in folder.

```yaml
formula: 'inFolder("Projects")'
formula: 'inFolder("Archive/2024")'
```

## File Properties

Available file metadata properties:

| Property | Description | Type |
|----------|-------------|------|
| `file.name` | File name without extension | string |
| `file.path` | Full path from vault root | string |
| `file.folder` | Parent folder path | string |
| `file.ext` | File extension | string |
| `file.ctime` | Creation time | date |
| `file.mtime` | Last modified time | date |
| `file.size` | File size in bytes | number |
| `file.link` | Link to the file | link |
| `file.frontmatter` | All frontmatter as object | object |

## Operators

### Comparison Operators

| Operator | Description |
|----------|-------------|
| `==` | Equal |
| `!=` | Not equal |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater or equal |
| `<=` | Less or equal |

### Logical Operators

| Operator | Description |
|----------|-------------|
| `&&` | AND |
| `\|\|` | OR |
| `!` | NOT |

### Arithmetic Operators

| Operator | Description |
|----------|-------------|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `%` | Modulo |

### String Operators

| Operator | Description |
|----------|-------------|
| `+` | Concatenation |

## Complex Formula Examples

### Age in Days

```yaml
formula: "(now() - file.ctime).days.round(0)"
```

### Days Until Due (with warning)

```yaml
formula: |
  if((due - now()).days < 0,
     "OVERDUE",
     if((due - now()).days < 7,
        "This week",
        "On track"))
```

### Progress Percentage

```yaml
formula: "(completed / total * 100).round(1) + '%'"
```

### Tag List Display

```yaml
formula: 'tags.filter(t => !t.startsWith("_")).join(", ")'
```

### Conditional Formatting

```yaml
formula: |
  if(priority == "high", "🔴",
     if(priority == "medium", "🟡", "🟢"))
```

### Word Count Estimate

```yaml
formula: "(file.size / 5).round(0)"
# Rough word count based on file size
```

### Last Activity

```yaml
formula: |
  if((now() - file.mtime).days < 1, "Today",
     if((now() - file.mtime).days < 7, "This week",
        if((now() - file.mtime).days < 30, "This month", "Older")))
```
