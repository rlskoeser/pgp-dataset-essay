# compile to Word document with numbering & bibliography 
# pull changes to ensure building up-to-date version
docx: pull
	pandoc -o pgp_dataset_essay.docx -t docx+native_numbering main.tex --verbose  --bibliography references.bib --citeproc

# pull changes from remote
pull:
	git pull
