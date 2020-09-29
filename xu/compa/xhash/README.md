#Xash
##What is Xash?
- Xash is a name make by 2 words: Xu in XuCompany and Hash.
- Xash is an markup language make by XuCompany.
- Xash use for name a file with categories and property tag. It was designed in Window platform.
##Xash Keyword
- Xash has three keywords, that is  brackets "[]", double dash "--" and hash "#".
#####BRACKETS
- BRACKETS are stand for a category mark. Between the BRACKETS has a syntax: [category-name]#[id]
- A complete word between BRACKETS is only one. That is the program can point to a file by the key [category-name]#[id]
#####NAME
- After BRACKETS is the main name of file.
#####DOUBLE DASH
- DOUBLE DASH mark others path of file name, with the name and property, and property together.
#####HASH
- Hash will be list the value item of the property
- Hash with suffix BRACKETS stand for a import property.
Value inside has syntax [category-name]#[id] and it point to a definition property.
##XDEF
- XDEF is a file with extension ".xdef".
- XDEF constant list of Xash with list property values. Another file with be point to XDEF to get value.
It (XDEF) make the file name shorter than. 
##EXAMPLE
######syntax:
	[news]Name of news--tag#tag1#tag2#tag3--label#label1
######contruct:
	news						categories
		Name of news			        name
			tag				property 1
				tag1			value 1
				tag2			value 2
				tag3			value 3
			label				property 2
				label1			value only
######example
	1. [news]The Diary--tag#diary#the diary#news#news for to day--author#Albert--date#23-09-2020.txt
    2. [news--01] The Diary--tag#diary#the diary#news#news for to day--author#Albert--date#23-09-2020
    3. [news--02] The Diary part 2--tag#diary#the diary#news#news for to day#part 2--author#Albert--date#23-09-2020
    4. [news--03] The Diary import from first line--tag#[news-01]--author#Albert--date#24-09-2020
    5. [news--04] The Diary with sub --tag#sub--author#Albert--date#25-09-2020--sub#[news-01]
######key:
	--tag#[news-01] in line 4
######is
    --tag#diary#the diary#news#news for to day
