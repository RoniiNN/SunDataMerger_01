C S V - F O R M A T 
__________________
Important notes 

* There is currently no such thing as a standard CSV format. 

§1 §2 §3 §4
* It is falsely believed by some that RFC 4180 is the CSV standard however it is just a memo not a standard.

§3

>  This memo provides information for the Internet community.  
>  It does not specify an Internet standard of any kind.  Distribution of this memo is unlimited.
>
> --- RFC 4180, Status of This Memo

§3

* CSV can mean a lot of things. And you can’t trust it to work well most of the time, unless you’re dealing with people in one country, all using the same locale settings and software. Which is pretty unlikely. TSV can work around most of the problems, but encodings are still troublesome. §1

   > [RFC 4180](https://tools.ietf.org/html/rfc4180) formalized CSV. It defines the [MIME type](https://en.wikipedia.org/wiki/MIME_type "MIME type") "text/csv", and CSV files that follow its rules should be very widely portable. Among its requirements:    
   > - MS-DOS-style lines that end with (CR/LF) characters (optional for the last line).
   > - An optional header record (there is no sure way to detect whether it is present, so care is required when importing).
   > -   Each record "should" contain the same number of comma-separated fields.
   > -   Any field _may_ be quoted (with double quotes).
   > -   Fields containing a line-break, double-quote or commas _should_ be quoted. (If they are not, the file will 	likely be impossible to process correctly).
   > - A (double) quote character in a field must be represented by two (double) quote characters. 
   
   §4


### CSV File Format
__________________

* Fields are separated with commas

> Microsoft Excel — which most people will use to read/write their CSV
> files — makes this decision based on the user locale settings. If the
> OS is set to a locale where the comma is the decimal mark
> (eg. most of Europe), the list separator is set to ";" instead of ","
> — and Excel uses that. 

§1

* Each record is one line   

>  ...but A record separator may consist of a line feed
> (ASCII/LF=0x0A),  or a carriage return and line feed pair
> (ASCII/CRLF=0x0D 0x0A). ...but: fields may contain embedded
> line-breaks (see below)  so a record may span more than one line. 

§2

* Leading and trailing space-characters adjacent to comma field separators are ignored.

> Ex: So   John  ,   Doe  ,... resolves to "John" and "Doe", etc. Space
> characters can be spaces, or tabs.

§2

* Fields with embedded commas must be delimited with double-quote characters.

> Ex:In the above example. "Anytown, WW" had to be delimited in double
> quotes  because it had an embedded comma.

§2

* Fields that contain double quote characters must be ... 

> surounded by double-quotes, and the  embedded double-quotes must each
> be represented by a pair of consecutive double quotes. Ex:So, John "Da
> Man" Doe would convert to "John ""Da Man""",Doe, 120 any st.,...

§2

* Fields with leading or trailing spaces must be delimited with double-quote characters.
>To preserve the leading and trailing spaces around the last name above: _John ," Doe ",..._
§2
* Fields may always be delimited with double quotes.

>The delimiters will always be discarded.

§2
* The first record in a CSV file may be a header record containing column (field) names

> There is no mechanism for automatically discerning if the first record
> is a header row, so in the general case, this will have to be provided
> by an outside process (such as prompting the user). The header row is
> encoded just like any other CSV record in accordance with the rules
> above. A header row for the multi-line example above, might be: 
> Location, Notes, "Start Date", ...

§2

#### Links:
§1:https://chriswarrick.com/blog/2017/04/07/csv-is-not-a-standard/

§2:http://www.creativyst.com/Doc/Articles

§3:https://www.ietf.org/rfc/rfc4180.txt

§4:https://en.wikipedia.org/wiki/Comma-separated_values#RFC_4180_standard

http://edoceo.com/utilitas/csv-file-format

https://tools.ietf.org/html/rfc4180