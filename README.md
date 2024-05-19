# Required libraries

pip install **requests**<br />
pip install **selenium**<br />
pip install **undetected_chromedriver**<br />
pip install **beutifulsoup4**<br />

!Don`t forget to update GoogleChrome to the latest version before using chromedriver

# Instruction

Input website url into variable "url"<br />
Input path to txt files: file1(author), file2(books), file3(author_books) (variables: "file1", "file2", "file3")<br />
Start parser and wait for the popup window to show up on your screen. Close this window and type smth into console in your IDE<br />
Wait until parser extract the data<br />
Parser writes in file1, file2, file3 SQL code for inserting extracted data to the DB<br />
